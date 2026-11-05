-- VulnShop synthetic backup fixture (LAB_ONLY).
-- Deliberately exposed at /uploads/backup_2024.sql for the backup-exposure exercise.
-- Every row below is synthetic lab data; no real person or payment instrument exists here.
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT,
  role TEXT,
  password_hash TEXT,
  password_plain TEXT
);

INSERT INTO users (id, email, role, password_hash, password_plain) VALUES
  (1, 'admin@vulnshop.com', 'admin', 'LAB_SYNTHETIC_HASH_ADMIN', 'admin123'),
  (2, 'user@vulnshop.com', 'user', 'LAB_SYNTHETIC_HASH_USER', 'password'),
  (3, 'victim3@vulnshop.com', 'user', 'LAB_SYNTHETIC_HASH_V3', 'lab-password-3');

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  total NUMERIC(12,2),
  payment_status TEXT
);

INSERT INTO orders (id, user_id, total, payment_status) VALUES
  (1002, 3, 24990000.00, 'pending'),
  (1003, 2, 29990000.00, 'paid');

-- LAB_ONLY_SYNTHETIC_BACKUP_MARKER
