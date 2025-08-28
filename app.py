from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, Grade

app = Flask(__name__)
app.secret_key = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    students = Student.query.all()
    # Precompute averages for listing
    avg_map = {}
    for s in students:
        if s.grades:
            avg_map[s.id] = round(sum(g.score for g in s.grades) / len(s.grades), 2)
        else:
            avg_map[s.id] = None
    return render_template("index.html", students=students, avg_map=avg_map)

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"].strip()
        roll = request.form["roll"].strip()

        if not name or not roll:
            flash("⚠️ Name and Roll Number are required.")
            return redirect(url_for("add_student"))

        if Student.query.filter_by(roll_number=roll).first():
            flash("⚠️ Roll number already exists!")
            return redirect(url_for("add_student"))

        new_student = Student(name=name, roll_number=roll)
        db.session.add(new_student)
        db.session.commit()
        flash("✅ Student added successfully!")
        return redirect(url_for("index"))
    return render_template("add_student.html")

@app.route("/add_grade/<int:student_id>", methods=["GET", "POST"])
def add_grade(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == "POST":
        subject = request.form["subject"].strip()
        try:
            score = int(request.form["score"])
        except ValueError:
            flash("⚠️ Score must be an integer between 0 and 100.")
            return redirect(url_for("add_grade", student_id=student.id))

        if not subject:
            flash("⚠️ Subject is required.")
            return redirect(url_for("add_grade", student_id=student.id))

        if 0 <= score <= 100:
            new_grade = Grade(subject=subject, score=score, student_id=student.id)
            db.session.add(new_grade)
            db.session.commit()
            flash("✅ Grade added successfully!")
        else:
            flash("⚠️ Score must be between 0 and 100.")
        return redirect(url_for("view_student", student_id=student.id))
    return render_template("add_grade.html", student=student)

@app.route("/student/<int:student_id>")
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    grades = Grade.query.filter_by(student_id=student.id).all()
    avg = round(sum(g.score for g in grades) / len(grades), 2) if grades else None
    return render_template("view_student.html", student=student, grades=grades, avg=avg)

@app.route("/delete_student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    # Delete grades first due to FK constraint
    for g in list(student.grades):
        db.session.delete(g)
    db.session.delete(student)
    db.session.commit()
    flash("🗑️ Student deleted.")
    return redirect(url_for("index"))

@app.route("/delete_grade/<int:grade_id>", methods=["POST"])
def delete_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    sid = grade.student_id
    db.session.delete(grade)
    db.session.commit()
    flash("🗑️ Grade removed.")
    return redirect(url_for("view_student", student_id=sid))

# Simple class average & subject topper utilities
@app.route("/reports")
def reports():
    students = Student.query.all()
    # Class averages per subject
    subject_scores = {}
    for s in students:
        for g in s.grades:
            subject_scores.setdefault(g.subject, []).append(g.score)
    subject_avg = {subj: round(sum(vals)/len(vals), 2) for subj, vals in subject_scores.items()} if subject_scores else {}

    # Topper per subject
    toppers = {}
    for subj, vals in subject_scores.items():
        top_grade = None
        top_student = None
        for s in students:
            for g in s.grades:
                if g.subject == subj:
                    if top_grade is None or g.score > top_grade:
                        top_grade = g.score
                        top_student = s
        if top_student is not None:
            toppers[subj] = {"student_name": top_student.name, "roll_number": top_student.roll_number, "score": top_grade}

    return render_template("reports.html", subject_avg=subject_avg, toppers=toppers)

if __name__ == "__main__":
    print("🚀 Student Performance Tracker is starting...")
    app.run(debug=True,host="0.0.0.0", port=5000)
    

