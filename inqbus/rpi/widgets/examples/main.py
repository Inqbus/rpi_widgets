from inqbus.rpi.widgets.display.curses import DisplayCurses
from inqbus.rpi.widgets.input.curses import InputCurses
from inqbus.rpi.widgets.input.pynput_input import PynputInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from inqbus.rpi.widgets.line import Line
from inqbus.rpi.widgets.lines import Lines
from inqbus.rpi.widgets.page import Page
from inqbus.rpi.widgets.select import Select

from zope.component import getUtility

import inqbus.rpi.widgets.gui  # noqa: F401
import inqbus.rpi.widgets.base.controller  # noqa: F401


gui = getUtility(IGUI)

display = DisplayCurses()
display.init()
gui.add_display(display)

display2 = DisplayCurses(terminal_pos_x=30, height=2)
display2.init()
gui.add_display(display2)


#input = PynputInput()
input = InputCurses(display.display)
gui.add_input(input)


layout = Page(pos_x=0,pos_y=0)

line = Line()
line.content = 'huhu'
layout.add_widget(line)

lines = Lines(render_on_content_change=False, fixed_pos=False)
lines.content = ['line1','line2']


select = Select(pos_y=1, height=4)
select.content = [
    lines,
    'sel2',
    'sel3',
    'sel4',
]

layout.add_widget(select)

gui.set_layout(layout)

gui.focus = select

gui.init()

gui.run(blocking=False)
