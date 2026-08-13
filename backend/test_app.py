import os
import unittest
import json
from app import app, init_db

class SkillGapMLTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        init_db()

    def test_1_data_analyst_skills(self):
        print("\n--- Running Test 1: Data Analyst Manual Skills ---")
        payload = {
            "skills": ["Python", "SQL", "Excel", "Statistics", "Pandas", "Power BI"]
        }
        res = self.app.post("/api/predict-career", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        
        print(f"Predicted Career: {data['predicted_career']}")
        print(f"ML Confidence: {data['ml_confidence']}%")
        print(f"Skill Match Score: {data['skill_match_score']}%")
        print(f"Missing Skills Count: {len(data['missing_skills'])}")

        self.assertEqual(data["status"], "success")
        self.assertIn("Data Analyst", data["predicted_career"])

    def test_2_aiml_engineer_skills(self):
        print("\n--- Running Test 2: AI/ML Engineer Manual Skills ---")
        payload = {
            "skills": ["Python", "NumPy", "Pandas", "Machine Learning", "TensorFlow", "Deep Learning"]
        }
        res = self.app.post("/api/predict-career", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        
        print(f"Predicted Career: {data['predicted_career']}")
        print(f"ML Confidence: {data['ml_confidence']}%")
        print(f"Skill Match Score: {data['skill_match_score']}%")

        self.assertEqual(data["status"], "success")
        self.assertIn("AI/ML Engineer", data["predicted_career"])

    def test_3_web_developer_skills(self):
        print("\n--- Running Test 3: Web Developer Manual Skills ---")
        payload = {
            "skills": ["HTML", "CSS", "JavaScript", "React", "Git"]
        }
        res = self.app.post("/api/predict-career", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        
        print(f"Predicted Career: {data['predicted_career']}")
        print(f"ML Confidence: {data['ml_confidence']}%")
        print(f"Skill Match Score: {data['skill_match_score']}%")

        self.assertEqual(data["status"], "success")
        self.assertIn("Web Developer", data["predicted_career"])

    def test_4_pdf_resume_upload(self):
        print("\n--- Running Test 4: PDF Resume NLP Upload ---")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_path = os.path.join(base_dir, "sample_resumes", "data_analyst_resume.pdf")
        
        self.assertTrue(os.path.exists(pdf_path), "Sample PDF resume does not exist")

        with open(pdf_path, "rb") as f:
            data = {"file": (f, "data_analyst_resume.pdf")}
            res = self.app.post("/api/analyze-resume", data=data, content_type="multipart/form-data")
        
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.data)
        
        print(f"Filename: {res_data['filename']}")
        print(f"Detected Skills: {res_data['detected_skills']}")
        print(f"NLP Predicted Career: {res_data['predicted_career']}")
        print(f"ML Confidence: {res_data['ml_confidence']}%")
        print(f"Skill Match Score: {res_data['skill_match_score']}%")
        print(f"Learning Path Steps: {len(res_data['learning_path'])}")

        self.assertEqual(res_data["status"], "success")
        self.assertTrue(len(res_data["detected_skills"]) > 0)

    def test_5_model_performance_api(self):
        print("\n--- Running Test 5: Model Performance API ---")
        res = self.app.get("/api/model-performance")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("structured_model", data["metrics"])
        self.assertIn("resume_nlp_model", data["metrics"])

if __name__ == "__main__":
    unittest.main()
