/**
 * API Service for AI Insights Blog
 * Handles all API calls to the backend with proper error handling
 * and request/response transformations.
 */

const BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://api.ai-insights-blog.com/v1';

/**
 * Makes an API call with proper error handling and headers
 * @param {string} endpoint - API endpoint (e.g., '/posts')
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {object} data - Request payload (optional)
 * @param {object} headers - Additional headers (optional)
 * @returns {Promise} - Resolves with response data or rejects with error
 */
export const apiCall = async (endpoint, method = 'GET', data = null, headers = {}) => {
  const url = `${BASE_URL}${endpoint}`;
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    credentials: 'include',
  };

  if (data) {
    config.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `API request failed with status ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

/**
 * Fetches data from the API with caching and retry logic
 * @param {string} endpoint - API endpoint
 * @param {object} options - Fetch options
 * @param {number} retries - Number of retry attempts
 * @returns {Promise} - Resolves with fetched data
 */
export const fetchData = async (endpoint, options = {}, retries = 2) => {
  try {
    const response = await apiCall(endpoint, 'GET', null, options.headers);
    return response;
  } catch (error) {
    if (retries > 0) {
      console.log(`Retrying ${endpoint}... (${retries} attempts left)`);
      return fetchData(endpoint, options, retries - 1);
    }
    throw error;
  }
};

// Specific API methods for common endpoints
export const api = {
  // Articles
  getArticles: (params = {}) => fetchData(`/posts?${new URLSearchParams(params)}`),
  getArticleById: (id) => fetchData(`/posts/${id}`),
  getFeaturedArticles: () => fetchData('/posts/featured'),
  getRelatedArticles: (id) => fetchData(`/posts/${id}/related`),
  searchArticles: (query) => fetchData(`/posts/search?query=${encodeURIComponent(query)}`),

  // Categories
  getCategories: () => fetchData('/categories'),
  getArticlesByCategory: (categoryId) => fetchData(`/categories/${categoryId}/posts`),

  // Authors
  getAuthors: () => fetchData('/authors'),
  getAuthorById: (id) => fetchData(`/authors/${id}`),

  // Newsletter
  subscribeToNewsletter: (email) => apiCall('/newsletter/subscribe', 'POST', { email }),

  // Analytics
  trackArticleView: (articleId) => apiCall('/analytics/view', 'POST', { articleId }),
};

export default api;