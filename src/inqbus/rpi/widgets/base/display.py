from inqbus.rpi.widgets.interfaces.widgets import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class Display(object):

    def __init__(self, line_count=4, chars_per_line=20, autoupdate=True):
        self.autoupdate = autoupdate
        self.line_count = line_count
        self.chars_per_line = chars_per_line
        self._pos_x = 0
        self._pos_y = 0
        self.init()

    def init(self):
        self.display = [ ' ' * self.chars_per_line for i in range(self.line_count)]

    def run(self):
        pass

    def done(self):
        pass

    def set_cursor_pos(self, x, y):
        self.pos_y, self.pos_x = (y, x)

    def write(self, line):
        if not self.pos_y < self.line_count :
            return
        if not self.pos_x < self.chars_per_line :
            return

        current_line = self.display[self.pos_y]
        current_line = current_line[0:self.pos_x] + line + current_line[self.pos_x + len(line):]
        current_line = current_line[0:self.chars_per_line]
        self.display[self.pos_y] = current_line
        if self.autoupdate:
            self.show()

    def show(self):
        print('+' + '-' * self.chars_per_line + '+')
        for line in self.display:
            print('|' + line + '|')
        print('+' + '-' * self.chars_per_line + '+')
