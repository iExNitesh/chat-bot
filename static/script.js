// API endpoint
const API_BASE_URL = window.location.origin;

// DOM elements
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const emotionIndicator = document.getElementById('emotionIndicator');
const emotionText = document.getElementById('emotionText');
const statusIndicator = document.getElementById('statusIndicator');
const welcomeTime = document.getElementById('welcomeTime');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set welcome message time
    welcomeTime.textContent = getCurrentTime();
    
    // Focus input on load
    userInput.focus();
    
    // Check API health
    checkHealth();
});

// Check API health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        if (response.ok) {
            updateStatus('online');
        } else {
            updateStatus('offline');
        }
    } catch (error) {
        updateStatus('offline');
        console.error('Health check failed:', error);
    }
}

function updateStatus(status) {
    const statusDot = statusIndicator.querySelector('.status-dot');
    const statusTextElement = statusIndicator.querySelector('.status-text');
    
    if (status === 'online') {
        statusDot.style.background = '#10b981';
        statusTextElement.textContent = 'Online';
    } else {
        statusDot.style.background = '#ef4444';
        statusTextElement.textContent = 'Offline';
    }
}

// Get current time
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
    });
}

// Send message
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Disable input and button
    userInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    userInput.value = '';
    
    // Hide emotion indicator
    emotionIndicator.style.display = 'none';
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add bot response
        addMessage(data.response, 'bot');
        
        // Show emotion if detected
        if (data.emotion && data.emotion !== 'neutral') {
            showEmotion(data.emotion);
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        removeTypingIndicator(typingId);
        addMessage('Sorry, I encountered an error. Please try again.', 'bot', true);
    } finally {
        // Re-enable input and button
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

function addMessage(text, sender, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    if (isError) {
        messageDiv.innerHTML = `
            <div class="message-content error-message">
                <p>${text}</p>
            </div>
        `;
    } else {
        const avatar = sender === 'user' ? '👤' : '🤖';
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <p>${escapeHtml(text)}</p>
                <span class="message-time">${getCurrentTime()}</span>
            </div>
        `;
    }
    
    // Remove welcome message if it exists
    const welcomeMessage = chatContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showTypingIndicator() {
    const typingId = `typing-${Date.now()}`;
    const typingDiv = document.createElement('div');
    typingDiv.id = typingId;
    typingDiv.className = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="typing-dots">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    
    chatContainer.appendChild(typingDiv);
    scrollToBottom();
    return typingId;
}

function removeTypingIndicator(typingId) {
    const typingElement = document.getElementById(typingId);
    if (typingElement) {
        typingElement.remove();
    }
}

function showEmotion(emotion) {
    emotionText.textContent = `Detected emotion: ${emotion}`;
    emotionIndicator.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        emotionIndicator.style.display = 'none';
    }, 5000);
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

