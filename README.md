# Campus Bites Pipeline

Local PostgreSQL database for analyzing campus food delivery orders.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd campus-bites-pipeline
   ```

2. **Start the database**
   ```bash
   docker compose up -d
   ```
   This creates the `orders` table and loads the CSV data automatically on first run.

3. **Connect to the database**
   ```bash
   docker compose exec db psql -U postgres -d campus_bites
   ```

4. **Run queries**
   ```sql
   SELECT * FROM orders LIMIT 10;
   ```

## Database Schema

| Column             | Type          | Description                            |
|--------------------|---------------|----------------------------------------|
| order_id           | INTEGER       | Primary key                            |
| order_date         | DATE          | Date of order                          |
| order_time         | TIME          | Time of order                          |
| customer_segment   | VARCHAR(50)   | Customer type (Dorm, Greek Life, etc.) |
| order_value        | DECIMAL(10,2) | Order total in dollars                 |
| cuisine_type       | VARCHAR(50)   | Type of food ordered                   |
| delivery_time_mins | INTEGER       | Delivery time in minutes               |
| promo_code_used    | BOOLEAN       | Whether a promo code was used          |
| is_reorder         | BOOLEAN       | Whether this is a repeat order         |

## Useful Commands

```bash
# Stop the database
docker compose down

# Stop and delete all data (fresh start)
docker compose down -v

# View container logs
docker compose logs db
```

## Connection Details

| Property | Value        |
|----------|--------------|
| Host     | localhost    |
| Port     | 5432         |
| Database | campus_bites |
| User     | postgres     |
| Password | postgres     |
