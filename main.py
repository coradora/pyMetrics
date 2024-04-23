import argparse
import os
from metrics import count_lines_of_code, cyclomatic_complexity

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
        self.filename = filename
        self.filetype = filetype
        self.lines_of_code = 0
        self.cyc_complexity = 0

    # 
    def retrieve_data(self):
        print(f"----- {self.filename} Metrics -----")
        print(f"Lines of Code: {self.lines_of_code}")
        print(f"Cyclomatic Complexity: {self.cyc_complexity}\n")
        return (self.filename, self.filetype, self.lines_of_code, self.cyc_complexity)

    def calculate(self):
        self.lines_of_code = count_lines_of_code(self.filename)
        self.cyc_complexity = cyclomatic_complexity(self.filename)

def process_file(filepath, filetype):
    x = Source(filepath, filetype)
    x.calculate()
    x.retrieve_data()
    #print(x.retrieve_data())

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
