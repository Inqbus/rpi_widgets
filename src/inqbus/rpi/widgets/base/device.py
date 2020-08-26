from zope.interface import implementer

from inqbus.rpi.widgets.interfaces.interfaces import IDevice


@implementer(IDevice)
class Device(object):
    """
    A device is the abstraction of a hardware device. Such a Device has to be :
    * initialized (init)
    * used (run)
    * and its resources freed in the end (done)
    """

    # Am I initialized
    initialized = False

    def init(self):
        pass

    def run(self):
        pass

    def done(self):
        pass
