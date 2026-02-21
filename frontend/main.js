// ========================================
// API CONFIGURATION
// ========================================
const API_BASE_URL = 'http://127.0.0.1:8000';

// ========================================
// DOM ELEMENTS
// ========================================
let elements = {};

function setupElements() {
    elements = {
        // Forms
        loginForm: document.getElementById('loginForm'),
        signupForm: document.getElementById('signupForm'),
        dashboardView: document.getElementById('dashboardView'),

        // Form Elements
        loginFormElement: document.getElementById('loginFormElement'),
        signupFormElement: document.getElementById('signupFormElement'),

        // Toggle Links
        showSignup: document.getElementById('showSignup'),
        showLogin: document.getElementById('showLogin'),

        // Address Toggle
        addressToggle: document.getElementById('addressToggle'),
        addressFields: document.getElementById('addressFields'),

        // Logout
        logoutBtn: document.getElementById('logoutBtn'),

        // Forget/Reset Password Elements
        forgetPasswordForm: document.getElementById('forgetPasswordForm'),
        resetPasswordForm: document.getElementById('resetPasswordForm'),

        // Forget/Reset Inputs
        forgetPasswordFormElement: document.getElementById('forgetPasswordFormElement'),
        resetPasswordFormElement: document.getElementById('resetPasswordFormElement'),

        // Links
        showForgetPassword: document.getElementById('showForgetPassword'),
        backToLoginFromForget: document.getElementById('backToLoginFromForget'),
        backToLoginFromReset: document.getElementById('backToLoginFromReset'),

        // Toast
        toast: document.getElementById('toast'),

        // Authenticated Change Password
        changePasswordBtn: document.getElementById('changePasswordBtn'),
        changePasswordForm: document.getElementById('changePasswordForm'),
        changePasswordFormElement: document.getElementById('changePasswordFormElement'),
        cancelChangePassword: document.getElementById('cancelChangePassword'),

        // Orders
        ordersView: document.getElementById('ordersView'),
        createOrderForm: document.getElementById('createOrderForm'),
        ordersList: document.getElementById('ordersList'),

        // Order Buttons/Forms
        btnMyOrders: document.getElementById('btnMyOrders'),
        btnCreateOrderView: document.getElementById('btnCreateOrderView'),
        btnBackToDashboard: document.getElementById('btnBackToDashboard'),
        createOrderFormElement: document.getElementById('createOrderFormElement'),
        cancelCreateOrder: document.getElementById('cancelCreateOrder'),
    };

    // Log to confirm elements are found
    console.log('DOM Elements initialized:', {
        loginForm: !!elements.loginForm,
        resetForm: !!elements.resetPasswordForm,
        dashboard: !!elements.dashboardView
    });
}

// ========================================
// STATE MANAGEMENT
// ========================================
let currentUser = null;
let authToken = null;
let resetFlowEmail = null; // Store email for reset flow
let currentEditingOrderId = null; // Track order being edited

// Check for existing session
function checkSession() {
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('authToken');

    if (storedUser && storedToken) {
        currentUser = JSON.parse(storedUser);
        authToken = storedToken;
        showDashboard(currentUser);
    }
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

// Show toast notification
function showToast(message, type = 'success') {
    elements.toast.textContent = message;
    elements.toast.className = `toast ${type}`;
    elements.toast.classList.add('show');

    setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 4000);
}

// Toggle loading state on button
function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// ========================================
// API FUNCTIONS
// ========================================

// Login API
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const error = await response.json();
            const errorMessage = typeof error.detail === 'string'
                ? error.detail
                : JSON.stringify(error.detail);
            throw new Error(errorMessage || 'Login failed');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// Signup API
async function signupUser(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        if (!response.ok) {
            const error = await response.json();
            const errorMessage = typeof error.detail === 'string'
                ? error.detail
                : JSON.stringify(error.detail);
            throw new Error(errorMessage || 'Signup failed');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Signup error:', error);
        throw error;
    }
}

// Forget Password API (Request OTP)
async function requestOtp(email) {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/forget-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email }),
        });

        if (!response.ok) {
            const error = await response.json();
            const errorMessage = typeof error.detail === 'string'
                ? error.detail
                : JSON.stringify(error.detail);
            throw new Error(errorMessage || 'Failed to send OTP');
        }
        return await response.json();
    } catch (error) {
        console.error('Forgot Password error:', error);
        throw error;
    }
}

