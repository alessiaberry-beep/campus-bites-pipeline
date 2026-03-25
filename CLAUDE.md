# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Campus Bites Pipeline is a data pipeline that loads campus food delivery order data from CSV into a PostgreSQL database for analysis.

## Commands

```bash
# Start the database
docker compose up -d

# Stop the database
docker compose down

# Fresh start (delete all data)
docker compose down -v

# Connect to database
docker compose exec db psql -U postgres -d campus_bites

# Load data (requires venv activated)
source venv/bin/activate
pip install pandas psycopg2-binary
python load_orders.py
```

## Architecture

- **docker-compose.yml**: PostgreSQL 16 container configuration
- **load_orders.py**: Python script that reads CSV, converts Yes/No to booleans, creates table, and inserts data
- **data/campus_bites_orders.csv**: Source data file

## Database

- **Host**: localhost:5432
- **Database**: campus_bites
- **User/Password**: postgres/postgres
- **Table**: orders (order_id, order_date, order_time, customer_segment, order_value, cuisine_type, delivery_time_mins, promo_code_used, is_reorder)
