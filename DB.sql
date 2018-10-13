CREATE TABLE server_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE ON CONFLICT FAIL,
    value TEXT NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT NOT NULL UNIQUE ON CONFLICT FAIL,
    credit REAL NOT NULL CHECK ( credit >= 0 )
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE ON CONFLICT FAIL,
    price REAL NOT NULL CHECK ( price >= 0 )
);

CREATE TABLE user_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (item_id) REFERENCES items(id),
    UNIQUE(user_id, item_id) ON CONFLICT FAIL
);

INSERT INTO server_settings (name, value)
VALUES ('start_credit_min', '12.7'),
       ('start_credit_max', '25.5');

INSERT INTO users (nickname, credit)
VALUES ("dude1", 30),
       ("dude2", 40);

INSERT INTO items (name, price)
VALUES ("Ship1", 5),
       ("Ship2", 10),
       ("Ship3", 7),
       ("Boat1", 2),
       ("Boat2", 3),
       ("Boat3", 4);

INSERT INTO user_item (user_id, item_id)
VALUES (1, 1), -- dude1 -> Ship1
       (1, 3), -- dude1 -> Ship3
       (1, 5), -- dude1 -> Boat2
       (2, 2), -- dude2 -> Ship2
       (2, 4); -- dude2 -> Boat1