// Reset Password API (Verify OTP & Reset)
async function resetPasswordApi(data) {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/reset-password-otp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const error = await response.json();
            const errorMessage = typeof error.detail === 'string'
                ? error.detail
                : JSON.stringify(error.detail);
            throw new Error(errorMessage || 'Password reset failed');
        }
        return await response.json();
    } catch (error) {
        console.error('Reset Password error:', error);
        throw error;
    }
}

// Authenticated Change Password API
async function changePasswordApi(oldPassword, newPassword) {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/reset_password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: newPassword
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            const errorMessage = typeof error.detail === 'string'
                ? error.detail
                : JSON.stringify(error.detail);
            throw new Error(errorMessage || 'Password update failed');
        }
        return await response.json();
    } catch (error) {
        console.error('Change Password error:', error);
        throw error;
    }
}

// Fetch Orders API
async function fetchOrdersApi() {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/orders`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) throw new Error('Failed to fetch orders');
        return await response.json();
    } catch (error) {
        console.error('Fetch Orders error:', error);
        throw error;
    }
}

// Create Order API
async function createOrderApi(orderData) {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(orderData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create order');
        }
        return await response.json();
    } catch (error) {
        console.error('Create Order error:', error);
        throw error;
    }
}

// Delete Order API
async function deleteOrderApi(orderId) {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/orders/${orderId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete order');
        }
        return await response.json();
    } catch (error) {
        console.error('Delete Order error:', error);
        throw error;
    }
}

// Update Order API
async function updateOrderApi(orderId, orderData) {
    try {
        const response = await fetch(`${API_BASE_URL}/v1/orders/${orderId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(orderData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to update order');
        }
        return await response.json();
    } catch (error) {
        console.error('Update Order error:', error);
        throw error;
    }
}


// ========================================
// VIEW MANAGEMENT
// ========================================

// Show login form
function showLoginForm() {
    elements.loginForm.style.display = 'block';
    elements.signupForm.style.display = 'none';
    elements.forgetPasswordForm.style.display = 'none';
    elements.resetPasswordForm.style.display = 'none';
    elements.changePasswordForm.style.display = 'none';
    elements.dashboardView.style.display = 'none';
}

// Show signup form
function showSignupForm() {
    elements.loginForm.style.display = 'none';
    elements.signupForm.style.display = 'block';
    elements.forgetPasswordForm.style.display = 'none';
    elements.resetPasswordForm.style.display = 'none';
    elements.changePasswordForm.style.display = 'none';
    elements.dashboardView.style.display = 'none';
}

// Show forget password form
function showForgetPasswordForm() {
    elements.loginForm.style.display = 'none';
    elements.signupForm.style.display = 'none';
    elements.forgetPasswordForm.style.display = 'block';
    elements.resetPasswordForm.style.display = 'none';
    elements.changePasswordForm.style.display = 'none';
    elements.dashboardView.style.display = 'none';
}

// Show reset password form
function showResetPasswordForm() {
    elements.loginForm.style.display = 'none';
    elements.signupForm.style.display = 'none';
    elements.forgetPasswordForm.style.display = 'none';
    elements.resetPasswordForm.style.display = 'block';
    elements.changePasswordForm.style.display = 'none';
    elements.dashboardView.style.display = 'none';
}

// Show authenticated change password form
function showChangePasswordForm() {
    elements.loginForm.style.display = 'none';
    elements.signupForm.style.display = 'none';
    elements.forgetPasswordForm.style.display = 'none';
    elements.resetPasswordForm.style.display = 'none';
    elements.dashboardView.style.display = 'none';
    elements.dashboardView.style.display = 'none';
    elements.changePasswordForm.style.display = 'block';
    elements.ordersView.style.display = 'none';
    elements.createOrderForm.style.display = 'none';
}

function showOrdersView() {
    elements.loginForm.style.display = 'none';
    elements.signupForm.style.display = 'none';
    elements.dashboardView.style.display = 'none';
    elements.ordersView.style.display = 'block';
    elements.createOrderForm.style.display = 'none';

    loadOrders();
}

