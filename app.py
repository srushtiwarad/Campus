from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "secret123"

# ----------------- Users -----------------
students = {
    "arya":"1234",
    "bob":"abcd",
    "alice":"pass1",
    "charlie":"pass2",
    "srushti":"srushti123",
    "student":"stud"
}

admins = {
    "dean":"d123",
    "admin":"admin123"
}

# ----------------- Complaints -----------------
complaints = [
    {"id":1, "student":"arya","title":"Wi-Fi not working","category":"Wi-Fi","description":"Internet slow","status":"Pending"},
    {"id":2, "student":"bob","title":"Mess food","category":"Mess","description":"Cold food","status":"In Progress"}
]

# ----------------- Routes -----------------
@app.route("/")
def home():
    return redirect("/student_login")

# -------- Student Login --------
@app.route("/student_login", methods=["GET","POST"])
def student_login():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]
        if username in students and students[username] == password:
            session["student"] = username
            return redirect("/student_dashboard")
        else:
            return "Invalid credentials!"
    return render_template("student_login.html")

# -------- Student Dashboard --------
@app.route("/student_dashboard", methods=["GET","POST"])
def student_dashboard():
    if "student" not in session:
        return redirect("/student_login")
    
    if request.method == "POST":
        new_complaint = {
            "id": len(complaints)+1,
            "student": session["student"],
            "title": request.form["title"],
            "category": request.form["category"],
            "description": request.form["description"],
            "status": "Pending"
        }
        complaints.append(new_complaint)
        return redirect("/student_dashboard")
    
    student_complaints = [c for c in complaints if c["student"] == session["student"]]
    return render_template("student_dashboard.html", complaints=student_complaints, student=session["student"].capitalize())

# -------- Admin Login --------
@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]
        if username in admins and admins[username] == password:
            session["admin"] = username
            return redirect("/admin_dashboard")
        else:
            return "Invalid credentials!"
    return render_template("admin_login.html")

# -------- Admin Dashboard --------
@app.route("/admin_dashboard", methods=["GET","POST"])
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin_login")
    
    filter_status = request.args.get("filter")
    filtered_complaints = complaints
    if filter_status:
        filtered_complaints = [c for c in complaints if c["status"].lower() == filter_status.lower()]
    
    return render_template("admin_dashboard.html", complaints=filtered_complaints)

# -------- Update Complaint Status --------
@app.route("/update_status", methods=["POST"])
def update_status():
    comp_id = int(request.form["id"])        # Get complaint ID
    new_status = request.form["status"]      # Get selected status
    for comp in complaints:                  # Find the complaint in list
        if comp["id"] == comp_id:
            comp["status"] = new_status     # Update the status
            break
    return redirect("/admin_dashboard")      # Redirect back to dashboard


# -------- Logout --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/student_login")

# ----------------- Run App -----------------
if __name__ == "__main__":
    app.run(debug=True)
