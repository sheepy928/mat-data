# Contributing Guidelines

Thank you for contributing to our materials science paper reproducibility database! Please follow these guidelines to submit paper reproduction instructions.

## How to Contribute

### Option 1: Use the Online Form (Recommended)

1. Visit our [submission form](https://YOUR_USERNAME.github.io/mat-data/)
2. Fill out all required fields
3. Generate and download your submission file
4. Fork this repository and add the file to `submissions/`
5. Submit a Pull Request

### Option 2: Manual Creation

1. **Fork this repository** to your GitHub account
2. **Create a new file** in the `submissions/` directory with your paper's reproduction data
3. **Submit a Pull Request** with your contribution

## Data Schema

### Required Fields

Every submission must include these fields:

- `username`: Your GitHub username
- `paper_title`: Full title of the paper
- `paper_pdf`: URL to the paper PDF (e.g., arXiv, journal website)
- `identifier`: Paper identifier (e.g., arXiv ID, DOI)
- `claims`: List of reproducible claims with instructions (at least one required)

### Optional Fields

- `code_url`: URL to the code repository
- `data_url`: URL to datasets (if separate from code)

### Claims Structure

Each claim must have:
- `claim`: The specific claim from the paper you're documenting
- `instruction`: A list of step-by-step instructions to reproduce the claim (array of strings)

## File Format

### Supported Formats

- JSON (`.json`)
- YAML (`.yaml` or `.yml`)

### File Naming

- Use descriptive filenames based on the paper
- Only use letters, numbers, underscores, and hyphens
- Examples: `response_matching_2024.json`, `dft-validation-li-s.yaml`

## Examples

See example files in the `submissions/` directory:
- [`example_submission.json`](submissions/example_submission.json)
- [`example_submission.yaml`](submissions/example_submission.yaml)

## Example YAML Structure

```yaml
username: your_github_username
paper_title: "Response Matching for generating materials and molecules"
paper_pdf: "https://arxiv.org/pdf/2405.09057.pdf"
identifier: "2405.09057"
code_url: "https://github.com/yourname/repo"  # Optional
data_url: "https://doi.org/10.5281/zenodo.1234567"  # Optional

claims:
  - claim: "Response Matching can generate Li-S structures that match known structures..."
    instruction:
      - "git checkout 3f4a9b2"
      - "pip install -r requirements.txt"
      - "python predict.py --structure data/some.dat -T 300"
      - "Check output/conductivity.txt; value should be 8.4 ± 0.2 mS cm⁻¹"

  - claim: "DFT validation gives an activation barrier of 0.21 eV."
    instruction:
      - "cd dft/nbarr"
      - "bash run_neb.sh Li10GeP2S12"
      - "python parse_neb.py results/neb.out"
      - "This should give 0.21 ± 0.02 eV"
```

## Validation

Your submission will be automatically validated when you create a Pull Request. The validation checks:

1. File format (must be valid JSON or YAML)
2. All required fields are present and non-empty
3. URLs are properly formatted
4. At least one claim with instructions is provided
5. Username format is valid

## What Happens After Merge

Once your PR is merged:
1. Your submission file will be automatically moved to `data/organized/<your-username>/`
2. The original file in `submissions/` will be removed
3. Multiple submissions from the same user will be grouped together

## Tips for Good Reproduction Instructions

- Be specific about software versions and dependencies
- Include exact commands that can be copy-pasted
- Specify expected outputs and acceptable ranges
- Note computational requirements (time, memory, GPUs)
- Include checksums or commit hashes for reproducibility

## Questions?

If you have questions about the data structure or submission process, please open an issue in this repository.