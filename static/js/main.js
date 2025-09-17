// Cikgu SPM Online Learning Platform - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile menu toggle
    initializeMobileMenu();

    // Initialize smooth scrolling
    initializeSmoothScrolling();

    // Initialize card hover effects
    initializeCardEffects();

    // Initialize search functionality
    initializeSearch();

    // Initialize loading states
    initializeLoadingStates();
});

// Mobile menu functionality
function initializeMobileMenu() {
    const mobileMenuButton = document.querySelector('[data-mobile-menu-toggle]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Card hover effects
function initializeCardEffects() {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('[data-search]');
    const searchResults = document.querySelector('[data-search-results]');

    if (searchInput && searchResults) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();

            if (query.length > 2) {
                // Simulate search - in real app, this would be an API call
                performSearch(query);
            } else {
                searchResults.innerHTML = '';
                searchResults.classList.add('hidden');
            }
        });
    }
}

function performSearch(query) {
    const searchResults = document.querySelector('[data-search-results]');
    const mockResults = [
        { title: 'Bahasa Melayu - KOMSAS', url: '/subjects/bahasa-melayu' },
        { title: 'Matematik - Algebra', url: '/subjects/matematik' },
        { title: 'Sains - Biologi', url: '/subjects/sains' },
        { title: 'English - Grammar', url: '/subjects/english' }
    ];

    const filteredResults = mockResults.filter(result =>
        result.title.toLowerCase().includes(query)
    );

    if (filteredResults.length > 0) {
        searchResults.innerHTML = filteredResults.map(result => `
            <a href="${result.url}" class="block p-2 hover:bg-base-200 rounded">
                ${result.title}
            </a>
        `).join('');
        searchResults.classList.remove('hidden');
    } else {
        searchResults.innerHTML = '<p class="p-2 text-gray-500">No results found</p>';
        searchResults.classList.remove('hidden');
    }
}

// Loading states
function initializeLoadingStates() {
    const buttons = document.querySelectorAll('[data-loading]');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.disabled = true;
            this.innerHTML = '<span class="loading"></span> Loading...';

            // Simulate loading - in real app, this would be based on API response
            setTimeout(() => {
                this.disabled = false;
                this.innerHTML = this.getAttribute('data-original-text') || 'Click';
            }, 2000);
        });

        // Store original text
        button.setAttribute('data-original-text', button.textContent);
    });
}

// Progress tracking
function updateProgress(subjectId, progress) {
    const progressBar = document.querySelector(`[data-progress="${subjectId}"]`);

    if (progressBar) {
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
    }
}

// Theme switcher (for future implementation)
function initializeThemeSwitcher() {
    const themeToggle = document.querySelector('[data-theme-toggle]');

    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
}

// Load saved theme
function loadSavedTheme() {
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('ms-MY', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Export functions for use in other scripts
window.cikgu = {
    showNotification,
    formatDate,
    updateProgress
};