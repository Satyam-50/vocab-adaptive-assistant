import { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import ReadingLab from './pages/ReadingLab'
import Dashboard from './pages/Dashboard'
import './index.css'

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window === 'undefined') {
      return false
    }

    const savedTheme = window.localStorage.getItem('theme')
    if (savedTheme) {
      return savedTheme === 'dark'
    }

    return window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? false
  })

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
  }

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode)
    document.documentElement.style.colorScheme = darkMode ? 'dark' : 'light'

    if (typeof window !== 'undefined') {
      window.localStorage.setItem('theme', darkMode ? 'dark' : 'light')
    }
  }, [darkMode])

  return (
    <Router>
      <div
        className={`min-h-screen transition-colors duration-300 ${
          darkMode ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'
        }`}
      >
        <Navbar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />

        <Routes>
          <Route path="/" element={<Home darkMode={darkMode} />} />
          <Route path="/reading" element={<ReadingLab darkMode={darkMode} />} />
          <Route path="/dashboard" element={<Dashboard darkMode={darkMode} />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
