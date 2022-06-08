DROP TABLE IF EXISTS numbers ;
DROP TABLE IF EXISTS duration;
DROP TABLE IF EXISTS alarms;
DROP TABLE IF EXISTS groupm;

CREATE TABLE numbers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Name TEXT NOT NULL,
    Number TEXT NOT NULL
);

CREATE TABLE duration (
    time INTEGER NOT NULL
);
CREATE TABLE groupm (
    message TEXT NOT NULL,
    Number TEXT NOT NULL
);

CREATE TABLE alarms (
    type TEXT NOT NULL,
    sensorid TEXT NOT NULL,
    gatewayid TEXT NOT NULL,
    value TEXT NOT NULL,
    time TEXT NOT NULL,
    sendstatus TEXT NOT NULL
);