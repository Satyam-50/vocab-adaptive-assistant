# Vocabulary Level Adaptive Reading Assistant - Frontend

A modern, responsive React + Vite frontend for the Vocabulary Level Adaptive Reading Assistant. Built with Tailwind CSS, React Router, and Axios.

## 🚀 Features

- **Modern UI**: Clean, SaaS-style design with glassmorphism and smooth animations
- **Responsive Design**: Mobile-first approach, works on all devices
- **Real-time Analysis**: Instant text difficulty detection and simplification
- **PDF Support**: Upload and analyze PDF documents directly
- **Dark Mode**: Toggle between light and dark themes
- **Error Handling**: Graceful error messages and loading states
- **No External APIs**: Works completely with local backend

## 🛠️ Tech Stack

- **React 18.3**: UI library with hooks
- **Vite 5.3**: Lightning-fast build tool
- **React Router 6**: Client-side routing
- **Tailwind CSS 3.4**: Utility-first styling
- **Axios 1.7.7**: HTTP client for API calls
- **PostCSS & Autoprefixer**: CSS processing

## 📦 Installation

### Prerequisites
- Node.js 16+ and npm

### Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Configure API URL** (if needed)
   Edit `.env` and set:
   ```
   VITE_API_URL=http://127.0.0.1:8000
   ```

## 🚀 Running

### Development Server
```bash
npm run dev
```
Opens automatically at `http://localhost:3000`

### Production Build
```bash
npm run build
```
Generates optimized files in `dist/` folder

### Preview Build
```bash
npm run preview
```
Test production build locally

## 📁 Project Structure

```
frontend-new/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Navbar.jsx      # Navigation bar (sticky)
│   │   ├── TextInput.jsx   # Input textarea + PDF upload
│   │   ├── OutputDisplay.jsx # Results display
│   │   ├── WordTooltip.jsx # Hover tooltip for words
│   │   └── Loader.jsx      # Loading spinner
│   ├── pages/              # Page components
│   │   ├── Home.jsx        # Landing page with hero
│   │   ├── ReadingLab.jsx  # Main feature page (2-column)
│   │   └── Dashboard.jsx   # Analytics dashboard
│   ├── services/
│   │   └── api.js          # Axios API service
│   ├── App.jsx             # Main app with routing
│   ├── main.jsx            # React entry point
│   └── index.css           # Tailwind + custom styles
├── index.html              # HTML entry point
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
├── postcss.config.js       # PostCSS configuration
├── package.json
└── .env.example            # Environment template
```

## 🎨 Design System

### Colors
- **Primary**: Blue (#3b82f6)
- **Secondary**: Purple (#8b5cf6)
- **Accent**: Amber (#f59e0b)
- **Backgrounds**: Slate variants

### Components
- **Cards**: Rounded with soft shadows
- **Buttons**: Primary (gradient), Secondary, Ghost styles
- **Inputs**: Full-width with focus states
- **Badges**: For level display

### Animations
- Fade-in effect on new content
- Smooth hover transitions
- Loading spinner animation

## 📡 API Integration

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### Analyze Text
```POST /analyze
{
  "text": "Your text here"
}
```

#### Analyze PDF
```POST /analyze/pdf
Content-Type: multipart/form-data
pdf_file: <file>
```

### Response Format
```json
{
  "level": "B2",
  "simplified_text": "Simplified version of text",
  "difficult_words": [
    {
      "word": "proliferation",
      "meaning": "rapid increase",
      "synonyms": ["growth", "expansion"]
    }
  ]
}
```

## 🔧 Configuration

### Environment Variables
```bash
VITE_API_URL=http://127.0.0.1:8000  # Backend API URL
```

### Tailwind Customization
Edit `tailwind.config.js` to customize:
- Colors
- Box shadows
- Typography
- Responsive breakpoints

## ✨ Features Explained

### Reading Lab
- **Left Column**: Text input or PDF upload
- **Right Column**: Real-time analysis results
- **Word Counter**: Shows word and character counts
- **Copy Button**: Copy simplified text to clipboard
- **Tooltips**: Hover over difficult words for meanings

### Home Page
- **Hero Section**: Gradient background, call-to-action buttons
- **Features Grid**: 6 key features showcased
- **Responsive**: Adapts to all screen sizes

### Dashboard
- **Coming Soon**: Placeholder for future analytics
- **Stats Cards**: Ready for progress tracking
- **Responsive Grid**: Works on mobile and desktop

## 🎯 Code Quality

- **Functional Components**: Using React hooks only
- **Modular Structure**: Reusable, maintainable components
- **Error Handling**: Try-catch blocks and user-friendly messages
- **Loading States**: Proper UX feedback during API calls
- **Responsive**: Mobile-first CSS approach
- **Comments**: Inline documentation where needed

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🚦 Development Workflow

1. **Start dev server**: `npm run dev`
2. **Make changes**: Edit components in `src/`
3. **Hot reload**: Changes reflect instantly
4. **Build**: `npm run build` for production
5. **Deploy**: Serve `dist/` folder

## 📝 Component API

### TextInput
```jsx
<TextInput
  inputText={string}
  setInputText={function}
  onAnalyzeText={function}
  onAnalyzePdf={function}
  onClear={function}
  loading={boolean}
/>
```

### OutputDisplay
```jsx
<OutputDisplay
  result={object | null}
  loading={boolean}
/>
```

### WordTooltip
```jsx
<WordTooltip
  word={string}
  meaning={string}
  synonyms={string[]}
/>
```

## 🐛 Troubleshooting

### API connection fails
- Check backend is running at `http://127.0.0.1:8000`
- Verify `.env` has correct `VITE_API_URL`
- Check browser console for CORS issues

### PDF upload not working
- Ensure backend has `python-multipart` installed
- File must be valid PDF format
- File size must be under 50MB

### Styling issues
- Run: `npm install` to ensure Tailwind is installed
- Check `tailwind.config.js` is correct
- Clear browser cache if needed

## 📦 Deployment

### Build Artifact
Production build in `dist/` folder ready to deploy to:
- Vercel
- Netlify
- AWS S3 + CloudFront
- Any static hosting

### Size Report
```
dist/static/js/main.*.js  ~120KB (gzipped)
dist/static/css/main.*.css ~25KB (gzipped)
```

## 📄 License

MIT - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

Built with ❤️ for vocab learners everywhere
