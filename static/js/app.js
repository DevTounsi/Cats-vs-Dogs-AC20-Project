document.addEventListener('DOMContentLoaded', () => {
    
    // =========================================
    // SLIDE DECK NAVIGATION & CONTROL
    // =========================================
    const slides = document.querySelectorAll('.slide');
    const navLinks = document.querySelectorAll('.nav-link');
    let currentSlideIndex = 0;
    
    // Sidebar elements
    const sidebar = document.getElementById('sidebar');
    const sidebarToggleBtn = document.getElementById('sidebar-toggle-btn');
    
    // Sidebar toggle functionality
    if (sidebarToggleBtn && sidebar) {
        // Restore collapse state if saved
        if (localStorage.getItem('sidebar-collapsed') === 'true') {
            sidebar.classList.add('collapsed');
            const icon = sidebarToggleBtn.querySelector('i');
            if (icon) icon.className = 'fa-solid fa-chevron-right';
        }
        
        sidebarToggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const isCollapsed = sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebar-collapsed', isCollapsed);
            
            // Toggle chevron icon
            const icon = sidebarToggleBtn.querySelector('i');
            if (icon) {
                if (isCollapsed) {
                    icon.className = 'fa-solid fa-chevron-right';
                } else {
                    icon.className = 'fa-solid fa-chevron-left';
                }
            }
        });
    }

    // Navigation Controls Elements
    const prevBtn = document.getElementById('prev-slide-btn');
    const nextBtn = document.getElementById('next-slide-btn');
    const indicatorText = document.getElementById('slide-indicator-text');

    function showSlide(index) {
        if (index < 0) index = 0;
        if (index >= slides.length) index = slides.length - 1;
        
        currentSlideIndex = index;
        
        // Hide all slides
        slides.forEach(slide => {
            slide.classList.remove('active');
        });
        
        // Show target slide
        if (slides[index]) {
            slides[index].classList.add('active');
            // Dispatch a custom event to notify charts to render/update when visible
            const event = new CustomEvent('slideChanged', { detail: { index: index, id: slides[index].id } });
            document.dispatchEvent(event);
        }
        
        // Update active nav state
        navLinks.forEach((link) => {
            if (parseInt(link.getAttribute('data-slide')) === index) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        // Update presentation controls UI
        if (indicatorText) {
            indicatorText.textContent = `${index + 1} / ${slides.length}`;
        }
        if (prevBtn) {
            prevBtn.disabled = (index === 0);
        }
        if (nextBtn) {
            nextBtn.disabled = (index === slides.length - 1);
        }
    }
    
    // Navigation controls click handlers
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            showSlide(currentSlideIndex - 1);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            showSlide(currentSlideIndex + 1);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Keyboard controls (Arrow keys)
    document.addEventListener('keydown', (e) => {
        // Do not navigate if user is in an input field
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
            return;
        }
        if (e.key === 'ArrowLeft') {
            showSlide(currentSlideIndex - 1);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else if (e.key === 'ArrowRight') {
            showSlide(currentSlideIndex + 1);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
    
    // Navigation link click handlers
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('href');
            if (targetId.startsWith('#')) {
                e.preventDefault();
                const slideIndex = parseInt(link.getAttribute('data-slide'));
                showSlide(slideIndex);
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });
    
    // Next slide trigger buttons
    const nextTriggers = document.querySelectorAll('.next-slide-trigger');
    nextTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const nextIndex = parseInt(trigger.getAttribute('data-next'));
            showSlide(nextIndex);
        });
    });
    
    // Initialize first slide (slide index 0)
    showSlide(0);
    
    
    // =========================================
    // IMAGE UPLOAD & INTERACTION
    // =========================================
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const previewContainer = document.querySelector('.preview-container');
    const imagePreview = document.getElementById('image-preview');
    const clearImageBtn = document.getElementById('clear-image-btn');
    const uploadPlaceholder = document.querySelector('.upload-placeholder');
    const submitBtn = document.getElementById('analyze-submit-btn');
    const analyzeForm = document.getElementById('analyze-form');
    
    // Click on drop zone opens file chooser
    dropZone.addEventListener('click', (e) => {
        // Don't trigger when clicking clear button or browse button (which also triggers)
        if (e.target !== clearImageBtn && !clearImageBtn.contains(e.target)) {
            fileInput.click();
        }
    });
    
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        }, false);
    });
    
    // Handle dropped files
    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });
    
    // Handle selected file
    fileInput.addEventListener('change', (e) => {
        if (fileInput.files.length > 0) {
            handleFileSelect(fileInput.files[0]);
        }
    });
    
    function handleFileSelect(file) {
        if (!file.type.startsWith('image/')) {
            alert('Veuillez sélectionner un fichier image valide.');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            uploadPlaceholder.style.display = 'none';
            previewContainer.style.display = 'block';
            submitBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }
    
    // Clear image selection
    clearImageBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        fileInput.value = '';
        imagePreview.src = '#';
        previewContainer.style.display = 'none';
        uploadPlaceholder.style.display = 'flex';
        submitBtn.disabled = true;
        
        // Return results panel to initial state
        document.getElementById('results-dashboard').style.display = 'none';
        document.getElementById('empty-results-state').style.display = 'flex';
        document.getElementById('loading-state').style.display = 'none';
        document.getElementById('error-alert').style.display = 'none';
    });
    
    
    // =========================================
    // API SUBMISSION & RESULT RENDERING
    // =========================================
    const emptyState = document.getElementById('empty-results-state');
    const loadingState = document.getElementById('loading-state');
    const resultsDashboard = document.getElementById('results-dashboard');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    
    analyzeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        if (fileInput.files.length === 0) return;
        
        // UI transitions
        emptyState.style.display = 'none';
        errorAlert.style.display = 'none';
        resultsDashboard.style.display = 'none';
        loadingState.style.display = 'flex';
        
        // Prepare payload
        const formData = new FormData();
        formData.append('image', fileInput.files[0]);
        
        const selectedClass = document.querySelector('input[name="true_class"]:checked').value;
        formData.append('true_class', selectedClass);
        
        // Execute request
        fetch('/api/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || "Une erreur est survenue."); });
            }
            return response.json();
        })
        .then(data => {
            // Hide loading
            loadingState.style.display = 'none';
            
            // Render models results
            renderModelResult('baseline', data.baseline);
            renderModelResult('optimized', data.optimized);
            renderModelResult('resnet', data.resnet);
            renderModelResult('yolo', data.yolo);
            
            // Show dashboard
            resultsDashboard.style.display = 'grid';
        })
        .catch(err => {
            loadingState.style.display = 'none';
            errorMessage.textContent = err.message;
            errorAlert.style.display = 'flex';
            emptyState.style.display = 'flex';
        });
    });
    
    function renderModelResult(modelKey, result) {
        const card = document.getElementById(`card-${modelKey}`);
        const predText = document.getElementById(`${modelKey}-pred`);
        const confText = document.getElementById(`${modelKey}-conf`);
        const statusBadge = document.getElementById(`${modelKey}-status`);
        const img = document.getElementById(`${modelKey}-img`);
        const latencyText = document.getElementById(`${modelKey}-latency`);
        
        // 1. Text & latency values
        predText.textContent = result.label;
        confText.textContent = `${result.confidence.toFixed(1)}%`;
        latencyText.textContent = Math.round(result.time_ms);
        
        // 2. Image source
        img.src = `data:image/jpeg;base64,${result.image_b64}`;
        
        // 3. Handle error state & card border highlights
        if (result.is_error) {
            card.classList.add('card-error');
            statusBadge.className = 'result-status-badge badge-error';
            statusBadge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Erreur !';
        } else {
            card.classList.remove('card-error');
            statusBadge.className = 'result-status-badge badge-correct';
            statusBadge.innerHTML = '<i class="fa-solid fa-circle-check"></i> Correct';
        }
        
        // Special case: if YOLO doesn't detect anything
        if (modelKey === 'yolo' && result.label.includes('Aucun')) {
            if (result.is_error) {
                statusBadge.className = 'result-status-badge badge-error';
                statusBadge.innerHTML = '<i class="fa-solid fa-circle-minus"></i> Non détecté';
            } else {
                // If ground truth is none and yolo got none, then correct (though not likely in UI options)
                statusBadge.className = 'result-status-badge badge-neutral';
                statusBadge.innerHTML = '<i class="fa-solid fa-circle-minus"></i> Non détecté';
            }
        }
    }
});
