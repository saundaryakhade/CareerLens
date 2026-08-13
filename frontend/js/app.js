// SkillGap ML - Core Shared Utility & API Client Module
const API_BASE = window.location.origin.startsWith("file://") ? "http://localhost:5000/api" : "/api";

// Active Nav Link Highlighting
document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname.split("/").pop() || "index.html";
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        const href = link.getAttribute("href");
        if (href === currentPath || (currentPath === "" && href === "index.html")) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
});

// UI Spinner Helper Functions
function showLoader(message = "Analyzing data with ML models...") {
    let loader = document.getElementById("global-loader");
    if (!loader) {
        loader = document.createElement("div");
        loader.id = "global-loader";
        loader.className = "loading-overlay";
        loader.innerHTML = `
            <div class="loading-spinner"></div>
            <div id="loader-text" style="font-weight: 600; font-size: 1.1rem;">${message}</div>
        `;
        document.body.appendChild(loader);
    } else {
        document.getElementById("loader-text").innerText = message;
    }
    loader.style.display = "flex";
}

function hideLoader() {
    const loader = document.getElementById("global-loader");
    if (loader) {
        loader.style.display = "none";
    }
}

// Global Alert / Toast Notification Helper
function showAlert(message, type = "error") {
    alert(`[${type.toUpperCase()}] ${message}`);
}

// Storage Helpers for Dashboard Pass-Through
function saveAnalysisResults(results) {
    sessionStorage.setItem("careerlens_last_analysis", JSON.stringify(results));
}

function getAnalysisResults() {
    const data = sessionStorage.getItem("careerlens_last_analysis") || sessionStorage.getItem("skillgap_last_analysis");
    return data ? JSON.parse(data) : null;
}
