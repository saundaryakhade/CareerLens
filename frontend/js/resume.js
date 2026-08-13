let selectedFile = null;

document.addEventListener("DOMContentLoaded", () => {
    setupDropzone();
    setupSampleButtons();
});

function setupDropzone() {
    const dropzone = document.getElementById("pdf-dropzone");
    const fileInput = document.getElementById("pdf-file-input");
    const analyzeBtn = document.getElementById("btn-analyze-resume");
    const removeBtn = document.getElementById("btn-remove-file");

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'), false);
    });

    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    removeBtn.addEventListener('click', () => {
        selectedFile = null;
        fileInput.value = "";
        document.getElementById("file-info-box").style.display = "none";
        document.getElementById("pdf-dropzone").style.display = "block";
        analyzeBtn.disabled = true;
    });

    analyzeBtn.addEventListener('click', uploadAndAnalyzeResume);
}

function handleFileSelect(file) {
    if (!file.name.toLowerCase().endswith ? !file.name.toLowerCase().endsWith('.pdf') : !file.name.toLowerCase().match(/\.pdf$/)) {
        showAlert("Please upload a valid PDF (.pdf) file.", "error");
        return;
    }

    selectedFile = file;
    document.getElementById("uploaded-filename").innerText = file.name;
    document.getElementById("uploaded-filesize").innerText = `${(file.size / 1024).toFixed(1)} KB`;

    document.getElementById("pdf-dropzone").style.display = "none";
    document.getElementById("file-info-box").style.display = "flex";
    document.getElementById("btn-analyze-resume").disabled = false;
}

function setupSampleButtons() {
    const sampleBtns = document.querySelectorAll(".sample-resume-btn");
    sampleBtns.forEach(btn => {
        btn.addEventListener("click", async () => {
            const filename = btn.dataset.file;
            showLoader(`Loading sample resume (${filename})...`);

            try {
                // Fetch sample PDF from sample_resumes folder or backend server
                const res = await fetch(`http://localhost:5000/api/sample-resume/${filename}`).catch(() => null);
                
                let fileBlob;
                if (res && res.ok) {
                    fileBlob = await res.blob();
                } else {
                    // Fallback to fetch from relative project path if static served
                    const staticRes = await fetch(`../sample_resumes/${filename}`);
                    fileBlob = await staticRes.blob();
                }

                const file = new File([fileBlob], filename, { type: "application/pdf" });
                hideLoader();
                handleFileSelect(file);
            } catch (err) {
                hideLoader();
                console.error("Error loading sample PDF:", err);
                showAlert("Could not load sample PDF. You can pick your own PDF file.", "error");
            }
        });
    });
}

async function uploadAndAnalyzeResume() {
    if (!selectedFile) {
        showAlert("Please select a PDF file first.", "error");
        return;
    }

    showLoader("Extracting text from PDF & running NLP Machine Learning classifier...");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch(`${API_BASE}/analyze-resume`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        hideLoader();

        if (data.status === "success") {
            saveAnalysisResults(data);
            window.location.href = "dashboard.html";
        } else {
            showAlert(data.message || "Failed to analyze resume.", "error");
        }
    } catch (err) {
        hideLoader();
        console.error("Resume analysis error:", err);
        showAlert("Unable to connect to Flask backend server. Ensure backend/app.py is running.", "error");
    }
}
