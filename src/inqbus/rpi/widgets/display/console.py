from inqbus.rpi.widgets.base.display import Display
from inqbus.rpi.widgets.errors import OutOfDisplay
from inqbus.rpi.widgets.interfaces.display import IDisplay
from zope.interface import implementer


@implementer(IDisplay)
class ConsoleDisplay(Display):
    """
    Display the changes of the gui on the console. Mostly usefull for debugging or developing on
    a desktop where the real hardware is not available.
    """

    def __init__(self,
                 height=4,
                 width=20,
                 autoupdate=True,
                 ):
        super(ConsoleDisplay, self).__init__(
                height=height,
                width=width,
                autoupdate=autoupdate
        )
        self.init()

    def init(self):
        """
        Initialize the frame_buffer. In this case we only build a character "frame buffer"
        :return:
        """
        super(ConsoleDisplay, self).init()
        self.clear()

    def clear(self):
        self.frame_buffer = [' ' * self.width for i in range(self.height)]

    def run(self):
        pass

    def done(self):
        pass

    def write(self, content):
        """
        Write given content to the frame_buffer at the current cursor position.
        :param content: the content given. String
        :return:
        """
        # copy the line where the cursor is set into new_line
        new_line = self.frame_buffer[self.pos_y]
        # insert the content into the new_line
        new_line = new_line[0:self.pos_x] + content + new_line[self.pos_x + len(content):]
        # clip new_line with the width of the frame_buffer
        new_line = new_line[0:self.width]
        # replace the line in the frame_buffer with the new_line
        self.frame_buffer[self.pos_y] = new_line
        # if the diplay autoupdate is set ..
        if self.autoupdate:
            # .. show the frame_buffer
            self.show()

    def show(self):
        """
        Do a simple representation of the frame_buffer by printing all its lines to the console.
        :return:
        """
        print('+' + '-' * self.width + '+')
        for line in self.frame_buffer:
            print('|' + line + '|')
        print('+' + '-' * self.width + '+')

