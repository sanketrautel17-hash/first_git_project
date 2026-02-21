# UserHub - Frontend

A modern, beautiful user management frontend built with Vite and vanilla JavaScript.

## Features

✨ **Modern Design**
- Stunning gradient backgrounds with animated orbs
- Glassmorphism UI with backdrop blur effects
- Smooth animations and transitions
- Fully responsive design

🔐 **Authentication**
- User registration with optional address
- Secure login system
- Session persistence with localStorage
- JWT token management

📱 **User Experience**
- Real-time form validation
- Toast notifications
- Loading states
- Beautiful user dashboard

## Tech Stack

- **Vite** - Fast build tool and dev server
- **Vanilla JavaScript** - No framework overhead
- **CSS3** - Modern styling with CSS variables
- **Inter Font** - Premium typography

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Your backend API running on `http://127.0.0.1:8000`

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The app will open automatically at `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## API Integration

The frontend connects to your FastAPI backend with the following endpoints:

- **POST /v1/login** - User authentication
- **POST /v1/users** - User registration

The Vite proxy is configured to forward `/v1/*` requests to `http://127.0.0.1:8000`

## Project Structure

```
frontend/
├── index.html      # Main HTML file
├── style.css       # Premium CSS with design system
├── main.js         # Application logic and API calls
├── vite.config.js  # Vite configuration
└── package.json    # Dependencies
```

## Configuration

To change the backend API URL, edit `main.js`:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)

## Features in Detail

### Login
- Email and password authentication
- Session persistence
- Automatic redirect to dashboard

### Signup
- Full name, email, mobile, and password
- Optional address (expandable section)
- All fields validated according to backend schema

### Dashboard
- Welcome message with user name
- User information display
- Status badge
- Optional address display
- Logout functionality

## Design Philosophy

This frontend prioritizes:
1. **Visual Excellence** - Premium, modern aesthetics
2. **User Experience** - Smooth, intuitive interactions
3. **Performance** - Fast load times with Vite
4. **Accessibility** - Semantic HTML and ARIA support

---

Made with ❤️ using Vite
