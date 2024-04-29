# pyMetrics
SENG4260 Final Project

pyMetrics is a Python tool for calculating various code metrics, generating coverage reports, and saving them in either text or HTML format.

## Features

- **Code Metrics:** Calculates multiple metrics, including lines of code, cyclomatic complexity, Halstead measures, and maintainability index.
- **Coverage Reports:** Runs tests and generates coverage data, including defect density.
- **Reports:** Outputs metrics and coverage data in either `.txt` or `.html` formats.

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/coradora/pyMetrics.git
    ```
2. Create and enter the virtual environment
    ```shell
    python -m venv venv
    python source/bin/activate
    ```
3. Install the required Python packages:

    ```shell
    pip install -r requirements.txt
    ```

## Usage

To run pyMetrics on a specific Python file or directory:

```shell
python main.py <path_to_file_or_directory> --output_type txt|html
```

## Example

To analyze the code in the examples/ex1 directory and generate an HTML report:

```shell
python main.py examples/ex1 --output_type html
```


