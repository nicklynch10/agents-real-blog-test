import React from 'react';
import PropTypes from 'prop-types';

/**
 * Header component for the AI Insights Blog
 * Displays the site navigation, logo, and theme toggle
 */
const Header = ({ siteTitle, onThemeToggle, currentTheme }) => {
  const categories = [
    'Machine Learning',
    'Deep Learning',
    'NLP',
    'Computer Vision',
    'AI Ethics',
    'Robotics'
  ];

  return (
    <header className={`header ${currentTheme}`}>
      <div className="header-container">
        <div className="logo-container">
          <h1 className="logo">
            <a href="/">{siteTitle}</a>
          </h1>
          <p className="tagline">Cutting-edge AI research and insights</p>
        </div>

        <nav className="main-nav">
          <ul className="nav-list">
            <li className="nav-item">
              <a href="/">Home</a>
            </li>
            <li className="nav-item dropdown">
              <span>Categories</span>
              <ul className="dropdown-menu">
                {categories.map((category) => (
                  <li key={category}>
                    <a href={`/category/${category.toLowerCase().replace(' ', '-')}`}>
                      {category}
                    </a>
                  </li>
                ))}
              </ul>
            </li>
            <li className="nav-item">
              <a href="/authors">Authors</a>
            </li>
            <li className="nav-item">
              <a href="/about">About</a>
            </li>
          </ul>
        </nav>

        <div className="header-actions">
          <button
            className="theme-toggle"
            onClick={onThemeToggle}
            aria-label={`Switch to ${currentTheme === 'dark' ? 'light' : 'dark'} mode`}
          >
            {currentTheme === 'dark' ? '☀️' : '🌙'}
          </button>
        </div>
      </div>
    </header>
  );
};

Header.propTypes = {
  siteTitle: PropTypes.string.isRequired,
  onThemeToggle: PropTypes.func.isRequired,
  currentTheme: PropTypes.oneOf(['light', 'dark']).isRequired,
};

Header.defaultProps = {
  siteTitle: 'AI Insights',
};

export default Header;