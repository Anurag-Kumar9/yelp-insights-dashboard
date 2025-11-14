# Contributing to Yelp Insights Dashboard

Thank you for your interest in contributing! 🎉 This project welcomes contributions from everyone.

## 🌟 How You Can Contribute

### Areas for Improvement

We're particularly interested in contributions in these areas:

- **Frontend**: Add charts (Chart.js/D3.js), filters, pagination, responsive design
- **Backend**: Implement caching (Redis), rate limiting, authentication, advanced analytics
- **Machine Learning**: Add topic modeling (LDA), aspect-based sentiment, transformer models
- **DevOps**: Docker containerization, CI/CD pipeline, deployment guides
- **Documentation**: Tutorials, API examples, architecture explanations
- **Performance**: Query optimization, connection pooling, caching strategies
- **Testing**: Unit tests, integration tests, performance benchmarks

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/yelp-insights-dashboard.git
cd yelp-insights-dashboard

# Add upstream remote
git remote add upstream https://github.com/Anurag-Kumar9/yelp-insights-dashboard.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv restaurent
source restaurent/bin/activate  # On Windows: restaurent\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download Yelp dataset (see README.md for details)
# Run the offline pipeline (see README.md Step 2)
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small (single responsibility)

### Commit Messages

Write clear, concise commit messages:

```
Add caching layer for restaurant endpoints

- Implement Redis caching for top 100 restaurants
- Add cache invalidation on data updates
- Reduce average response time from 100ms to 15ms
```

Format: `<Type>: <Short description>` (50 chars or less)

Types: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`

### Testing

- Test your changes locally before submitting
- Ensure existing functionality still works
- Add tests for new features when applicable
- Verify the dashboard loads and displays data correctly

### Documentation

- Update README.md if you change functionality
- Add inline comments for complex logic
- Update API documentation for new endpoints
- Include examples in docstrings

## 🔄 Pull Request Process

1. **Update your fork** with the latest changes from upstream:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

2. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** from your fork to the main repository

4. **In your PR description**, include:
   - What problem does this solve?
   - What changes were made?
   - How to test the changes?
   - Screenshots (if UI changes)
   - Related issue numbers (if applicable)

5. **Wait for review** - maintainers will review and provide feedback

6. **Make requested changes** if needed:
   ```bash
   # Make changes
   git add .
   git commit -m "Address review feedback"
   git push origin feature/your-feature-name
   ```

## 🐛 Reporting Bugs

Found a bug? Please open an issue with:

- **Clear title** describing the problem
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, dataset size)
- **Error messages** or logs (if applicable)
- **Screenshots** (if UI-related)

## 💡 Suggesting Enhancements

Have an idea? Open an issue with:

- **Clear description** of the enhancement
- **Use case** - why is this valuable?
- **Proposed solution** (if you have one)
- **Alternative solutions** considered

## 📋 Code Review Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] Changes are focused and minimal
- [ ] No debugging code or commented-out code
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Changes don't break existing functionality
- [ ] No sensitive data (API keys, passwords) in code

## 🤝 Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers get started
- Credit others for their ideas
- Focus on technical merit

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

Feel free to:
- Open an issue for discussion
- Reach out to [@Anurag-Kumar9](https://github.com/Anurag-Kumar9)

Thank you for making this project better! 🙏
