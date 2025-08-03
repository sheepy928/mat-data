# Materials Science Paper Reproducibility Database

This repository implements an automated crowdsourcing system for collecting reproducibility instructions for materials science papers using GitHub Actions.

## Overview

Contributors submit data through Pull Requests, which are automatically validated and organized by username after merge.

## Repository Structure

```
.
├── submissions/           # Directory for new data submissions
├── data/
│   └── organized/        # Organized data by username
├── scripts/              # Python scripts for validation and organization
├── .github/workflows/    # GitHub Actions workflows
└── tests/               # Test files
```

## How It Works

1. **Submission**: Contributors create a Pull Request with their data file in the `submissions/` directory
2. **Validation**: GitHub Action automatically validates the submission format and required fields
3. **Review**: Maintainers review and merge valid submissions
4. **Organization**: After merge, files are automatically moved to `data/organized/<username>/`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed submission guidelines.

### Easy Submission Form

Use our [online submission form](https://YOUR_USERNAME.github.io/mat-data/) to easily create properly formatted submission files without worrying about JSON/YAML syntax.

## Scripts

### `scripts/validate_submission.py`

Validates submission files for required fields and correct format.

```bash
python scripts/validate_submission.py <file_path> [required_fields...]
```

### `scripts/organize_by_username.py`

Organizes submission files into username-based directories.

```bash
python scripts/organize_by_username.py <source_dir> <target_dir>
```

## GitHub Actions

- **`validate-pr.yml`**: Runs on Pull Requests to validate submissions
- **`organize-merged.yml`**: Runs after merge to organize files by username

## Requirements

- Python 3.9+
- PyYAML (for YAML file support)

## License

[Your license here]