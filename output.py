import os

def save_report(data_summary, filename, filetype):
    """
    Saves the provided data summary into a specified format.

    Args:
        data_summary (dict): The summary of metrics to save.
        filename (str): The base filename for the output file.
        filetype (str): The type of output report ('txt' or 'html').
    """
    base_filename, _ = os.path.splitext(filename)
    output_file = f"{base_filename}_metrics.{filetype}"

    if filetype == 'txt':
        with open(output_file, 'w') as f:
            f.write(f"----- {filename} Metrics -----\n")
            for key, value in data_summary.items():
                f.write(f"{key}: {value}\n")
    elif filetype == 'html':
        with open(output_file, 'w') as f:
            f.write(f"<html><body><h2>{filename} Metrics</h2><ul>")
            for key, value in data_summary.items():
                f.write(f"<li>{key}: {value}</li>")
    else:
        raise ValueError("Unsupported output type. Please choose either 'txt' or 'html'.")

    print(f"Report saved as {output_file}")
