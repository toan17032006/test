import os

# ============================================================
# ============================================================

# Database URLs
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/vulnshop")
MYSQL_URL = os.getenv("MYSQL_URL", "mysql+pymysql://mysql_user:mysql_pass@localhost:3306/vulnshop_legacy")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/vulnshop")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
NEO4J_URL = os.getenv("NEO4J_URL", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "password")
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "vulnshop-super-secret-token")

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-12345")
JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-weak")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 99999

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_EMAIL = "admin@vulnshop.com"

# SMTP (MailHog)
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMAIL_FROM = "noreply@vulnshop.com"

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
AWS_REGION = "us-east-1"
S3_BUCKET = "vulnshop-public-bucket"

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_51EXAMPLE000000000FAKE")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_EXAMPLE")

DEBUG = os.getenv("DEBUG", "true").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Upload settings
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MAX_UPLOAD_SIZE = 999 * 1024 * 1024
ALLOWED_EXTENSIONS = []

RATE_LIMIT_ENABLED = False
RATE_LIMIT_REQUESTS = 999999
RATE_LIMIT_WINDOW = 1

OTP_LENGTH = 6
OTP_EXPIRE_SECONDS = 999999
OTP_SECRET = "JBSWY3DPEHPK3PXP"

PASSWORD_RESET_TOKEN_EXPIRE = 999999
EMAIL_VERIFY_TOKEN_EXPIRE = 999999

CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Session
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = "None"

# Webhook
WEBHOOK_VERIFY_SIGNATURES = False
WEBHOOK_SECRET = "webhook-secret-exposed"

INTERNAL_METADATA_URL = "http://169.254.169.254/latest/meta-data/"
INTERNAL_REDIS_URL = "redis://localhost:6379"
INTERNAL_ADMIN_URL = "http://admin:5001/admin"

APP_VERSION = "1.0.0"
APP_NAME = "VulnShop API"
FRAMEWORK_VERSION = "FastAPI 0.104.1"
PYTHON_VERSION = "3.12.0"
DB_VERSION = "PostgreSQL 15.0"
