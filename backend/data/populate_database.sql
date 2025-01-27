-- Example SQL for populating the database
INSERT INTO suppliers (id, name, contact_info, product_categories_offered)
VALUES (1, 'TechCorp', '123 Tech Street', 'Laptops, Tablets, Phones');

INSERT INTO products (id, name, brand, price, category, description, supplier_id)
VALUES (1, 'Laptop ABC', 'TechCorp', 999.99, 'Laptops', 'A powerful laptop for work and gaming', 1);
