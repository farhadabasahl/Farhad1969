# Database Schema Documentation

## Table: crypto_prices

### Overview
This table stores the price information for various cryptocurrencies.

### Columns

- **id**: Integer, Primary Key, Auto-incremented
  - Unique identifier for each record.
- **name**: String(50)
  - The name of the cryptocurrency.
- **last_trade**: Numeric(10, 2)
  - The most recent trade price of the cryptocurrency.
- **volume**: Numeric
  - The trading volume of the cryptocurrency.
- **time**: Timestamp
  - The time at which the record was created, defaults to the current timestamp.

### Indexes

- **idx_name**: Improves the performance of queries filtering by cryptocurrency name.
- **idx_last_trade**: Optimizes queries sorting or filtering by the last trade price.
- **idx_volume**: Enhances query performance for operations involving volume.

### Modifications

- **2024-05-25**: Changed the data type of `volume` to `Numeric(15, 2)` to accommodate larger values.

