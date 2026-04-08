export default function Dashboard({ darkMode }) {
  return (
    <div className={`min-h-screen py-8 px-4 sm:px-6 lg:px-8 transition-colors duration-300 ${darkMode ? 'bg-slate-950' : 'bg-slate-50'}`}>
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className={`text-4xl font-bold ${darkMode ? 'text-white' : 'text-slate-900'}`}>Dashboard</h1>
          <p className={`mt-2 ${darkMode ? 'text-slate-300' : 'text-slate-600'}`}>Track your learning progress and achievements</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Stats Cards */}
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-600 font-semibold">Sessions Completed</p>
                <p className="text-3xl font-bold text-primary mt-2">0</p>
              </div>
              <span className="text-4xl">📊</span>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-600 font-semibold">Words Learned</p>
                <p className="text-3xl font-bold text-primary mt-2">0</p>
              </div>
              <span className="text-4xl">📚</span>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-600 font-semibold">Current Level</p>
                <p className="text-3xl font-bold text-primary mt-2">—</p>
              </div>
              <span className="text-4xl">🎯</span>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-600 font-semibold">Texts Analyzed</p>
                <p className="text-3xl font-bold text-primary mt-2">0</p>
              </div>
              <span className="text-4xl">📄</span>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-600 font-semibold">PDFs Processed</p>
                <p className="text-3xl font-bold text-primary mt-2">0</p>
              </div>
              <span className="text-4xl">📕</span>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-600 font-semibold">Streak</p>
                <p className="text-3xl font-bold text-primary mt-2">0 days</p>
              </div>
              <span className="text-4xl">🔥</span>
            </div>
          </div>
        </div>

        {/* Coming Soon Section */}
        <div className="mt-12 card bg-gradient-to-r from-blue-50 to-cyan-50 border-2 border-blue-200 dark:from-slate-900 dark:to-slate-800 dark:border-slate-700">
          <div className="text-center py-12">
            <p className={`text-2xl font-bold mb-4 ${darkMode ? 'text-white' : 'text-slate-900'}`}>🚀 Coming Soon</p>
            <p className={`text-lg mb-6 ${darkMode ? 'text-slate-300' : 'text-slate-600'}`}>
              We're building advanced analytics, progress tracking, and personalized learning paths.
            </p>
            <div className={`space-y-2 ${darkMode ? 'text-slate-200' : 'text-slate-700'}`}>
              <p>✓ Detailed reading history</p>
              <p>✓ Vocabulary mastery tracking</p>
              <p>✓ Personalized recommendations</p>
              <p>✓ Learning streaks & achievements</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
