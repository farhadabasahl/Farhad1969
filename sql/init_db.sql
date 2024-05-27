CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    last_trade NUMERIC,
    volume NUMERIC,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);