Welcome to inqbus.rpi.widgets!
==============================

inqbus.rpi.widgets (IRW) is a framework for extensible GUI systems for the RaspberryPi or other systems with small displays.
But there are virtually no limits to extend or shape IRW.

**This is a work in progress! Please do not use this for production.**

IRW has the some neat features:

 * It is quite extensible due to its component design based on the Zope Component Architecture.


![plot](../master/doc/source/diagram_input.png)

![plot](../master/doc/source/diagram_output.png)


 * Native support of a wide range of character displays

     IRW suports all the displays RPLCD can access (Hitachi mostly)

     And can easily be extended to support any display by implementing just two member functions::

         @implementer(IDisplay)
         class MyDisplay(Display):

         def set_cursor_pos(x, y)
             ...

         def write(string)
             ...

 * Character display emulation
  - IRW has support for display emulation as
    * Curses
    * Console (e.g. for logging/debuggin of display changes)

    this enables you to develop your application on a desktop and then deploy it on the raspberry for debugging.
    This is cool but not a true emulation of the Hitachi! It is just a framebuffer emulation.

 * Support of multiple displays in parallel

     You can write in parallel to all displays attached independed of their type
     Each display reacts to the input in its own way. 
     You attach two displays in parallel, a 4 line and a 2 line LCD display. You display a menu of 5 lines. The menu will be rendered in both diplays. Scrolling down the menu will after hitting line 2 force the two line display to scroll while the four line display will scroll first when line 4 is aproached. This is experimental!

 * Support of multiple input devices in parallel

     You can attach any number of input devices.
     Blocking as well as non blocking input devices are supported.

     A non-blocking input device can coded simply as::

         @implementer(IInput)
         class MyInput(Input):

             def someone_has_clicked(self):
                 gui = getUtility(IGUI)
                 self.gui.dispatch(InputClick)

     For a blocking input device just change two lines::

         @implementer(IBlockingInput)
         class MyInput(BlockingInput):
