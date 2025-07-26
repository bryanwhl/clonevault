# TwinNet - Digital Twin Agent Platform

A modern React application for managing digital twin agents and professional networking automation.

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation & Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000` (or `http://localhost:3001` if port 3000 is in use).

### Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Starts development server with hot reload |
| `npm run build` | Builds the application for production |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Check code quality with ESLint |
| `npm run lint:fix` | Auto-fix linting issues |

## 📦 Tech Stack

### Core Framework
- **React 18.2** - Modern React with hooks and TypeScript
- **TypeScript 5.0** - Type-safe development
- **Vite 4.4** - Fast build tool and development server

### UI & Styling
- **Tailwind CSS 3.3** - Utility-first CSS framework
- **shadcn/ui** - High-quality React component library (30+ components)
- **Radix UI** - Accessible headless UI primitives
- **Lucide React** - Beautiful icon library
- **CSS Variables** - Modern theming with dark mode support

### Key Dependencies
- **class-variance-authority** - Component variant management
- **tailwind-merge** - Intelligent Tailwind class merging
- **clsx** - Conditional className utility

### Additional UI Libraries
- **React Day Picker** - Date picker component
- **Recharts** - Chart and data visualization
- **Embla Carousel** - Touch-friendly carousel
- **React Hook Form** - Form state management
- **Sonner** - Toast notifications
- **Vaul** - Drawer component

### Development Tools
- **ESLint** - Code linting and formatting
- **PostCSS & Autoprefixer** - CSS processing
- **Vite Plugin React** - React integration for Vite

## 🏗️ Project Structure

```
web_app/
├── src/
│   └── main.tsx           # Application entry point
├── components/
│   ├── ui/                # shadcn/ui component library
│   ├── AgentConfig.tsx    # Agent configuration interface
│   ├── AgentNetwork.tsx   # Agent network management
│   ├── Dashboard.tsx      # Main dashboard
│   ├── Header.tsx         # Navigation header
│   ├── Profile.tsx        # User profile management
│   └── ...
├── styles/
│   └── globals.css        # Global styles and CSS variables
├── App.tsx                # Main application component
├── index.html             # HTML entry point
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── package.json           # Dependencies and scripts
```

## ✨ Application Features

### Core Functionality
- **Professional Networking Platform** - TwinNet concept for automated networking
- **Digital Twin Agent Management** - Configure and manage AI agents
- **Dashboard Analytics** - Real-time agent status and performance metrics
- **Profile Management** - Comprehensive user profile editing
- **Agent Configuration** - Personality, networking preferences, and privacy settings
- **Activity Feeds** - Track agent interactions and networking activity
- **Connection Management** - Manage professional connections

### UI/UX Features
- **Modern Design** - Clean, professional interface
- **Dark Mode Support** - Built-in theme switching
- **Responsive Layout** - Mobile-first responsive design
- **Accessibility** - WCAG compliant with proper ARIA labels
- **Component Library** - 30+ reusable UI components

## 🎨 Styling & Theming

The application uses a modern CSS variable-based theming system with support for light and dark modes. Color values use the oklch color space for consistent, modern color handling.

### Design Tokens
- Comprehensive color palette with semantic naming
- Consistent spacing and typography scales
- Border radius and shadow utilities
- Animation and transition presets

## 🔧 Configuration

### TypeScript
- Strict type checking enabled
- Path aliases configured (`@/*` maps to root directory)
- Modern ES modules and JSX transform

### Tailwind CSS
- Custom design tokens integration
- Component-scoped styles
- Optimized production builds with unused CSS removal

### Vite
- Fast development server with hot module replacement
- Optimized production builds with code splitting
- Source maps for debugging

## 🚦 Development Guidelines

### Code Quality
- ESLint configured for React and TypeScript
- Consistent code formatting
- Type safety enforced throughout

### Component Architecture
- Functional components with hooks
- Proper separation of concerns
- Reusable UI component library
- Accessibility-first approach

## 📝 License

This project includes components from shadcn/ui and uses images from Unsplash. See `Attributions.md` for detailed licensing information.

## 🤝 Contributing

1. Install dependencies: `npm install`
2. Start development server: `npm run dev`
3. Make your changes
4. Run linting: `npm run lint`
5. Build for production: `npm run build`
6. Test the production build: `npm run preview`

---

Built with ❤️ using modern React and TypeScript