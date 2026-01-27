from flask import Flask, render_template, request, redirect, session, flash
from database import get_db, close_db

app = Flask(__name__)
app.secret_key = "secret123"
app.teardown_appcontext(close_db)

# ---------------- CREATE DEFAULT ADMIN ----------------
def create_default_admin():
    db = get_db()
    admin = db.execute(
        "SELECT * FROM users WHERE role='admin'"
    ).fetchone()

    if admin is None:
        db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "admin")
        )
        db.commit()
        print("Default admin created")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/student_login")

# -------- STUDENT REGISTER --------
@app.route("/student_register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, "student")
            )
            db.commit()
            flash("Registered successfully! Please login.", "success")
            return redirect("/student_login")

        except:
            flash("User already registered. Please login.", "error")
            return redirect("/student_login")

    return render_template("student_register.html")

# -------- STUDENT LOGIN --------
@app.route("/student_login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND role='student'",
            (username,)
        ).fetchone()

        if user and user["password"] == password:
            session["student"] = username
            return redirect("/student_dashboard")
        else:
            flash("Invalid credentials!", "error")

    return render_template("student_login.html")

# -------- STUDENT DASHBOARD --------
@app.route("/student_dashboard", methods=["GET", "POST"])
def student_dashboard():
    if "student" not in session:
        return redirect("/student_login")

    db = get_db()

    if request.method == "POST":
        db.execute("""
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
        flash("Complaint submitted successfully!", "success")
        return redirect("/student_dashboard")

    complaints = db.execute(
        "SELECT * FROM complaints WHERE student=?",
        (session["student"],)
    ).fetchall()

    return render_template(
        "student_dashboard.html",
        complaints=complaints,
        student=session["student"]
    )

# -------- ADMIN LOGIN --------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]

        db = get_db()
        admin = db.execute(
            "SELECT * FROM users WHERE username=? AND role='admin'",
            (username,)
        ).fetchone()

        if admin and admin["password"] == password:
            session["admin"] = username
            return redirect("/admin_dashboard")
        else:
            flash("Invalid admin credentials!", "error")

    return render_template("admin_login.html")

# -------- ADMIN DASHBOARD (FILTER WORKING) --------
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin_login")

    filter_status = request.args.get("filter")
    db = get_db()

    if filter_status == "pending":
        complaints = db.execute(
            "SELECT * FROM complaints WHERE status='Pending'"
        ).fetchall()

    elif filter_status == "in progress":
        complaints = db.execute(
            "SELECT * FROM complaints WHERE status='In Progress'"
        ).fetchall()

    elif filter_status == "resolved":
        complaints = db.execute(
            "SELECT * FROM complaints WHERE status='Resolved'"
        ).fetchall()

    else:
        complaints = db.execute(
            "SELECT * FROM complaints"
        ).fetchall()

    return render_template("admin_dashboard.html", complaints=complaints)

# -------- UPDATE STATUS --------
@app.route("/update_status", methods=["POST"])
def update_status():
    if "admin" not in session:
        return redirect("/admin_login")

    db = get_db()
    db.execute(
        "UPDATE complaints SET status=? WHERE id=?",
        (request.form["status"], request.form["id"])
    )
    db.commit()

    flash("Status updated successfully!", "success")
    return redirect("/admin_dashboard")

# -------- DELETE COMPLAINT --------
@app.route("/delete_complaint/<int:id>", methods=["POST"])
def delete_complaint(id):
    if "admin" not in session:
        return redirect("/admin_login")

    db = get_db()
    db.execute(
        "DELETE FROM complaints WHERE id=?",
        (id,)
    )
    db.commit()

    flash("Complaint deleted successfully!", "success")
    return redirect("/admin_dashboard")

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/student_login")

# -------- RUN APP --------
if __name__ == "__main__":
    with app.app_context():
        create_default_admin()
    app.run(host="0.0.0.0", port=5000, debug=True)
