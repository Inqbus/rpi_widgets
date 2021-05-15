from inqbus.rpi.widgets.base.render import Renderer, render_session
from inqbus.rpi.widgets.base.widget import Widget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.widgets import ILinesWidget
from inqbus.rpi.widgets.line import Line
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(ILinesWidget)
class Lines(Widget):
    """
    Lines Widget.
    Representing one or more lines.
    This widget contains a list of lines which will
    be rendered left_bounded.
    """
    def init_content(self):
        self._content = []

    def handle_new_content(self, value):
        # accept only a list of ether strings or Line Instances
        assert isinstance(value, list)
        # for all given lines
        for line_val in value:
            # if line is string
            if isinstance(line_val, str):
                # .. then transform it into a line instance
                line = Line(fixed_pos=False)
                line.render_on_content_change = False
                line._can_focus = True
                line.content = line_val
                self._content.append(line)
            else:
                # .. else just append to the content
                line_val._can_focus = True
                self._content.append(line_val)


        # if render on content_change
        if self.render_on_content_change:
            # .. render the widget
            self.render()

    @property
    def height(self):
        """
        The height of the widget in characters
        """
        if self._desired_height is None:
            return len(self._content)
        else:
            return self._desired_height

    @height.setter
    def height(self, value):
        """
        Set the height to a fixed value

        Args: value: height
        """
        self._desired_height = value


@implementer(IRenderer)
class LinesRenderer(Renderer):
    """
    Renderer for a LinesWidget
    """
    __used_for__ = (ILinesWidget, Interface)

    @render_session
    def render(self, pos_x=None, pos_y=None):

        self.clear()
        pos_x, pos_y = self.render_position(pos_x, pos_y)
        prefix = ''
        offset = 0
        # If the line can be focused add a prefix
        if self.widget.can_focus:
            offset = 1
            if self.widget.has_focus:
                prefix = self.special_chars['FOCUS_LEFT']
            else:
                prefix = ' '

        for line in self.widget.content:
            self.display.write_at_pos(
                pos_x,
                pos_y,
                prefix
            )
            renderer = line.render_for_display(
                    self.display,
                    pos_x=pos_x + offset,
                    pos_y=pos_y
            )
            pos_y += renderer.rendered_height
            self.update_render_dimensions(renderer)
        # return the coordinate after the content
        # ToDo width, height handling
        return self

    def clear(self):
        """
        Clean widget from the display
        """
        if not self.was_rendered:
            return

        for line in self.widget.content:
            renderer = line.get_renderer_for_display(self.display)
            renderer.clear()


# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(LinesRenderer, (ILinesWidget, Interface), IRenderer)
