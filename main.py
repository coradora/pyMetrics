import argparse
from metrics import count_lines_of_code, cyclomatic_complexity

def parse_arguments():
    # Create the parser
    parser = argparse.ArgumentParser(prog = 'pyMetrics', \
        description='Calculate Metric Data from Source Code.')

    # Add the positional argument for the source code filename
    parser.add_argument('filename', type=str, help='The filename of the source code to analyze')
    parser.add_argument('--output_type', required=False, type=str, help='The file type of the output report, such as txt, html, and csv.')

    # Parse the command line arguments
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
        print(f"Cyclomatic Complexity: {self.cyc_complexity}")
        return (self.filename, self.filetype, self.lines_of_code, self.cyc_complexity)

    def calculate(self):
        self.lines_of_code = count_lines_of_code(self.filename)
        self.cyc_complexity = cyclomatic_complexity(self.filename)

def main():
    args = parse_arguments()
    x = Source(args.filename, args.output_type)
    x.calculate()
    print(x.retrieve_data())

if __name__ == "__main__":
    main()
