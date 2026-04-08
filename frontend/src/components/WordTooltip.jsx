import { useState } from 'react'

export default function WordTooltip({ word, meaning, synonyms }) {
  const [showTooltip, setShowTooltip] = useState(false)

  return (
    <div className="relative inline-block">
      <button
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        onClick={() => setShowTooltip(!showTooltip)}
        className="cursor-help font-semibold underline transition-colors text-primary hover:text-blue-700 dark:text-cyan-300 dark:hover:text-cyan-200"
        aria-label={`${word} - ${meaning}`}
      >
        {word}
      </button>

      {showTooltip && (
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 z-50 fade-in">
          <div className="whitespace-nowrap rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-xl dark:border-slate-700 dark:bg-slate-800 dark:text-white">
            <div className="font-bold text-primary dark:text-cyan-300">{word}</div>
            <div className="text-sm mt-1">{meaning}</div>
            {synonyms && synonyms.length > 0 && (
              <div className="text-xs text-slate-600 mt-2 dark:text-slate-300">
                Similar: {synonyms.join(', ')}
              </div>
            )}
            {/* Arrow pointer */}
            <div className="absolute top-full left-1/2 h-2 w-2 -translate-x-1/2 rotate-45 border-r border-b border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-800"></div>
          </div>
        </div>
      )}
    </div>
  )
}
