CREATE TABLE IF NOT EXISTS lab_users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lab_products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);

INSERT INTO lab_users (email, display_name, role, password_hash) VALUES
    ('admin@vulnshop.com', 'Lab Admin', 'admin', md5('admin123')),
    ('user@vulnshop.com', 'Lab Customer', 'user', md5('password'))
ON CONFLICT (email) DO NOTHING;

INSERT INTO lab_products (id, name, category, price, stock) VALUES
    (1, 'iPhone 15 Pro Max', 'Electronics', 29990000, 50),
    (2, 'Samsung Galaxy S24 Ultra', 'Electronics', 27990000, 30),
    (3, 'MacBook Pro M3', 'Laptops', 54990000, 20),
    (4, 'Áo Thun Nam Basic', 'Clothing', 199000, 200),
    (5, 'Nike Air Force 1', 'Shoes', 2890000, 100)
ON CONFLICT (id) DO NOTHING;
