from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])


@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json
    conn = get_db()

    conn.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (data["name"], data["age"], data["course"]),
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})


@app.route("/update_student/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.json
    conn = get_db()

    conn.execute(
        "UPDATE students SET name=?, age=?, course=? WHERE id=?",
        (data["name"], data["age"], data["course"], id),
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "updated"})


@app.route("/delete_student/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})


if __name__ == "__main__":

    conn = sqlite3.connect("students.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, course TEXT)"
    )
    conn.close()

    app.run(debug=True)