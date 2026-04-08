import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'

export default function Navbar({ darkMode, toggleDarkMode }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <nav
      className={`sticky top-0 z-50 backdrop-blur-md transition-all duration-300 ${
        darkMode
          ? 'border-b border-slate-800/80 bg-slate-950/85'
          : 'border-b border-slate-200/80 bg-white/85'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link
            to="/"
            className="flex items-center gap-2 font-bold text-lg bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent"
          >
            <span className="text-2xl">📚</span>
            <span className="hidden sm:inline">Vocab Assistant</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <Link
              to="/"
              className={`font-semibold transition-all ${
                isActive('/')
                  ? 'text-primary border-b-2 border-primary'
                  : darkMode
                    ? 'text-slate-300 hover:text-white'
                    : 'text-slate-700 hover:text-primary'
              }`}
            >
              Home
            </Link>
            <Link
              to="/reading"
              className={`font-semibold transition-all ${
                isActive('/reading')
                  ? 'text-primary border-b-2 border-primary'
                  : darkMode
                    ? 'text-slate-300 hover:text-white'
                    : 'text-slate-700 hover:text-primary'
              }`}
            >
              Reading Lab
            </Link>
            <Link
              to="/dashboard"
              className={`font-semibold transition-all ${
                isActive('/dashboard')
                  ? 'text-primary border-b-2 border-primary'
                  : darkMode
                    ? 'text-slate-300 hover:text-white'
                    : 'text-slate-700 hover:text-primary'
              }`}
            >
              Dashboard
            </Link>
          </div>

          {/* Dark Mode Toggle + Mobile Menu */}
          <div className="flex items-center gap-4">
            <button
              onClick={toggleDarkMode}
              className={`p-2 rounded-full border transition-all duration-300 ${
                darkMode
                  ? 'border-slate-700 bg-slate-900 text-yellow-300 hover:border-slate-600 hover:bg-slate-800'
                  : 'border-slate-200 bg-slate-100 text-slate-700 hover:border-slate-300 hover:bg-slate-200'
              }`}
              aria-label="Toggle dark mode"
              aria-pressed={darkMode}
            >
              {darkMode ? '☀️' : '🌙'}
            </button>

            {/* Mobile Menu Button */}
            <button
              className={`md:hidden p-2 rounded-full border transition-all duration-300 ${
                darkMode
                  ? 'border-slate-700 bg-slate-900 text-slate-100 hover:bg-slate-800'
                  : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-100'
              }`}
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle navigation menu"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div
            className={`md:hidden pb-4 border-t ${
              darkMode ? 'border-slate-800' : 'border-slate-200'
            }`}
          >
            <Link
              to="/"
              className={`block px-4 py-2 font-semibold transition-colors ${
                darkMode
                  ? 'text-slate-300 hover:text-white'
                  : 'text-slate-700 hover:text-primary'
              }`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              to="/reading"
              className={`block px-4 py-2 font-semibold transition-colors ${
                darkMode
                  ? 'text-slate-300 hover:text-white'
                  : 'text-slate-700 hover:text-primary'
              }`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Reading Lab
            </Link>
            <Link
              to="/dashboard"
              className={`block px-4 py-2 font-semibold transition-colors ${
                darkMode
                  ? 'text-slate-300 hover:text-white'
                  : 'text-slate-700 hover:text-primary'
              }`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Dashboard
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}
