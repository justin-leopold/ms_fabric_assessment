# PowerBI Assessment Python Package

A comprehensive toolkit for assessing PowerBI assets, reports, and datasets. This repository provides tools to evaluate, analyze, and optimize your PowerBI implementations.

## Overview

The PowerBI Assessment package provides automated tools to:
- Scan and analyze PowerBI reports and datasets
- Identify performance bottlenecks and optimization opportunities
- Generate assessment reports with recommendations
- Validate compliance with best practices

## Prerequisites

- Python 3.7 or higher
- pip package manager
- Access to PowerBI assets you want to assess

## Installation

### From PyPI (recommended)

```shell
pip install fabric-audit
```

### From Source

1. Clone this repository:
```shell
git clone https://github.com/your-organization/entdata-pbi-assessment-package-py.git
cd entdata-pbi-assessment-package-py
```

2. Create and activate a virtual environment:
```shell
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package in development mode:
```shell
pip install -e .
```

### Using Pre-built Wheel

If you have a pre-built wheel file:

```shell
pip install fabric_audit-1.14-py3-none-any.whl
```

## Using an Existing Virtual Environment

If you have a pre-configured virtual environment:

```shell
source fabric_audit-1.14-py3-none-any/.venv/bin/activate
```

## Usage

```python
from fabric_audit import PowerBIAssessor

# Initialize the assessor
assessor = PowerBIAssessor()

# Run assessment on a report
results = assessor.assess_report("path/to/report.pbix")

# Generate assessment report
assessor.generate_report(results, "assessment_report.html")
```

## Development

### Setting up Development Environment

```shell
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Running Tests

```shell
pytest
```

### Building the Package

After making changes to the codebase, rebuild the package:

```shell
python -m build --wheel
```

This will generate a new wheel file in the `dist/` directory.

## Troubleshooting

- **ImportError**: Ensure you have activated the virtual environment
- **Missing Dependencies**: Run `pip install -e .` to install all required packages
- **Permission Issues**: Use `sudo` or contact your system administrator

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or support, please contact justinaleopold@gmail.com.