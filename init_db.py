import sqlite3


def dbconnection(self):
    try:
        conn = sqlite3.connect("sensorsName.sqllite")
    except sqlite3.error as e:
        print(e)

    cursor = conn.cursor()
    sql_query = """CREATE TABLE sensorNames (
    id integer PRIMARY KEY AUTOINCREMENT,
    sensorId integer NOT NULL ,
    sensorName text 
    )"""
    cursor.execute(sql_query)
    return conn


    def addsensors(self):
        conn = sqlite3.connect("sensorsName.sqllite")
        cursor = conn.cursor()
        ids =self.sensor_number()
        for num in ids:
            cursor.execute("INSERT INTO sensorNames (sensorId,sensorName) VALUES (?,?)",(num,' '))
            print("added" + num)

