// HTMX Utilities for Cikgu Learning Platform

// Utility functions for common HTMX operations
const htmxUtils = {
    // Show loading state
    showLoading: function(targetSelector) {
        const target = document.querySelector(targetSelector);
        if (target) {
            target.classList.add('htmx-loading');
            target.style.opacity = '0.5';
        }
    },

    // Hide loading state
    hideLoading: function(targetSelector) {
        const target = document.querySelector(targetSelector);
        if (target) {
            target.classList.remove('htmx-loading');
            target.style.opacity = '1';
        }
    },

    // Debounce function for search inputs
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Format file size
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Format date
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('ms-MY', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Show success message
    showSuccess: function(message) {
        showToast(message, 'success');
    },

    // Show error message
    showError: function(message) {
        showToast(message, 'error');
    },

    // Show info message
    showInfo: function(message) {
        showToast(message, 'info');
    },

    // Confirm action
    confirmAction: function(message, onConfirm) {
        showConfirm(message, onConfirm);
    },

    // Open modal with content
    openModal: function(content) {
        openModal(content);
    },

    // Close modal
    closeModal: function() {
        closeModal();
    },

    // Update progress bar
    updateProgress: function(percent) {
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = percent + '%';
        }
    },

    // Auto-resize textarea
    autoResizeTextarea: function(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    },

    // Copy to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            showToast('Failed to copy', 'error');
        });
    },

    // Validate form
    validateForm: function(form) {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('input-error');
                isValid = false;
            } else {
                input.classList.remove('input-error');
            }
        });

        return isValid;
    },

    // Clear form
    clearForm: function(form) {
        form.reset();
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.classList.remove('input-error');
        });
    },

    // Toggle theme
    toggleTheme: function() {
        const html = document.documentElement;
        const isDark = html.classList.contains('dark');

        if (isDark) {
            html.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        } else {
            html.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        }
    },

    // Initialize theme
    initTheme: function() {
        const theme = localStorage.getItem('theme') || 'light';
        const html = document.documentElement;

        if (theme === 'dark') {
            html.classList.add('dark');
        }
    },

    // Scroll to element
    scrollToElement: function(elementId, behavior = 'smooth') {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior: behavior });
        }
    },

    // Add to favorites
    addToFavorites: function(itemId, itemType) {
        htmx.ajax('POST', `/api/favorites/add`, {
            target: '#favorites-result',
            values: { item_id: itemId, item_type: itemType }
        });
    },

    // Remove from favorites
    removeFromFavorites: function(itemId) {
        htmx.ajax('POST', `/api/favorites/remove`, {
            target: '#favorites-result',
            values: { item_id: itemId }
        });
    },

    // Rate item
    rateItem: function(itemId, rating) {
        htmx.ajax('POST', `/api/rate`, {
            target: '#rating-result',
            values: { item_id: itemId, rating: rating }
        });
    },

    // Submit assessment
    submitAssessment: function(assessmentId, answers) {
        htmx.ajax('POST', `/api/assessments/${assessmentId}/submit`, {
            target: '#assessment-result',
            values: { answers: JSON.stringify(answers) }
        });
    },

    // Save draft
    saveDraft: function(content, contentType) {
        htmx.ajax('POST', `/api/drafts/save`, {
            target: '#draft-result',
            values: { content: content, content_type: contentType }
        });
    },

    // Load draft
    loadDraft: function(draftId) {
        htmx.ajax('GET', `/api/drafts/${draftId}`, {
            target: '#draft-content'
        });
    },

    // Search with filters
    searchWithFilters: function(query, filters = {}) {
        const formData = new FormData();
        formData.append('query', query);

        Object.keys(filters).forEach(key => {
            formData.append(key, filters[key]);
        });

        htmx.ajax('POST', `/api/search`, {
            target: '#search-results',
            values: formData
        });
    },

    // Sort table
    sortTable: function(column, direction) {
        htmx.ajax('GET', `/api/sort?column=${column}&direction=${direction}`, {
            target: '#table-content'
        });
    },

    // Export data
    exportData: function(format, filters = {}) {
        const formData = new FormData();
        formData.append('format', format);

        Object.keys(filters).forEach(key => {
            formData.append(key, filters[key]);
        });

        // For file downloads, we'll use a regular form submission
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/api/export';

        formData.forEach((value, key) => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = key;
            input.value = value;
            form.appendChild(input);
        });

        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    htmxUtils.initTheme();

    // Initialize auto-resize textareas
    document.querySelectorAll('textarea[data-auto-resize]').forEach(textarea => {
        htmxUtils.autoResizeTextarea(textarea);

        textarea.addEventListener('input', function() {
            htmxUtils.autoResizeTextarea(this);
        });
    });

    // Initialize form validation
    document.querySelectorAll('form[data-validate]').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!htmxUtils.validateForm(this)) {
                e.preventDefault();
                htmxUtils.showError('Please fill in all required fields');
            }
        });
    });

    // Initialize search debouncing
    document.querySelectorAll('input[data-search]').forEach(input => {
        const searchFunc = htmxUtils.debounce(function() {
            const query = input.value.trim();
            const target = input.getAttribute('data-target');

            if (query.length >= 2 || query.length === 0) {
                htmx.ajax('GET', `/api/search?q=${encodeURIComponent(query)}`, {
                    target: target
                });
            }
        }, 500);

        input.addEventListener('input', searchFunc);
    });
});

// Export for global use
window.htmxUtils = htmxUtils;