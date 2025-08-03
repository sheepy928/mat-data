# Materials Science Paper Reproducibility Pipeline

## Overview

This repository implements an automated pipeline for crowdsourcing reproducibility instructions for materials science papers. Contributors submit structured data about papers and their reproducible claims, which are automatically validated and organized.

## Pipeline Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Contributor   │────▶│   GitHub Fork    │────▶│   Pull Request  │
│  (Uses Web Form)│     │ (adds to         │     │                 │
└─────────────────┘     │  submissions/)   │     └────────┬────────┘
                        └──────────────────┘              │
                                                          ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │  File Organized  │◀────│  PR Validation  │
                        │  by Username     │     │  (GitHub Action)│
                        │ (data/organized/)│     └────────┬────────┘
                        └──────────────────┘              │
                                ▲                         ▼
                                │                ┌─────────────────┐
                        ┌───────┴─────────┐     │   Review &      │
                        │ Post-Merge      │◀────│   Merge         │
                        │ Organization    │     │                 │
                        │ (GitHub Action) │     └─────────────────┘
                        └─────────────────┘
```

## Components

### 1. Web Submission Form
- **URL**: `https://YOUR_USERNAME.github.io/mat-data/`
- **Purpose**: User-friendly interface for creating submission files
- **Features**:
  - Dynamic form with validation
  - Support for multiple claims and instruction steps
  - Generates JSON/YAML files
  - Copy to clipboard and download functionality

### 2. Data Schema

#### Required Fields:
- `username`: GitHub username of the contributor
- `paper_title`: Full title of the paper
- `paper_pdf`: URL to the paper (PDF or webpage)
- `identifier`: Unique identifier (arXiv ID, DOI, etc.)
- `code_url`: Repository URL containing the code
- `claims`: Array of reproducible claims

#### Optional Fields:
- `data_url`: Separate dataset URL if not included in code repository

#### Claims Structure:
```yaml
claims:
  - claim: "Description of the scientific claim"
    instruction:
      - "Step 1: git clone https://..."
      - "Step 2: pip install -r requirements.txt"
      - "Step 3: python run_experiment.py"
      - "Step 4: Check results match paper's claim"
```

### 3. Validation Script
- **Location**: `scripts/validate_submission.py`
- **Validates**:
  - File format (JSON/YAML syntax)
  - Required fields presence
  - URL format validation
  - Username format (alphanumeric + hyphen/underscore)
  - Claims structure (at least one claim with instructions)

### 4. GitHub Actions

#### PR Validation (`validate-pr.yml`)
- **Triggers**: On pull requests modifying `submissions/**`
- **Actions**:
  1. Checks out PR code
  2. Installs Python dependencies
  3. Identifies changed submission files
  4. Runs validation script on each file
  5. Posts validation results as PR comment

#### Post-Merge Organization (`organize-merged.yml`)
- **Triggers**: On push to main branch with changes to submission files
- **Actions**:
  1. Runs organization script
  2. Moves files from `submissions/` to `data/organized/<username>/`
  3. Commits and pushes changes automatically
  4. Creates summary in GitHub Actions

### 5. Organization Script
- **Location**: `scripts/organize_by_username.py`
- **Functions**:
  - Reads username from submission files
  - Creates user-specific directories
  - Handles filename conflicts
  - Moves files to organized structure
  - Removes processed files from submissions

## Submission Workflow

### For Contributors:

1. **Option A - Web Form (Recommended)**:
   ```
   Visit form → Fill fields → Generate file → Download → Fork repo → 
   Add to submissions/ → Create PR
   ```

2. **Option B - Manual**:
   ```
   Fork repo → Create JSON/YAML → Add to submissions/ → Create PR
   ```

### Automated Processing:

1. **PR Stage**:
   - Validation runs automatically
   - Bot comments with validation results
   - Contributor fixes any issues
   - Maintainer reviews and merges

2. **Post-Merge**:
   - Files automatically moved to `data/organized/<username>/`
   - Original files removed from `submissions/`
   - Changes committed back to repository

## Directory Structure

```
mat-data/
├── .github/workflows/
│   ├── validate-pr.yml      # PR validation workflow
│   ├── organize-merged.yml  # Post-merge organization
│   └── deploy-pages.yml     # GitHub Pages deployment
├── data/
│   └── organized/           # Organized submissions by username
│       └── <username>/      # User-specific directories
├── docs/                    # GitHub Pages website
│   ├── index.html          # Submission form
│   ├── style.css           # Form styling
│   └── script.js           # Form logic
├── scripts/
│   ├── validate_submission.py    # Validation logic
│   └── organize_by_username.py   # Organization logic
├── submissions/             # Incoming submissions
│   └── .gitkeep            # Placeholder file
└── tests/                   # Test suite
    └── test_validation.py   # Validation tests
```

## Example Submission

```json
{
  "username": "researcher123",
  "paper_title": "Response Matching for generating materials and molecules",
  "paper_pdf": "https://arxiv.org/pdf/2405.09057.pdf",
  "identifier": "2405.09057",
  "code_url": "https://github.com/example/response-matching",
  "data_url": "https://doi.org/10.5281/zenodo.1234567",
  "claims": [
    {
      "claim": "Response Matching can generate Li-S structures that match known structures in the Materials Project database",
      "instruction": [
        "git checkout 3f4a9b2",
        "pip install -r requirements.txt",
        "python predict.py --structure data/some.dat -T 300",
        "Check output/conductivity.txt; value should be 8.4 ± 0.2 mS cm⁻¹"
      ]
    }
  ]
}
```

## Benefits

1. **For Contributors**:
   - Simple web form interface
   - No need to understand JSON/YAML syntax
   - Automatic validation feedback
   - Clear submission guidelines

2. **For Maintainers**:
   - Automated validation reduces review burden
   - Consistent data format
   - Automatic organization by contributor
   - Scalable to many submissions

3. **For Users**:
   - Structured, searchable reproduction instructions
   - Verified data format
   - Easy to find submissions by contributor
   - Machine-readable for further processing

## Setup Instructions

1. Fork this repository
2. Enable GitHub Pages (Settings → Pages → Source: GitHub Actions)
3. Update URLs in README.md and CONTRIBUTING.md
4. Repository is ready to accept submissions

## Future Enhancements

- Search functionality across submissions
- API endpoint for programmatic access
- Integration with paper databases
- Automated testing of reproduction instructions
- Citation tracking and metrics