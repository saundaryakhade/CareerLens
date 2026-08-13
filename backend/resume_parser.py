import re
from pypdf import PdfReader

# Master skill dictionary with regex synonyms
ALL_SKILLS_MAP = {
    "Python": [r"\bpython\b", r"\bpy\b"],
    "SQL": [r"\bsql\b", r"\bmysql\b", r"\bpostgresql\b", r"\bsqlite\b", r"\btsql\b", r"\bplsql\b"],
    "Excel": [r"\bexcel\b", r"\bms excel\b", r"\bspreadsheet\b", r"\bpivot tables\b"],
    "Statistics": [r"\bstatistics\b", r"\bstatistical\b", r"\bprobability\b", r"\bhypothesis testing\b"],
    "Pandas": [r"\bpandas\b"],
    "NumPy": [r"\bnumpy\b"],
    "Power BI": [r"\bpower bi\b", r"\bpowerbi\b", r"\bdax\b"],
    "Tableau": [r"\btableau\b"],
    "Data Visualization": [r"\bdata visualization\b", r"\bvisualizations\b", r"\bcharting\b", r"\bdashboards\b"],
    "Data Modeling": [r"\bdata modeling\b", r"\ber diagram\b", r"\bstar schema\b", r"\bdatabase design\b"],
    "ETL": [r"\betl\b", r"\bdata pipeline\b", r"\bdata engineering\b", r"\bingestion\b"],
    "Machine Learning": [r"\bmachine learning\b", r"\bml\b", r"\bscikit-learn\b", r"\bsklearn\b", r"\bpredictive modeling\b"],
    "Deep Learning": [r"\bdeep learning\b", r"\bneural networks\b", r"\bcnn\b", r"\brnn\b"],
    "TensorFlow": [r"\btensorflow\b", r"\btf\b", r"\bkeras\b"],
    "PyTorch": [r"\bpytorch\b", r"\btorch\b"],
    "HTML": [r"\bhtml\b", r"\bhtml5\b"],
    "CSS": [r"\bcss\b", r"\bcss3\b", r"\bflexbox\b", r"\bgrid\b"],
    "JavaScript": [r"\bjavascript\b", r"\bjs\b", r"\bes6\b"],
    "React": [r"\breact\b", r"\breactjs\b", r"\breact\.js\b"],
    "REST API": [r"\brest api\b", r"\brestful\b", r"\bapi integration\b", r"\bhttp api\b"],
    "Responsive Design": [r"\bresponsive design\b", r"\bmobile-friendly\b", r"\bresponsive ui\b"],
    "Git": [r"\bgit\b", r"\bgithub\b", r"\bgitlab\b", r"\bversion control\b"],
    "Linux": [r"\blinux\b", r"\bubuntu\b", r"\bcentos\b", r"\bbash\b", r"\bshell scripting\b"],
    "Networking": [r"\bnetworking\b", r"\btcp/ip\b", r"\bdns\b", r"\bip routing\b", r"\bwireshark\b"],
    "Cybersecurity": [r"\bcybersecurity\b", r"\binformation security\b", r"\bsecurity auditing\b"],
    "Network Security": [r"\bnetwork security\b", r"\bfirewall\b", r"\bids/ips\b", r"\bvpn\b"],
    "SIEM": [r"\bsiem\b", r"\bsplunk\b", r"\belk stack\b", r"\blog analysis\b"],
    "Communication": [r"\bcommunication\b", r"\bpresentation skills\b", r"\btechnical writing\b", r"\bstakeholder\b"],
    "Problem Solving": [r"\bproblem solving\b", r"\banalytical skills\b", r"\bcritical thinking\b"],
    "Requirements Analysis": [r"\brequirements analysis\b", r"\brequirements gathering\b", r"\buser stories\b", r"\bprocess modeling\b"]
}

def extract_text_from_pdf(pdf_file_path):
    try:
        reader = PdfReader(pdf_file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF {pdf_file_path}: {e}")
        return ""

def extract_skills_from_text(text):
    if not text:
        return []

    text_lower = text.lower()
    detected_skills = []

    for skill_name, patterns in ALL_SKILLS_MAP.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                detected_skills.append(skill_name)
                break

    return detected_skills
