import os
import pandas as pd
from database import get_db_connection
from analyzer import analyze_skill_gap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_RESOURCES_CSV = os.path.join(BASE_DIR, "data", "skill_resources.csv")

def get_skill_resource(skill_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT skill, resource_type, resource_name, description FROM skill_resources WHERE LOWER(skill) = LOWER(?)", (skill_name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception as e:
        print("Database query error for resources:", e)

    if os.path.exists(SKILL_RESOURCES_CSV):
        df = pd.read_csv(SKILL_RESOURCES_CSV)
        match = df[df["skill"].str.lower() == skill_name.lower()]
        if not match.empty:
            return match.iloc[0].to_dict()

    return {
        "skill": skill_name,
        "resource_type": "Tutorial",
        "resource_name": f"{skill_name} Guide",
        "description": f"Learn key fundamentals and practical applications of {skill_name}."
    }

def generate_learning_path(user_skills, career_name):
    gap_analysis = analyze_skill_gap(user_skills, career_name)
    missing_skills = gap_analysis["missing_skills"]

    if not missing_skills:
        return {
            "career": career_name,
            "learning_path": [],
            "message": "Congratulations! You possess all core required skills for this career."
        }

    # Dependency ordering using topological sort / prerequisite sorting
    missing_dict = {item["skill"]: item for item in missing_skills}
    ordered_skills = []
    visited = set()

    def add_skill(skill_item):
        skill_name = skill_item["skill"]
        if skill_name in visited:
            return
        
        prereq = skill_item.get("prerequisite", "").strip()
        # If prerequisite exists and is also missing, add prerequisite first
        if prereq and prereq in missing_dict and prereq not in visited:
            add_skill(missing_dict[prereq])
            
        visited.add(skill_name)
        ordered_skills.append(skill_item)

    # Sort missing skills initially by importance (descending)
    sorted_missing = sorted(missing_skills, key=lambda x: x["importance"], reverse=True)
    
    for item in sorted_missing:
        add_skill(item)

    # Build final learning path items with attached learning resources
    learning_path = []
    for step_num, item in enumerate(ordered_skills, start=1):
        resource = get_skill_resource(item["skill"])
        learning_path.append({
            "step": step_num,
            "skill": item["skill"],
            "category": item["category"],
            "importance": item["importance"],
            "priority": item["priority"],
            "priority_code": item["priority_code"],
            "prerequisite": item["prerequisite"],
            "resource": resource
        })

    return {
        "career": career_name,
        "total_steps": len(learning_path),
        "learning_path": learning_path,
        "gap_summary": gap_analysis
    }
