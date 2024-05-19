CREATE TABLE crypto_prices (
    name VARCHAR(50),
    last_trade NUMERIC,
    volume NUMERIC,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
