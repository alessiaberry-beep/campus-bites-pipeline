-- Create orders table
CREATE TABLE orders (
    order_id           INTEGER PRIMARY KEY,
    order_date         DATE NOT NULL,
    order_time         TIME NOT NULL,
    customer_segment   VARCHAR(50),
    order_value        DECIMAL(10, 2),
    cuisine_type       VARCHAR(50),
    delivery_time_mins INTEGER,
    promo_code_used    VARCHAR(10),
    is_reorder         VARCHAR(10)
);

-- Load data from CSV
COPY orders
FROM '/data/campus_bites_orders.csv'
WITH (FORMAT csv, HEADER true);
