import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import GlobalStyle from './styles/GlobalStyle';
import theme from './styles/theme';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import ArticlesPage from './pages/ArticlesPage';
import ArticleDetailPage from './pages/ArticleDetailPage';
import AuthorsPage from './pages/AuthorsPage';
import AuthorDetailPage from './pages/AuthorDetailPage';
import SearchPage from './pages/SearchPage';
import NewsletterPage from './pages/NewsletterPage';
import NotFoundPage from './pages/NotFoundPage';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorBoundary from './components/ErrorBoundary';
import { fetchArticles } from './api/articles';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const initializeApp = async () => {
      try {
        const data = await fetchArticles();
        setArticles(data);
        setIsLoading(false);
      } catch (err) {
        setError(err.message);
        setIsLoading(false);
      }
    };

    initializeApp();
  }, []);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  if (isLoading) {
    return <LoadingSpinner fullPage />;
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Error loading content</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <ThemeProvider theme={isDarkMode ? theme.dark : theme.light}>
      <GlobalStyle />
      <Router>
        <ErrorBoundary>
          <Header isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
          <main>
            <Routes>
              <Route path="/" element={<HomePage articles={articles} />} />
              <Route path="/articles" element={<ArticlesPage articles={articles} />} />
              <Route path="/articles/:slug" element={<ArticleDetailPage />} />
              <Route path="/authors" element={<AuthorsPage />} />
              <Route path="/authors/:id" element={<AuthorDetailPage />} />
              <Route path="/search" element={<SearchPage articles={articles} />} />
              <Route path="/newsletter" element={<NewsletterPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </main>
          <Footer />
        </ErrorBoundary>
      </Router>
    </ThemeProvider>
  );
}

export default App;