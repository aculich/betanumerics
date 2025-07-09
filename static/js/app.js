// Global variables
let recentIdentifiers = [];

// Copy to clipboard function
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent || element.innerText;
    
    navigator.clipboard.writeText(text).then(() => {
        // Show a brief success message
        const button = element.nextElementSibling;
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('text-green-600');
        
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('text-green-600');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    });
}

// Show result section
function showResult(identifier, url, isEasterEgg = false) {
    const resultDiv = document.getElementById('result');
    const easterEggDiv = document.getElementById('easterEgg');
    
    if (isEasterEgg) {
        resultDiv.classList.add('hidden');
        easterEggDiv.classList.remove('hidden');
        createSlugAnimation();
    } else {
        easterEggDiv.classList.add('hidden');
        resultDiv.classList.remove('hidden');
        
        document.getElementById('identifier').textContent = identifier;
        document.getElementById('url').textContent = url;
        
        // Add to recent identifiers
        addToRecentIdentifiers(identifier, url);
    }
}

// Add identifier to recent list
function addToRecentIdentifiers(identifier, url) {
    const recent = {
        identifier: identifier,
        url: url,
        timestamp: new Date().toLocaleTimeString()
    };
    
    recentIdentifiers.unshift(recent);
    
    // Keep only last 5
    if (recentIdentifiers.length > 5) {
        recentIdentifiers = recentIdentifiers.slice(0, 5);
    }
    
    updateRecentIdentifiersDisplay();
}

// Update the recent identifiers display
function updateRecentIdentifiersDisplay() {
    const recentDiv = document.getElementById('recentIdentifiers');
    const recentList = document.getElementById('recentList');
    
    if (recentIdentifiers.length === 0) {
        recentDiv.classList.add('hidden');
        return;
    }
    
    recentDiv.classList.remove('hidden');
    recentList.innerHTML = '';
    
    recentIdentifiers.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'flex items-center justify-between p-3 bg-gray-50 rounded';
        itemDiv.innerHTML = `
            <div class="flex items-center space-x-3">
                <code class="font-mono text-sm">${item.identifier}</code>
                <span class="text-xs text-gray-500">${item.timestamp}</span>
            </div>
            <button 
                onclick="copyToClipboard('recent-url-${item.identifier}')"
                class="text-blue-600 hover:text-blue-800 text-sm"
            >
                Copy URL
            </button>
        `;
        
        // Add hidden element for copying
        const hiddenUrl = document.createElement('div');
        hiddenUrl.id = `recent-url-${item.identifier}`;
        hiddenUrl.className = 'hidden';
        hiddenUrl.textContent = item.url;
        document.body.appendChild(hiddenUrl);
        
        recentList.appendChild(itemDiv);
    });
}

// Show loading state
function showLoading() {
    const button = document.getElementById('generateBtn');
    button.disabled = true;
    button.textContent = 'Generating...';
    button.classList.add('opacity-50');
}

// Hide loading state
function hideLoading() {
    const button = document.getElementById('generateBtn');
    button.disabled = false;
    button.textContent = 'Generate Identifier';
    button.classList.remove('opacity-50');
}

// Show error message
function showError(message) {
    // Create error alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4';
    alertDiv.innerHTML = `
        <strong class="font-bold">Error!</strong>
        <span class="block sm:inline">${message}</span>
        <button onclick="this.parentElement.remove()" class="float-right text-red-700 hover:text-red-900">
            ×
        </button>
    `;
    
    const form = document.getElementById('generateForm');
    form.parentNode.insertBefore(alertDiv, form);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Form submission handler
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('generateForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value.trim();
        
        if (!email) {
            showError('Please enter an email address');
            return;
        }
        
        showLoading();
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showResult(data.identifier, data.url, data.easter_egg);
            } else {
                showError(data.error || 'An error occurred while generating the identifier');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please try again.');
        } finally {
            hideLoading();
        }
    });
}); 