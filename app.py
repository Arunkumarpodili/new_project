from flask import Flask, render_template, request, jsonify, flash, redirect,session
from flask_mysqldb  import MySQL, MySQLdb
import pandas as pd
import json
from scipy.signal import savgol_filter
import mysql.connector as sql
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
app = Flask(__name__)
db_connection = sql.connect(host='localhost', database='vehicledata1', user="root", password='aparna',auth_plugin='mysql_native_password')
app.secret_key = "caircocoders-ednalan"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'aparna'
app.config['MYSQL_DB'] = "vehicledata1"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
@app.route("/", methods=["GET", "POST"])
def get_odo():
    return render_template("index.html", c1result=None)
@app.route("/count", methods=["POST"])
def count():
    if request.method == "POST":
        start_date = request.form['start']
        end_date = request.form['end']
        selected_table = request.form.get('table_name')
        cur = mysql.connection.cursor()
        alltables = ['b1allsaints',"b1trivenienterprises002","b1rajkamalscreations003","b1youdeemerchandising004"]
        results = []
        for total in alltables:
            query = "SELECT * FROM {} WHERE date_time BETWEEN %s AND %s".format(total)
            cur.execute(query, (start_date, end_date))
            table_data = cur.fetchall()
            df = pd.DataFrame(table_data)
            df.rename(columns={'Data Actual Time': 'date_time'}, inplace=True)
            op_col = []
            for i in df['Speed']:
                op_col.append(i)
            np.set_printoptions(threshold=np.inf)
            lower_limit = int(request.form.get('lower_limit', 0))
            upper_limit1 = int(request.form.get('upper_limit1', 0))
            upper_limit2 = int(request.form.get('upper_limit2', 0))

            x = np.array(op_col)
            x1 = x.astype('int32')
            sub_lists = np.split(x1, np.where(np.diff(x1) < 0)[0] + 1)
            id_count = 0
            for unit in sub_lists:
                if min(unit) <= lower_limit and max(unit) > upper_limit1 and max(unit) < upper_limit2 and len(
                        set(unit)) > 1:
                    id_count += 1
            results.append((id_count, total))
            results.sort(reverse=True)
            top_3_results = results[:3]
            data = [
                {"data": item[0], "label": item[1]} for item in top_3_results
            ]
            json_data1 = json.dumps(data)
            print(json_data1)

        if selected_table == 'all':
            selected_tables = [ 'b1rajkamals003', 'b1youdeemerchandising004','b1trivenienterprises005','b1panchsheelapharma006']
        else:
            selected_tables = [selected_table]
        id_count=0
        for table in selected_tables:
            query = "SELECT * FROM {} WHERE date_time BETWEEN %s AND %s".format(table)
            cur.execute(query, (start_date, end_date))
            table_data = cur.fetchall()
            df = pd.DataFrame(table_data)
            op_col = []
            for i in df['Speed']:
                op_col.append(i)
            np.set_printoptions(threshold=np.inf)
            lower_limit = int(request.form.get('lower_limit', 0))
            upper_limit1 = int(request.form.get('upper_limit1', 0))
            upper_limit2 = int(request.form.get('upper_limit2', 0))
            x = np.array(op_col)
            x1 = x.astype('int32')
            sub_lists = np.split(x1, np.where(np.diff(x1) < 0)[0] + 1)
            id_count = 0
            for unit in sub_lists:
                if min(unit) <= lower_limit and max(unit) > upper_limit1 and max(unit) < upper_limit2 and len(
                        set(unit)) > 1:
                    id_count += 1
        return jsonify({'htmlresponse': render_template('acceleration.html',id_count=id_count,results=results,json_data1=json_data1)})

