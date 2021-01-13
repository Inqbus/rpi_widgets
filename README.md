Welcome to inqbus.rpi.widgets's documentation!
==============================================

rpi.widgets (RW) is a basic framework for extensible GUI systems for the RaspberryPi or other systems with small displays.
But there are no limits to extend or shape RW.

RW has the some neat features:

    * It is quite extensible due to its :doc:`component_design`.
    
![plot](../master/doc/source/diagram_input.png)

.. figure:: ../master/doc/source/diagram_input.png
     :width: 800px
     :align: center
     :alt: alternate text
     :figclass: align-center

.. figure:: ./doc/source/diagram_output.png
     :width: 800px
     :align: center
     :alt: alternate text
     :figclass: align-center

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

        IRW has support for display emulation as
            * Curses
            * Console (e.g. for logging/debuggin of display changes)

        this enables you to develop your application on a desktop and then deploy it on the raspberry for debugging.

        .. note::

            This is not a true emulation of the Hitachi! It is just a framebuffer emulation.

    * Support of multiple displays in parallel

        You can write in parallel to all displays attached independed of their type

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
