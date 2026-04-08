import { useState } from 'react'
import TextInput from '../components/TextInput'
import OutputDisplay from '../components/OutputDisplay'
import WordTooltip from '../components/WordTooltip'
import { analyzeText, analyzePdf } from '../services/api'

export default function ReadingLab({ darkMode }) {
  const [inputText, setInputText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyzeText = async (text) => {
    if (!text.trim()) {
      setError('Please enter some text to analyze')
      return
    }

    setLoading(true)
    setError('')

    try {
      const data = await analyzeText(text)
      setResult(data)
      setError('')
    } catch (err) {
      setError(err.message || 'Failed to analyze text. Please check the backend service.')
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyzePdf = async (file) => {
    if (!file) {
      setError('Please select a PDF file')
      return
    }

    setLoading(true)
    setError('')

    try {
      const data = await analyzePdf(file)
      setResult(data)
      setError('')
      // Optionally update the textarea with extracted text
      // setInputText(data.original_text || '')
    } catch (err) {
      setError(err.message || 'Failed to analyze PDF. Please check the backend service.')
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setInputText('')
    setResult(null)
    setError('')
  }

  return (
    <div className={`min-h-screen py-8 px-4 sm:px-6 lg:px-8 transition-colors duration-300 ${darkMode ? 'bg-slate-950' : 'bg-slate-50'}`}>
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className={`text-4xl font-bold ${darkMode ? 'text-white' : 'text-slate-900'}`}>Reading Lab</h1>
          <p className={`mt-2 ${darkMode ? 'text-slate-300' : 'text-slate-600'}`}>
            Analyze your text, get instant simplification, and learn difficult vocabulary
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg fade-in flex items-start gap-3 dark:border-red-900/50 dark:bg-red-950/40 dark:text-red-300">
            <span className="text-xl">⚠️</span>
            <div>
              <p className="font-semibold">Analysis Error</p>
              <p className="text-sm mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* Two Column Layout */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Input */}
          <div>
            <TextInput
              inputText={inputText}
              setInputText={setInputText}
              onAnalyzeText={handleAnalyzeText}
              onAnalyzePdf={handleAnalyzePdf}
              onClear={handleClear}
              loading={loading}
            />

            {/* Difficult Words - directly below input actions */}
            {result && !loading && (
              <div className="mt-4 card fade-in border border-sky-200/70 bg-gradient-to-br from-white via-sky-50 to-indigo-50 dark:border-slate-700 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800">
                <h3 className="mb-4 text-xl font-bold text-slate-900 dark:text-slate-100">Difficult Words</h3>
                {result.difficult_words && result.difficult_words.length > 0 ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {result.difficult_words.map((item) => (
                      <div
                        key={item.word}
                        className="rounded-2xl border border-sky-200/80 bg-gradient-to-br from-white to-sky-50 p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md dark:border-slate-600 dark:from-slate-900 dark:to-slate-800"
                      >
                        <div className="font-bold mb-2">
                          <WordTooltip
                            word={item.word}
                            meaning={item.meaning}
                            synonyms={item.synonyms}
                          />
                        </div>
                        <p className="text-sm text-slate-700 dark:text-slate-300">{item.meaning}</p>
                        {item.synonyms && item.synonyms.length > 0 && (
                          <div className="mt-2 flex flex-wrap gap-1 text-xs text-slate-600 dark:text-slate-400">
                            {item.synonyms.map((syn, idx) => (
                              <span
                                key={idx}
                                className="rounded-full border border-sky-100 bg-white px-2 py-1 dark:border-slate-600 dark:bg-slate-800"
                              >
                                {syn}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="py-6 text-center text-slate-500 dark:text-slate-400">✨ No difficult words detected!</p>
                )}
              </div>
            )}
          </div>

          {/* Right Column - Output */}
          <div>
            <OutputDisplay result={result} loading={loading} showDifficultWords={false} />
          </div>
        </div>

        {/* Info Box */}
        <div className="mt-12 rounded-xl border border-blue-200 bg-blue-50 p-6 dark:border-blue-900/50 dark:bg-blue-950/40">
          <p className="text-blue-900 dark:text-blue-100">
            <span className="font-semibold">💡 Tip:</span> You can paste text from any source or upload a PDF file directly. The system will automatically detect the reading difficulty level (A1-C2), simplify the text, and highlight difficult vocabulary.
          </p>
        </div>
      </div>
    </div>
  )
}
