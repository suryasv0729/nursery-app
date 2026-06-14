// Global Variables
let currentUser = null;
let authToken = localStorage.getItem('token');

// Utility: Show Toast
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    const bgClass = type === 'success' ? 'bg-green-600' : (type === 'error' ? 'bg-red-600' : 'bg-blue-600');
    
    toast.className = `${bgClass} text-white px-6 py-3 rounded-lg shadow-lg flex items-center toast-appear`;
    toast.innerHTML = `
        <i class="fa-solid fa-${type === 'success' ? 'check-circle' : 'circle-exclamation'} mr-2"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.replace('toast-appear', 'toast-disappear');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Custom Fetch with Auth
async function apiCall(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    try {
        const res = await fetch(endpoint, { ...options, headers });
        const data = await res.json().catch(() => ({}));
        
        if (res.status === 401) {
            // Token expired or invalid
            logout();
        }
        return { ok: res.ok, status: res.status, data };
    } catch (e) {
        console.error('API Error:', e);
        return { ok: false, data: { message: 'Network error' } };
    }
}

// Authentication Logic
const authModal = document.getElementById('auth-modal');
const authModalContent = document.getElementById('auth-modal-content');
const tabLogin = document.getElementById('tab-login');
const tabRegister = document.getElementById('tab-register');
const formLogin = document.getElementById('login-form');
const formRegister = document.getElementById('register-form');

function openAuthModal() {
    if(authModal) {
        authModal.classList.remove('hidden');
        setTimeout(() => authModal.classList.add('show'), 10);
    }
}

function closeAuthModal() {
    if(authModal) {
        authModal.classList.remove('show');
        setTimeout(() => authModal.classList.add('hidden'), 300);
    }
}

function updateNavAuth() {
    const userBtn = document.getElementById('user-menu-btn');
    const dropdown = document.getElementById('user-dropdown');
    
    const userDataStr = localStorage.getItem('user');
    if (userDataStr && authToken) {
        currentUser = JSON.parse(userDataStr);
        let menuHtml = `
            <div class="px-4 py-2 border-b">
                <p class="text-sm font-medium text-gray-900 truncate">${currentUser.name}</p>
                <p class="text-xs text-gray-500 truncate">${currentUser.email}</p>
            </div>
            <a href="/orders" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"><i class="fa-solid fa-box mr-2"></i> Orders</a>
        `;
        if (currentUser.role === 'admin') {
            menuHtml += `<a href="/admin" class="block px-4 py-2 text-sm text-green-700 hover:bg-gray-100 font-medium"><i class="fa-solid fa-gauge mr-2"></i> Admin Panel</a>`;
        }
        menuHtml += `<a href="#" onclick="logout(); return false;" class="block px-4 py-2 text-sm text-red-600 hover:bg-gray-100"><i class="fa-solid fa-sign-out-alt mr-2"></i> Logout</a>`;
        
        if (dropdown) dropdown.innerHTML = menuHtml;
        
        if(userBtn) {
            userBtn.querySelector('button').innerHTML = `<div class="w-8 h-8 rounded-full bg-green-100 text-green-700 flex items-center justify-center font-bold text-sm border border-green-200">${currentUser.name.charAt(0).toUpperCase()}</div>`;
            userBtn.onclick = null;
            userBtn.classList.add('group');
        }
        updateCartCount();
    } else {
        if(userBtn) {
            userBtn.querySelector('button').innerHTML = `<i class="fa-regular fa-user text-xl"></i>`;
            userBtn.onclick = openAuthModal;
        }
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    authToken = null;
    currentUser = null;
    window.location.reload();
}

async function updateCartCount() {
    if(!authToken) return;
    const countEl = document.getElementById('cart-count');
    if(!countEl) return;
    
    const { ok, data } = await apiCall('/api/cart/');
    if(ok && Array.isArray(data)) {
        const total = data.reduce((acc, item) => acc + item.quantity, 0);
        countEl.textContent = total;
        countEl.classList.remove('opacity-0');
        if(total === 0) countEl.classList.add('opacity-0');
    }
}

// Chatbot Logic
const chatToggle = document.getElementById('chat-toggle');
const chatWindow = document.getElementById('chat-window');
const chatClose = document.getElementById('close-chat');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('send-chat');
const chatMessages = document.getElementById('chat-messages');

function appendMessage(text, isUser = false) {
    const div = document.createElement('div');
    div.className = `flex gap-2 ${isUser ? 'justify-end' : ''}`;
    
    const bubble = document.createElement('div');
    bubble.className = isUser 
        ? 'bg-blue-600 text-white p-3 rounded-lg rounded-tr-none max-w-[85%] break-words'
        : 'bg-green-100 text-green-900 p-3 rounded-lg rounded-tl-none max-w-[85%] break-words';
        
    if (isUser) {
        bubble.textContent = text;
    } else {
        bubble.innerHTML = text;
    }
    
    div.appendChild(bubble);
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function handleChat() {
    const text = chatInput.value.trim();
    if(!text) return;
    
    appendMessage(text, true);
    chatInput.value = '';
    chatSend.disabled = true;
    
    // Add typing indicator
    const typingId = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.id = typingId;
    div.className = `flex gap-2`;
    div.innerHTML = `<div class="bg-green-100 text-green-900 px-4 py-3 rounded-lg rounded-tl-none flex space-x-1 items-center">
                        <div class="w-2 h-2 bg-green-500 rounded-full animate-bounce"></div>
                        <div class="w-2 h-2 bg-green-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                        <div class="w-2 h-2 bg-green-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                     </div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        const { ok, data } = await apiCall('/api/chat/', {
            method: 'POST',
            body: JSON.stringify({ message: text })
        });
        
        document.getElementById(typingId)?.remove();
        
        if (ok && data.reply) {
            appendMessage(data.reply, false);
        } else {
            appendMessage("I'm having trouble connecting to my plant database.", false);
        }
    } catch (e) {
        document.getElementById(typingId)?.remove();
        appendMessage("An error occurred connecting to the service.", false);
    }
    chatSend.disabled = false;
    chatInput.focus();
}

