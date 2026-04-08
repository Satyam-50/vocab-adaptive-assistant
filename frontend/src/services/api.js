import axios from 'axios'

const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  import.meta.env.REACT_APP_API_URL ||
  'http://127.0.0.1:8000'

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

/**
 * Analyze text for difficulty level, simplification, and vocabulary
 * @param {string} text - Input text to analyze
 * @returns {Promise} Analysis result with level, simplified_text, difficult_words
 */
export const analyzeText = async (text) => {
  try {
    if (!text || !text.trim()) {
      throw new Error('Text cannot be empty')
    }
    const response = await client.post('/analyze', { text: text.trim() })
    return response.data
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.message ||
      'Failed to analyze text. Please check the backend service.'
    throw new Error(message)
  }
}

/**
 * Analyze PDF file for difficulty level, simplification, and vocabulary
 * @param {File} file - PDF file to analyze
 * @returns {Promise} Analysis result with level, simplified_text, difficult_words
 */
export const analyzePdf = async (file) => {
  try {
    if (!file) {
      throw new Error('File cannot be empty')
    }
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      throw new Error('Only PDF files are supported')
    }

    const formData = new FormData()
    formData.append('pdf_file', file)

    const response = await client.post('/analyze/pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.message ||
      'Failed to analyze PDF. Please check the file and backend service.'
    throw new Error(message)
  }
}

/**
 * Health check endpoint
 * @returns {Promise} Health status
 */
export const healthCheck = async () => {
  try {
    const response = await client.get('/health')
    return response.data
  } catch (error) {
    throw new Error('Backend service is unavailable')
  }
}

export default client
