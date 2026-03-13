const API_BASE_URL = '';

let uploadedFile = null;
let documentLoaded = false;

const fileInput = document.getElementById('fileInput');
const selectFileBtn = document.getElementById('selectFileBtn');
const uploadArea = document.getElementById('uploadArea');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');
const uploadLoader = document.getElementById('uploadLoader');

const summarySection = document.getElementById('summarySection');
const summaryContent = document.getElementById('summaryContent');
const summaryLoader = document.getElementById('summaryLoader');
const generateSummaryBtn = document.getElementById('generateSummaryBtn');

const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const qaLoader = document.getElementById('qaLoader');
const qaResults = document.getElementById('qaResults');

selectFileBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    fileInput.click();
});

uploadArea.addEventListener('click', (e) => {
    if (e.target === uploadArea || e.target.closest('.upload-icon') || e.target.closest('p')) {
        e.preventDefault();
        fileInput.click();
    }
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.background = '#e0e7ff';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.background = '#f8f9ff';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.background = '#f8f9ff';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (!validTypes.includes(file.type)) {
        showStatus('Please select a PDF or DOCX file', 'error');
        return;
    }
    
    uploadedFile = file;
    fileName.textContent = file.name;
    fileInfo.style.display = 'block';
    uploadStatus.style.display = 'none';
}

uploadBtn.addEventListener('click', async () => {
    if (!uploadedFile) {
        showStatus('Please select a file first', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', uploadedFile);
    
    uploadLoader.style.display = 'block';
    uploadStatus.style.display = 'none';
    uploadBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus(`✓ File uploaded successfully! Processed ${data.total_chunks} chunks (${data.total_words} words)`, 'success');
            documentLoaded = true;
            
            summarySection.style.display = 'block';
            summaryContent.innerHTML = '<p class="placeholder">Click "Generate Summary" to get an AI-powered summary of your document</p>';
        } else {
            showStatus(`Error: ${data.error}`, 'error');
            if (data.error.includes('quota') || data.error.includes('API key')) {
                showStatus(`${data.error}\n\nPlease check your Google API key and billing status.`, 'error');
            }
        }
    } catch (error) {
        console.error('Upload error:', error);
        showStatus(`Upload failed: ${error.message}`, 'error');
    } finally {
        uploadLoader.style.display = 'none';
        uploadBtn.disabled = false;
    }
});

function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `status-message ${type}`;
    uploadStatus.style.display = 'block';
}

generateSummaryBtn.addEventListener('click', async () => {
    if (!documentLoaded) {
        alert('Please upload a document first');
        return;
    }
    
    await generateSummary();
});

async function generateSummary() {
    summaryContent.innerHTML = '<p class="placeholder">Generating summary...</p>';
    summaryLoader.style.display = 'block';
    generateSummaryBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            summaryContent.innerHTML = `
                <div style="margin-bottom: 15px;">
                    <strong style="color: #667eea;">Document:</strong> ${data.document}
                </div>
                <div style="white-space: pre-wrap;">${data.summary}</div>
            `;
        } else {
            summaryContent.innerHTML = `<p style="color: #ef4444;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        summaryContent.innerHTML = `<p style="color: #ef4444;">Failed to generate summary: ${error.message}</p>`;
    } finally {
        summaryLoader.style.display = 'none';
        generateSummaryBtn.disabled = false;
    }
}

askBtn.addEventListener('click', async () => {
    const question = questionInput.value.trim();
    
    if (!question) {
        alert('Please enter a question');
        return;
    }
    
    if (!documentLoaded) {
        alert('Please upload a document first');
        return;
    }
    
    qaLoader.style.display = 'block';
    askBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayAnswer(data);
            questionInput.value = '';
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert(`Failed to get answer: ${error.message}`);
    } finally {
        qaLoader.style.display = 'none';
        askBtn.disabled = false;
    }
});

questionInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        askBtn.click();
    }
});

function displayAnswer(data) {
    const qaItem = document.createElement('div');
    qaItem.className = 'qa-item';
    
    qaItem.innerHTML = `
        <div class="qa-question">Q: ${data.question}</div>
        <div class="qa-answer">${data.answer}</div>
        <div class="qa-meta">
            📄 Source: ${data.document} | 
            📊 Chunks analyzed: ${data.chunks_used}
        </div>
    `;
    
    qaResults.insertBefore(qaItem, qaResults.firstChild);
}

async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`);
        const data = await response.json();
        
        if (data.document_loaded) {
            documentLoaded = true;
            summarySection.style.display = 'block';
        }
    } catch (error) {
        console.error('Status check failed:', error);
    }
}

checkStatus();
