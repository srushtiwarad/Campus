from flask import Flask, render_template, request, redirect, session
from database import get_db

app = Flask(__name__)
app.secret_key = "secret123"

# ----------------- Home -----------------
@app.route("/")
def home():
    return redirect("/student_login")

# -------- Student Register --------
@app.route("/student_register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, "student")
            )
            db.commit()
            return redirect("/student_login")
        except:
            return "User already exists!"

    return render_template("student_register.html")

# -------- Student Login --------
@app.route("/student_login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role='student'",
            (username, password)
        )
        user = cur.fetchone()

        if user:
            session["student"] = username
            return redirect("/student_dashboard")
        else:
            return "Invalid credentials!"

    return render_template("student_login.html")

# -------- Student Dashboard --------
@app.route("/student_dashboard", methods=["GET", "POST"])
def student_dashboard():
    if "student" not in session:
        return redirect("/student_login")

    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        cur.execute("""
            INSERT INTO complaints (student, title, category, description, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["student"],
            request.form["title"],
            request.form["category"],
            request.form["description"],
            "Pending"
        ))
        db.commit()
        return redirect("/student_dashboard")

    cur.execute(
        "SELECT * FROM complaints WHERE student=?",
        (session["student"],)
    )
    complaints = cur.fetchall()

    return render_template(
        "student_dashboard.html",
        complaints=complaints,
        student=session["student"]
    )

# -------- Admin Login --------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = username
            return redirect("/admin_dashboard")
        else:
            return "Invalid credentials!"

    return render_template("admin_login.html")

# -------- Admin Dashboard --------
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin_login")

    status = request.args.get("filter")
    db = get_db()
    cur = db.cursor()

    if status:
        cur.execute("SELECT * FROM complaints WHERE status=?", (status,))
    else:
        cur.execute("SELECT * FROM complaints")

    complaints = cur.fetchall()
    return render_template("admin_dashboard.html", complaints=complaints)

# -------- Update Complaint Status --------
@app.route("/update_status", methods=["POST"])
def update_status():
    comp_id = request.form["id"]
    new_status = request.form["status"]

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE complaints SET status=? WHERE id=?",
        (new_status, comp_id)
    )
    db.commit()

    return redirect("/admin_dashboard")

# -------- Logout --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/student_login")

# ----------------- Run App -----------------
if __name__ == "__main__":
    app.run(debug=True)