// Initialization and Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    updateNavAuth();
    
    // Auth Modal Tabs & Links
    const formForgot = document.getElementById('forgot-form');
    const showForgotBtn = document.getElementById('show-forgot-btn');
    const backToLoginBtn = document.getElementById('back-to-login-btn');

    if(tabLogin && tabRegister) {
        tabLogin.onclick = () => {
            tabLogin.classList.replace('text-gray-500', 'text-green-600');
            tabLogin.classList.add('border-b-2', 'border-green-600', 'bg-green-50');
            tabRegister.classList.replace('text-green-600', 'text-gray-500');
            tabRegister.classList.remove('border-b-2', 'border-green-600', 'bg-green-50');
            formLogin.classList.remove('hidden');
            formRegister.classList.add('hidden');
            if(formForgot) formForgot.classList.add('hidden');
        };
        tabRegister.onclick = () => {
            tabRegister.classList.replace('text-gray-500', 'text-green-600');
            tabRegister.classList.add('border-b-2', 'border-green-600', 'bg-green-50');
            tabLogin.classList.replace('text-green-600', 'text-gray-500');
            tabLogin.classList.remove('border-b-2', 'border-green-600', 'bg-green-50');
            formRegister.classList.remove('hidden');
            formLogin.classList.add('hidden');
            if(formForgot) formForgot.classList.add('hidden');
        };
    }
    
    if(showForgotBtn) {
        showForgotBtn.onclick = () => {
            formLogin.classList.add('hidden');
            formRegister.classList.add('hidden');
            formForgot.classList.remove('hidden');
        };
    }
    if(backToLoginBtn) backToLoginBtn.onclick = () => tabLogin.click();
    
    const closeBtn = document.getElementById('close-modal');
    if(closeBtn) closeBtn.onclick = closeAuthModal;
    
    // Handle Login
    if(formLogin) {
        formLogin.onsubmit = async (e) => {
            e.preventDefault();
            const btn = document.getElementById('login-btn');
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
            btn.disabled = true;
            
            const req = {
                email: document.getElementById('login-email').value,
                password: document.getElementById('login-password').value
            };
            
            const { ok, data } = await apiCall('/api/auth/login', {
                method: 'POST', body: JSON.stringify(req)
            });
            
            if(ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                authToken = data.token;
                showToast('Login successful!');
                
                if (data.user && data.user.role === 'admin') {
                    window.location.href = '/admin';
                } else {
                    closeAuthModal();
                    updateNavAuth();
                    window.location.reload();
                }
            } else {
                showToast(data.message || 'Login failed', 'error');
            }
            btn.innerHTML = 'Sign In';
            btn.disabled = false;
        };
    }
    
    // Handle Forgot Password
    if(formForgot) {
        formForgot.onsubmit = async (e) => {
            e.preventDefault();
            const btn = document.getElementById('forgot-btn');
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
            btn.disabled = true;
            
            const { ok, data } = await apiCall('/api/auth/forgot-password', {
                method: 'POST', body: JSON.stringify({ email: document.getElementById('forgot-email').value })
            });
            
            if(ok) {
                showToast(data.message);
                tabLogin.click();
            } else {
                showToast(data.message || 'Failed', 'error');
            }
            btn.innerHTML = 'Send Reset Link';
            btn.disabled = false;
        };
    }
    
    // Handle Register
    if(formRegister) {
        formRegister.onsubmit = async (e) => {
            e.preventDefault();
            const btn = document.getElementById('reg-btn');
            
            const regName = document.getElementById('reg-name').value;
            const regEmail = document.getElementById('reg-email').value;
            const regPassword = document.getElementById('reg-password').value;
            const regConfirm = document.getElementById('reg-confirm-password').value;
            
            if(regPassword !== regConfirm) {
                showToast('Passwords do not match!', 'error');
                return;
            }
            
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
            btn.disabled = true;
            
            const req = { name: regName, email: regEmail, password: regPassword };
            
            const { ok, data } = await apiCall('/api/auth/register', {
                method: 'POST', body: JSON.stringify(req)
            });
            
            if(ok) {
                showToast('Registration successful! Please login.');
                tabLogin.click(); // Switch to login tab
            } else {
                showToast(data.message || 'Registration failed', 'error');
            }
            btn.innerHTML = 'Create Account';
            btn.disabled = false;
        };
    }

    // Chatbot UI Toggle
    if(chatToggle && chatWindow && chatClose) {
        chatToggle.onclick = () => {
            chatWindow.classList.toggle('hidden');
            if(!chatWindow.classList.contains('hidden')) {
                setTimeout(() => chatWindow.classList.add('show'), 10);
                chatInput.focus();
            } else {
                chatWindow.classList.remove('show');
            }
        };
        chatClose.onclick = () => {
            chatWindow.classList.remove('show');
            setTimeout(() => chatWindow.classList.add('hidden'), 300);
        };
        chatSend.onclick = handleChat;
        chatInput.onkeypress = (e) => { if(e.key === 'Enter') handleChat(); };
    }
    
    // Auth Dropdown toggle for mobile/click
    const userMenuBtn = document.getElementById('user-menu-btn');
    const userDropdown = document.getElementById('user-dropdown');
    if(userMenuBtn && userDropdown) {
        // Handled basically by CSS group-hover, but optionally we can do JS clicks.
    }
});

