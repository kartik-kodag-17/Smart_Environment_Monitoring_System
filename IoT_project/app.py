from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="172.22.96.1",
        user="iot_project",
        password="iot@123",
        database="smart_env_monitoring",
        port = 3306,
        use_pure = True
    )

@app.route("/" , methods = ['GET'])
def index():
    return render_template("dashboard.html")

@app.route("/data" , methods = ['GET'])
def data():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT temp, humid, smoke_level, dta FROM env_data ORDER BY dta DESC LIMIT 50"
        )

        row = cursor.fetchall()
        cursor.close()
        db.close()

        if row:
            return jsonify(row)
        else:
            return jsonify({"temp": 0, "humid": 0, "smoke_level": 0, "dta": "No data"})

    except Exception as e:
        return jsonify({"error": str(e)})

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000, debug=True)