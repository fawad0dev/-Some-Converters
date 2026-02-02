// Global state
let currentFiles = [];
let conversionId = null;
let selectedFormat = null;

// Format mappings for different categories
const formatMappings = {
    'image': ['png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp'],
    'document': ['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
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
        handleFileSelect(Array.from(files));
    }
}

// Setup file input
function setupFileInput() {
    const fileInput = document.getElementById('file-input');
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(Array.from(e.target.files));
        }
    });
}

// Handle file selection
async function handleFileSelect(files) {
    currentFiles = files;
    
    // Show progress
    showSection('progress-section');
    updateProgress('Uploading files...', 20);
    
    try {
        // Upload files
        const formData = new FormData();
        
        // Add all files to form data
        files.forEach(file => {
            formData.append('files', file);
        });
        
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
        updateProgress('Files uploaded successfully', 100);
        setTimeout(() => {
            displayFileInfo(data);
            showConversionOptions(data);
            showSection('conversion-section');
        }, 500);
        
    } catch (error) {
        console.error('Upload error:', error);
        showError(error.message);
    }
}

// Display file information
function displayFileInfo(data) {
    const filesList = document.getElementById('files-list');
    filesList.innerHTML = '';
    
    // Check if single file or multiple files
    const files = data.files || [{ filename: data.filename, size: data.size, category: data.category }];
    
    files.forEach(fileData => {
        const filePreview = document.createElement('div');
        filePreview.className = 'file-preview';
        
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
        
        filePreview.innerHTML = `
            <span class="file-icon">${iconMap[fileData.category] || '📄'}</span>
            <div class="file-details">
                <h3 class="file-name">${fileData.filename}</h3>
                <p class="file-size">${formatBytes(fileData.size)}</p>
                <p class="file-category">Category: ${capitalizeFirst(fileData.category)}</p>
            </div>
        `;
        
        filesList.appendChild(filePreview);
    });
}

// Show conversion options
function showConversionOptions(data) {
    const formatButtons = document.getElementById('format-buttons');
    formatButtons.innerHTML = '';
    
    // Get category from single or multiple files
    const category = data.category || (data.files && data.files.length > 0 ? data.files[0].category : null);
    
    if (!category) {
        return;
    }
    
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
        showError('Please select a target format');
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
    const fileCount = data.files_converted || 1;
    const message = fileCount > 1 
        ? `Your ${fileCount} files are ready in a ZIP archive (${formatBytes(data.output_size)})`
        : `Your ${selectedFormat.toUpperCase()} file is ready (${formatBytes(data.output_size)})`;
    
    document.getElementById('output-info').textContent = message;
    
    // Show warnings if any errors occurred
    if (data.errors && data.errors.length > 0) {
        const errorList = data.errors.join(', ');
        document.getElementById('output-info').textContent += `\n\nNote: Some files had issues: ${errorList}`;
    }
    
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
    currentFiles = [];
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
