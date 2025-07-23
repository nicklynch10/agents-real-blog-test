import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  test('renders homepage header', () => {
    render(<App />);
    const headerElement = screen.getByText(/AI Insights Blog/i);
    expect(headerElement).toBeInTheDocument();
  });

  test('renders navigation links', () => {
    render(<App />);
    const homeLink = screen.getByText(/Home/i);
    const articlesLink = screen.getByText(/Articles/i);
    const aboutLink = screen.getByText(/About/i);
    
    expect(homeLink).toBeInTheDocument();
    expect(articlesLink).toBeInTheDocument();
    expect(aboutLink).toBeInTheDocument();
  });

  test('renders theme toggle button', () => {
    render(<App />);
    const themeToggle = screen.getByLabelText(/Toggle dark mode/i);
    expect(themeToggle).toBeInTheDocument();
  });

  test('renders newsletter signup form', () => {
    render(<App />);
    const newsletterHeader = screen.getByText(/Stay Updated/i);
    const emailInput = screen.getByPlaceholderText(/your@email.com/i);
    const subscribeButton = screen.getByText(/Subscribe/i);
    
    expect(newsletterHeader).toBeInTheDocument();
    expect(emailInput).toBeInTheDocument();
    expect(subscribeButton).toBeInTheDocument();
  });

  test('renders footer content', () => {
    render(<App />);
    const copyrightText = screen.getByText(/© \d{4} AI Insights Blog/i);
    const socialLinks = screen.getAllByRole('link', { name: /twitter|linkedin|reddit/i });
    
    expect(copyrightText).toBeInTheDocument();
    expect(socialLinks.length).toBeGreaterThan(0);
  });

  test('renders loading state initially', () => {
    render(<App />);
    const loadingIndicator = screen.getByTestId('loading-indicator');
    expect(loadingIndicator).toBeInTheDocument();
  });
});