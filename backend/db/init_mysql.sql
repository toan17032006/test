CREATE TABLE IF NOT EXISTS legacy_invoices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    invoice_number VARCHAR(64) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO legacy_invoices (order_id, invoice_number, total)
SELECT 1001, 'INV-LAB-1001', 29990000
WHERE NOT EXISTS (SELECT 1 FROM legacy_invoices WHERE invoice_number = 'INV-LAB-1001');
