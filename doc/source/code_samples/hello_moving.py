from time import sleep
from inqbus.rpi.widgets import DisplayCurses
from inqbus.rpi.widgets import IGUI
from inqbus.rpi.widgets import Text
from zope.component import getUtility

# load the gui component
# load the base controller component

text = Text()
text.content = 'Hello World'
text.fixed_pos = True

gui = getUtility(IGUI)
display = DisplayCurses()

gui.add_display(display)
gui.set_layout(text)

gui.init()
gui.run(blocking=False)

while True:
    sleep(1)
    text.clear()
    text.pos_y = (text.pos_y + 1) % 4
    text.render()

gui.done()
