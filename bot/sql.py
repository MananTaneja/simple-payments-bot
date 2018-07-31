CREATE_TABLE_USERS = """CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY,
    username NVARCHAR(32),
    first_name NVARCHAR(256),
    last_name NVARCHAR(256),
    first_seen DATETIME DEFAULT (DATETIME('now', 'utc', '+1 hour')),
    allowed BOOLEAN DEFAULT 1 -- users allowed to use the bot
);"""

# see issue #1
CREATE_TABLE_PAYMENTS = """CREATE TABLE IF NOT EXISTS Payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    unique_id NVARCHAR(128),
    user_id INTEGER,
    price INTEGER,
    successfull BOOLEAN,
    telegram_payment_id NVARCHAR(128),
    provider_payment_id NVARCHAR(128),
    invoice_date TIMESTAMP,
    successful_payment_date TIMESTAMP,
    test_token BOOLEAN DEFAULT 1 --if we were using the test token when the invoice has been issued
);"""

INSERT_OR_REPLACE_USER = """INSERT OR REPLACE INTO Users (user_id, username, first_name, last_name, first_seen)
VALUES (?, ?, ?, ?, DATETIME('now', 'utc', '+1 hour'));"""

UPDATE_USER = """UPDATE Users
SET username = ?, first_name = ?, last_name = ?
WHERE user_id = ?;"""

INSERT_PAYMENT_INVOICE = """INSERT INTO Payments (unique_id, user_id, price, invoice_date, test_token)
VALUES (?, ?, ?, ?, ?);"""

UPDATE_PAYMENT_SUCCESSFULL = """UPDATE Payments
SET
    successfull = 1
    ,telegram_payment_id = ?
    ,provider_payment_id = ?
    ,successful_payment_date = ?
WHERE unique_id = ?;"""

SELECT_TABLES = "SELECT name FROM sqlite_master WHERE type='table';"
