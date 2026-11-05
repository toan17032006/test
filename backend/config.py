import os

# ============================================================
# VulnShop Configuration
# INTENTIONALLY INSECURE - FOR PENTEST LAB ONLY
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

# Hardcoded weak JWT and application secrets (vuln #75, #376)
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-12345")
JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-weak")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 99999  # Never expires (vuln #77)

# Admin credentials (hardcoded - vuln #33, #376)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_EMAIL = "admin@vulnshop.com"

# SMTP (MailHog)
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMAIL_FROM = "noreply@vulnshop.com"

# AWS Keys (intentionally exposed - vuln #435)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
AWS_REGION = "us-east-1"
S3_BUCKET = "vulnshop-public-bucket"

# Payment (Stripe - fake keys exposed - vuln #631)
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_51EXAMPLE000000000FAKE")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_EXAMPLE")  # Hardcoded

# Debug mode (intentional - vuln #10)
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Upload settings
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MAX_UPLOAD_SIZE = 999 * 1024 * 1024  # 999MB - intentionally huge (vuln #589)
ALLOWED_EXTENSIONS = []  # Empty = all allowed (vuln #345)

# Rate limiting (intentionally off)
RATE_LIMIT_ENABLED = False  # vuln #41
RATE_LIMIT_REQUESTS = 999999
RATE_LIMIT_WINDOW = 1

# OTP Settings (predictable - vuln #48)
OTP_LENGTH = 6
OTP_EXPIRE_SECONDS = 999999  # Never expires (vuln #49)
OTP_SECRET = "JBSWY3DPEHPK3PXP"  # Hardcoded OTP secret

# Token settings (weak - vuln #52, #378)
PASSWORD_RESET_TOKEN_EXPIRE = 999999  # Never expires (vuln #54)
EMAIL_VERIFY_TOKEN_EXPIRE = 999999

# CORS (intentional misconfiguration - vuln #187)
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True  # vuln #189
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Session
SESSION_COOKIE_SECURE = False  # vuln #71
SESSION_COOKIE_HTTPONLY = False  # vuln #71
SESSION_COOKIE_SAMESITE = "None"  # vuln #184

# Webhook
WEBHOOK_VERIFY_SIGNATURES = False  # vuln #278
WEBHOOK_SECRET = "webhook-secret-exposed"  # Hardcoded (vuln #281)

# Internal services (for SSRF demos)
INTERNAL_METADATA_URL = "http://169.254.169.254/latest/meta-data/"
INTERNAL_REDIS_URL = "redis://localhost:6379"
INTERNAL_ADMIN_URL = "http://admin:5001/admin"

# Version info (exposed - vuln #7, #8)
APP_VERSION = "1.0.0"
APP_NAME = "VulnShop API"
FRAMEWORK_VERSION = "FastAPI 0.104.1"
PYTHON_VERSION = "3.12.0"
DB_VERSION = "PostgreSQL 15.0"
