import argparse
import sys
from pylolcat import install, uninstall

if __name__ == "__main__":
    lolcat = install()

    parser = argparse.ArgumentParser(
        description='Lolcat, but in python',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage='python3 -m pylolcat [OPTION]... [FILE]...',
    )

    parser.add_argument(
        '--step',
        type=int,
        default=6,
        help='How many colors to skip between each character'
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=0,
        help='Seed for random color generator'
    )

    parser.add_argument(
        'FILE',
        nargs='*',
        default=['-'],
        help='Concatenate FILE(s) to standard output. If no FILE or if FILE is -, read standard input.'
    )

    parser.epilog = '''
examples:
    python3 -m pylolcat --step 6 --seed 0 file1 - file2         Output file1, then stdin, then file2.
    python3 -m pylolcat                                         Copy standard input to standard output.
    fortune | python3 -m pylolcat                               Display a rainbow cookie.
    '''

    args = parser.parse_args()
    
    lolcat.step = args.step
    lolcat.seed = args.seed

    for file in args.FILE:
        if file == '-':
            lines = sys.stdin.readlines()
        else:
            with open(file, encoding='utf-8') as f:
                lines = f.readlines()

        for i, line in enumerate(lines):
            print(line.rstrip('\n'), end='\n' if (i != len(lines) - 1) else '')

    uninstall()