/**
 * Utility functions for the AI Insights Blog application
 */

/**
 * Formats a date string into a human-readable format
 * @param {string|Date} date - The date to format (can be string or Date object)
 * @param {string} [locale='en-US'] - The locale to use for formatting
 * @returns {string} Formatted date string (e.g., "January 1, 2023")
 */
export const formatDate = (date, locale = 'en-US') => {
  if (!date) return '';

  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    
    if (isNaN(dateObj.getTime())) {
      throw new Error('Invalid date');
    }

    return new Intl.DateTimeFormat(locale, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }).format(dateObj);
  } catch (error) {
    console.error('Error formatting date:', error);
    return '';
  }
};

/**
 * Validates user input based on specified rules
 * @param {string} input - The input to validate
 * @param {Object} options - Validation options
 * @param {number} [options.minLength=0] - Minimum length required
 * @param {number} [options.maxLength=Infinity] - Maximum length allowed
 * @param {RegExp} [options.pattern] - Regular expression pattern to match
 * @param {boolean} [options.required=false] - Whether the input is required
 * @returns {Object} Validation result { isValid: boolean, message: string }
 */
export const validateInput = (input, options = {}) => {
  const {
    minLength = 0,
    maxLength = Infinity,
    pattern,
    required = false,
  } = options;

  // Handle required field
  if (required && !input?.trim()) {
    return {
      isValid: false,
      message: 'This field is required',
    };
  }

  // Skip further validation if input is empty and not required
  if (!required && !input?.trim()) {
    return {
      isValid: true,
      message: '',
    };
  }

  // Validate length
  if (input.length < minLength) {
    return {
      isValid: false,
      message: `Must be at least ${minLength} characters`,
    };
  }

  if (input.length > maxLength) {
    return {
      isValid: false,
      message: `Must be less than ${maxLength} characters`,
    };
  }

  // Validate pattern if provided
  if (pattern && !pattern.test(input)) {
    return {
      isValid: false,
      message: 'Invalid format',
    };
  }

  return {
    isValid: true,
    message: '',
  };
};

/**
 * Helper function to debounce function calls
 * @param {Function} func - The function to debounce
 * @param {number} delay - The delay in milliseconds
 * @returns {Function} Debounced function
 */
export const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
};

/**
 * Helper function to truncate text with ellipsis
 * @param {string} text - The text to truncate
 * @param {number} maxLength - Maximum length before truncation
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Helper function to generate a unique ID
 * @returns {string} Unique ID
 */
export const generateId = () => {
  return Math.random().toString(36).substring(2, 15) + 
         Math.random().toString(36).substring(2, 15);
};

/**
 * Helper function to capitalize the first letter of a string
 * @param {string} str - The string to capitalize
 * @returns {string} Capitalized string
 */
export const capitalize = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
};

/**
 * Helper function to convert a string to kebab-case
 * @param {string} str - The string to convert
 * @returns {string} kebab-case string
 */
export const toKebabCase = (str) => {
  if (!str) return '';
  return str
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[\s_]+/g, '-')
    .toLowerCase();
};