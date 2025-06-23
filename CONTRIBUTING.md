# Contributing to TimestringPy

Thank you for your interest in contributing to TimestringPy! We welcome contributions from everyone, whether you're fixing a bug, adding a feature, or improving documentation.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- A GitHub account

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/TimestringPy.git
   cd TimestringPy
   ```
3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Write clear, descriptive variable and function names
- Keep functions focused and single-purpose
- Use docstrings for all public functions and classes

### Commit Messages

Use clear and descriptive commit messages:

- Start with `feat`, `fix`, `docs`, `refactor` or `test` to indicate the type of change
- Use the present tense ("Add feature" not "Added feature")
- Be concise but descriptive in the first line (max 50 characters)

  - Use the body for detailed explanations if necessary

- Use bullet points to summarize changes in the body
- Write a meaningful description of what the commit does and why it is necessary

Example:

```
feat: add support for custom time units

- Add `custom_units` parameter to `parse_timestring`
- Allow users to define their own time units
- Update documentation with examples

This change allows users to specify custom time units
when parsing timestrings, enhancing flexibility and usability.
```

### Forking and Branching

To make changes, please fork the repository and after you're done with your changes, create a pull request.

## Testing

### Running Tests

Run the test suite before submitting any changes:

```bash
# All tests
python -m unittest discover
# Specific test module
python -m unittest timestring.test_init.TestParseTimestring.test_basic_parsing
```

### Writing Tests

- Write tests for all new functionality
- Follow the existing test structure in `timestring/test_init.py`
- Use descriptive test method names that explain what is being tested
- Include both positive and negative test cases
- Test edge cases and error conditions

Example test structure:

```python
def test_new_feature(self):
    """Test description of what this test verifies"""
    # Arrange
    input_value = "test input"
    expected_result = 42

    # Act
    result = parse_timestring(input_value)

    # Assert
    self.assertEqual(result, expected_result)

    # Or if you want to be shorter
    self.assertEqual(parse_timestring("test input"), 42)
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- A clear description of the bug
- Steps to reproduce the issue
- Expected vs. actual behavior
- Python version and operating system
- Minimal code example that demonstrates the issue

### Feature Requests

For new features:

- Describe the feature and its use case
- Explain why it would be valuable to other users
- Consider backwards compatibility
- Provide examples of how the feature would be used

### Code Contributions

1. **Start with an issue**: For significant changes, create an issue first to discuss the approach
2. **Write tests**: All new code should include appropriate tests
3. **Update documentation**: Update README.md or docstrings as needed
4. **Maintain backwards compatibility**: Avoid breaking existing APIs unless absolutely necessary

## Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the guidelines above
3. **Write or update tests** for your changes
4. **Run the test suite** and ensure all tests pass
5. **Update documentation** if necessary
6. **Submit a pull request** with:
   - Clear title and description
   - Reference to any related issues
   - List of changes made
   - Screenshots or examples if applicable

### Pull Request Template

```
## Description

Brief description of changes made.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing

- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Related Issues

Fixes #<issue number>

## Additional Notes

Any additional information or context.
```

## Code Review Process

- All submissions require review before merging
- Reviews focus on code quality, functionality, and adherence to guidelines
- Be open to feedback and willing to make changes
- Reviewers will be constructive and respectful

## Documentation

- Keep README.md up to date with new features
- Update docstrings for any modified functions
- Include code examples for new functionality
- Consider adding usage examples to the README

## Questions and Support

If you have questions about contributing:

- Check existing issues and discussions
- Create a new discussion in the [`Questions` category](https://github.com/The-LukeZ/TimestringPy/discussions/new?category=questions)
- Be specific about what you need help with

## Recognition

Contributors will be recognized in:

- Git commit history
- Release notes for significant contributions
- Acknowledgments in documentation

## Code of Conduct

Be respectful and professional in all interactions. We want to maintain a welcoming environment for contributors of all skill levels.

Thank you for contributing to TimestringPy! Your contributions help make this project better for everyone.
