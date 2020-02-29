import subprocess
import tempfile


LATEX_TEMPLATE = r"""\documentclass[varwidth=true,border=5pt]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\begin{document}
$%s$
\end{document}"""


def exec(cmd, capture_output=True):
    log = subprocess.run(cmd, capture_output=capture_output)
    if log.returncode:
        print('\nAn error occured when running the command "' + cmd[0] + '"')
        if capture_output:
            print("This is the error message:\n")
            print(log.stdout.decode('utf-8'))
    return log.returncode == 0


def display_tex(latex):
    # generate a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = f'{tmpdirname}/out'

        # create a .tex file
        with open(f'{filename}.tex', 'w') as f:
            f.write(LATEX_TEMPLATE % latex)

        latex_cmd = ['pdflatex', '-interaction=nonstopmode', 
                     f'-output-directory={tmpdirname}', f'{filename}.tex']
        convert_cmd = ['convert', '-quiet', '-density', '2000', '-quality', '90',
                       '-alpha', 'off', '-resize', '25%', f'{filename}.pdf', f'{filename}.png']
        display_cmd = ['imgcat', f'{filename}.png']

        # generate a .pdf from the .tex
        if exec(latex_cmd):
            # generate a .png from the .pdf
            if exec(convert_cmd):
                # display the .png
                exec(display_cmd, capture_output=False)


if __name__ == "__main__":
    while True:
        str_in = input("Enter LaTeX: ")
        if not str_in: 
            break
        print()
        display_tex(str_in)
        print()