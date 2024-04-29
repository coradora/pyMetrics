# Main.py

import argparse
import os
from metrics import *
from coverage_handler import *
from output import save_report

def parse_arguments():
    parser = argparse.ArgumentParser(prog='pyMetrics',
                                     description='Calculate Metric Data from Source Code.')
    parser.add_argument('path', type=str, help='The path of the source code file or directory to analyze')
    parser.add_argument('--output_type', required=False, type=str, default='txt',
                        help='The file type of the output report, such as txt or html.')
    args = parser.parse_args()
    return args

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
        self.statement_coverage = 0
        self.defect_density = 0
        self.internal_reuse = 0

    def calculate(self):
        self._lines_of_code = count_lines_of_code(self._filename)
        self._cyc_complexity, self._internal_reuse = cyclomatic_complexity_with_reuse(self._filename)
        self._halstead_measure_N, self._halstead_measure_n = halstead_measure(self._filename)
        self._halstead_volume = halstead_volume(self._halstead_measure_N, self._halstead_measure_n)
        self._maintainability_index, self._maintainability_flag = maintainability_index(self._halstead_volume, self._cyc_complexity, self._lines_of_code)

    def coverage(self):
        self.statement_coverage, self.defect_density = run_coverage_for_file(self._filename)

    def retrieve_data(self):
        data_summary = {
            "----- Metrics -----": "",
            "Lines of Code": self._lines_of_code,
            "Cyclomatic Complexity": self._cyc_complexity,
            "Halstead Total Elements (N)": self._halstead_measure_N,
            "Halstead Total Unique Elements (μ)": self._halstead_measure_n,
            "Halstead Volume": self._halstead_volume,
            "Internal Reuse": self._internal_reuse,
            "Maintainability Index": self._maintainability_index,
            "Flag": self._maintainability_flag,
            "----- Coverage -----": "",
            "Statement Coverage": self.statement_coverage,
            "Defect Density": self.defect_density
        }

        # Print data selectively
        for key, value in data_summary.items():
            if value != "":  # Print only data entries
                print(f"{key}: {value}")
            else:  # Print headings or special entries directly
                print(f"{key}")

        return data_summary

    def process(self):
        self.calculate()
        self.coverage()
        print(f"\n{self._filename}")
        data_summary = self.retrieve_data()

        save_report(data_summary, self._filename, self._filetype)

def main():
    args = parse_arguments()
    if os.path.isdir(args.path):
        for root, dirs, files in os.walk(args.path):
            for file in files:
                if file.endswith('.py') and not file.endswith('_test.py'):
                    filepath = os.path.join(root, file)
                    source = Source(filepath, args.output_type)
                    source.process()
    else:
        if not args.path.endswith('_test.py'):
            source = Source(args.path, args.output_type)
            source.process()

if __name__ == "__main__":
    main()
