import argparse
import os
from metrics import *

def parse_arguments():
    parser = argparse.ArgumentParser(prog='pyMetrics',
                                     description='Calculate Metric Data from Source Code.')
    parser.add_argument('path', type=str, help='The path of the source code file or directory to analyze')
    parser.add_argument('--output_type', required=False, type=str, default='txt',
                        help='The file type of the output report, such as txt, html, and csv.')
    args = parser.parse_args()
    return args

# Class definition for Source
# Easier management of larger directories & reporting

class Source:
    def __init__(self, filename, filetype):
        self._filename = filename
        self._filetype = filetype
        self._lines_of_code = 0
        self._cyc_complexity = 0
        self._halstead_measure_N = 0
        self._halstead_measure_n = 0
        self._halstead_volume = 0
        self._maintainability_index = 0
        self._maintainability_flag = 0

    # Print and return calculated data
    def retrieve_data(self):
        # Prepare a summary of metrics in a dictionary
        data_summary = {
            "Filename": self._filename,
            "Lines of Code": self._lines_of_code,
            "Cyclomatic Complexity": self._cyc_complexity,
            "Halstead Total Elements (N)": self._halstead_measure_N,
            "Halstead Total Unique Elements (μ)": self._halstead_measure_n,
            "Halstead Volume": self._halstead_volume,
            "Maintainability Index": self._maintainability_index,
            "Flag": self._maintainability_flag
        }
        
        # Print the summary
        print(f"----- {self._filename} Metrics -----")
        for key, value in data_summary.items():
            print(f"{key}: {value}")
        
        # Return the summary dictionary
        return data_summary

    def calculate(self):
        self._lines_of_code = count_lines_of_code(self._filename)
        self._cyc_complexity = cyclomatic_complexity(self._filename)
        self._halstead_measure_N, self._halstead_measure_n = halstead_measure(self._filename)
        self._halstead_volume = halstead_volume(self._halstead_measure_N, self._halstead_measure_n)
        self._maintainability_index, self._maintainability_flag = maintainability_index(self._halstead_volume, self._cyc_complexity, self._lines_of_code)

def process_file(filepath, filetype):
    x = Source(filepath, filetype)
    x.calculate()
    data = x.retrieve_data()

def main():
    args = parse_arguments()
    if os.path.isdir(args.path):
        # Iterate over all files in the directory
        for root, dirs, files in os.walk(args.path):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    process_file(filepath, args.output_type)
    else:
        process_file(args.path, args.output_type)

if __name__ == "__main__":
    main()
