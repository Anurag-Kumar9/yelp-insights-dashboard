# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation and community files for better visibility
- LICENSE file (MIT)
- CONTRIBUTING.md with detailed contribution guidelines
- CODE_OF_CONDUCT.md following Contributor Covenant 2.0
- SECURITY.md with security policy and vulnerability reporting
- Issue templates (Bug Report, Feature Request, Question)
- Pull Request template with checklist
- GitHub Actions workflow for linting
- CITATION.cff for academic citations
- README badges for Python, FastAPI, License, Code Style, and PRs
- Table of Contents in README
- Star History chart in README
- Topics guide for GitHub discoverability

### Changed
- Enhanced README with better structure and navigation
- Improved README with keywords for SEO

## [1.0.0] - Initial Release

### Added
- ETL pipeline for Yelp dataset ingestion (business, review, user data)
- SQLite database schema with optimized indexes
- NLP pipeline with VADER sentiment analysis
- TF-IDF keyword extraction for positive/negative reviews
- K-Means clustering of user profiles into 5 archetypes
- Logistic Regression model for star rating prediction
- FastAPI REST API with async support
- Interactive dashboard UI with vanilla JavaScript
- Performance optimization (43 days → 2 hours pipeline runtime)
- Comprehensive README with architecture diagrams
- Demo GIF showing dashboard in action

### Performance
- Database index optimization: 500× query speedup
- Dashboard load time: < 100ms
- Support for 100+ concurrent users
- Batch ETL processing of 10GB dataset in ~2-4 hours

---

**Note:** This changelog will be updated with each new release.
