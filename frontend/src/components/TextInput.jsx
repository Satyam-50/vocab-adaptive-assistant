import { useRef, useState } from 'react'

const MAX_PDF_SIZE_MB = 200
const MAX_PDF_SIZE_BYTES = MAX_PDF_SIZE_MB * 1024 * 1024

export default function TextInput({
  inputText,
  setInputText,
  onAnalyzeText,
  onAnalyzePdf,
  onClear,
  loading,
}) {
  const [pdfFile, setPdfFile] = useState(null)
  const [pdfError, setPdfError] = useState('')
  const fileInputRef = useRef(null)

  const wordCount = inputText.trim().split(/\s+/).filter(w => w.length > 0).length
  const charCount = inputText.length

  const handlePdfSelect = (e) => {
    const file = e.target.files?.[0]
    setPdfError('')

    if (file) {
      if (!file.name.toLowerCase().endsWith('.pdf')) {
        setPdfError('Please select a PDF file')
        setPdfFile(null)
        return
      }
      if (file.size > MAX_PDF_SIZE_BYTES) {
        setPdfError(`File size exceeds ${MAX_PDF_SIZE_MB}MB limit`)
        setPdfFile(null)
        return
      }
      setPdfFile(file)
    }
  }

  const handleAnalyzePdf = async () => {
    if (!pdfFile) {
      setPdfError('Please select a PDF file')
      return
    }
    await onAnalyzePdf(pdfFile)
  }

  const handleClear = () => {
    setInputText('')
    setPdfFile(null)
    setPdfError('')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
    onClear?.()
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-slate-900 mb-6 dark:text-slate-100">Input Text or PDF</h2>

      {/* Textarea */}
      <div className="mb-4">
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste any English text to analyze readability, vocabulary difficulty, and get intelligent simplification..."
          className="input-field resize-none h-64 font-mono text-sm"
        />
        <div className="mt-2 flex justify-between text-sm text-slate-500 dark:text-slate-400">
          <span>{wordCount} words</span>
          <span>{charCount} characters</span>
        </div>
      </div>

      {/* PDF Upload */}
      <div className="mb-6 border-t pt-6">
        <label className="block text-sm font-semibold text-slate-700 mb-3 dark:text-slate-300">
          Upload PDF
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handlePdfSelect}
          disabled={loading}
          className="block w-full cursor-pointer text-sm text-slate-500 file:mr-4 file:cursor-pointer file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:shadow-md transition-all dark:text-slate-400"
        />
        {pdfFile && (
          <p className="mt-2 text-sm text-green-600 dark:text-green-400">✓ Selected: {pdfFile.name}</p>
        )}
        {pdfError && (
          <p className="mt-2 text-sm text-red-600 dark:text-red-400">✗ {pdfError}</p>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => onAnalyzeText(inputText)}
          disabled={loading || !inputText.trim()}
          className="btn-primary"
        >
          {loading ? 'Analyzing Text...' : 'Analyze Text'}
        </button>

        <button
          onClick={handleAnalyzePdf}
          disabled={loading || !pdfFile}
          className="btn-primary"
        >
          {loading ? 'Analyzing PDF...' : 'Analyze PDF'}
        </button>

        <button
          onClick={handleClear}
          disabled={!inputText && !pdfFile && loading}
          className="btn-ghost"
        >
          Clear All
        </button>
      </div>
    </div>
  )
}
