# 🚀 QUICK START GUIDE - Running the Complete Application

## Prerequisites
- Node.js 16+ and npm installed
- Python 3.8+ with virtual environment activated
- Backend dependencies installed

---

## ⚡ Quick Launch (All in One)

### Terminal 1: Start Backend
```powershell
cd c:\Users\SATYAM VISHWAKARMA\OneDrive\Desktop\vocab-adaptive-assistant
.venv\Scripts\Activate.ps1

# Install dependencies (first time only)
pip install -r backend/requirements.txt

# Run backend on port 8000
python -m uvicorn backend.app.main:app --reload
```

Expected output:
```
Uvicorn running on http://127.0.0.1:8000
Press CTRL+C to quit
```

---

### Terminal 2: Start Frontend
```powershell
cd c:\Users\SATYAM VISHWAKARMA\OneDrive\Desktop\vocab-adaptive-assistant\frontend-new

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

Expected output:
```
VITE v5.3.1  ready in 123 ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

---

## 🌐 Access the Application

**Open in browser:**
```
http://localhost:3000
```

---

## 📋 What You Can Do

### On Home Page (`/`)
- See landing page with features overview
- Click "Start Reading Lab" or "View Dashboard"

### On Reading Lab (`/reading`)
**Left Side:**
- Paste English text into textarea
- See word/character count update in real-time
- Upload PDF file (optional)
- Click "Analyze Text" to process textarea
- Click "Analyze PDF" to process PDF file
- Click "Clear All" to reset

**Right Side:**
- See detected CEFR level (A1-C2) with color badge
- View quick metrics (difficult words count, simplified words, characters)
- Read simplified version of your text
- Click "Copy" to copy simplified text
- Hover over difficult words to see meaning & synonyms

### On Dashboard (`/dashboard`)
- See placeholder stats cards
- View coming soon section

---

## 🎨 Features to Try

### 1. **Analyze Text**
```
Sample text to paste:
"The proliferation of artificial intelligence has fundamentally transformed contemporary society."

Expected:
- Level: B2 or C1
- Simplified: "AI is becoming very common and has changed modern life."
- Difficult words: proliferation, artificial, fundamentally, etc.
```

### 2. **Analyze PDF**
- Download a PDF (e.g., article, research paper)
- Upload via "Upload PDF" button
- Click "Analyze PDF"
- Results appear on the right

### 3. **Dark Mode**
- Click moon icon (🌙) in navbar
- UI switches to dark theme
- Click sun icon (☀️) to switch back

---

## 🛠️ Development Features

### Hot Reload
- Edit any file in `frontend-new/src/`
- Changes appear instantly in browser
- No page refresh needed

### Browser DevTools
- Press F12 to open DevTools
- Check Network tab for API calls
- Use Console to debug

### Backend Reload
- Edit Python files in `backend/`
- Backend auto-reloads with `--reload` flag
- No need to restart manually

---

## 📊 Testing Scenarios

### Scenario 1: Simple Text Analysis
```
Input: "Hello, this is a test."
Expected: A1 level, minimal simplification, few difficult words
```

### Scenario 2: Complex Text
```
Input: "Quantum computing leverages superposition and entanglement for exponential computational advantages."
Expected: C1-C2 level, significant simplification, many difficult words
```

### Scenario 3: PDF Upload
```
Steps:
1. Select a PDF file
2. Click "Analyze PDF"
3. See extracted text analyzed
```

---

## 🐛 Troubleshooting

### Frontend fails to load
**Problem:** http://localhost:3000 shows blank page
```bash
# Solution:
cd frontend-new
npm install
npm run dev
# Check console for errors (F12)
```

### API connection error
**Problem:** "Unable to analyze text. Check backend service."
```bash
# Check backend is running:
# Terminal 1 should show: "Uvicorn running on http://127.0.0.1:8000"
# If not, restart it

# Check .env file
cat frontend-new\.env
# Should contain: VITE_API_URL=http://127.0.0.1:8000
```

### PDF upload not working
**Problem:** "Failed to parse PDF"
```bash
# Ensure backend has required package:
pip install python-multipart

# Restart backend
# Ctrl+C, then run again:
python -m uvicorn backend.app.main:app --reload
```

### Port already in use
**Problem:** "Port 3000 already in use"
```bash
# Use different port:
npm run dev -- --port 3001
# Open: http://localhost:3001
```

---

## 📦 Build for Production

### Frontend Build
```bash
cd frontend-new
npm run build
# Output: dist/ folder with optimized files
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel login
vercel
# Follow prompts to deploy
```

### Deploy to Netlify
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod --dir=dist
```

---

## 🎯 API Endpoints (for reference)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check backend is running |
| `/analyze` | POST | Analyze text |
| `/analyze/pdf` | POST | Analyze PDF |

### Example Requests

**Analyze Text:**
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world"}'
```

**Check Health:**
```bash
curl http://127.0.0.1:8000/health
```

---

## 📊 Performance Tips

### For Speed
- Use `npm run dev` for development (instant reload)
- Use Vite's optimized build for production
- Clear browser cache if styling looks wrong

### For Better Experience
- Use modern browser (Chrome/Firefox/Safari)
- Check internet connection
- Ensure backend is responsive

---

## 🔒 Security Notes

- Backend is local only (127.0.0.1)
- No data is sent to external services
- PDF files are processed locally
- All data stays on your machine

---

## 💡 Pro Tips

1. **Keyboard Shortcuts in Dev:**
   - `Ctrl+J` opens Vite shortcuts
   - `R` to reload
   - `Shift+R` to reset

2. **Component Debugging:**
   - Install React DevTools browser extension
   - Inspect component state and props

3. **API Debugging:**
   - Network tab in DevTools shows all requests
   - Check response payload for errors

---

## 🎉 You're All Set!

Everything is ready to use. Just:
1. Start backend (Terminal 1)
2. Start frontend (Terminal 2)
3. Open http://localhost:3000
4. Start analyzing text!

---

## 📚 Full Documentation

For more details, see:
- `frontend-new/README.md` - Complete frontend documentation
- `FRONTEND_BUILD_SUMMARY.md` - Technical build details
- `README.md` - Overall project documentation

---

**Happy Learning! 📖**
