import os
import pandas as pd
from database import get_db_connection

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAREER_SKILLS_CSV = os.path.join(BASE_DIR, "data", "career_skills.csv")

def get_career_requirements(career_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT career, skill, category, importance, prerequisite FROM career_skills WHERE career = ?", (career_name,))
        rows = cursor.fetchall()
        conn.close()

        if rows:
            return [dict(r) for r in rows]
    except Exception as e:
        print("Database query error, falling back to CSV:", e)

    if os.path.exists(CAREER_SKILLS_CSV):
        df = pd.read_csv(CAREER_SKILLS_CSV)
        filtered = df[df["career"].str.lower() == career_name.lower()]
        return filtered.to_dict(orient="records")

    return []

def analyze_skill_gap(user_skills, target_career):
    requirements = get_career_requirements(target_career)
    
    if not requirements:
        return {
            "career": target_career,
            "skill_match_score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "category_coverage": {}
        }

    user_skills_lower = {s.strip().lower() for s in user_skills}

    total_importance = 0
    matched_importance = 0

    matched_skills = []
    missing_skills = []
    
    category_stats = {} # {category: {"total": 0, "matched": 0}}

    for req in requirements:
        skill_name = req["skill"]
        category = req.get("category", "General")
        importance = int(req.get("importance", 3))
        prereq = str(req.get("prerequisite", "")).strip() if pd.notna(req.get("prerequisite")) else ""

        total_importance += importance

        if category not in category_stats:
            category_stats[category] = {"total": 0, "matched": 0}
        category_stats[category]["total"] += 1

        is_present = skill_name.lower() in user_skills_lower

        if is_present:
            matched_importance += importance
            category_stats[category]["matched"] += 1
            matched_skills.append({
                "skill": skill_name,
                "category": category,
                "importance": importance
            })
        else:
            if importance >= 5:
                priority = "High"
                priority_code = "🔴"
            elif importance == 4:
                priority = "Medium"
                priority_code = "🟡"
            else:
                priority = "Low"
                priority_code = "🟢"

            missing_skills.append({
                "skill": skill_name,
                "category": category,
                "importance": importance,
                "prerequisite": prereq,
                "priority": priority,
                "priority_code": priority_code
            })

    skill_match_score = round((matched_importance / total_importance) * 100, 2) if total_importance > 0 else 0.0

    # Calculate coverage per category
    category_coverage = {}
    for cat, stats in category_stats.items():
        pct = round((stats["matched"] / stats["total"]) * 100, 1) if stats["total"] > 0 else 0
        category_coverage[cat] = {
            "matched": stats["matched"],
            "total": stats["total"],
            "percentage": pct
        }

    return {
        "career": target_career,
        "skill_match_score": skill_match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "category_coverage": category_coverage
    }
