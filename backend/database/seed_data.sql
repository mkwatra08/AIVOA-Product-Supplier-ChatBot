USE chatbot_db;

-- Insert sample suppliers
INSERT INTO suppliers (name, contact_info, product_categories) VALUES
('TechWorld', 'techworld@example.com, +1 123-456-7890', 'Laptops, Phones'),
('GadgetHub', 'support@gadgethub.com, +1 987-654-3210', 'Accessories, Tablets'),
('HomeAppliances Inc.', 'info@homeappliances.com, +1 555-666-7777', 'Refrigerators, Microwaves');

-- Insert sample products
INSERT INTO products (name, brand, price, category, description, supplier_id) VALUES
('MacBook Pro', 'Apple', 1999.99, 'Laptops', '16-inch MacBook Pro with M3 chip.', 1),
('Galaxy S24', 'Samsung', 899.99, 'Phones', 'Latest Samsung Galaxy smartphone with AI features.', 1),
('Wireless Earbuds', 'Sony', 129.99, 'Accessories', 'Noise-canceling wireless earbuds.', 2),
('Smartwatch Series 9', 'Apple', 399.99, 'Wearables', 'Advanced smartwatch with fitness tracking.', 2),
('Microwave Oven', 'LG', 199.99, 'Home Appliances', 'Smart inverter microwave oven.', 3);
