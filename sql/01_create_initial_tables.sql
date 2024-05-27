CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    last_trade NUMERIC(10, 2) NOT NULL,
    volume NUMERIC NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_name ON crypto_prices(name);
