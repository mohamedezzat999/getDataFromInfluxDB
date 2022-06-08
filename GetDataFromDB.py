import csv
import sqlite3

from influxdb import InfluxDBClient

domain = 'skarpthub.duckdns.org'
ip = '192.168.1.174'
port = 8086


class InfluxDB:
    client = InfluxDBClient(ip, port, 'skarpt', 'skarpt', "mohamed.autogen.Tzone")

    def put_data_in_csv(self, values):
        csv_columns = ['SensorID', 'time', 'Temperature', 'Humidity', 'GatewayID', 'Battery']
        csv_file = "SensorReport.csv"
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in values:
                    writer.writerow(data)
        except IOError:
            print(IOError)

    def sensor_number(self):
        sensorids = self.client.query("SHOW TAG VALUES ON mohamed FROM Tzone WITH KEY = SensorID")
        sensorids = list(sensorids.get_points(measurement="Tzone"))
        ids = []
        for sensorid in sensorids:
            ids.append(sensorid['value'])
        return ids

    def sensor_data(self, sensor_id, from2, to):
        # sensor_id = 62210222
        # self.client.get_list_database()

        results = self.client.query(
            "SELECT * FROM mohamed.autogen.Tzone WHERE SensorID = '{}' and time > '{}' and time < '{}'  ".format(
                sensor_id, from2, to))
        valus_gen = results.get_points(measurement="Tzone")
        # results = self.client.query("SELECT * FROM example.autogen.Tzone WHERE SensorID = '{}' AND time > '{}' and
        # time < '{}'".format(sensor_id,startDate,endDate))
        values = list(valus_gen)
        # return values[-2881:-1]
        return values

    def sort_the_graph(self, results):
        labels = []
        val = []
        if len(results) < 1000:
            for i in results[0::50]:
                labels.append(i['Temperature'])
                val.append(i['time'])
        elif len(results) < 5000:
            for i in results[0::100]:
                labels.append(i['Temperature'])
                val.append(i['time'])
        elif len(results) < 10000:
            for i in results[0::200]:
                labels.append(i['Temperature'])
                val.append(i['time'])
        elif len(results) < 40000:
            for i in results[0::620]:
                labels.append(i['Temperature'])
                val.append(i['time'])
        else:
            for i in results[0::1500]:
                labels.append(i['Temperature'])
                val.append(i['time'])

        return val, labels

    def sort_the_graph_hum(self, results):
        labels = []
        val = []
        if len(results) < 1000:
            for i in results[0::50]:
                labels.append(i['Temperature'])
                val.append(i['time'])
        elif len(results) < 5000:
            for i in results[0::100]:
                labels.append(i['Humidity'])
                val.append(i['time'])
        elif len(results) < 10000:
            for i in results[0::200]:
                labels.append(i['Humidity'])
                val.append(i['time'])
        elif len(results) < 40000:
            for i in results[0::620]:
                labels.append(i['Humidity'])
                val.append(i['time'])
        else:
            for i in results[0::1500]:
                labels.append(i['Humidity'])
                val.append(i['time'])

        return val, labels


    def names(self):
        conn = sqlite3.connect("sensorsName.sqllite")
        cursor = conn.cursor()
        cursor.execute("SELECT sensorName FROM sensorNames")
        names = [
            dict(id=row[0], sensorId=row[1], sensorName=row[2]) for row in cursor.fetchall()
        ]
        if names is not None:
            print( names)



if __name__ == '__main__':
    i = InfluxDB()
    # i.sensor_data()
    i.names()