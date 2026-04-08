import { useState } from 'react'
import WordTooltip from './WordTooltip'
import Loader from './Loader'

const levelColors = {
  A1: 'from-green-400 to-green-600',
  A2: 'from-emerald-400 to-emerald-600',
  B1: 'from-blue-400 to-blue-600',
  B2: 'from-purple-400 to-purple-600',
  C1: 'from-orange-400 to-orange-600',
  C2: 'from-red-400 to-red-600',
}

export default function OutputDisplay({ result, loading, showDifficultWords = true }) {
  const [copied, setCopied] = useState(false)

  const copySimplifiedText = async () => {
    if (!result?.simplified_text) return

    try {
      await navigator.clipboard.writeText(result.simplified_text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      alert('Failed to copy text')
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold text-slate-900 mb-6 dark:text-slate-100">Analysis Output</h2>
        <Loader />
      </div>
    )
  }

  if (!result) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold text-slate-900 mb-6 dark:text-slate-100">Analysis Output</h2>
        <div className="text-center py-12">
          <p className="text-slate-500 text-lg dark:text-slate-400">
            😊 Analyze text or upload a PDF to see results
          </p>
        </div>
      </div>
    )
  }

  const wordCount = result.simplified_text.trim().split(/\s+/).filter(w => w.length > 0).length
  const colorGradient = levelColors[result.level] || levelColors.B1

  return (
    <div className="space-y-4">
      {/* Level Badge */}
      <div className={`card bg-gradient-to-r ${colorGradient} text-white text-center py-8 fade-in`}>
        <div className="text-sm font-semibold opacity-90 mb-2">DETECTED LEVEL</div>
        <div className="text-5xl font-bold">{result.level}</div>
        <div className="text-sm opacity-90 mt-2">
          {result.level === 'A1' && 'Beginner'}
          {result.level === 'A2' && 'Elementary'}
          {result.level === 'B1' && 'Intermediate'}
          {result.level === 'B2' && 'Upper Intermediate'}
          {result.level === 'C1' && 'Advanced'}
          {result.level === 'C2' && 'Mastery'}
        </div>
      </div>

      {/* Quick Metrics */}
      <div className="grid grid-cols-3 gap-3">
        <div className="card text-center fade-in">
          <div className="text-sm text-slate-600 font-semibold dark:text-slate-400">Difficult Words</div>
          <div className="text-3xl font-bold text-primary mt-2">
            {result.difficult_words?.length || 0}
          </div>
        </div>
        <div className="card text-center fade-in">
          <div className="text-sm text-slate-600 font-semibold dark:text-slate-400">Simplified Words</div>
          <div className="text-3xl font-bold text-primary mt-2">{wordCount}</div>
        </div>
        <div className="card text-center fade-in">
          <div className="text-sm text-slate-600 font-semibold dark:text-slate-400">Characters</div>
          <div className="text-3xl font-bold text-primary mt-2">
            {result.simplified_text.length}
          </div>
        </div>
      </div>

      {/* Simplified Text */}
      <div className="card fade-in">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100">Simplified Text</h3>
          <button
            onClick={copySimplifiedText}
            className={`text-sm font-semibold px-3 py-1 rounded-full transition-all ${
              copied
                ? 'bg-green-100 text-green-700 dark:bg-green-950/50 dark:text-green-300'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            {copied ? '✓ Copied!' : 'Copy'}
          </button>
        </div>
        <p className="text-slate-700 leading-relaxed whitespace-pre-wrap dark:text-slate-300">
          {result.simplified_text}
        </p>
      </div>

      {showDifficultWords && (
        <div className="card fade-in">
          <h3 className="text-xl font-bold text-slate-900 mb-4 dark:text-slate-100">Difficult Words</h3>
          {result.difficult_words && result.difficult_words.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {result.difficult_words.map((item) => (
                <div key={item.word} className="rounded-2xl border border-accent/20 bg-gradient-to-r from-accent/10 to-orange-100 p-4 dark:border-amber-500/20 dark:from-slate-800 dark:to-slate-900">
                  <div className="font-bold mb-2">
                    <WordTooltip
                      word={item.word}
                      meaning={item.meaning}
                      synonyms={item.synonyms}
                    />
                  </div>
                  <p className="text-sm text-slate-700 dark:text-slate-300">{item.meaning}</p>
                  {item.synonyms && item.synonyms.length > 0 && (
                    <div className="text-xs text-slate-600 mt-2 flex flex-wrap gap-1 dark:text-slate-400">
                      {item.synonyms.map((syn, idx) => (
                        <span key={idx} className="rounded-full bg-white px-2 py-1 dark:bg-slate-800">
                          {syn}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-500 text-center py-6">✨ No difficult words detected!</p>
          )}
        </div>
      )}
    </div>
  )
}
