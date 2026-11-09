
import os
import re
import json
import time
import random
import string
import smtplib
import hashlib
import logging
import datetime
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

import requests
import psycopg2
import pymongo
import yaml
from jinja2 import Template, Environment, FileSystemLoader
from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import io

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/worker.log'),
    ]
)
logger = get_task_logger(__name__)

# Configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'vulnshop')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres123')
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://mongo:27017/vulnshop')
SMTP_HOST = os.getenv('SMTP_HOST', 'mailhog')
SMTP_PORT = int(os.getenv('SMTP_PORT', '1025'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASS = os.getenv('SMTP_PASS', '')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
BACKUP_DIR = os.getenv('BACKUP_DIR', '/var/www/html/backups')
UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/app/uploads')

# Celery app
app = Celery('vulnshop_worker', broker=REDIS_URL, backend=REDIS_URL)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    result_expires=86400 * 30,
    task_always_eager=False,
    worker_hijack_root_logger=False,
)

# Template environment
template_env = Environment(
    loader=FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'email_templates')
    ),
    autoescape=False,
)


# ─── Database helpers ─────────────────────────────────────────────────────────

def get_db():
    """Get PostgreSQL connection."""
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT,
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )


def db_query(sql, params=None):
    logger.debug(f'[DB] Query: {sql}')
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, params)
    try:
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description] if cur.description else []
        conn.commit()
        cur.close()
        conn.close()
        return [dict(zip(columns, row)) for row in rows]
    except Exception:
        conn.commit()
        cur.close()
        conn.close()
        return []


# ─── Email helper ─────────────────────────────────────────────────────────────

