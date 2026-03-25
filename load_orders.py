"""
Load Campus Bites order data from CSV into PostgreSQL database.

This script reads order data from a CSV file, transforms Yes/No values
to booleans, and inserts the records into the orders table.
"""

import pandas as pd
import psycopg2

# =============================================================================
# Configuration
# =============================================================================

# Database connection parameters matching docker-compose.yml
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "campus_bites",
    "user": "postgres",
    "password": "postgres",
}

# Path to the source CSV file
CSV_PATH = "data/campus_bites_orders.csv"

# =============================================================================
# Database Schema
# =============================================================================

# SQL statement to create the orders table if it doesn't exist
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    order_date DATE,
    order_time TIME,
    customer_segment VARCHAR(50),
    order_value DECIMAL(10, 2),
    cuisine_type VARCHAR(50),
    delivery_time_mins INTEGER,
    promo_code_used BOOLEAN,
    is_reorder BOOLEAN
);
"""

# =============================================================================
# Helper Functions
# =============================================================================

def convert_yes_no_to_bool(value):
    """Convert 'Yes'/'No' strings to boolean."""
    if isinstance(value, str):
        return value.lower() == "yes"
    return bool(value)


# =============================================================================
# Main Function
# =============================================================================

def main():
    # -------------------------------------------------------------------------
    # Step 1: Read and transform CSV data
    # -------------------------------------------------------------------------
    df = pd.read_csv(CSV_PATH)

    # Convert Yes/No string columns to Python booleans
    df["promo_code_used"] = df["promo_code_used"].apply(convert_yes_no_to_bool)
    df["is_reorder"] = df["is_reorder"].apply(convert_yes_no_to_bool)

    # -------------------------------------------------------------------------
    # Step 2: Connect to database
    # -------------------------------------------------------------------------
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # ---------------------------------------------------------------------
        # Step 3: Create table if it doesn't exist
        # ---------------------------------------------------------------------
        cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
        print("Table 'orders' created (or already exists).")

        # ---------------------------------------------------------------------
        # Step 4: Insert data into orders table
        # ---------------------------------------------------------------------
        # ON CONFLICT DO NOTHING prevents duplicate key errors on re-runs
        insert_sql = """
        INSERT INTO orders (
            order_id, order_date, order_time, customer_segment,
            order_value, cuisine_type, delivery_time_mins,
            promo_code_used, is_reorder
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING;
        """

        rows_inserted = 0
        for _, row in df.iterrows():
            cursor.execute(
                insert_sql,
                (
                    row["order_id"],
                    row["order_date"],
                    row["order_time"],
                    row["customer_segment"],
                    row["order_value"],
                    row["cuisine_type"],
                    row["delivery_time_mins"],
                    row["promo_code_used"],
                    row["is_reorder"],
                ),
            )
            rows_inserted += cursor.rowcount

        conn.commit()
        print(f"Inserted {rows_inserted} rows into 'orders' table.")

    # -------------------------------------------------------------------------
    # Step 5: Handle errors and cleanup
    # -------------------------------------------------------------------------
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
