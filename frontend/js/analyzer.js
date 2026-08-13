// Master list of 29 skills with category labels
const MASTER_SKILLS = [
    { name: "Python", category: "Programming" },
    { name: "SQL", category: "Database" },
    { name: "Excel", category: "Analytics" },
    { name: "Statistics", category: "Analytics" },
    { name: "Pandas", category: "Programming" },
    { name: "NumPy", category: "Programming" },
    { name: "Power BI", category: "Analytics" },
    { name: "Tableau", category: "Analytics" },
    { name: "Data Visualization", category: "Analytics" },
    { name: "Data Modeling", category: "Database" },
    { name: "ETL", category: "Database" },
    { name: "Machine Learning", category: "AI" },
    { name: "Deep Learning", category: "AI" },
    { name: "TensorFlow", category: "AI" },
    { name: "PyTorch", category: "AI" },
    { name: "HTML", category: "Web Development" },
    { name: "CSS", category: "Web Development" },
    { name: "JavaScript", category: "Web Development" },
    { name: "React", category: "Web Development" },
    { name: "REST API", category: "Web Development" },
    { name: "Git", category: "Tools" },
    { name: "Linux", category: "Security" },
    { name: "Networking", category: "Security" },
    { name: "Cybersecurity", category: "Security" },
    { name: "Network Security", category: "Security" },
    { name: "SIEM", category: "Security" },
    { name: "Communication", category: "Business" },
    { name: "Problem Solving", category: "Business" },
    { name: "Requirements Analysis", category: "Business" }
];

let selectedSkills = new Set();
let currentCategoryFilter = "ALL";

document.addEventListener("DOMContentLoaded", () => {
    renderSkillsGrid();
    setupEventListeners();
    
    // Check URL params if pre-selected target career was clicked from careers.html
    const urlParams = new URLSearchParams(window.location.search);
    const targetCareer = urlParams.get("target");
    if (targetCareer) {
        applyPresetForCareer(targetCareer);
    }
});

function renderSkillsGrid() {
    const grid = document.getElementById("skills-checkbox-grid");
    const searchQuery = document.getElementById("skill-search-input").value.toLowerCase().trim();

    grid.innerHTML = "";

    const filtered = MASTER_SKILLS.filter(skill => {
        const matchesCat = (currentCategoryFilter === "ALL") || 
                           (currentCategoryFilter === "Analytics" && (skill.category === "Analytics" || skill.category === "Visualization")) ||
                           (skill.category === currentCategoryFilter);
        const matchesSearch = skill.name.toLowerCase().includes(searchQuery);
        return matchesCat && matchesSearch;
    });

    if (filtered.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1 / -1; padding: 2rem; text-align: center; color: var(--text-muted);">No skills found matching search criteria.</div>`;
        return;
    }

    filtered.forEach(skill => {
        const isChecked = selectedSkills.has(skill.name);
        const item = document.createElement("label");
        item.className = "skill-checkbox-item";
        if (isChecked) {
            item.style.borderColor = "var(--primary)";
            item.style.backgroundColor = "var(--primary-light)";
        }

        item.innerHTML = `
            <input type="checkbox" value="${skill.name}" ${isChecked ? 'checked' : ''}>
            <span style="font-weight: 500; font-size: 0.92rem;">${skill.name}</span>
        `;

        const checkbox = item.querySelector("input");
        checkbox.addEventListener("change", (e) => {
            if (e.target.checked) {
                selectedSkills.add(skill.name);
                item.style.borderColor = "var(--primary)";
                item.style.backgroundColor = "var(--primary-light)";
            } else {
                selectedSkills.delete(skill.name);
                item.style.borderColor = "var(--border-color)";
                item.style.backgroundColor = "white";
            }
            updateCounter();
        });

        grid.appendChild(item);
    });

    updateCounter();
}

function updateCounter() {
    const counterEl = document.getElementById("selected-skills-counter");
    counterEl.innerText = `${selectedSkills.size} Skill${selectedSkills.size === 1 ? '' : 's'} Selected`;
}

function setupEventListeners() {
    // Search input
    document.getElementById("skill-search-input").addEventListener("input", renderSkillsGrid);

    // Category filter buttons
    const catButtons = document.querySelectorAll(".category-btn");
    catButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            catButtons.forEach(b => {
                b.style.background = "white";
                b.style.color = "var(--text-main)";
            });
            btn.style.background = "var(--primary)";
            btn.style.color = "white";
            currentCategoryFilter = btn.dataset.cat;
            renderSkillsGrid();
        });
    });

    // Preset buttons
    const presetButtons = document.querySelectorAll(".preset-btn");
    presetButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const preset = btn.dataset.preset;
            if (preset === "da") {
                selectedSkills = new Set(["Python", "SQL", "Excel", "Statistics", "Pandas", "Power BI"]);
            } else if (preset === "ml") {
                selectedSkills = new Set(["Python", "NumPy", "Pandas", "Statistics", "Machine Learning", "TensorFlow"]);
            } else if (preset === "web") {
                selectedSkills = new Set(["HTML", "CSS", "JavaScript", "React", "REST API", "Git"]);
            } else if (preset === "sec") {
                selectedSkills = new Set(["Linux", "Networking", "Cybersecurity", "Network Security", "SIEM"]);
            } else if (preset === "clear") {
                selectedSkills.clear();
            }
            renderSkillsGrid();
        });
    });

    // Predict My Career Submit Handler
    document.getElementById("btn-predict-career").addEventListener("click", async () => {
        if (selectedSkills.size === 0) {
            showAlert("Please select at least 1 skill before predicting your career fit.", "error");
            return;
        }

        const skillList = Array.from(selectedSkills);
        showLoader("Running Machine Learning classification model & calculating skill gap...");

        try {
            const response = await fetch(`${API_BASE}/predict-career`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ skills: skillList })
            });

            const data = await response.json();
            hideLoader();

            if (data.status === "success") {
                saveAnalysisResults(data);
                window.location.href = "dashboard.html";
            } else {
                showAlert(data.message || "Failed to predict career.", "error");
            }
        } catch (err) {
            hideLoader();
            console.error("Prediction error:", err);
            showAlert("Unable to connect to Flask backend server. Ensure backend/app.py is running.", "error");
        }
    });
}

function applyPresetForCareer(careerName) {
    if (careerName === "Data Analyst") {
        selectedSkills = new Set(["Python", "SQL", "Excel", "Statistics", "Pandas"]);
    } else if (careerName === "AI/ML Engineer") {
        selectedSkills = new Set(["Python", "NumPy", "Pandas", "Statistics", "Machine Learning"]);
    } else if (careerName === "Web Developer") {
        selectedSkills = new Set(["HTML", "CSS", "JavaScript", "React"]);
    } else if (careerName === "Cybersecurity Analyst") {
        selectedSkills = new Set(["Linux", "Networking", "Cybersecurity"]);
    } else if (careerName === "Business Analyst") {
        selectedSkills = new Set(["Excel", "SQL", "Requirements Analysis", "Communication"]);
    }
    renderSkillsGrid();
}
