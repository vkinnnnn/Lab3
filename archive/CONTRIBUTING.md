# Contributing to Complete Document Extractor

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Google Cloud service account with Document AI API

### Local Setup

```bash
# Clone repository
git clone <repo-url>
cd Lab3

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Add service account key
# Place service-account-key.json in Lab3/
```

### Running Locally

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small
- Write descriptive variable names

### Example

```python
def extract_document(
    file_content: bytes,
    mime_type: str,
    filename: str
) -> Dict[str, Any]:
    """
    Extract complete document data.
    
    Args:
        file_content: Binary content of document
        mime_type: MIME type (e.g., 'application/pdf')
        filename: Name of the file
        
    Returns:
        Complete extraction result with accuracy metrics
    """
    # Implementation
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_extractor.py

# Run with coverage
pytest --cov=processing tests/
```

### Writing Tests

- Add tests for new features
- Test edge cases
- Test error handling
- Use descriptive test names

```python
def test_extract_numbers_from_text():
    """Test that all numbers are extracted correctly"""
    text = "The amount is $1,234.56 and 45%"
    numbers = extract_numbers(text)
    assert len(numbers) == 2
    assert numbers[0]["type"] == "currency"
    assert numbers[1]["type"] == "percentage"
```

## Pull Request Process

1. **Update Documentation**: Update README.md if needed
2. **Add Tests**: Include tests for new features
3. **Check Code Style**: Ensure code follows style guidelines
4. **Update CHANGELOG**: Add entry to CHANGELOG.md
5. **Describe Changes**: Write clear PR description
6. **Link Issues**: Reference related issues

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
```

## Reporting Issues

### Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Error messages/logs

### Feature Requests

Include:
- Clear description
- Use case
- Expected behavior
- Alternative solutions considered

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

### Review Criteria

- Code quality and style
- Test coverage
- Documentation
- Performance impact
- Security considerations

## Areas for Contribution

### High Priority

- [ ] Batch processing support
- [ ] Additional language support
- [ ] Performance optimizations
- [ ] Enhanced error handling
- [ ] More comprehensive tests

### Medium Priority

- [ ] UI improvements
- [ ] Additional export formats
- [ ] Custom field training
- [ ] Advanced table analysis
- [ ] Cloud deployment guides

### Documentation

- [ ] API examples
- [ ] Tutorial videos
- [ ] Use case documentation
- [ ] Troubleshooting guide
- [ ] Performance tuning guide

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute!
