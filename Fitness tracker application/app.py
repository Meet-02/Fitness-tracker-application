from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'database/mydata.db')


# ---------- DB Helper ----------
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv


# ---------- Home Page ----------
@app.route('/')
def index():
    workouts = query_db("SELECT * FROM workouts ORDER BY id DESC")
    diets = query_db("SELECT * FROM diets ORDER BY id DESC")
    wearables = query_db("SELECT * FROM wearables ORDER BY id DESC")

    return render_template("index.html", workouts=workouts, diets=diets, wearables=wearables)


# =====================================================
#                WORKOUTS
# =====================================================

# --- API Endpoints ---
@app.route("/workouts", methods=["GET"])
def get_workouts():
    rows = query_db("SELECT * FROM workouts ORDER BY id DESC")
    return jsonify([{"id": r[0], "type": r[1], "duration": r[2], "calories": r[3]} for r in rows])

@app.route("/workouts", methods=["POST"])
def add_workout_api():
    data = request.json
    query_db("INSERT INTO workouts (type,duration,calories) VALUES (?,?,?)",
             (data["type"], data["duration"], data["calories"]))
    return jsonify({"message": "Workout added"})


# --- Form Submission ---
@app.route("/add_workout", methods=["POST"])
def add_workout_form():
    type_ = request.form["type"]
    duration = request.form["duration"]
    calories = request.form["calories"]
    query_db("INSERT INTO workouts (type,duration,calories) VALUES (?,?,?)",
             (type_, duration, calories))
    return redirect(url_for("index"))


@app.route("/update_workout/<int:id>", methods=["GET", "POST"])
def update_workout(id):
    if request.method == "POST":
        type_ = request.form["type"]
        duration = request.form["duration"]
        calories = request.form["calories"]
        query_db("UPDATE workouts SET type=?, duration=?, calories=? WHERE id=?",
                 (type_, duration, calories, id))
        return redirect(url_for("index"))
    workout = query_db("SELECT * FROM workouts WHERE id=?", (id,), one=True)
    return render_template("update_workout.html", workout=workout)


@app.route("/delete_workout/<int:id>")
def delete_workout(id):
    query_db("DELETE FROM workouts WHERE id=?", (id,))
    return redirect(url_for("index"))


# =====================================================
#                DIETS
# =====================================================

@app.route("/diets", methods=["GET"])
def get_diets():
    rows = query_db("SELECT * FROM diets ORDER BY id DESC")
    return jsonify([{"id": r[0], "meal": r[1], "calories": r[2], "protein": r[3]} for r in rows])

@app.route("/diets", methods=["POST"])
def add_diet_api():
    data = request.json
    query_db("INSERT INTO diets (meal,calories,protein) VALUES (?,?,?)",
             (data["meal"], data["calories"], data["protein"]))
    return jsonify({"message": "Diet added"})


@app.route("/add_diet", methods=["POST"])
def add_diet_form():
    meal = request.form["meal"]
    calories = request.form["calories"]
    protein = request.form["protein"]
    query_db("INSERT INTO diets (meal,calories,protein) VALUES (?,?,?)",
             (meal, calories, protein))
    return redirect(url_for("index"))


@app.route("/update_diet/<int:id>", methods=["GET", "POST"])
def update_diet(id):
    if request.method == "POST":
        meal = request.form["meal"]
        calories = request.form["calories"]
        protein = request.form["protein"]
        query_db("UPDATE diets SET meal=?, calories=?, protein=? WHERE id=?",
                 (meal, calories, protein, id))
        return redirect(url_for("index"))
    diet = query_db("SELECT * FROM diets WHERE id=?", (id,), one=True)
    return render_template("update_diet.html", diet=diet)


@app.route("/delete_diet/<int:id>")
def delete_diet(id):
    query_db("DELETE FROM diets WHERE id=?", (id,))
    return redirect(url_for("index"))


# =====================================================
#                WEARABLES
# =====================================================

@app.route("/wearables", methods=["GET"])
def get_wearables():
    rows = query_db("SELECT * FROM wearables ORDER BY id DESC LIMIT 10")
    return jsonify([{"id": r[0], "heart_rate": r[1], "steps": r[2], "recorded_at": r[3]} for r in rows])

@app.route("/wearables", methods=["POST"])
def add_wearable_api():
    data = request.json
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query_db("INSERT INTO wearables (heart_rate,steps,recorded_at) VALUES (?,?,?)",
             (data["heart_rate"], data["steps"], now))
    return jsonify({"message": "Wearable data added"})


@app.route("/add_wearable", methods=["POST"])
def add_wearable_form():
    heart_rate = request.form["heart_rate"]
    steps = request.form["steps"]
    recorded_at = request.form["recorded_at"]
    query_db("INSERT INTO wearables (heart_rate,steps,recorded_at) VALUES (?,?,?)",
             (heart_rate, steps, recorded_at))
    return redirect(url_for("index"))


@app.route("/update_wearable/<int:id>", methods=["GET", "POST"])
def update_wearable(id):
    if request.method == "POST":
        heart_rate = request.form["heart_rate"]
        steps = request.form["steps"]
        recorded_at = request.form["recorded_at"]
        query_db("UPDATE wearables SET heart_rate=?, steps=?, recorded_at=? WHERE id=?",
                 (heart_rate, steps, recorded_at, id))
        return redirect(url_for("index"))
    wearable = query_db("SELECT * FROM wearables WHERE id=?", (id,), one=True)
    return render_template("update_wearable.html", wearable=wearable)


@app.route("/delete_wearable/<int:id>")
def delete_wearable(id):
    query_db("DELETE FROM wearables WHERE id=?", (id,))
    return redirect(url_for("index"))


# =====================================================
# Run App
# =====================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
