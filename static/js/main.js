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

// Push notification functionality
class PushNotificationManager {
    constructor() {
        this.subscription = null;
        this.isSupported = 'serviceWorker' in navigator && 'PushManager' in window;
        this.publicKey = null;
    }

    async initialize() {
        if (!this.isSupported) {
            console.log('Push notifications not supported');
            return false;
        }

        try {
            // Get VAPID public key from server
            const response = await fetch('/api/push/vapid-public-key');
            const data = await response.json();

            if (!data.public_key) {
                throw new Error('Failed to get VAPID public key');
            }

            this.publicKey = data.public_key;

            // Register service worker
            await this.registerServiceWorker();

            // Check existing subscription
            await this.checkExistingSubscription();

            return true;
        } catch (error) {
            console.error('Failed to initialize push notifications:', error);
            return false;
        }
    }

    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/static/js/service-worker.js');
                console.log('Service Worker registered successfully');
                return registration;
            } catch (error) {
                console.error('Service Worker registration failed:', error);
                return null;
            }
        }
        return null;
    }

    async checkExistingSubscription() {
        if ('serviceWorker' in navigator) {
            const registration = await navigator.serviceWorker.ready;
            this.subscription = await registration.pushManager.getSubscription();
            return this.subscription;
        }
        return null;
    }

    async subscribe() {
        if (!this.publicKey) {
            throw new Error('VAPID public key not available');
        }

        try {
            const registration = await navigator.serviceWorker.ready;

            // Convert VAPID key to Uint8Array
            const applicationServerKey = this.urlBase64ToUint8Array(this.publicKey);

            this.subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: applicationServerKey
            });

            // Send subscription to server
            const response = await fetch('/api/push/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.subscription.toJSON())
            });

            if (!response.ok) {
                throw new Error('Failed to register subscription with server');
            }

            console.log('Push notification subscription successful');
            return true;
        } catch (error) {
            console.error('Failed to subscribe to push notifications:', error);
            return false;
        }
    }

    async unsubscribe() {
        if (!this.subscription) {
            return true;
        }

        try {
            // Unsubscribe from service
            await this.subscription.unsubscribe();

            // Notify server
            const response = await fetch('/api/push/unsubscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    endpoint: this.subscription.endpoint
                })
            });

            if (!response.ok) {
                throw new Error('Failed to unregister subscription from server');
            }

            this.subscription = null;
            console.log('Unsubscribed from push notifications');
            return true;
        } catch (error) {
            console.error('Failed to unsubscribe from push notifications:', error);
            return false;
        }
    }

    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/-/g, '+')
            .replace(/_/g, '/');

        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);

        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }

        return outputArray;
    }

    async testNotification() {
        try {
            const response = await fetch('/api/push/test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                window.cikgu.showNotification('Test notification sent!', 'success');
            } else {
                window.cikgu.showNotification('Failed to send test notification', 'error');
            }
        } catch (error) {
            console.error('Failed to send test notification:', error);
            window.cikgu.showNotification('Failed to send test notification', 'error');
        }
    }
}

// Service Worker for push notifications
const serviceWorkerCode = `
self.addEventListener('push', function(event) {
    if (event.data) {
        const data = event.data.json();

        const options = {
            body: data.body || 'New notification',
            icon: '/static/img/icon-192x192.png',
            badge: '/static/img/badge-72x72.png',
            vibrate: [100, 50, 100],
            data: data.data || {}
        };

        event.waitUntil(
            self.registration.showNotification(data.title || 'Notification', options)
        );
    }
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();

    if (event.notification.data && event.notification.data.url) {
        event.waitUntil(
            clients.openWindow(event.notification.data.url)
        );
    }
});

self.addEventListener('notificationclose', function(event) {
    console.log('Notification was closed', event);
});

// Handle background sync for offline functionality
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

async function doBackgroundSync() {
    try {
        // Sync data with server when online
        const cache = await caches.open('cikgu-cache');
        const pendingRequests = await cache.match('/pending-requests');

        if (pendingRequests) {
            const requests = await pendingRequests.json();
            for (const request of requests) {
                try {
                    await fetch(request.url, request.options);
                } catch (error) {
                    console.error('Failed to sync request:', error);
                }
            }

            await cache.delete('/pending-requests');
        }
    } catch (error) {
        console.error('Background sync failed:', error);
    }
}
`;

// Create and register service worker
function createServiceWorker() {
    const blob = new Blob([serviceWorkerCode], { type: 'application/javascript' });
    const swUrl = URL.createObjectURL(blob);

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register(swUrl)
            .then(registration => {
                console.log('Service Worker registered with scope:', registration.scope);
                URL.revokeObjectURL(swUrl);
            })
            .catch(error => {
                console.error('Service Worker registration failed:', error);
                URL.revokeObjectURL(swUrl);
            });
    }
}

// Initialize push notifications when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize existing functionality
    initializeMobileMenu();
    initializeSmoothScrolling();
    initializeCardEffects();
    initializeSearch();
    initializeLoadingStates();

    // Initialize push notifications
    const pushManager = new PushNotificationManager();
    pushManager.initialize().then(success => {
        if (success) {
            // Add push notification toggle to UI
            addPushNotificationUI(pushManager);
        }
    });

    // Create service worker
    createServiceWorker();
});

function addPushNotificationUI(pushManager) {
    // Create push notification toggle button
    const pushToggle = document.createElement('button');
    pushToggle.className = 'btn btn-sm btn-outline-primary';
    pushToggle.innerHTML = '🔔 Enable Notifications';
    pushToggle.style.position = 'fixed';
    pushToggle.style.bottom = '20px';
    pushToggle.style.right = '20px';
    pushToggle.style.zIndex = '1000';

    let isSubscribed = false;

    pushToggle.addEventListener('click', async function() {
        if (!isSubscribed) {
            const success = await pushManager.subscribe();
            if (success) {
                pushToggle.innerHTML = '🔕 Disable Notifications';
                isSubscribed = true;
                window.cikgu.showNotification('Notifications enabled!', 'success');
            }
        } else {
            const success = await pushManager.unsubscribe();
            if (success) {
                pushToggle.innerHTML = '🔔 Enable Notifications';
                isSubscribed = false;
                window.cikgu.showNotification('Notifications disabled', 'info');
            }
        }
    });

    document.body.appendChild(pushToggle);
}

// Export functions for use in other scripts
window.cikgu = {
    showNotification,
    formatDate,
    updateProgress,
    pushManager: new PushNotificationManager()
};