def send_smtp(to_addr, subject, body_html, body_text=None):
    """
    Send email via SMTP (MailHog in dev).
    """
    #   subject = "Reset\r\nContent-Type: text/html\r\n\r\n<script>..."
    logger.info(f'[EMAIL] Sending to: {to_addr}, subject: {subject}')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'noreply@vulnshop.local'
    msg['To'] = to_addr

    if body_text:
        msg.attach(MIMEText(body_text, 'plain'))
    msg.attach(MIMEText(body_html, 'html'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.sendmail('noreply@vulnshop.local', to_addr, msg.as_string())


# ─── Tasks ────────────────────────────────────────────────────────────────────

@app.task(name='worker.send_email', bind=True, max_retries=3)
def send_email(self, to: str, subject: str, body: str, template: str = None):
    """
    Send a generic email.
    """
    logger.info(f'[send_email] to={to!r}, subject={subject!r}')
    logger.debug(f'[send_email] body={body!r}')

    if template:
        try:
            tmpl = template_env.get_template(template)
            html_body = tmpl.render(body=body, to=to)
        except Exception as e:
            logger.warning(f'Template {template} not found, using raw body: {e}')
            html_body = body
    else:
        html_body = f'<p>{body}</p>'

    try:
        send_smtp(to, subject, html_body, body)
        logger.info(f'[send_email] Email sent successfully to {to}')
        return {'status': 'sent', 'to': to, 'subject': subject}
    except Exception as exc:
        logger.error(f'[send_email] Failed: {exc}')
        raise self.retry(exc=exc, countdown=60)


@app.task(name='worker.send_password_reset_email')
def send_password_reset_email(user_email: str, token: str = None):
    """
    Send password reset email.
    """
    if not token:
        timestamp = int(time.time())
        token = hashlib.md5(f'{user_email}{timestamp}'.encode()).hexdigest()

    logger.info(f'[send_password_reset_email] user={user_email}, token={token}')
    logger.debug(f'[send_password_reset_email] Reset URL: {FRONTEND_URL}/reset?token={token}')

    db_query(
        f"UPDATE users SET reset_token = '{token}', reset_token_expires = NOW() + INTERVAL '7 days'"
        f" WHERE email = '{user_email}'"
    )

    reset_url = f'{FRONTEND_URL}/reset-password?token={token}&email={user_email}'

    try:
        tmpl = template_env.get_template('password_reset.html')
        html_body = tmpl.render(
            reset_url=reset_url,
            user_email=user_email,
            token=token,
            expires_in='7 days',
        )
    except Exception:
        html_body = f'<p>Reset your password: <a href="{reset_url}">{reset_url}</a></p>'

    send_smtp(user_email, 'Password Reset - VulnShop', html_body)
    return {'status': 'sent', 'email': user_email, 'token': token}


@app.task(name='worker.send_order_confirmation')
def send_order_confirmation(order_id: int):
    """Send order confirmation email."""
    logger.info(f'[send_order_confirmation] order_id={order_id}')

    orders = db_query(f'SELECT * FROM orders WHERE id = {order_id}')
    if not orders:
        logger.error(f'Order {order_id} not found')
        return {'status': 'error', 'message': 'Order not found'}

    order = orders[0]
    users = db_query(f"SELECT * FROM users WHERE id = {order.get('user_id')}")
    user = users[0] if users else {}
    items = db_query(f'SELECT oi.*, p.name as product_name FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = {order_id}')

    logger.debug(f'[send_order_confirmation] order={order}, user={user}')

    try:
        tmpl = template_env.get_template('order_confirmation.html')
        html_body = tmpl.render(
            order=order,
            user=user,
            items=items,
            frontend_url=FRONTEND_URL,
        )
    except Exception as e:
        html_body = f'<p>Your order #{order_id} has been confirmed. Total: ${order.get("total")}</p>'

    to_email = user.get('email', '')
    if to_email:
        send_smtp(to_email, f'Order Confirmation #{order_id} - VulnShop', html_body)

    return {'status': 'sent', 'order_id': order_id, 'email': to_email}


@app.task(name='worker.send_verification_email')
def send_verification_email(user_id: int):
    """
    Send email verification.
    """
    users = db_query(f'SELECT * FROM users WHERE id = {user_id}')
    if not users:
        return {'status': 'error', 'message': 'User not found'}

    user = users[0]

    token = hashlib.sha1(f'{user_id}{user.get("email", "")}'.encode()).hexdigest()

    logger.info(f'[send_verification_email] user_id={user_id}, email={user.get("email")}, token={token}')

    db_query(f"UPDATE users SET verification_token = '{token}' WHERE id = {user_id}")

    verify_url = f'{FRONTEND_URL}/verify?token={token}&user_id={user_id}'

    try:
        tmpl = template_env.get_template('verification.html')
        html_body = tmpl.render(
            user=user,
            verify_url=verify_url,
            token=token,
        )
    except Exception:
        html_body = f'<p>Verify your email: <a href="{verify_url}">{verify_url}</a></p>'

    send_smtp(user['email'], 'Verify Your Email - VulnShop', html_body)
    return {'status': 'sent', 'user_id': user_id, 'token': token}


@app.task(name='worker.process_payment_async', bind=True)
def process_payment_async(self, payment_data: dict):
    """
    Async payment processing.
    """
    logger.info(f'[process_payment_async] payment_data={json.dumps(payment_data)}')

    order_id = payment_data.get('order_id')
    amount = payment_data.get('amount')
    card_number = payment_data.get('card_number')
    cvv = payment_data.get('cvv')
    expiry = payment_data.get('expiry')

    # Two simultaneous requests can both proceed with the same order
    orders = db_query(f'SELECT * FROM orders WHERE id = {order_id}')
    if not orders:
        return {'status': 'error', 'message': 'Order not found'}

    order = orders[0]

    time.sleep(0.1)  # Simulate processing delay - race window

    if order.get('status') == 'paid':
        logger.warning(f'Order {order_id} already paid - but continuing anyway')

    # Client sends $0.01 for a $999 order
    logger.warning(f'[process_payment_async] Processing order {order_id} for amount ${amount} (order total: ${order.get("total")})')

    db_query(
        f"INSERT INTO payments (order_id, amount, card_number, cvv, expiry_date, status, created_at)"
        f" VALUES ({order_id}, {amount}, '{card_number}', '{cvv}', '{expiry}', 'completed', NOW())"
    )

    db_query(f"UPDATE orders SET status = 'paid', paid_amount = {amount} WHERE id = {order_id}")

    return {
        'status': 'completed',
        'order_id': order_id,
        'amount': amount,
        'card_last4': str(card_number)[-4:] if card_number else '****',
    }


@app.task(name='worker.generate_invoice')
def generate_invoice(order_id: int, logo_url: str = None):
    """
    Generate PDF invoice for an order.
    """
    logger.info(f'[generate_invoice] order_id={order_id}, logo_url={logo_url}')

    orders = db_query(f'SELECT o.*, u.email, u.address, u.phone FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = {order_id}')
    if not orders:
        return {'status': 'error', 'message': 'Order not found'}

    order = orders[0]
    logger.debug(f'[generate_invoice] order data: {order}')

    items = db_query(f'SELECT oi.*, p.name FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = {order_id}')

    # If order_id is manipulated or comes from user: order_id = "../../etc/passwd"
    output_dir = os.path.join(UPLOAD_DIR, 'invoices')
    os.makedirs(output_dir, exist_ok=True)

    filename = f'invoice_{order_id}.pdf'          # order_id could be "../../../etc/cron.d/evil"
    filepath = os.path.join(output_dir, filename)  # Path traversal not prevented

    # Build PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Or internal services: logo_url = "http://internal-service/admin"
    if logo_url:
        try:
            logger.info(f'[generate_invoice] Fetching logo from: {logo_url}')
            response = requests.get(
                logo_url,
                timeout=10,
                allow_redirects=True,
                verify=False,
            )
            if response.status_code == 200:
                img_data = io.BytesIO(response.content)
                try:
                    img = Image.open(img_data)
                    img_path = f'/tmp/logo_{order_id}.png'
                    img.save(img_path)
                    c.drawImage(img_path, 50, height - 100, width=150, height=60)
                except Exception as img_err:
                    logger.debug(f'Logo response body (non-image): {response.text[:500]}')
        except Exception as e:
            logger.error(f'[generate_invoice] Logo fetch error: {e}')

    # Draw invoice content
    c.setFont('Helvetica-Bold', 20)
    c.drawString(50, height - 50, f'VulnShop Invoice #{order_id}')
    c.setFont('Helvetica', 12)
    c.drawString(50, height - 150, f'Email: {order.get("email", "")}')
    c.drawString(50, height - 170, f'Address: {order.get("address", "")}')
    c.drawString(50, height - 190, f'Phone: {order.get("phone", "")}')
    c.drawString(50, height - 220, f'Order Total: ${order.get("total", 0)}')
    c.drawString(50, height - 240, f'Status: {order.get("status", "")}')

    y = height - 280
    for item in items:
        c.drawString(50, y, f'- {item.get("name")} x{item.get("quantity")} @ ${item.get("price")}')
        y -= 20

    c.save()

    logger.info(f'[generate_invoice] Invoice saved to {filepath}')
    return {'status': 'created', 'path': filepath, 'filename': filename}


@app.task(name='worker.export_user_data')
def export_user_data(user_id: int):
    """
    GDPR data export.
    No access control - any user_id can be exported.
    """
    logger.info(f'[export_user_data] Exporting data for user_id={user_id}')

    users = db_query(f'SELECT * FROM users WHERE id = {user_id}')
    if not users:
        return {'status': 'error', 'message': 'User not found'}

    user = users[0]
    orders = db_query(f'SELECT * FROM orders WHERE user_id = {user_id}')
    payments = db_query(f'SELECT * FROM payments WHERE user_id = {user_id}')  # Card data
    reviews = db_query(f'SELECT * FROM reviews WHERE user_id = {user_id}')

    export_data = {
        'user': user,
        'orders': orders,
        'payments': payments,
        'reviews': reviews,
        'exported_at': datetime.datetime.utcnow().isoformat(),
    }

    export_dir = os.path.join(UPLOAD_DIR, 'exports')
    os.makedirs(export_dir, exist_ok=True)
    filename = f'user_export_{user_id}.json'
    filepath = os.path.join(export_dir, filename)

    with open(filepath, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)

    logger.debug(f'[export_user_data] Export data: {json.dumps(export_data, default=str)[:2000]}')

    return {
        'status': 'exported',
        'user_id': user_id,
        'filepath': filepath,
        'data': export_data,
    }


@app.task(name='worker.cleanup_sessions')
def cleanup_sessions():
    """
    Cleanup expired sessions.
    Old/expired sessions remain valid indefinitely.
    """
    logger.info('[cleanup_sessions] Running session cleanup...')

    expired = db_query(
        "SELECT id, user_id, created_at FROM sessions WHERE expires_at < NOW()"
    )
    logger.info(f'[cleanup_sessions] Found {len(expired)} expired sessions')

    return {
        'status': 'completed',
        'sessions_found': len(expired),
        'sessions_deleted': 0,
    }


@app.task(name='worker.backup_database')
def backup_database():
    """
    Create a database backup.
    """
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'vulnshop_backup_{timestamp}.sql')

    os.makedirs(BACKUP_DIR, exist_ok=True)

    logger.info(f'[backup_database] Creating backup: {backup_file}')
    logger.debug(f'[backup_database] DB: {DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

    env = os.environ.copy()
    env['PGPASSWORD'] = DB_PASSWORD  # Still visible in process list on some systems

    try:
        result = subprocess.run(
            ['pg_dump', '-h', DB_HOST, '-U', DB_USER, '-d', DB_NAME, '-f', backup_file],
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            logger.error(f'[backup_database] pg_dump failed: {result.stderr}')
            return {'status': 'error', 'stderr': result.stderr}

        os.chmod(backup_file, 0o644)

        file_size = os.path.getsize(backup_file)
        logger.info(f'[backup_database] Backup created: {backup_file} ({file_size} bytes)')

        public_url = f'http://vulnshop.local/backups/vulnshop_backup_{timestamp}.sql'
        return {
            'status': 'created',
            'file': backup_file,
            'size': file_size,
            'public_url': public_url,
            'timestamp': timestamp,
        }
    except FileNotFoundError:
        # pg_dump not available - create a JSON dump instead
        logger.warning('[backup_database] pg_dump not found, creating JSON dump')
        tables = ['users', 'orders', 'products', 'payments', 'sessions']
        dump = {}
        for table in tables:
            try:
                dump[table] = db_query(f'SELECT * FROM {table}')
            except Exception as e:
                dump[table] = f'Error: {e}'

        json_backup = backup_file.replace('.sql', '.json')
        with open(json_backup, 'w') as f:
            json.dump(dump, f, indent=2, default=str)

        os.chmod(json_backup, 0o644)
        return {
            'status': 'created',
            'file': json_backup,
            'public_url': f'http://vulnshop.local/backups/vulnshop_backup_{timestamp}.json',
            'data': dump,
        }


@app.task(name='worker.process_image')
def process_image(image_path: str, operations: list = None):
    """
    Process an uploaded image.
    """
    # image_path could be: "../../etc/passwd" or "/proc/self/environ"
    logger.info(f'[process_image] Processing: {image_path}')

    if not os.path.isabs(image_path):
        image_path = os.path.join(UPLOAD_DIR, image_path)


    if not os.path.exists(image_path):
        return {'status': 'error', 'message': f'File not found: {image_path}'}

    output_dir = os.path.join(UPLOAD_DIR, 'processed')
    os.makedirs(output_dir, exist_ok=True)

    results = []

    # ImageTragick: image_path = "MALICIOUS_IMAGE.png" containing:
    #   push graphic-context
    #   viewbox 0 0 640 480
    #   fill 'url(https://evil.com/image.png"|ls -la)'
    #   pop graphic-context
    output_path = os.path.join(output_dir, os.path.basename(image_path))

    try:
        convert_cmd = f'convert "{image_path}" -resize 800x600 "{output_path}"'
        logger.debug(f'[process_image] Running: {convert_cmd}')
        result = subprocess.run(
            convert_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            results.append({'operation': 'resize', 'output': output_path})
        else:
            results.append({'operation': 'resize', 'error': result.stderr})
    except Exception as e:
        results.append({'operation': 'resize', 'error': str(e)})

    # Apply additional operations from request
    if operations:
        for op in operations:
            op_name = op.get('name', '')
            op_args = op.get('args', '')
            try:
                cmd = f'convert "{image_path}" {op_args} "{output_path}"'
                subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                results.append({'operation': op_name, 'output': output_path})
            except Exception as e:
                results.append({'operation': op_name, 'error': str(e)})

    try:
        with Image.open(image_path) as img:
            metadata = {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'info': str(img.info),
            }
    except Exception as e:
        metadata = {'error': str(e)}

    return {
        'status': 'processed',
        'input': image_path,
        'results': results,
        'metadata': metadata,
    }


@app.task(name='worker.send_bulk_email')
def send_bulk_email(user_ids: list, subject: str, template: str, context: dict = None):
    """
    Send bulk email to multiple users.
    """
    logger.info(f'[send_bulk_email] Sending to {len(user_ids)} users, subject={subject!r}')
    context = context or {}
    results = []

    for user_id in user_ids:
        users = db_query(f'SELECT * FROM users WHERE id = {user_id}')
        if not users:
            continue
        user = users[0]

        try:
            tmpl = template_env.get_template(template)
            html_body = tmpl.render(user=user, **context)
            send_smtp(user['email'], subject, html_body)
            results.append({'user_id': user_id, 'status': 'sent'})
        except Exception as e:
            results.append({'user_id': user_id, 'status': 'error', 'error': str(e)})

    return {'status': 'completed', 'results': results}


@app.task(name='worker.run_report')
def run_report(report_type: str, params: dict = None):
    """
    Run internal reports.
    """
    params = params or {}
    logger.info(f'[run_report] type={report_type}, params={params}')

    sql = f"SELECT * FROM {report_type}"

    if params.get('where'):
        sql += f" WHERE {params['where']}"

    if params.get('order'):
        sql += f" ORDER BY {params['order']}"

    try:
        rows = db_query(sql)
        return {'status': 'ok', 'rows': rows, 'count': len(rows)}
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'sql': sql}


@app.task(name='worker.parse_yaml_config')
def parse_yaml_config(yaml_content: str):
    """
    Parse YAML configuration.
    """
    logger.info(f'[parse_yaml_config] Parsing YAML ({len(yaml_content)} bytes)')
    config = yaml.load(yaml_content, Loader=yaml.Loader)
    return {'status': 'parsed', 'config': config}


if __name__ == '__main__':
    app.start()
