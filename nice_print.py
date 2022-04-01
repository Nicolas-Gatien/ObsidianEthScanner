class Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def green_print(input):
    output = f"{Colours.OKGREEN}" + input + f"{Colours.ENDC}"
    print(f"{output}")

def yellow_print(input):
    output = f"{Colours.WARNING}" + input + f"{Colours.WARNING}"
    print(f"{output}")

def cyan_print(input):
    output = f"{Colours.OKCYAN}" + input + f"{Colours.OKCYAN}"
    print(f"{output}")