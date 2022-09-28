CREATE TABLE user
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username NVARCHAR(70) NOT NULL UNIQUE,
    password NVARCHAR(200) NOT NULL,
    email NVARCHAR(150) NOT NULL,
    type INTEGER NOT NULL DEFAULT 0,
    lastresettime BIGINT,
    lastresetcode NVARCHAR(70)
);

CREATE TABLE transfers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner INTEGER NOT NULL,
    recvname NVARCHAR(200) NOT NULL,
    recvaccnum NVARCHAR(40) NOT NULL,
    transferdate BIGINT NOT NULL,
    ammount BIGINT NOT NULL CHECK (ammount > 0), 
    FOREIGN KEY (owner) REFERENCES user(id)
);
