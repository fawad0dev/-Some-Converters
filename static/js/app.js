// Global state
let currentFile = null;
let conversionId = null;
let selectedFormat = null;

// Format mappings for different categories
const formatMappings = {
    'image': ['png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp'],
    'document': ['pdf', 'docx', 'txt'],
    'audio': ['mp3', 'wav', 'ogg', 'flac'],
    'video': ['mp4', 'mkv', 'avi', 'webm', 'gif'],
    '3d': ['obj', 'gltf', 'glb'],
    'font': ['ttf', 'otf', 'woff', 'woff2'],
    'data': ['json', 'csv', 'xml'],
    'archive': ['zip', 'tar'],
    'design': ['png', 'jpg', 'svg']
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupUploadArea();
    setupFileInput();
});

// Setup drag and drop
function setupUploadArea() {
    const uploadArea = document.getElementById('upload-area');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.add('dragging');
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.remove('dragging');
        });
    });
    
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => {
        document.getElementById('file-input').click();
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
}

// Setup file input
function setupFileInput() {
    const fileInput = document.getElementById('file-input');
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

// Handle file selection
async function handleFileSelect(file) {
    currentFile = file;
    
    // Show progress
    showSection('progress-section');
    updateProgress('Uploading file...', 20);
    
    try {
        // Upload file
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }
        
        const data = await response.json();
        conversionId = data.conversion_id;
        
        // Update UI with file info
        updateProgress('File uploaded successfully', 100);
        setTimeout(() => {
            displayFileInfo(data);
            showConversionOptions(data.category);
            showSection('conversion-section');
        }, 500);
        
    } catch (error) {
        console.error('Upload error:', error);
        showError(error.message);
    }
}

// Display file information
function displayFileInfo(data) {
    document.getElementById('file-name').textContent = data.filename;
    document.getElementById('file-size').textContent = formatBytes(data.size);
    document.getElementById('file-category').textContent = `Category: ${capitalizeFirst(data.category)}`;
    
    // Set appropriate icon
    const iconMap = {
        'image': '🖼️',
        'document': '📄',
        'audio': '🎵',
        'video': '🎬',
        'data': '📊',
        'archive': '🗜️',
        'font': '🔤',
        '3d': '🎮',
        'design': '🎨'
    };
    
    document.querySelector('.file-icon').textContent = iconMap[data.category] || '📄';
}

// Show conversion options
function showConversionOptions(category) {
    const formatButtons = document.getElementById('format-buttons');
    formatButtons.innerHTML = '';
    
    const formats = formatMappings[category] || [];
    
    formats.forEach(format => {
        const btn = document.createElement('button');
        btn.className = 'format-btn';
        btn.textContent = format.toUpperCase();
        btn.onclick = () => selectFormat(format, btn);
        formatButtons.appendChild(btn);
    });
}

// Select target format
function selectFormat(format, button) {
    // Remove selection from all buttons
    document.querySelectorAll('.format-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Select clicked button
    button.classList.add('selected');
    selectedFormat = format;
    
    // Enable convert button
    document.getElementById('convert-btn').disabled = false;
}

// Start conversion
async function startConversion() {
    if (!selectedFormat || !conversionId) {
        alert('Please select a target format');
        return;
    }
    
    showSection('progress-section');
    updateProgress('Converting file...', 30);
    
    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                conversion_id: conversionId,
                target_format: selectedFormat
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Conversion failed');
        }
        
        const data = await response.json();
        
        // Simulate progress
        updateProgress('Finalizing...', 80);
        
        setTimeout(() => {
            updateProgress('Complete!', 100);
            setTimeout(() => {
                showDownloadSection(data);
            }, 500);
        }, 500);
        
    } catch (error) {
        console.error('Conversion error:', error);
        showError(error.message);
    }
}

// Show download section
function showDownloadSection(data) {
    document.getElementById('output-info').textContent = 
        `Your ${selectedFormat.toUpperCase()} file is ready (${formatBytes(data.output_size)})`;
    showSection('download-section');
}

// Download converted file
async function downloadFile() {
    if (!conversionId) return;
    
    try {
        window.location.href = `/api/download/${conversionId}`;
        
        // Clean up after a delay
        setTimeout(() => {
            cleanupFiles();
        }, 2000);
        
    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download file');
    }
}

// Cleanup files
async function cleanupFiles() {
    if (!conversionId) return;
    
    try {
        await fetch(`/api/cleanup/${conversionId}`, {
            method: 'DELETE'
        });
    } catch (error) {
        console.error('Cleanup error:', error);
    }
}

// Show error
function showError(message) {
    document.getElementById('error-message').textContent = message;
    showSection('error-section');
}

// Update progress
function updateProgress(message, percent) {
    document.getElementById('progress-message').textContent = message;
    document.getElementById('progress-fill').style.width = `${percent}%`;
}

// Show section
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
}

// Reset app
function resetApp() {
    // Clean up if needed
    if (conversionId) {
        cleanupFiles();
    }
    
    // Reset state
    currentFile = null;
    conversionId = null;
    selectedFormat = null;
    
    // Reset UI
    document.getElementById('file-input').value = '';
    document.getElementById('convert-btn').disabled = true;
    showSection('upload-section');
}

// Utility functions
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
