# Security Policy

## Supported Versions

This project is actively maintained. We recommend using the latest version from the `master` branch.

| Version | Supported          |
| ------- | ------------------ |
| Latest (master)   | :white_check_mark: |
| Older commits     | :x:                |

## Reporting a Vulnerability

We take the security of Yelp Insights Dashboard seriously. If you discover a security vulnerability, please follow these steps:

### 🔒 Private Disclosure

**DO NOT** open a public issue for security vulnerabilities.

Instead, please report security issues privately:

1. **Email**: Contact [@Anurag-Kumar9](https://github.com/Anurag-Kumar9) via GitHub
2. **Include**: 
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### ⏱️ Response Timeline

- **Initial Response**: Within 48 hours of report
- **Status Update**: Within 7 days with assessment
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next planned release

### 🛡️ Security Best Practices

When using this project:

1. **Don't commit sensitive data**
   - Never include API keys, passwords, or tokens in code
   - Use environment variables for sensitive configuration
   - Add `.env` files to `.gitignore`

2. **Database security**
   - SQLite database may contain user data - protect it appropriately
   - Don't expose the database file publicly
   - Consider encryption for production deployments

3. **API security** (for production use)
   - Implement authentication/authorization
   - Add rate limiting to prevent abuse
   - Use HTTPS in production
   - Validate and sanitize all inputs
   - Enable CORS only for trusted domains

4. **Dependencies**
   - Regularly update dependencies
   - Review `requirements.txt` for known vulnerabilities
   - Use tools like `pip-audit` or `safety` to scan dependencies

5. **Deployment**
   - Don't run with debug mode in production
   - Use a reverse proxy (nginx/Apache)
   - Implement logging and monitoring
   - Set appropriate file permissions

## Known Security Considerations

### Current Implementation (Development/Demo)

This project is designed as a **development/demo application** with the following security considerations:

1. **No Authentication**: The API is open and doesn't require authentication
   - ✅ Acceptable for local development and demos
   - ❌ Not suitable for production without adding auth

2. **SQLite Database**: Embedded database without user authentication
   - ✅ Fine for single-user local deployment
   - ❌ Consider PostgreSQL/MySQL for multi-user production

3. **No Input Validation**: Minimal validation on prediction endpoint
   - ⚠️ Add input sanitization for production use

4. **CORS**: May be configured to allow all origins
   - ⚠️ Restrict to specific domains in production

### Recommended for Production

If deploying this to production, consider:

- [ ] Add authentication (OAuth2, JWT)
- [ ] Implement rate limiting
- [ ] Add input validation and sanitization
- [ ] Use HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Add logging and monitoring
- [ ] Use a production WSGI server (Gunicorn + Uvicorn)
- [ ] Implement database access controls
- [ ] Add API versioning
- [ ] Set up automated security scanning in CI/CD

## Disclosure Policy

- We will acknowledge receipt of your report within 48 hours
- We will confirm the vulnerability and determine its severity
- We will work on a fix and release it appropriately
- We will credit you for the discovery (unless you prefer anonymity)
- After the fix is deployed, we will publish a security advisory

## Security Updates

Security updates will be released as:
- Patch commits to the main branch
- GitHub Security Advisories for significant issues
- Updated documentation if configuration changes are needed

## Contact

For security concerns, reach out via:
- GitHub: [@Anurag-Kumar9](https://github.com/Anurag-Kumar9)

Thank you for helping keep Yelp Insights Dashboard secure! 🔒