// Exposed Functions for HTML buttons
window.addToCart = async function(productId, quantity=1) {
    if(!authToken) {
        openAuthModal();
        showToast('Please login to continue', 'info');
        return;
    }
    const {ok, data} = await apiCall('/api/cart/add', {
        method: 'POST', 
        body: JSON.stringify({ product_id: productId, quantity })
    });
    if(ok) {
        showToast('Added to cart!');
        updateCartCount();
    } else {
        showToast(data.message || 'Failed', 'error');
    }
};

window.toggleWishlist = async function(productId, element) {
    if(!authToken) {
        openAuthModal();
        return;
    }
    const {ok, data} = await apiCall('/api/cart/wishlist/toggle', {
        method: 'POST',
        body: JSON.stringify({ product_id: productId })
    });
    
    if(ok) {
        showToast(data.message);
        if(element) {
            const icon = element.querySelector('i');
            if(data.is_wishlisted) {
                icon.classList.remove('fa-regular');
                icon.classList.add('fa-solid', 'text-red-500');
            } else {
                icon.classList.add('fa-regular');
                icon.classList.remove('fa-solid', 'text-red-500');
            }
        }
    }
};

window.requireAuthLink = function(e) {
    if(!authToken) {
        if (e) e.preventDefault();
        openAuthModal();
        showToast('Please sign in to access this page!', 'info');
        return false;
    }
    return true;
};
