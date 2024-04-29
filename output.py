import os
import webbrowser
from jinja2 import Environment, FileSystemLoader


# Get the root directory 
def get_root_directory():
    return os.path.dirname(os.path.abspath(__file__))


def save_report(data_summary, filename, filetype):
    base_filename, _ = os.path.splitext(filename)
    output_file = f"{base_filename}_metrics.{filetype}"

    if filetype == 'txt':
        with open(output_file, 'w') as f:
            f.write(f"----- {filename} Metrics -----\n")
            for key, value in data_summary.items():
                f.write(f"{key}: {value}\n")
    elif filetype == 'html':
        root_directory = get_root_directory()
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('base.html')

        # Render the template and provide data context
        html_content = template.render(filename=filename, data_summary=data_summary, root_directory=root_directory)

        # Save the rendered HTML content to the output file
        with open(output_file, 'w') as f:
            f.write(html_content)
    else:
        raise ValueError("Unsupported output type. Please choose either 'txt' or 'html'.")

    print(f"Report saved as {output_file}")

    if filetype == 'html':
        webbrowser.open(output_file)