function showCreateOrderForm(editOrder = null) {
    elements.ordersView.style.display = 'none';
    elements.createOrderForm.style.display = 'block';

    // Reset or Prefill
    if (editOrder) {
        currentEditingOrderId = editOrder.id;
        document.querySelector('#createOrderForm h2').textContent = 'Edit Order';
        document.querySelector('#createOrderForm .btn-text').textContent = 'Update Order';

        // Fill fields
        const firstItem = (editOrder.order_items && editOrder.order_items.length > 0) ? editOrder.order_items[0] : {};
        document.getElementById('productName').value = firstItem.name || '';
        document.getElementById('orderPrice').value = editOrder.order_price;
        document.getElementById('orderQuantity').value = editOrder.order_quantity;

        if (editOrder.address) {
            document.getElementById('orderStreet').value = editOrder.address.street_address;
            document.getElementById('orderCity').value = editOrder.address.city;
            document.getElementById('orderState').value = editOrder.address.state;
            document.getElementById('orderPostalCode').value = editOrder.address.postal_code;
            document.getElementById('orderCountry').value = editOrder.address.country;
        }
    } else {
        currentEditingOrderId = null;
        document.querySelector('#createOrderForm h2').textContent = 'New Order';
        document.querySelector('#createOrderForm .btn-text').textContent = 'Place Order';
        elements.createOrderFormElement.reset();
    }
}

async function loadOrders() {
    elements.ordersList.innerHTML = '<div class="empty-state">Loading...</div>';
    try {
        const data = await fetchOrdersApi();
        const orders = data.orders || [];

        // Store orders in a global look-up optional or just attach to DOM?
        // simple way: just use data attributes
        window.userOrders = orders;

        if (orders.length === 0) {
            elements.ordersList.innerHTML = '<div class="empty-state">No orders found. Create one!</div>';
            return;
        }

        elements.ordersList.innerHTML = orders.map(order => {
            const itemsHtml = (order.order_items || []).map(item => `
                <div style="font-size: 0.85em; margin-top: 2px; padding-left: 10px; color: #aaa;">
                    • ${item.name || 'Item'} x${item.quantity} - $${item.price}
                </div>
            `).join('');

            return `
            <div class="info-card" style="margin-bottom: 10px; padding: 15px; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; position: relative;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <strong style="color:white;">${order.order_number}</strong>
                    <div>
                        <span class="status-badge">${order.order_status}</span>
                        <div style="display:inline-block; margin-left: 10px;">
                            <button onclick="handleEditOrder('${order.id}')" style="background:none; border:none; cursor:pointer; font-size:1.2em;" title="Edit">✏️</button>
                            <button onclick="handleDeleteOrder('${order.id}')" style="background:none; border:none; cursor:pointer; font-size:1.2em;" title="Delete">🗑️</button>
                        </div>
                    </div>
                </div>
                <div style="color: var(--text-secondary); font-size: 0.9em;">
                    <div style="margin-bottom: 5px;">Items: ${order.order_quantity} | Total: $${order.total_amount}</div>
                    <div style="background: rgba(0,0,0,0.2); padding: 5px; border-radius: 4px; margin-bottom: 5px;">
                        ${itemsHtml || 'No items listed'}
                    </div>
                    <div>${new Date(order.created_at).toLocaleDateString()}</div>
                </div>
            </div>
            `;
        }).join('');

    } catch (error) {
        elements.ordersList.innerHTML = `<div class="empty-state" style="color:var(--error)">Failed to load orders</div>`;
    }
}

// Show dashboard
function showDashboard(userData) {
    elements.loginForm.style.display = 'none';
    elements.signupForm.style.display = 'none';
    elements.forgetPasswordForm.style.display = 'none';
    elements.resetPasswordForm.style.display = 'none';
    elements.changePasswordForm.style.display = 'none';
    elements.dashboardView.style.display = 'block';
    elements.ordersView.style.display = 'none';
    elements.createOrderForm.style.display = 'none';

    // Populate user info
    document.getElementById('userName').textContent =
        `${userData.user.first_name} ${userData.user.last_name}`;
    document.getElementById('userEmail').textContent = userData.user.email;
    document.getElementById('userMobile').textContent = userData.user.mobile_number;
    document.getElementById('userStatus').textContent = userData.user.status;
    document.getElementById('userCreated').textContent = formatDate(userData.user.created_at);

    // Show address if available
    if (userData.user.address) {
        const addressSection = document.getElementById('userAddressSection');
        const addressText = `${userData.user.address.street_address}, ${userData.user.address.city}, ${userData.user.address.state} ${userData.user.address.postal_code}, ${userData.user.address.country}`;
        document.getElementById('userAddress').textContent = addressText;
        addressSection.style.display = 'block';
    }
}