@app.route("/range", methods=["POST", "GET"])
def range():
    formatted_num=None
    if request.method == "POST":
        start_date = request.form['start']
        end_date = request.form['end']
        selected_table = request.form.get('table_name')
        cur = mysql.connection.cursor()
        alltables = ['b1allsaints',"b1trivenienterprises002","b1rajkamalscreations003","b1youdeemerchandising004"]
        results = []
        for total in alltables:
            query = "SELECT * FROM {} WHERE date_time BETWEEN %s AND %s".format(total)
            cur.execute(query, (start_date, end_date))
            table_data = cur.fetchall()
            df = pd.DataFrame(table_data)
            df = df[(df['IGN'] == 'On') & (df['GPS'] == 'On')]
            df2 = df.drop_duplicates(subset=['Odometer'])
            df1 = df2[df2['Odometer'] != 0]
            df1["Odometer"] = df1["Odometer"].diff()
            df3 = df1.groupby(df1.date_time.dt.date)['Odometer'].sum()
            result = df3.sum() / len(df3) * 0.001
            formatted_num = "{:.2f}".format(result)
            results.append((result, total))
            results.sort(reverse=True)
            top_3_results = results[:3]
            data = [
                {"data": item[0], "label": item[1]} for item in top_3_results
            ]
            json_data = json.dumps(data)

        if selected_table == 'all':
            selected_tables = ['b1allsaints',"b1trivenienterprises002","b1rajkamalscreations003","b1youdeemerchandising004"]
        else:
            selected_tables = [selected_table]
        total_sum = 0
        id_count = 0
        counts = []
        individual_results = []  # Store individual results for each selected table
        for table in selected_tables:
            query = "SELECT * FROM {} WHERE date_time BETWEEN %s AND %s".format(table)
            cur.execute(query, (start_date, end_date))
            table_data = cur.fetchall()
            df = pd.DataFrame(table_data)
            df.rename(columns={'Data Actual Time': 'date_time'}, inplace=True)

            df = df[(df['IGN'] == 'On') & (df['GPS'] == 'On')]
            df2 = df.drop_duplicates(subset=['Odometer'])
            df1 = df2[df2['Odometer'] != 0]
            df1["Odometer"] = df1["Odometer"].diff()
            df3 = df1.groupby(df1.date_time.dt.date)['Odometer'].sum()

            result = df3.sum() / len(df3)* 0.001
            formatted_num = "{:.2f}".format(result)
            total_sum += result
            individual_results.append(result)  # Store the individual result for the current table
            counts.append((id_count, table))

        average_result = sum(individual_results) / len(individual_results)  # Calculate the average result
        formatted_average_result = "{:.2f}".format(average_result)  # Format the average result to 2 decimal places

        return jsonify({'htmlresponse': render_template('odo.html',average_result=average_result, c1result=formatted_num,json_data=json_data,count_result=id_count)})
@app.route("/speed",methods=["POST"])
def speed():
    if request.method == "POST":
        start_date = request.form['start']
        end_date = request.form['end']
        selected_table = request.form.get('table_name')
        cur = mysql.connection.cursor()
        if selected_table == 'all':
            selected_tables = ['b1allsaints',"b1trivenienterprises002","b1rajkamalscreations003","b1youdeemerchandising004"]
        else:
            selected_tables = [selected_table]
        for table in selected_tables:
            query = "SELECT * FROM {} WHERE date_time BETWEEN %s AND %s".format(table)
            cur.execute(query, (start_date, end_date))
            table_data = cur.fetchall()
            df = pd.DataFrame(table_data)
            df["date_time"] = pd.to_datetime(df["date_time"])
            df1 = df[df['Speed'] != 0]
            grouped = df1.groupby(df1.date_time.dt.date)
            df2 = df[df['Speed'] <= 35]
            grouped1 = df.groupby(df2.date_time.dt.date)
            top_speed =grouped1["Speed"].max()
            avg_speed = grouped["Speed"].mean()
            df_json = avg_speed.to_json(date_format='iso')
            df1_json = top_speed.to_json(date_format="iso")
        return jsonify({'htmlresponse': render_template('speed.html',data=df_json,data1=df1_json)})
@app.route("/batterycyclescount",methods=["POST"])
def battery():
    if request.method == "POST":
        start_date = request.form['start']
        end_date = request.form['end']
        selected_table = request.form.get('table_name')
        cur = mysql.connection.cursor()
        if selected_table == 'all':
            selected_tables = ['b1allsaints',"b1trivenienterprises002","b1rajkamalscreations003","b1youdeemerchandising004"]
        else:
            selected_tables = [selected_table]
        for table in selected_tables:
            query = "SELECT * FROM {} WHERE date_time BETWEEN %s AND %s".format(table)
            cur.execute(query, (start_date, end_date))
            table_data = cur.fetchall()
            df = pd.DataFrame(table_data)
            df["date_time"] = pd.to_datetime(df["date_time"])
            d = df[df["Voltage(v)"].astype(float) > 40]
            y = d["Voltage(v)"]
            yhat = savgol_filter(y, 201, 2)
            sub_lists = np.split(yhat, np.where(np.diff(yhat) > 0)[0] + 1)
            id_count1 = 0
            id_list1 = []
            for unit in sub_lists:
                if max(unit) > 0 and len(set(unit)) > 1:
                    print("cycles")
            id_list2 = []
            for unit in sub_lists:
                if max(unit) > 0 and len(set(unit)) > 1:
                    id = (max(unit) - min(unit)) / 13.6
                    id_list2.append(id)
            count=sum(id_list2)
            formatted_count = "{:.2f}".format(count)
            print(sum(id_list2))
        return jsonify({'htmlresponse': render_template('battery.html',data=formatted_count)})
if __name__== '__main__':
 app.run(debug=True,port="3796")