import curses

from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class DisplayCurses(Display):
    """
    Curses frame_buffer.
    """
    initialized = False
    curses_display_created = False

    def __init__(self,
                 height=4,
                 width=20,
                 autoupdate=True,
                 terminal_pos_x=0,
                 terminal_pos_y=0,
                 ):
        super(DisplayCurses, self).__init__(height=height, width=width, autoupdate=autoupdate)
        # Setup curses window at a given terminal position
        self.terminal_pos_x = terminal_pos_x
        self.terminal_pos_y = terminal_pos_y

    def init(self):
        super(DisplayCurses, self).init()
        if not DisplayCurses.curses_display_created:

            # Initialize a curses screen
            curses.initscr()
            # hide the cursor
            curses.curs_set(0)
            DisplayCurses.curses_display_created = True

        # get a new window from curses at 0,0 on the active console
        self.display = curses.newwin(self.height + 3, self.width + 2, self.terminal_pos_y, self.terminal_pos_x)
        self.initialized = True
        # Draw a frame around the active char display area
        self.draw_frame()

    def draw_frame(self):
        """
        Draw a frame around the active char display area
        """
        try:
            self.display.addstr(0, 0, '+' + '-' * self.width + '+')
            for pos_y in range(self.height):
                self.display.addstr(pos_y + 1, 0, '|')
                self.display.addstr(pos_y + 1, self.width + 1, '|')
            self.display.addstr(self.height + 1, 0, '+' + '-' * self.width + '+')
        except Exception as e:
            pass

    def write(self, line):
        # chack for range violations
        if not self.initialized:
            return
        if not self.pos_y < self.height:
            return
        if not self.pos_x < self.width:
            return
        # display the given string. Offset the write position into the frame
        self.display.addstr(self.pos_y + 1, self.pos_x + 1, line)
        # rerender
        self.display.refresh()
