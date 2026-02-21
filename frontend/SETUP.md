# 🚀 Quick Setup Guide

## Your Frontend is Ready!

I've created a beautiful, modern frontend for your User Management API.

## What's Included

✅ **Login Page** - Secure user authentication
✅ **Signup Page** - User registration with optional address
✅ **Dashboard** - User profile and information display
✅ **Premium Design** - Animated gradients, glassmorphism, smooth transitions
✅ **Responsive** - Works on desktop, tablet, and mobile
✅ **API Integration** - Connected to your backend at http://127.0.0.1:8000

## 📋 Next Steps

Since Node.js was just installed, you need to **restart your terminal** for npm to work.

### Option 1: Using Batch Files (Easiest)

1. **Close this terminal window**
2. **Open a new PowerShell or Command Prompt**
3. Navigate to the frontend folder:
   ```bash
   cd c:\Users\SANKET\OneDrive\Documents\GitHub\first_project\frontend
   ```
4. Double-click `install.bat` to install dependencies
5. Double-click `start.bat` to start the dev server

### Option 2: Using Commands

1. **Close this terminal window**
2. **Open a new PowerShell or Command Prompt**
3. Run these commands:
   ```bash
   cd c:\Users\SANKET\OneDrive\Documents\GitHub\first_project\frontend
   npm install
   npm run dev
   ```

## 🎯 Testing Your App

1. **Start your backend** (if not already running):
   ```bash
   cd c:\Users\SANKET\OneDrive\Documents\GitHub\first_project
   python main.py
   ```

2. **Start the frontend** (in a new terminal):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open your browser** to `http://localhost:3000`

## 🎨 Features to Try

### 1. Create an Account
- Click "Create one" on the login page
- Fill in your details (first name, last name, email, mobile, password)
- Optionally expand "Add Address" to include your address
- Click "Create Account"

### 2. Login
- Use your email and password
- Your session will be saved (even if you refresh!)

### 3. View Dashboard
- See your user information beautifully displayed
- Check your account status
- View your address if you added one

### 4. Logout
- Click the "Logout" button to end your session

## 🎭 Design Highlights

- **Animated Background** - Floating gradient orbs
- **Glassmorphism** - Frosted glass effect on cards
- **Smooth Transitions** - Buttery smooth animations
- **Premium Typography** - Inter font from Google Fonts
- **Toast Notifications** - Beautiful success/error messages
- **Micro-interactions** - Hover effects and button animations

## 📁 Project Structure

```
frontend/
├── index.html       # Main HTML structure
├── style.css        # Premium CSS with design system
├── main.js          # API integration & app logic
├── vite.config.js   # Vite configuration with proxy
├── package.json     # Dependencies
├── install.bat      # Easy dependency installation
├── start.bat        # Easy dev server start
└── README.md        # Detailed documentation
```

## ⚙️ Configuration

The frontend is pre-configured to work with your backend. If you need to change the API URL, edit `main.js`:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

## 🐛 Troubleshooting

**npm not found?**
- Restart your terminal after Node.js installation
- Make sure Node.js is in your PATH

**Backend connection failed?**
- Ensure your backend is running on port 8000
- Check CORS settings in your backend

**Port 3000 already in use?**
- Change the port in `vite.config.js`

## 📚 Need Help?

Check out `README.md` for more detailed documentation!

---

**Enjoy your beautiful new frontend! 🎉**
