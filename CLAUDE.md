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

# View container logs
docker compose logs db

# Connect to database
docker compose exec db psql -U postgres -d campus_bites

# Load data (safe to re-run; uses ON CONFLICT DO NOTHING)
source venv/bin/activate
python load_orders.py
```

## Architecture

- **docker-compose.yml**: PostgreSQL 16 container with healthcheck and persistent volume
- **load_orders.py**: Python script that reads CSV, converts Yes/No to booleans, creates table, and inserts data (idempotent)
- **data/campus_bites_orders.csv**: Source data file

## Database

- **Connection**: localhost:5432, database `campus_bites`, user/password `postgres/postgres`
- **Table**: `orders` with columns: order_id (PK), order_date, order_time, customer_segment, order_value, cuisine_type, delivery_time_mins, promo_code_used (bool), is_reorder (bool)
