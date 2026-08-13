import os
import csv
import random

# Ensure data directory exists
data_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(data_dir, exist_ok=True)

# Set random seed for reproducibility
random.seed(42)

# ==========================================
# 1. GENERATE career_prediction_dataset.csv
# ==========================================
skills = [
    "Python", "SQL", "Excel", "Statistics", "Pandas", "NumPy", "Power BI",
    "Tableau", "Data Visualization", "Data Modeling", "ETL", "Machine Learning",
    "Deep Learning", "TensorFlow", "PyTorch", "HTML", "CSS", "JavaScript",
    "React", "REST API", "Git", "Linux", "Networking", "Cybersecurity",
    "Network Security", "SIEM", "Communication", "Problem Solving", "Requirements Analysis"
]

career_skill_profiles = {
    "Data Analyst": {
        "core": ["Python", "SQL", "Excel", "Statistics", "Pandas", "NumPy", "Power BI", "Tableau", "Data Visualization"],
        "secondary": ["Data Modeling", "ETL", "Communication", "Problem Solving", "Git"],
        "prob_core": 0.88, "prob_sec": 0.45, "prob_noise": 0.08
    },
    "AI/ML Engineer": {
        "core": ["Python", "NumPy", "Pandas", "Statistics", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
        "secondary": ["SQL", "Git", "Linux", "Data Visualization", "ETL"],
        "prob_core": 0.90, "prob_sec": 0.50, "prob_noise": 0.06
    },
    "Web Developer": {
        "core": ["HTML", "CSS", "JavaScript", "React", "REST API", "Git"],
        "secondary": ["Python", "Linux", "Communication", "Problem Solving"],
        "prob_core": 0.92, "prob_sec": 0.40, "prob_noise": 0.05
    },
    "Cybersecurity Analyst": {
        "core": ["Linux", "Networking", "Cybersecurity", "Network Security", "SIEM"],
        "secondary": ["Python", "Git", "Problem Solving", "Communication", "REST API"],
        "prob_core": 0.90, "prob_sec": 0.45, "prob_noise": 0.06
    },
    "Business Analyst": {
        "core": ["Excel", "SQL", "Statistics", "Power BI", "Data Visualization", "Requirements Analysis", "Communication", "Problem Solving"],
        "secondary": ["Tableau", "Data Modeling", "Python", "ETL"],
        "prob_core": 0.88, "prob_sec": 0.45, "prob_noise": 0.07
    }
}

prediction_rows = []
records_per_career = 70  # 70 * 5 = 350 records total (>300)

for career, profile in career_skill_profiles.items():
    for _ in range(records_per_career):
        row = {}
        for skill in skills:
            if skill in profile["core"]:
                row[skill] = 1 if random.random() < profile["prob_core"] else 0
            elif skill in profile["secondary"]:
                row[skill] = 1 if random.random() < profile["prob_sec"] else 0
            else:
                row[skill] = 1 if random.random() < profile["prob_noise"] else 0
        row["career"] = career
        prediction_rows.append(row)

random.shuffle(prediction_rows)

career_pred_path = os.path.join(data_dir, "career_prediction_dataset.csv")
with open(career_pred_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=skills + ["career"])
    writer.writeheader()
    writer.writerows(prediction_rows)

print(f"Generated {len(prediction_rows)} records in {career_pred_path}")

# ==========================================
# 2. GENERATE resume_career_dataset.csv
# ==========================================
resume_templates = {
    "Data Analyst": [
        "Data Professional with expertise in Python, SQL, Excel, and Pandas. Proficient in building interactive Power BI dashboards, executing complex data visualizations, and generating actionable business insights.",
        "Experienced Data Analyst skilled in SQL queries, data manipulation with NumPy and Pandas, Excel pivot tables, and statistical modeling. Strong background in ETL pipelines and Tableau visual reporting.",
        "Analytical thinker with solid skills in Python data analysis, SQL database management, data modeling, and data visualization tools like Power BI. Proven track record of turning raw data into strategic business reports.",
        "Passionate Data Analyst intern experienced in exploratory data analysis using Pandas and NumPy. Knowledgeable in SQL queries, Excel formulas, Statistics, and creating dashboards.",
        "Business-focused Data Analyst proficient in SQL, Python, ETL processing, data hygiene, and statistical testing. Skilled at conveying complex data insights using Tableau and Power BI.",
        "Junior Analyst with hands-on experience in Excel spreadsheet analysis, SQL database queries, Python scripts, statistical distribution analysis, and business intelligence reports.",
        "Results-oriented Data Analyst adept in Python data processing, SQL stored procedures, Pandas, NumPy, statistical modeling, and designing executive dashboard presentations."
    ],
    "AI/ML Engineer": [
        "Machine Learning Engineer with strong background in Python, NumPy, Pandas, Scikit-learn, PyTorch, and TensorFlow. Experienced in building deep neural networks, model training, hyperparameter optimization, and Git version control.",
        "AI Developer skilled in building machine learning models using Python, TensorFlow, and PyTorch. Solid foundation in linear algebra, statistics, natural language processing, and deep learning algorithms.",
        "Data Science Enthusiast specializing in Machine Learning, Deep Learning, computer vision, and neural network architectures using Python, NumPy, and PyTorch. Familiar with Linux and Git workflows.",
        "AI/ML Specialist with expertise in predictive modeling, feature engineering using Pandas, statistical analysis, model deployment, and deep learning frameworks including TensorFlow and PyTorch.",
        "Graduate researcher focusing on Machine Learning and Deep Learning. Experienced in writing clean Python code, performing statistical evaluations, utilizing NumPy for tensor computations, and managing code with Git.",
        "Software Engineer transitioning to AI/ML with strong proficiency in Python, NumPy, Pandas, Scikit-learn, Machine Learning algorithms, deep neural nets, and PyTorch.",
        "AI Engineer adept at building supervised and unsupervised machine learning pipelines, optimizing models with Scikit-learn and TensorFlow, and deploying scalable Python microservices."
    ],
    "Web Developer": [
        "Full-stack Web Developer skilled in HTML, CSS, JavaScript, React, and REST API integration. Passionate about responsive UI design, clean code standards, frontend state management, and Git collaboration.",
        "Frontend Developer with experience in modern JavaScript, HTML5, CSS3, React components, and RESTful web services. Proven ability to build pixel-perfect, accessible, and responsive user interfaces.",
        "Web Application Developer proficient in HTML, CSS, JavaScript, React, REST API development, and version control using Git. Knowledgeable in frontend optimization and modern UI frameworks.",
        "Junior Web Developer experienced in building interactive frontend interfaces using React, JavaScript, CSS animations, HTML structure, and consuming backend REST APIs. Proficient with Git and GitHub.",
        "Software Developer specializing in web development using JavaScript, React, REST API architecture, HTML5, CSS3 styles, and Git branch workflows.",
        "Responsive Web Developer skilled in HTML structure, CSS layouts, client-side JavaScript, React single-page applications, and Git version control system.",
        "Web Engineer passionate about user experience, frontend performance, React state management, HTML, CSS grid/flexbox, REST APIs, and team collaboration via Git."
    ],
    "Cybersecurity Analyst": [
        "Cybersecurity Professional experienced in Linux systems, network protocol analysis, SIEM tools, firewalls, and network security policies. Strong analytical skills and knowledge of ethical hacking principles.",
        "Information Security Analyst skilled in Linux command line, networking infrastructure, intrusion detection systems, SIEM monitoring, threat detection, and network security standard operating procedures.",
        "Security Operations Analyst proficient in monitoring network security logs using SIEM software, configuring Linux servers, analyzing network traffic, and incident response procedures.",
        "Cybersecurity Analyst with strong background in computer networking, Linux administration, Python scripting for automation, security auditing, SIEM log analysis, and network defense.",
        "Information Assurance Specialist experienced in Linux environment, network security architecture, vulnerability assessment, SIEM tool management, and security policy enforcement.",
        "Junior Cybersecurity Analyst with hands-on practice in Linux OS, IP networking, Wireshark packet analysis, SIEM dashboard monitoring, and network security practices.",
        "System and Security Administrator proficient in Linux terminal scripting, network routing, firewalls, SIEM alert triage, and threat mitigation."
    ],
    "Business Analyst": [
        "Business Analyst with expertise in requirements analysis, SQL database querying, Excel reporting, Power BI reporting, and executive communication. Proven record in bridging business needs and technical solutions.",
        "Detail-oriented Business Analyst skilled in gather user requirements, process modeling, data visualization, SQL queries, Excel dashboards, and stakeholder management.",
        "Operations Business Analyst proficient in requirements analysis, statistical business analysis, Excel data modeling, Power BI reports, and problem-solving methodologies.",
        "Junior Business Analyst experienced in creating requirements documents, SQL data retrieval, advanced Excel formulas, Power BI dashboards, and cross-functional communication.",
        "Strategy & Business Analyst with strong problem-solving skills, SQL proficiency, Excel analytical reporting, requirements gathering, and business process optimization.",
        "Business Systems Analyst skilled in translating business goals into requirements specs, using SQL and Excel for data inspection, and presenting reports in Power BI.",
        "Analytical Business Consultant experienced in requirement engineering, data-driven decision making, Power BI visualization, SQL data analysis, and professional communication."
    ]
}

resume_rows = []
# Generate 250 variation records (>200) by combining templates and random skill add-ons
modifiers = [
    "Proven experience in cross-functional projects.",
    "Fast learner with strong analytical skills.",
    "Certified professional eager to drive tech solutions.",
    "Hands-on project experience in academic and commercial environments.",
    "Strong technical aptitude and team collaboration abilities.",
    "Adept at troubleshooting, problem solving, and technical writing.",
    "Passionate about leveraging modern software and data technologies."
]

for career, templates in resume_templates.items():
    for i in range(50): # 50 * 5 = 250 records
        base = random.choice(templates)
        mod = random.choice(modifiers)
        text = f"{base} {mod}"
        resume_rows.append({"resume_text": text, "career": career})

random.shuffle(resume_rows)

resume_csv_path = os.path.join(data_dir, "resume_career_dataset.csv")
with open(resume_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["resume_text", "career"])
    writer.writeheader()
    writer.writerows(resume_rows)

print(f"Generated {len(resume_rows)} records in {resume_csv_path}")

# ==========================================
# 3. GENERATE career_skills.csv
# ==========================================
career_skills_data = [
    # Data Analyst
    {"career": "Data Analyst", "skill": "Python", "category": "Programming", "importance": 5, "prerequisite": ""},
    {"career": "Data Analyst", "skill": "SQL", "category": "Database", "importance": 5, "prerequisite": ""},
    {"career": "Data Analyst", "skill": "Excel", "category": "Analytics", "importance": 4, "prerequisite": ""},
    {"career": "Data Analyst", "skill": "Statistics", "category": "Mathematics", "importance": 5, "prerequisite": ""},
    {"career": "Data Analyst", "skill": "Pandas", "category": "Programming", "importance": 4, "prerequisite": "Python"},
    {"career": "Data Analyst", "skill": "NumPy", "category": "Programming", "importance": 3, "prerequisite": "Python"},
    {"career": "Data Analyst", "skill": "Data Visualization", "category": "Analytics", "importance": 5, "prerequisite": "Statistics"},
    {"career": "Data Analyst", "skill": "Power BI", "category": "Visualization", "importance": 5, "prerequisite": "Data Visualization"},
    {"career": "Data Analyst", "skill": "Tableau", "category": "Visualization", "importance": 4, "prerequisite": "Data Visualization"},
    {"career": "Data Analyst", "skill": "Data Modeling", "category": "Database", "importance": 4, "prerequisite": "SQL"},
    {"career": "Data Analyst", "skill": "ETL", "category": "Data Engineering", "importance": 3, "prerequisite": "SQL"},
    {"career": "Data Analyst", "skill": "Git", "category": "Tools", "importance": 2, "prerequisite": ""},

    # AI/ML Engineer
    {"career": "AI/ML Engineer", "skill": "Python", "category": "Programming", "importance": 5, "prerequisite": ""},
    {"career": "AI/ML Engineer", "skill": "NumPy", "category": "Programming", "importance": 4, "prerequisite": "Python"},
    {"career": "AI/ML Engineer", "skill": "Pandas", "category": "Programming", "importance": 4, "prerequisite": "Python"},
    {"career": "AI/ML Engineer", "skill": "Statistics", "category": "Mathematics", "importance": 5, "prerequisite": ""},
    {"career": "AI/ML Engineer", "skill": "Machine Learning", "category": "AI", "importance": 5, "prerequisite": "Python"},
    {"career": "AI/ML Engineer", "skill": "Scikit-learn", "category": "AI", "importance": 5, "prerequisite": "Machine Learning"},
    {"career": "AI/ML Engineer", "skill": "TensorFlow", "category": "AI", "importance": 4, "prerequisite": "Machine Learning"},
    {"career": "AI/ML Engineer", "skill": "PyTorch", "category": "AI", "importance": 4, "prerequisite": "Machine Learning"},
    {"career": "AI/ML Engineer", "skill": "Deep Learning", "category": "AI", "importance": 5, "prerequisite": "Machine Learning"},
    {"career": "AI/ML Engineer", "skill": "SQL", "category": "Database", "importance": 3, "prerequisite": ""},
    {"career": "AI/ML Engineer", "skill": "Git", "category": "Tools", "importance": 3, "prerequisite": ""},

    # Web Developer
    {"career": "Web Developer", "skill": "HTML", "category": "Web Development", "importance": 5, "prerequisite": ""},
    {"career": "Web Developer", "skill": "CSS", "category": "Web Development", "importance": 5, "prerequisite": "HTML"},
    {"career": "Web Developer", "skill": "JavaScript", "category": "Programming", "importance": 5, "prerequisite": "HTML"},
    {"career": "Web Developer", "skill": "Git", "category": "Tools", "importance": 4, "prerequisite": ""},
    {"career": "Web Developer", "skill": "Responsive Design", "category": "Web Development", "importance": 4, "prerequisite": "CSS"},
    {"career": "Web Developer", "skill": "REST API", "category": "Backend", "importance": 3, "prerequisite": "JavaScript"},
    {"career": "Web Developer", "skill": "React", "category": "Frontend", "importance": 4, "prerequisite": "JavaScript"},

    # Cybersecurity Analyst
    {"career": "Cybersecurity Analyst", "skill": "Networking", "category": "Security", "importance": 5, "prerequisite": ""},
    {"career": "Cybersecurity Analyst", "skill": "Linux", "category": "Operating Systems", "importance": 5, "prerequisite": ""},
    {"career": "Cybersecurity Analyst", "skill": "Python", "category": "Programming", "importance": 4, "prerequisite": ""},
    {"career": "Cybersecurity Analyst", "skill": "Cybersecurity", "category": "Security", "importance": 5, "prerequisite": ""},
    {"career": "Cybersecurity Analyst", "skill": "Network Security", "category": "Security", "importance": 5, "prerequisite": "Networking"},
    {"career": "Cybersecurity Analyst", "skill": "SIEM", "category": "Security", "importance": 4, "prerequisite": "Cybersecurity"},
    {"career": "Cybersecurity Analyst", "skill": "Git", "category": "Tools", "importance": 2, "prerequisite": ""},

    # Business Analyst
    {"career": "Business Analyst", "skill": "Excel", "category": "Analytics", "importance": 5, "prerequisite": ""},
    {"career": "Business Analyst", "skill": "SQL", "category": "Database", "importance": 4, "prerequisite": ""},
    {"career": "Business Analyst", "skill": "Statistics", "category": "Mathematics", "importance": 4, "prerequisite": ""},
    {"career": "Business Analyst", "skill": "Power BI", "category": "Visualization", "importance": 5, "prerequisite": ""},
    {"career": "Business Analyst", "skill": "Data Visualization", "category": "Analytics", "importance": 4, "prerequisite": ""},
    {"career": "Business Analyst", "skill": "Requirements Analysis", "category": "Business", "importance": 5, "prerequisite": ""},
    {"career": "Business Analyst", "skill": "Communication", "category": "Soft Skills", "importance": 5, "prerequisite": ""},
    {"career": "Business Analyst", "skill": "Problem Solving", "category": "Soft Skills", "importance": 4, "prerequisite": ""}
]

career_skills_path = os.path.join(data_dir, "career_skills.csv")
with open(career_skills_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["career", "skill", "category", "importance", "prerequisite"])
    writer.writeheader()
    writer.writerows(career_skills_data)

print(f"Generated {len(career_skills_data)} records in {career_skills_path}")

# ==========================================
# 4. GENERATE skill_resources.csv
# ==========================================
resources_data = [
    {"skill": "Python", "resource_type": "Course", "resource_name": "Python Fundamentals", "description": "Learn Python programming fundamentals, data structures, and functions."},
    {"skill": "SQL", "resource_type": "Course", "resource_name": "SQL Fundamentals", "description": "Master SQL syntax, joins, aggregations, and database queries."},
    {"skill": "Excel", "resource_type": "Course", "resource_name": "Advanced Excel", "description": "Learn formulas, pivot tables, lookup functions, and data analysis in Excel."},
    {"skill": "Statistics", "resource_type": "Course", "resource_name": "Statistics for Data Analysis", "description": "Understand descriptive & inferential statistics, probability, and hypothesis testing."},
    {"skill": "Pandas", "resource_type": "Course", "resource_name": "Pandas Data Analysis", "description": "Master data manipulation, cleaning, and filtering with Python Pandas."},
    {"skill": "NumPy", "resource_type": "Course", "resource_name": "NumPy Fundamentals", "description": "Learn numerical computing, multidimensional array manipulation, and linear algebra."},
    {"skill": "Data Visualization", "resource_type": "Course", "resource_name": "Data Visualization Principles", "description": "Master chart selection, visual hierarchy, and storytelling with data."},
    {"skill": "Power BI", "resource_type": "Course", "resource_name": "Power BI Fundamentals", "description": "Build interactive business dashboards, DAX measures, and data models."},
    {"skill": "Tableau", "resource_type": "Course", "resource_name": "Tableau Fundamentals", "description": "Create interactive visual analytics, calculated fields, and executive dashboards."},
    {"skill": "Data Modeling", "resource_type": "Course", "resource_name": "Data Modeling Fundamentals", "description": "Learn ER diagrams, normalization, star schema, and relational database design."},
    {"skill": "ETL", "resource_type": "Course", "resource_name": "ETL & Data Engineering Essentials", "description": "Understand extract-transform-load pipeline concepts and data warehouse ingestion."},
    {"skill": "Machine Learning", "resource_type": "Course", "resource_name": "Machine Learning Fundamentals", "description": "Learn supervised and unsupervised ML algorithms, model evaluation, and tuning."},
    {"skill": "Scikit-learn", "resource_type": "Course", "resource_name": "Scikit-Learn Essentials", "description": "Implement classification, regression, clustering, and preprocessing pipelines in Python."},
    {"skill": "Deep Learning", "resource_type": "Course", "resource_name": "Deep Learning Fundamentals", "description": "Understand neural networks, backpropagation, CNNs, RNNs, and optimization techniques."},
    {"skill": "TensorFlow", "resource_type": "Course", "resource_name": "TensorFlow Fundamentals", "description": "Build, train, and deploy neural network architectures using Keras and TensorFlow."},
    {"skill": "PyTorch", "resource_type": "Course", "resource_name": "PyTorch Fundamentals", "description": "Master dynamic computation graphs, neural layers, and deep learning training loops."},
    {"skill": "HTML", "resource_type": "Course", "resource_name": "HTML Fundamentals", "description": "Master semantic HTML5 structure, forms, tables, and document layout fundamentals."},
    {"skill": "CSS", "resource_type": "Course", "resource_name": "CSS Fundamentals", "description": "Learn modern CSS layout, styling, Flexbox, CSS Grid, and responsive styling."},
    {"skill": "JavaScript", "resource_type": "Course", "resource_name": "JavaScript Fundamentals", "description": "Learn modern ES6+ JavaScript, DOM manipulation, async programming, and APIs."},
    {"skill": "React", "resource_type": "Course", "resource_name": "React Fundamentals", "description": "Master component-driven development, React hooks, state management, and props."},
    {"skill": "Responsive Design", "resource_type": "Course", "resource_name": "Responsive Web Design", "description": "Build mobile-friendly layouts using media queries, fluid typography, and dynamic grids."},
    {"skill": "REST API", "resource_type": "Course", "resource_name": "REST API Integration", "description": "Understand HTTP verbs, JSON parsing, backend API design, and Fetch integrations."},
    {"skill": "Git", "resource_type": "Course", "resource_name": "Git & GitHub Essentials", "description": "Master version control, branching strategies, commit history, and GitHub PR workflows."},
    {"skill": "Linux", "resource_type": "Course", "resource_name": "Linux Fundamentals", "description": "Master shell commands, file systems, permissions, package managers, and bash scripting."},
    {"skill": "Networking", "resource_type": "Course", "resource_name": "Networking Fundamentals", "description": "Learn OSI model, TCP/IP protocols, DNS, DHCP, routing, and network architecture."},
    {"skill": "Cybersecurity", "resource_type": "Course", "resource_name": "Cybersecurity Fundamentals", "description": "Understand security concepts, threat intelligence, encryption, and attack vectors."},
    {"skill": "Network Security", "resource_type": "Course", "resource_name": "Network Security & Defense", "description": "Learn firewalls, VPNs, IDS/IPS, network monitoring, and security hardening."},
    {"skill": "SIEM", "resource_type": "Course", "resource_name": "SIEM Fundamentals", "description": "Analyze security logs, configure alerts, and triage incidents using SIEM platforms."},
    {"skill": "Requirements Analysis", "resource_type": "Course", "resource_name": "Requirements Engineering", "description": "Learn stakeholder interviewing, user story mapping, and functional specification docs."},
    {"skill": "Communication", "resource_type": "Course", "resource_name": "Professional Communication", "description": "Enhance technical writing, presentation skills, and cross-functional team collaboration."},
    {"skill": "Problem Solving", "resource_type": "Course", "resource_name": "Analytical Problem Solving", "description": "Master structured problem breakdown, root-cause analysis, and critical thinking frameworks."}
]

resources_path = os.path.join(data_dir, "skill_resources.csv")
with open(resources_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["skill", "resource_type", "resource_name", "description"])
    writer.writeheader()
    writer.writerows(resources_data)

print(f"Generated {len(resources_data)} records in {resources_path}")
