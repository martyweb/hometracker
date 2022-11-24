drop table IF EXISTS apps;
CREATE TABLE IF NOT EXISTS apps (app TEXT PRIMARY KEY, appclass TEXT,status TEXT NOT NULL,lastrun TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

insert or ignore into apps VALUES("Weather","weather","Not Running", null);
insert or ignore into apps VALUES("Speed Test", "speed_test","Not Running", null);
insert or ignore into apps VALUES("Air Quality", "air_quality","Not Running", null);
insert or ignore into apps VALUES("Polution", "polution","Not Running", null);

drop table IF EXISTS logs;
CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT,log TEXT NOT NULL,created TIMESTAMP DEFAULT CURRENT_TIMESTAMP);