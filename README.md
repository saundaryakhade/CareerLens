# CareerLens – AI Career Prediction & Skill Gap Analyzer

**Tagline**: *Discover Your Career Fit. Build Your Future.*

CareerLens is an AI-powered machine learning and natural language processing (NLP) platform designed to analyze student skill footprints and resume documents, predict optimal career fits using trained classification models, quantify weighted skill match scores, categorize skill gaps by priority, and generate prerequisite-ordered personalized learning paths.

---

## 1. Problem Statement
Students acquire technical and analytical skills across diverse coursework and self-study, but often lack clarity on which specific career track best aligns with their present skill set. Furthermore, identifying missing high-priority skills and structuring an optimal learning sequence remains a significant challenge. CareerLens solves this problem through real machine learning classification, natural language resume parsing, weighted skill gap analysis, and interactive visualization.

---

## 2. Project Architecture & Flow

```text
                                 CareerLens
                                     │
              ┌──────────────────────┴──────────────────────┐
              ↓                                             ↓
     Manual Skill Selection                         Upload PDF Resume
              │                                             │
      Feature Engineering                             PDF Text Extraction
              │                                             ↓
              │                                     NLP Skill Extraction
              │                                             ↓
              │                                     TF-IDF Vectorizer
              │                                             ↓
      Structured ML Model                             NLP Resume Model
              │                                             │
              └──────────────────────┬──────────────────────┘
                                     ↓
                             Career Prediction
                                     ↓
                           Prediction Confidence
                                     ↓
                         Career Skill Requirements
                                     ↓
                          Skill Match Score (%)
                                     ↓
                            Skill Gap Priority
                                     ↓
                        Personalized Learning Path
                                     ↓
                          CareerLens Dashboard
```

---

## 3. Technology Stack

* **Frontend**: HTML5, Vanilla CSS3 (Custom Glassmorphism Tech Theme), Vanilla JavaScript (ES6+), Fetch API, Chart.js.
* **Backend**: Python 3.12, Flask REST API, SQLite database (`database/skillgap.db`).
* **Machine Learning**: Pandas, NumPy, Scikit-learn (`LogisticRegression`, `DecisionTreeClassifier`, `RandomForestClassifier`), Joblib.
* **NLP**: `pypdf` for PDF text extraction, Regex pattern matching, `TfidfVectorizer` for text feature extraction.

---

## 4. Dataset Description

The system utilizes 4 datasets located in `data/`:

1. **`career_prediction_dataset.csv`**: 350 structured records containing 29 binary skill features (`0` = not present, `1` = present) mapped across 5 target career tracks:
   - `Data Analyst`
   - `AI/ML Engineer`
   - `Web Developer`
   - `Cybersecurity Analyst`
   - `Business Analyst`
2. **`resume_career_dataset.csv`**: 250 synthetic resume text documents representing varied phrasing, action verbs, and skill combinations for text-based NLP model training.
3. **`career_skills.csv`**: Career skill requirements database with fields `career`, `skill`, `category`, `importance` (1 to 5), and `prerequisite`.
4. **`skill_resources.csv`**: Educational catalog providing course titles, resource types, and descriptions for all 29 skills.

---

## 5. Machine Learning & NLP Pipelines

### A. Structured Skill Classifier
- **Features**: 29 binary skill indicators.
- **Algorithms Evaluated**: Logistic Regression, Decision Tree Classifier, Random Forest Classifier.
- **Selection Criterion**: Highest weighted F1 score on 20% test validation set.
- **Artifact**: Saved as `models/career_model.joblib`.

### B. Resume NLP Text Classifier
- **Pipeline**: PDF text extraction → TF-IDF Vectorization (`max_features=500`, `ngram_range=(1,2)`) → Classifier (`LogisticRegression` / `RandomForestClassifier`).
- **Artifacts**: Saved as `models/resume_model.joblib` and `models/tfidf_vectorizer.joblib`.

### C. Metric Distinction
- **ML Prediction Confidence**: Output of model `predict_proba()`, indicating classification probability.
- **Skill Match Score**: Weighted mathematical calculation comparing user skills against role requirements:
  $$\text{Skill Match Score} = \frac{\sum \text{importance of matched skills}}{\sum \text{importance of all required skills for target career}} \times 100$$

---

## 6. Installation & Setup Instructions

### Prerequisites
- Python 3.10+ installed on your system.
- `uv` (recommended) or standard `python` / `pip`.

### Step 1: Navigate to Project Directory
```bash
cd SkillGapML
```

### Step 2: Initialize Virtual Environment & Install Dependencies
Using `uv`:
```bash
uv venv .venv
uv pip install -r backend/requirements.txt
```
Or using standard Python:
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r backend/requirements.txt
```

### Step 3: Generate Datasets & Train ML Models
```bash
# Generate datasets (350 structured records, 250 resume records, skills, resources)
python data/generate_datasets.py

# Train & evaluate ML models, save joblib artifacts & metrics.json
python backend/train_model.py
```

### Step 4: Generate Sample PDF Resumes
```bash
python sample_resumes/generate_resumes.py
```

### Step 5: Run Integration Test Suite
```bash
python backend/test_app.py
```

### Step 6: Start Flask Backend API Server
```bash
python backend/app.py
```
The Flask backend will start on `http://localhost:5000`.

### Step 7: Open the Frontend Application
Simply open `frontend/index.html` in your web browser or visit:
**`http://localhost:5000`**

---

## 7. Key Application Pages

- **Home (`/index.html`)**: Landing page introducing CareerLens, problem statement, feature cards, and quick actions.
- **Careers (`/careers.html`)**: Catalog of 5 tech career tracks with core required skills.
- **Skill Analyzer (`/analyzer.html`)**: Interactive manual skill selection with search input, category filters, quick presets, and skill counter.
- **CareerLens Resume Intelligence (`/resume.html`)**: Drag-and-drop PDF resume upload zone, instant text extraction, NLP skill detection, and quick sample resume tests.
- **Dashboard (`/dashboard.html`)**: Interactive results dashboard with 4 top stat cards, metric explanation callout, matched skills badges, priority-categorized missing skills (🔴 High, 🟡 Medium, 🟢 Low), 3 Chart.js graphs, and connected learning path timeline.
- **CareerLens ML Performance (`/model-performance.html`)**: Real training evaluation dashboard showing Accuracy, Precision, Recall, F1 score, confusion matrices, and algorithm comparison table.

---

## 8. License & Copyright
© 2026 CareerLens — *Discover Your Career Fit. Build Your Future.*
