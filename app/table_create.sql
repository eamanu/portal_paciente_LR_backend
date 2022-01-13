CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id CHAR(25) NOT NULL,
    password_hash CHAR(100) NOT NULL
)

INSERT INTO users(user_id, password_hash)
    VALUES ('admin', '$2b$12$nW9bzZJggFAyYYI.soU8GurU.0g82ftRBNfn.v9vtIDWmt/RJdgr2')
