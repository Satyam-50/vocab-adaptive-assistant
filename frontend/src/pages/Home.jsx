import { Link } from 'react-router-dom'

export default function Home({ darkMode }) {
  const shellClasses = darkMode ? 'bg-slate-950 text-slate-100' : 'bg-[#f6f9ff] text-slate-900'
  const heroClasses = darkMode
    ? 'from-slate-950 via-indigo-950 to-cyan-950'
    : 'from-[#eef6ff] via-[#edf1ff] to-[#fff7ed]'
  const heroAccentClasses = darkMode ? 'bg-cyan-400/20' : 'bg-sky-300/40'
  const sectionClasses = darkMode ? 'bg-slate-950' : 'bg-[#f9fbff]'
  const panelClasses = darkMode ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200'
  const mutedText = darkMode ? 'text-slate-300' : 'text-slate-600'
  const heroText = darkMode ? 'text-white' : 'text-slate-900'
  const heroLead = darkMode ? 'text-slate-200/90' : 'text-slate-600'
  const heroCard = darkMode
    ? 'border-white/20 bg-white/10 text-white'
    : 'border-sky-100 bg-white/85 text-sky-700'
  const heroPrimaryButton = darkMode
    ? 'bg-white text-slate-950 hover:bg-slate-100'
    : 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white hover:from-blue-700 hover:to-cyan-600'
  const heroSecondaryButton = darkMode
    ? 'border-white/20 bg-white/10 text-white hover:bg-white/20'
    : 'border-slate-200 bg-white text-slate-800 hover:bg-slate-50'
  const heroTitleGradient = darkMode
    ? 'from-cyan-300 via-sky-300 to-amber-300'
    : 'from-blue-600 via-indigo-600 to-cyan-500'

  return (
    <main className={`min-h-screen flex flex-col transition-colors duration-300 ${shellClasses}`}>
      <section className={`relative overflow-hidden bg-gradient-to-br ${heroClasses} py-20 px-4 sm:px-6 lg:px-8`}>
        <div className={`absolute -left-20 top-0 h-56 w-56 rounded-full blur-3xl ${heroAccentClasses}`} />
        <div
          className={`absolute -right-16 bottom-4 h-64 w-64 rounded-full blur-3xl ${
            darkMode ? 'bg-blue-500/15' : 'bg-amber-200/35'
          }`}
        />

        <div className="relative max-w-5xl mx-auto text-center fade-in">
          <div className={`mb-6 inline-flex items-center justify-center rounded-full px-4 py-2 text-3xl shadow-lg backdrop-blur-md ${heroCard}`}>
            📖
          </div>

          <h1 className={`text-4xl sm:text-5xl lg:text-6xl font-black mb-6 leading-tight tracking-tight text-balance ${heroText}`}>
            Vocabulary Level{' '}
            <span className={`bg-gradient-to-r ${heroTitleGradient} bg-clip-text text-transparent`}>
              Adaptive Reading Assistant
            </span>
          </h1>

          <p className={`mx-auto mb-10 max-w-3xl text-lg sm:text-xl ${heroLead}`}>
            Analyze, simplify, and learn vocabulary intelligently. Master English at your pace.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-stretch sm:items-center">
            <Link
              to="/reading"
              className={`inline-flex items-center justify-center rounded-full px-8 py-3 font-semibold shadow-xl transition-all duration-300 hover:-translate-y-0.5 hover:shadow-2xl ${heroPrimaryButton}`}
            >
              Start Reading Lab →
            </Link>
            <Link
              to="/dashboard"
              className={`inline-flex items-center justify-center rounded-full px-8 py-3 font-semibold backdrop-blur-md transition-all duration-300 hover:-translate-y-0.5 ${heroSecondaryButton}`}
            >
              View Dashboard
            </Link>
          </div>
        </div>
      </section>

      <section className={`py-20 px-4 sm:px-6 lg:px-8 ${sectionClasses}`}>
        <div className="max-w-6xl mx-auto">
          <h2 className={`text-3xl font-bold text-center mb-4 ${darkMode ? 'text-white' : 'text-slate-900'}`}>
            Powerful Features
          </h2>
          <p className={`text-center max-w-2xl mx-auto mb-12 ${mutedText}`}>
            Everything is designed to make difficult reading feel lighter, clearer, and more interactive.
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="card fade-in">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold mb-3">Level Detection</h3>
              <p className={mutedText}>
                Instantly detect your text difficulty level from A1 (beginner) to C2 (mastery) using advanced AI.
              </p>
            </div>

            <div className="card fade-in" style={{ animationDelay: '0.1s' }}>
              <div className="text-4xl mb-4">✨</div>
              <h3 className="text-xl font-bold mb-3">Text Simplification</h3>
              <p className={mutedText}>
                Get automatically simplified versions of complex texts while preserving meaning and context.
              </p>
            </div>

            <div className="card fade-in" style={{ animationDelay: '0.2s' }}>
              <div className="text-4xl mb-4">📚</div>
              <h3 className="text-xl font-bold mb-3">Vocabulary Help</h3>
              <p className={mutedText}>
                Identify difficult words with meanings, synonyms, and usage examples for better understanding.
              </p>
            </div>

            <div className="card fade-in" style={{ animationDelay: '0.3s' }}>
              <div className="text-4xl mb-4">📄</div>
              <h3 className="text-xl font-bold mb-3">PDF Support</h3>
              <p className={mutedText}>
                Upload and analyze PDF documents directly. Extract and process text with ease.
              </p>
            </div>

            <div className="card fade-in" style={{ animationDelay: '0.4s' }}>
              <div className="text-4xl mb-4">📈</div>
              <h3 className="text-xl font-bold mb-3">Progress Tracking</h3>
              <p className={mutedText}>
                Track your learning progress and see improvements over time with detailed analytics.
              </p>
            </div>

            <div className="card fade-in" style={{ animationDelay: '0.5s' }}>
              <div className="text-4xl mb-4">🔐</div>
              <h3 className="text-xl font-bold mb-3">Offline First</h3>
              <p className={mutedText}>
                Works completely offline with no external APIs. Your data stays private and secure.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className={`py-20 px-4 sm:px-6 lg:px-8 ${darkMode ? 'bg-slate-900/50' : 'bg-slate-100/80'}`}>
        <div className={`max-w-5xl mx-auto rounded-3xl border px-6 py-12 sm:px-10 ${panelClasses}`}>
          <div className="grid gap-8 lg:grid-cols-[1.4fr_0.9fr] lg:items-center">
            <div>
              <p className="mb-3 inline-flex rounded-full bg-primary/10 px-4 py-1 text-sm font-semibold text-primary">
                Built for readers, students, and curious learners
              </p>
              <h2 className={`text-3xl sm:text-4xl font-bold mb-4 ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                Ready to Improve Your English?
              </h2>
              <p className={mutedText}>
                Start analyzing your reading material today and unlock your vocabulary potential.
              </p>
            </div>

            <div className="flex lg:justify-end">
              <Link
                to="/reading"
                className="inline-flex w-full sm:w-auto items-center justify-center rounded-full bg-slate-950 px-8 py-4 font-semibold text-white shadow-xl transition-all duration-300 hover:-translate-y-0.5 hover:shadow-2xl dark:bg-white dark:text-slate-950"
              >
                Get Started Now →
              </Link>
            </div>
          </div>
        </div>
      </section>

      <footer className={`border-t px-4 sm:px-6 lg:px-8 py-12 ${darkMode ? 'border-slate-800 bg-slate-950 text-slate-300' : 'border-slate-200 bg-white text-slate-600'}`}>
        <div className="max-w-6xl mx-auto">
          <div className="grid gap-8 md:grid-cols-3 md:items-start">
            <div>
              <div className="mb-4 text-2xl">📚</div>
              <p className={`max-w-sm ${mutedText}`}>
                Vocabulary Level Adaptive Reading Assistant helps learners analyze text, simplify reading, and grow vocabulary with confidence.
              </p>
            </div>

            <div>
              <h3 className={`mb-4 text-sm font-bold uppercase tracking-[0.2em] ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                Explore
              </h3>
              <div className="space-y-2">
                <Link to="/reading" className="block transition-colors hover:text-primary">
                  Reading Lab
                </Link>
                <Link to="/dashboard" className="block transition-colors hover:text-primary">
                  Dashboard
                </Link>
              </div>
            </div>

            <div>
              <h3 className={`mb-4 text-sm font-bold uppercase tracking-[0.2em] ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                Built With
              </h3>
              <div className="flex flex-wrap gap-2">
                <span className="rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary">FastAPI</span>
                <span className="rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary">React</span>
                <span className="rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary">Tailwind</span>
              </div>
            </div>
          </div>

          <div className={`mt-10 border-t pt-6 text-center text-sm ${darkMode ? 'border-slate-800 text-slate-400' : 'border-slate-200 text-slate-500'}`}>
            © 2024 Vocabulary Level Adaptive Reading Assistant. Powered by{' '}
            <span className="font-semibold text-primary">FastAPI + React</span>
          </div>
        </div>
      </footer>
    </main>
  )
}
