import subprocess
import time
import tempfile


LATEX_TEMPLATE = r"""\documentclass[varwidth=true,border=5pt]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\begin{document}
$%s$
\end{document}"""


class tcolor:
    class fg:
        DEFAULT = '\033[39m'
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        LIGHT_GRAY = '\033[37m'
        DARK_GRAY = '\033[90m'
        LIGHT_RED = '\033[91m'
        LIGHT_GREEN = '\033[92m'
        LIGHT_YELLOW = '\033[93m'
        LIGHT_BLUE = '\033[94m'
        LIGHT_MAGENTA = '\033[95m'
        LIGHT_CYAN = '\033[96m'
        WHITE = '\033[97m'

    class bg:
        DEFAULT = '\033[49m'
        BLACK = '\033[40m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        YELLOW = '\033[43m'
        BLUE = '\033[44m'
        MAGENTA = '\033[45m'
        CYAN = '\033[46m'
        LIGHT_GRAY = '\033[47m'
        DARK_GRAY = '\033[100m'
        LIGHT_RED = '\033[101m'
        LIGHT_GREEN = '\033[102m'
        LIGHT_YELLOW = '\033[103m'
        LIGHT_BLUE = '\033[104m'
        LIGHT_MAGENTA = '\033[105m'
        LIGHT_CYAN = '\033[106m'
        WHITE = '\033[107m'

    class style:
        RESET = '\033[0m'
        BOLD = '\033[1m'
        DIM = '\033[2m'
        UNDERLINED = '\033[4m'
        BLINK = '\033[5m'
        REVERSE = '\033[7m'
        HIDDEN = '\033[8m'
        RESET_BOLD = '\033[21m'
        RESET_DIM = '\033[22m'
        RESET_UNDERLINED = '\033[24m'
        RESET_BLINK = '\033[25m'
        RESET_REVERSE = '\033[27m'
        RESET_HIDDEN = '\033[28m'


def exec(cmd, capture_output=True):
    log = subprocess.run(cmd, capture_output=capture_output)
    if log.returncode:
        print('Error when executing command')
        if capture_output:
            print(tcolor.fg.LIGHT_YELLOW + log.stdout.decode('utf-8') + tcolor.fg.DEFAULT)


def display_tex(latex):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = f'{tmpdirname}/out'

        with open(f'{filename}.tex', 'w') as f:
            f.write(LATEX_TEMPLATE % latex)

        latex_cmd = ['pdflatex', '-interaction=nonstopmode', f'-output-directory={tmpdirname}', f'{filename}.tex']
        convert_cmd = ['convert', '-quiet', '-density', '3000', '-quality', '90', '-alpha', 'off', '-background', 'white', '-resize', '15%', f'{filename}.pdf', f'{filename}.png']
        display_cmd = ['imgcat', f'{filename}.png']


        print(tcolor.bg.WHITE + tcolor.fg.BLACK + 'What does this formula mean?' + tcolor.fg.DEFAULT + tcolor.bg.DEFAULT + '\n')
        exec(latex_cmd)
        exec(convert_cmd)
        exec(display_cmd, capture_output=False)

 
if __name__ == "__main__":
    display_tex(r'\displaystyle\bigcup_{t\in \mathbb{N}} \left\{\frac{1}{t^6}\right\}')