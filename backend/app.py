import os
import sqlite3
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

from database import init_db, get_db_connection
from model_utils import (
    predict_career_from_skills,
    predict_career_from_resume_text,
    get_model_metrics
)
from resume_parser import extract_text_from_pdf, extract_skills_from_text
from analyzer import analyze_skill_gap, get_career_requirements
from recommender import generate_learning_path, get_skill_resource

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Initialize Flask App with static frontend serving
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

# Initialize Database on Startup
with app.app_context():
    init_db()

@app.route("/api/careers", methods=["GET"])
def get_careers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT career FROM career_skills")
        rows = cursor.fetchall()
        careers = [r["career"] for r in rows]
        
        result = []
        for c in careers:
            reqs = get_career_requirements(c)
            result.append({
                "name": c,
                "required_skills_count": len(reqs),
                "core_skills": [r["skill"] for r in reqs if int(r.get("importance", 0)) >= 4][:5]
            })
        conn.close()
        return jsonify({"status": "success", "careers": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/careers/<career_name>", methods=["GET"])
def get_career_details(career_name):
    try:
        reqs = get_career_requirements(career_name)
        if not reqs:
            return jsonify({"status": "error", "message": f"Career '{career_name}' not found"}), 404
        return jsonify({
            "status": "success",
            "career": career_name,
            "requirements": reqs
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/predict-career", methods=["POST"])
def predict_career():
    try:
        data = request.get_json() or {}
        user_skills = data.get("skills", [])

        if not isinstance(user_skills, list):
            return jsonify({"status": "error", "message": "'skills' must be a list"}), 400

        # ML Prediction using Structured Model
        prediction = predict_career_from_skills(user_skills)
        predicted_career = prediction["predicted_career"]
        ml_confidence = prediction["confidence"]
        probabilities = prediction["probabilities"]

        # Skill Gap & Match Score
        gap_analysis = analyze_skill_gap(user_skills, predicted_career)
        skill_match_score = gap_analysis["skill_match_score"]

        # Learning Path
        learning_path = generate_learning_path(user_skills, predicted_career)

        # Save to database history
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analysis_history (user_skills, predicted_career, ml_confidence, skill_match_score, source_type)
                VALUES (?, ?, ?, ?, ?)
            """, (",".join(user_skills), predicted_career, ml_confidence, skill_match_score, "manual"))
            conn.commit()
            conn.close()
        except Exception as db_err:
            print("History save error:", db_err)

        return jsonify({
            "status": "success",
            "source": "manual_skills",
            "user_skills": user_skills,
            "predicted_career": predicted_career,
            "ml_confidence": ml_confidence,
            "career_probabilities": probabilities,
            "skill_match_score": skill_match_score,
            "matched_skills": gap_analysis["matched_skills"],
            "missing_skills": gap_analysis["missing_skills"],
            "category_coverage": gap_analysis["category_coverage"],
            "learning_path": learning_path["learning_path"]
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/analyze-skills", methods=["POST"])
def analyze_skills():
    try:
        data = request.get_json() or {}
        user_skills = data.get("skills", [])
        career = data.get("career", "")

        if not career:
            return jsonify({"status": "error", "message": "'career' is required"}), 400

        gap_analysis = analyze_skill_gap(user_skills, career)
        learning_path = generate_learning_path(user_skills, career)

        return jsonify({
            "status": "success",
            "user_skills": user_skills,
            "target_career": career,
            "skill_match_score": gap_analysis["skill_match_score"],
            "matched_skills": gap_analysis["matched_skills"],
            "missing_skills": gap_analysis["missing_skills"],
            "category_coverage": gap_analysis["category_coverage"],
            "learning_path": learning_path["learning_path"]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "No file attached"}), 400

        file = request.files["file"]
        if file.filename == "" or not file.filename.lower().endswith(".pdf"):
            return jsonify({"status": "error", "message": "Please upload a valid .pdf file"}), 400

        # Save uploaded file
        filepath = os.path.join(UPLOADS_DIR, file.filename)
        file.save(filepath)

        # 1. Extract PDF text
        resume_text = extract_text_from_pdf(filepath)
        if not resume_text:
            return jsonify({
                "status": "error",
                "message": "Unable to extract readable text from PDF. The file may be image-only or corrupted."
            }), 400

        # 2. Extract skills using NLP regex matcher
        detected_skills = extract_skills_from_text(resume_text)

        # 3. Predict career using Resume NLP ML Model (TF-IDF + Classifier)
        nlp_prediction = predict_career_from_resume_text(resume_text)
        predicted_career = nlp_prediction["predicted_career"]
        ml_confidence = nlp_prediction["confidence"]
        probabilities = nlp_prediction["probabilities"]

        # 4. Perform skill match & gap analysis using detected skills
        gap_analysis = analyze_skill_gap(detected_skills, predicted_career)
        skill_match_score = gap_analysis["skill_match_score"]

        # 5. Generate learning path
        learning_path = generate_learning_path(detected_skills, predicted_career)

        # Save history
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analysis_history (user_skills, predicted_career, ml_confidence, skill_match_score, source_type)
                VALUES (?, ?, ?, ?, ?)
            """, (",".join(detected_skills), predicted_career, ml_confidence, skill_match_score, "resume_pdf"))
            conn.commit()
            conn.close()
        except Exception as db_err:
            print("History save error:", db_err)

        return jsonify({
            "status": "success",
            "source": "resume_pdf",
            "filename": file.filename,
            "resume_text_snippet": resume_text[:300] + ("..." if len(resume_text) > 300 else ""),
            "detected_skills": detected_skills,
            "predicted_career": predicted_career,
            "ml_confidence": ml_confidence,
            "career_probabilities": probabilities,
            "skill_match_score": skill_match_score,
            "matched_skills": gap_analysis["matched_skills"],
            "missing_skills": gap_analysis["missing_skills"],
            "category_coverage": gap_analysis["category_coverage"],
            "learning_path": learning_path["learning_path"]
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/skill-gap/<career_name>", methods=["GET"])
def get_skill_gap_route(career_name):
    try:
        user_skills_param = request.args.get("skills", "")
        user_skills = [s.strip() for s in user_skills_param.split(",") if s.strip()]
        result = analyze_skill_gap(user_skills, career_name)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/learning-path/<career_name>", methods=["GET"])
def get_learning_path_route(career_name):
    try:
        user_skills_param = request.args.get("skills", "")
        user_skills = [s.strip() for s in user_skills_param.split(",") if s.strip()]
        result = generate_learning_path(user_skills, career_name)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/resources/<skill_name>", methods=["GET"])
def get_resource_route(skill_name):
    try:
        res = get_skill_resource(skill_name)
        return jsonify({"status": "success", "resource": res})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/sample-resume/<filename>", methods=["GET"])
def get_sample_resume(filename):
    try:
        sample_dir = os.path.join(BASE_DIR, "sample_resumes")
        from flask import send_from_directory
        return send_from_directory(sample_dir, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/model-performance", methods=["GET"])

def get_performance_route():
    try:
        metrics = get_model_metrics()
        return jsonify({"status": "success", "metrics": metrics})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("Starting SkillGap ML Flask Backend on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