// ========================================
// EVENT HANDLERS
// ========================================

// ========================================
// INITIALIZATION
// ========================================

function setupEventListeners() {
    // Login form submission
    elements.loginFormElement.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = e.target.querySelector('button[type="submit"]');
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;

        setButtonLoading(submitBtn, true);

        try {
            const response = await loginUser(email, password);

            // Store user data and token
            currentUser = response;
            authToken = response.access_token;
            localStorage.setItem('user', JSON.stringify(response));
            localStorage.setItem('authToken', response.access_token);

            // Show success message
            showToast('Login successful! Welcome back.', 'success');

            // Show dashboard
            setTimeout(() => {
                showDashboard(response);
            }, 500);

        } catch (error) {
            showToast(error.message || 'Login failed. Please try again.', 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });

    // Signup form submission
    elements.signupFormElement.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = e.target.querySelector('button[type="submit"]');

        // Collect form data
        const userData = {
            first_name: document.getElementById('signupFirstName').value,
            last_name: document.getElementById('signupLastName').value,
            email: document.getElementById('signupEmail').value,
            mobile_number: document.getElementById('signupMobile').value,
            password: document.getElementById('signupPassword').value,
        };

        // Add address if fields are filled
        const streetAddress = document.getElementById('streetAddress').value;
        const city = document.getElementById('city').value;
        const state = document.getElementById('state').value;
        const postalCode = document.getElementById('postalCode').value;
        const country = document.getElementById('country').value;

        if (streetAddress && city && state && postalCode && country) {
            userData.address = {
                street_address: streetAddress,
                city: city,
                state: state,
                postal_code: postalCode,
                country: country,
            };
        }

        setButtonLoading(submitBtn, true);

        try {
            const response = await signupUser(userData);

            // Show success message
            showToast('Account created! Please login now.', 'success');

            // Redirect to login page
            setTimeout(() => {
                showLoginForm();
            }, 1500);

        } catch (error) {
            showToast(error.message || 'Signup failed. Please try again.', 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });

    // Forget Password Submission (Send OTP)
    elements.forgetPasswordFormElement.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const email = document.getElementById('forgetEmail').value.trim();

        setButtonLoading(submitBtn, true);

        try {
            await requestOtp(email);
            resetFlowEmail = email; // Store email for next step
            showToast('OTP sent successfully! Check your email.', 'success');

            setTimeout(() => {
                showResetPasswordForm();
            }, 1000);

        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });

    // Reset Password Submission
    elements.resetPasswordFormElement.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const otp = document.getElementById('resetOtp').value.trim();
        const newPassword = document.getElementById('newPassword').value;
        const confirmNewPassword = document.getElementById('confirmNewPassword').value;

        if (newPassword !== confirmNewPassword) {
            showToast("Passwords do not match", "error");
            return;
        }

        setButtonLoading(submitBtn, true);

        try {
            const resetData = {
                email: resetFlowEmail,
                otp: otp,
                new_password: newPassword,
                confirm_password: confirmNewPassword
            };

            await resetPasswordApi(resetData);
            showToast('Password reset successfully! Please login.', 'success');

            setTimeout(() => {
                showLoginForm();
            }, 1000);

        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });

    // Authenticated Change Password
    elements.changePasswordBtn.addEventListener('click', () => {
        showChangePasswordForm();
    });

    elements.cancelChangePassword.addEventListener('click', (e) => {
        e.preventDefault();
        showDashboard(currentUser);
    });

    elements.changePasswordFormElement.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const oldPassword = document.getElementById('oldPassword').value;
        const newPassword = document.getElementById('changeNewPassword').value;
        const confirmPassword = document.getElementById('changeConfirmPassword').value;

        if (newPassword !== confirmPassword) {
            showToast("New passwords do not match", "error");
            return;
        }

        setButtonLoading(submitBtn, true);

        try {
            await changePasswordApi(oldPassword, newPassword);
            showToast('Password updated successfully! Please login again.', 'success');

            // Logout user to force re-login with new credentials
            setTimeout(() => {
                elements.logoutBtn.click();
            }, 1500);

        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });

    // Orders Navigation
    elements.btnMyOrders.addEventListener('click', () => {
        showOrdersView();
    });

    elements.btnBackToDashboard.addEventListener('click', () => {
        showDashboard(currentUser);
    });

    elements.btnCreateOrderView.addEventListener('click', () => {
        showCreateOrderForm();
    });

    elements.cancelCreateOrder.addEventListener('click', (e) => {
        e.preventDefault();
        showOrdersView();
    });

    // Create/Update Order Submission
    elements.createOrderFormElement.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = e.target.querySelector('button[type="submit"]');
        setButtonLoading(submitBtn, true);

        try {
            const productName = document.getElementById('productName').value;
            const price = parseFloat(document.getElementById('orderPrice').value);
            const qty = parseInt(document.getElementById('orderQuantity').value);

            const orderData = {
                order_price: price,
                order_quantity: qty,
                total_amount: price * qty,
                order_items: [{ name: productName, price: price, quantity: qty }],
                address: {
                    street_address: document.getElementById('orderStreet').value,
                    city: document.getElementById('orderCity').value,
                    state: document.getElementById('orderState').value,
                    postal_code: document.getElementById('orderPostalCode').value,
                    country: document.getElementById('orderCountry').value
                }
            };

            if (currentEditingOrderId) {
                // UPDATE Mode
                // Must include order_number because Backend Schema requires it
                const existingOrder = window.userOrders.find(o => o.id === currentEditingOrderId);
                if (existingOrder) {
                    orderData.order_number = existingOrder.order_number;
                }
                await updateOrderApi(currentEditingOrderId, orderData);
                showToast('Order updated successfully!', 'success');
            } else {
                // CREATE Mode
                orderData.order_number = Date.now().toString();
                await createOrderApi(orderData);
                showToast('Order placed successfully!', 'success');
            }

            elements.createOrderFormElement.reset();
            currentEditingOrderId = null;

            setTimeout(() => {
                showOrdersView();
            }, 1000);

        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });

    // Global Handlers for Edit/Delete (since they are dynamic)
    window.handleEditOrder = (id) => {
        const order = window.userOrders.find(o => o.id === id);
        if (order) {
            showCreateOrderForm(order);
        }
    };

    window.handleDeleteOrder = async (id) => {
        if (!confirm('Are you sure you want to delete this order?')) return;

        try {
            await deleteOrderApi(id);
            showToast('Order deleted successfully', 'success');
            loadOrders(); // Refresh list
        } catch (error) {
            showToast(error.message, 'error');
        }
    };

    // Toggle between login and signup
    elements.showSignup.addEventListener('click', (e) => {
        e.preventDefault();
        showSignupForm();
    });

    elements.showLogin.addEventListener('click', (e) => {
        e.preventDefault();
        showLoginForm();
    });

    // New Links Logic
    elements.showForgetPassword.addEventListener('click', (e) => {
        e.preventDefault();
        showForgetPasswordForm();
    });

    elements.backToLoginFromForget.addEventListener('click', (e) => {
        e.preventDefault();
        showLoginForm();
    });

    elements.backToLoginFromReset.addEventListener('click', (e) => {
        e.preventDefault();
        showLoginForm();
    });

    // Address toggle
    elements.addressToggle.addEventListener('click', () => {
        const isVisible = elements.addressFields.style.display !== 'none';
        elements.addressFields.style.display = isVisible ? 'none' : 'block';
        elements.addressToggle.classList.toggle('active');
    });

    // Logout
    elements.logoutBtn.addEventListener('click', () => {
        // Clear session
        currentUser = null;
        authToken = null;
        localStorage.removeItem('user');
        localStorage.removeItem('authToken');

        // Reset forms
        elements.loginFormElement.reset();
        elements.signupFormElement.reset();
        elements.forgetPasswordFormElement.reset();
        elements.resetPasswordFormElement.reset();
        elements.changePasswordFormElement.reset();

        // Show login form
        showLoginForm();

        showToast('Logged out successfully.', 'success');
    });
}

function init() {
    console.log('✨ Initialization starting...');
    setupElements();
    setupEventListeners();

    // Check for existing session
    checkSession();

    console.log('✨ UserHub initialized successfully!');
    console.log('Backend API:', API_BASE_URL);
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
