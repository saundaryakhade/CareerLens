import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESUMES_DIR = os.path.join(BASE_DIR, "sample_resumes")
os.makedirs(RESUMES_DIR, exist_ok=True)

sample_profiles = [
    {
        "filename": "data_analyst_resume.pdf",
        "name": "Alex Mercer",
        "title": "Data Analyst",
        "skills": "Python, SQL, Excel, Statistics, Pandas, NumPy, Power BI, Data Visualization",
        "summary": "Results-oriented Data Analyst with 3 years of experience analyzing complex datasets using Python, SQL, and Excel. Proficient in data cleaning with Pandas and NumPy, building interactive Power BI dashboards, and communicating statistical findings to stakeholders."
    },
    {
        "filename": "aiml_engineer_resume.pdf",
        "name": "Samantha Chen",
        "title": "AI/ML Engineer",
        "skills": "Python, NumPy, Pandas, Statistics, Machine Learning, Deep Learning, TensorFlow, PyTorch, Scikit-learn, Git",
        "summary": "Passionate Artificial Intelligence Engineer specializing in Machine Learning and Deep Learning architectures. Extensive experience training neural network models using Python, TensorFlow, and PyTorch, conducting statistical evaluation, and managing version control via Git."
    },
    {
        "filename": "web_developer_resume.pdf",
        "name": "David Miller",
        "title": "Frontend Web Developer",
        "skills": "HTML, CSS, JavaScript, React, REST API, Git, Responsive Design",
        "summary": "Creative Web Developer with expertise in HTML5, CSS3, JavaScript, and React framework. Skilled in building responsive UI components, integrating REST API services, and collaborating on version-controlled projects with Git."
    },
    {
        "filename": "cybersecurity_resume.pdf",
        "name": "Marcus Vance",
        "title": "Cybersecurity Analyst",
        "skills": "Linux, Networking, Cybersecurity, Network Security, SIEM, Python, Firewalls",
        "summary": "Certified Cybersecurity Specialist experienced in Linux server administration, network protocol analysis, SIEM security log monitoring, and network defense strategies. Adept at Python automation for threat intelligence."
    },
    {
        "filename": "business_analyst_resume.pdf",
        "name": "Elena Rostova",
        "title": "Business Analyst",
        "skills": "Excel, SQL, Statistics, Power BI, Data Visualization, Requirements Analysis, Communication, Problem Solving",
        "summary": "Detail-oriented Business Analyst skilled in requirements analysis, stakeholder interviewing, and business reporting. Proficient in SQL database queries, advanced Excel modeling, Power BI visualizations, and cross-functional project communication."
    }
]

def generate_pdf(filepath, profile):
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 22)
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.drawString(50, height - 60, profile["name"])

    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(50, height - 85, profile["title"])

    # Line separator
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(1)
    c.line(50, height - 95, width - 50, height - 95)

    # Professional Summary Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.drawString(50, height - 130, "PROFESSIONAL SUMMARY")

    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    
    # Simple line wrapping
    words = profile["summary"].split(" ")
    line = ""
    y = height - 150
    for word in words:
        if c.stringWidth(line + " " + word, "Helvetica", 11) < (width - 100):
            line += (" " if line else "") + word
        else:
            c.drawString(50, y, line)
            y -= 16
            line = word
    if line:
        c.drawString(50, y, line)
        y -= 25

    # Core Skills Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.drawString(50, y, "TECHNICAL & CORE SKILLS")
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.1, 0.4, 0.7)
    c.drawString(50, y, "Skills: ")
    
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawString(95, y, profile["skills"])
    y -= 30

    # Experience Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.drawString(50, y, "WORK EXPERIENCE")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawString(50, y, f"Senior {profile['title']} — TechCorp Solutions")
    y -= 16
    
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, y, "2021 – Present | New York, NY")
    y -= 20

    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    bullets = [
        f"Leveraged {profile['skills'].split(',')[0]} and {profile['skills'].split(',')[1]} to optimize workflow processes.",
        f"Designed and deployed enterprise solutions incorporating {profile['skills'].split(',')[2]}.",
        "Collaborated with cross-functional technical teams to deliver data-driven results on schedule."
    ]

    for bullet in bullets:
        c.drawString(60, y, f"•  {bullet}")
        y -= 16

    c.save()
    print(f"Generated sample PDF resume: {filepath}")

def main():
    for prof in sample_profiles:
        path = os.path.join(RESUMES_DIR, prof["filename"])
        generate_pdf(path, prof)

if __name__ == "__main__":
    main()
