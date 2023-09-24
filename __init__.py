import sys
from rich.console import Console
from rich.style import Style
from rich.color import Color
import colorsys

__stdout__ = sys.stdout

class Lolcat:
    def __init__(
            self, 
            step: int = 3,
            file: any = None,
            seed: int = 0,
            prefix: str = ''
    ):
        '''
        @step - how many colors to skip between each character
        @file - file to write to
        @seed - seed for random color generator
        @prefix - prefix to add before each line, for example: `[green1]Prefix[/green1]`
        '''
        self.line = 0
        self.current = seed % 360 / 360
        self.step = step
        self.prefix = prefix
        self.file = file

    def get_color(self) -> Style:
        self.current += (1 / 360) * self.step
            
        if self.current >= 1:
            self.current = 0

        color = Color.from_rgb(
            *[
                round(i * 255) for i in colorsys.hsv_to_rgb(self.current, 1.0, 1.0)
            ]
        )

        return Style.from_color(color)

    def new_line(self) -> None:
        '''
        Adds value to
        self.current 
        self.line

        Used when you want to insert new line into formatting
        '''

        self.current = self.step * self.line
        self.line += 1

    def render(self, text: str) -> str:
        '''
        Renders text with colors
        '''

        out_text = ""
        for char in text:
            color = self.get_color()

            if char == '\n':
                self.current = self.step * self.line
                self.line += 1

                out_text += char
                continue
            
            rendered_char = color.render(char)
            out_text += rendered_char

        return out_text

    def print(self, *values, end='\n', sep=' ', file=None, flush=False):
        '''
        Prints the values to a stream, or to sys.stdout by default. Optional keyword arguments:
        file: a file-like object (stream); defaults to the current sys.stdout.
        sep: string inserted between values, default a space.
        end: string appended after the last value, default a newline.
        flush: whether to forcibly flush the stream.
        '''
        
        text = sep.join([str(value) for value in values]) + end

        if isinstance(sys.stdout, Lolcat) and file is None:
            self.write(text)
            return

        out = file or self.file or __stdout__

        if self.prefix != '':
            Console(file=out).print(self.prefix, end='')

        print(self.render(text), end='', file=out, flush=flush)

    def write(self, text: str) -> None:
        '''
        Writes the string to the stream.

        Don't use this method directly; use print() instead.
        '''

        self.print(text, end='', sep='', file=__stdout__)

    def flush(self) -> None:
        '''
        Flushes the stream.
        '''

        (self.file or __stdout__).flush()

def install() -> Lolcat:
    '''
    Installs lolcat as default stdout stream
    '''

    if isinstance(sys.stdout, Lolcat):
        return sys.stdout
    
    lolcat = Lolcat()
    lolcat._stdout_ = sys.stdout
    sys.stdout = lolcat
    return lolcat

def uninstall() -> None:
    '''
    Uninstalls lolcat from default stdout stream
    '''

    if isinstance(sys.stdout, Lolcat):
        sys.stdout = getattr(sys.stdout, '_stdout_', __stdout__)