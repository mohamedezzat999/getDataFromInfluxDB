import GetDataFromDB
from flask import Flask, render_template, request, redirect, send_file
from flask import send_from_directory
from flask_datepicker import datepicker
import os
from flask_caching import Cache

cache = Cache()

sensor_report = Flask(__name__)
sensor_report.config['SECRET_KEY'] = '$#@!'
datepicker(sensor_report)
newfrom, newTo = "", ""

cache.init_app(sensor_report)
sensor_report.config['CACHE_TYPE'] = 'SimpleCache '


@sensor_report.route("/", methods=('GET', 'POST'))
@cache.cached(timeout=30)
def homepage():
    global newfrom, newTo, values, sensor_id
    sensor_id = request.form.get("sensor_id")
    g = GetDataFromDB.InfluxDB()
    ids = g.sensor_number()
    g.createDB()
    try:
        if request.method == 'POST':
            if request.form.get('submit_button') == 'Show Report':
                values = g.sensor_data(sensor_id, newfrom, newTo)
                return redirect('/report')
            """elif request.form.get('submit_button2') == 'Show Graph':
                print("graph is here")
                values = g.sensor_data(sensor_id, newfrom, newTo)
                return redirect("/graph")"""
            if request.form.get('submit_button3') == 'Show Graph':
                values = g.sensor_data(sensor_id, newfrom, newTo)
                if request.form['radio'] == 'tem':
                    return redirect("/graph_temperature")
                elif request.form['radio'] == 'hum':
                    return redirect("/graph_humidity")
                else:
                    print("something is wrong")
            if request.form.get('submit_button4') == 'Insert sensor name':
                print("add sensor button has been pressed!")
                return redirect('/add_name_for_sensor')
            else:
                data_get = request.get_json(force=True)
                from2 = data_get['from']
                to = data_get['to']
                newfrom = from2.replace("T", " ") + ":00"
                newTo = to.replace("T", " ") + ":00"
            # print(sensor_id, newfrom, newTo)
            """if request.form['submit_button'] == 'Set Duration':
            from2 = request.form.get('startTime')
            to = request.form.get('endTime')
            newfrom = from2.replace("T", " ") + ":00"
            newTo =  to.replace("T", " ") + ":00"
            print(sensor_id,newfrom,newTo)"""

    except Exception as e:
        print("Oops!", e, "occurred.")
        # return redirect(url_for('main'))
    return render_template('main.html', sensorsids=ids)


@sensor_report.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(sensor_report.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@sensor_report.route("/report", methods=('GET', 'POST'))
@cache.cached(timeout=30)
def report():
    g = GetDataFromDB.InfluxDB()
    g.put_data_in_csv(values)
    try:
        if request.method == 'POST':
            return redirect('/download_the_report')
        return render_template("index.html", sensors=values)
    except Exception as e:
        print("Oops!", e, "occurred.")


@sensor_report.route("/download_the_report")
def download_the_report():
    p = "SensorReport.csv"
    return send_file(p, as_attachment=True)


@sensor_report.route("/graph_temperature")
@cache.cached(timeout=30)
def graph_tem():
    g = GetDataFromDB.InfluxDB()
    try:
        labels, val = g.sort_the_graph(values)
        line_labels = labels
        line_values = val
        return render_template('graph.html', title='Temperature For Sensor ID :' + sensor_id, max=50,
                               labels=line_labels,
                               val=line_values)
    except Exception as e:
        print("Oops!", e, "occurred.")


@sensor_report.route("/graph_humidity")
@cache.cached(timeout=30)
def graph_hum():
    g = GetDataFromDB.InfluxDB()
    try:
        labels, val = g.sort_the_graph_hum(values)
        line_labels = labels
        line_values = val
        return render_template('graph.html', title='Humidity For Sensor ID :' + sensor_id, max=100,
                               labels=line_labels,
                               val=line_values)
    except Exception as e:
        print("Oops!", e, "occurred.")


@sensor_report.route("/add_name_for_sensor")
@cache.cached(timeout=30)
def sensor_name():
    g = GetDataFromDB.InfluxDB()
    ids = g.sensor_number()
    sensor_id = request.form.get("sensor_id")
    return render_template('sensor_named.html', sensorsids=ids)


if __name__ == '__main__':
    sensor_report.run(debug=True, port=9000)
