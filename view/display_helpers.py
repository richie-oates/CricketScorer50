import pyfiglet

def print_title(text, color="YELLOW"):
    pyfiglet.print_figlet(text, colors=color)

def subtitle(text):
    subtitle = "=" * len(text) + "\n"
    subtitle += text + "\n"
    subtitle += "=" * len(text)
    return subtitle