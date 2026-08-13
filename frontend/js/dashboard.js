let chartProbabilitiesInstance = null;
let chartCoverageInstance = null;
let chartCategoriesInstance = null;

document.addEventListener("DOMContentLoaded", () => {
    const analysisData = getAnalysisResults();

    if (!analysisData || !analysisData.predicted_career) {
        document.getElementById("dashboard-empty-state").style.display = "block";
        document.getElementById("dashboard-content").style.display = "none";
        return;
    }

    document.getElementById("dashboard-empty-state").style.display = "none";
    document.getElementById("dashboard-content").style.display = "block";

    renderDashboard(analysisData);
});

function renderDashboard(data) {
    // Analysis source header
    const sourceLabel = document.getElementById("analysis-source-label");
    if (data.source === "resume_pdf") {
        sourceLabel.innerHTML = `📄 CareerLens Resume Intelligence: <strong>${data.filename || "Uploaded Resume"}</strong>`;
    } else {
        sourceLabel.innerHTML = `⚡ CareerLens Manual Skill Check (${(data.user_skills || []).length} Skills Inputted)`;
    }

    // Top Stat Cards
    document.getElementById("stat-predicted-career").innerText = data.predicted_career;
    document.getElementById("stat-ml-confidence").innerText = `${data.ml_confidence}%`;
    document.getElementById("stat-skill-match").innerText = `${data.skill_match_score}%`;
    
    const detectedCount = data.source === "resume_pdf" 
        ? (data.detected_skills || []).length 
        : (data.user_skills || []).length;
    document.getElementById("stat-skills-count").innerText = detectedCount;

    // Render Matched / Strong Skills
    const matchedContainer = document.getElementById("matched-skills-container");
    const matchedList = data.matched_skills || [];
    if (matchedList.length === 0) {
        matchedContainer.innerHTML = `<span style="color: var(--text-muted); font-size: 0.9rem;">No matching skills detected for this career profile.</span>`;
    } else {
        matchedContainer.innerHTML = matchedList.map(item => `
            <span class="skill-tag matched">
                ✓ ${item.skill}
            </span>
        `).join('');
    }

    // Render Missing Skills with Priority
    const missingContainer = document.getElementById("missing-skills-container");
    const missingList = data.missing_skills || [];
    if (missingList.length === 0) {
        missingContainer.innerHTML = `
            <div class="priority-card priority-low">
                <span>🎉 Perfect Coverage! You possess all required skills for ${data.predicted_career}.</span>
            </div>
        `;
    } else {
        missingContainer.innerHTML = missingList.map(item => `
            <div class="priority-card priority-${item.priority.toLowerCase()}">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span>${item.priority_code}</span>
                    <strong style="font-size: 0.95rem;">${item.skill}</strong>
                    <span style="font-size: 0.8rem; opacity: 0.8;">(${item.category})</span>
                </div>
                <div style="text-align: right;">
                    <span class="skill-tag" style="font-size: 0.75rem; padding: 0.2rem 0.6rem;">${item.priority} Priority</span>
                    ${item.prerequisite ? `<div style="font-size: 0.75rem; opacity: 0.85; margin-top: 0.2rem;">Requires: ${item.prerequisite}</div>` : ''}
                </div>
            </div>
        `).join('');
    }

    // Render Charts
    renderProbabilitiesChart(data.career_probabilities || {});
    renderCoverageChart(matchedList.length, missingList.length);
    renderCategoryChart(data.category_coverage || {});

    // Render Learning Path Timeline
    renderLearningPath(data.learning_path || []);
}

function renderProbabilitiesChart(probabilities) {
    const ctx = document.getElementById("chart-probabilities").getContext("2d");
    if (chartProbabilitiesInstance) chartProbabilitiesInstance.destroy();

    const labels = Object.keys(probabilities);
    const values = Object.values(probabilities);

    chartProbabilitiesInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Prediction Confidence (%)',
                data: values,
                backgroundColor: labels.map((l, i) => i === 0 ? 'rgba(79, 70, 229, 0.85)' : 'rgba(148, 163, 184, 0.5)'),
                borderColor: labels.map((l, i) => i === 0 ? '#4f46e5' : '#94a3b8'),
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => ` Probability: ${ctx.raw}%`
                    }
                }
            },
            scales: {
                x: { max: 100, min: 0, ticks: { callback: v => v + '%' } }
            }
        }
    });
}

function renderCoverageChart(matchedCount, missingCount) {
    const ctx = document.getElementById("chart-coverage").getContext("2d");
    if (chartCoverageInstance) chartCoverageInstance.destroy();

    chartCoverageInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Present Skills', 'Missing Skills'],
            datasets: [{
                data: [matchedCount, missingCount],
                backgroundColor: ['#10b981', '#ef4444'],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function renderCategoryChart(categoryCoverage) {
    const ctx = document.getElementById("chart-categories").getContext("2d");
    if (chartCategoriesInstance) chartCategoriesInstance.destroy();

    const labels = Object.keys(categoryCoverage);
    const values = labels.map(cat => categoryCoverage[cat].percentage);

    chartCategoriesInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Category Mastery (%)',
                data: values,
                backgroundColor: 'rgba(14, 165, 233, 0.75)',
                borderColor: '#0ea5e9',
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { max: 100, min: 0, ticks: { callback: v => v + '%' } }
            }
        }
    });
}

function renderLearningPath(pathList) {
    const container = document.getElementById("learning-path-container");
    const countBadge = document.getElementById("learning-steps-count");

    countBadge.innerText = `${pathList.length} Learning Step${pathList.length === 1 ? '' : 's'}`;

    if (pathList.length === 0) {
        container.innerHTML = `
            <div class="card" style="text-align: center; color: var(--text-muted); padding: 2rem;">
                No missing skills detected. You have already mastered the core skills required for this career path!
            </div>
        `;
        return;
    }

    container.innerHTML = pathList.map(step => `
        <div class="timeline-node">
            <div class="timeline-number">${step.step}</div>
            <div class="timeline-content">
                <div class="timeline-header">
                    <div class="timeline-title">${step.skill}</div>
                    <span class="skill-tag" style="font-size: 0.75rem; background: var(--light-bg);">
                        ${step.priority_code} ${step.priority} Priority
                    </span>
                </div>
                <div style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 0.5rem;">
                    Category: <strong>${step.category}</strong> ${step.prerequisite ? ` | Prerequisite required: <strong style="color: var(--primary);">${step.prerequisite}</strong>` : ''}
                </div>
                
                ${step.resource ? `
                    <div class="timeline-resource">
                        <div style="font-weight: 700; color: var(--dark); margin-bottom: 0.2rem;">
                            📚 ${step.resource.resource_type}: ${step.resource.resource_name}
                        </div>
                        <div style="color: var(--text-muted); font-size: 0.85rem;">
                            ${step.resource.description}
                        </div>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}
