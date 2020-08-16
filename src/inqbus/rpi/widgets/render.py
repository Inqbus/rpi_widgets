from inqbus.rpi.widgets.interfaces.widgets import (
    IRenderer, ILineWidget,
    IPageWidget, ISelectWidget, ILinesWidget, )
from inqbus.rpi.widgets.base.render import Renderer
from zope.component import getGlobalSiteManager
from zope.interface import implementer, Interface


@implementer(IRenderer)
class LineRenderer(Renderer):
    __used_for__ = (ILineWidget, Interface)
    def render(self, pos_x=None, pos_y=None):
        super(LineRenderer, self).render(pos_x=pos_x, pos_y=pos_y)
        self.display.write_at_pos(pos_x, pos_y, self.widget.content)


@implementer(IRenderer)
class LinesRenderer(Renderer):
    __used_for__ = (ILinesWidget,)

    def render(self, pos_x=None, pos_y=None):
        super(LinesRenderer, self).render(pos_x=pos_x, pos_y=pos_y)
        widget = self.widget
        y_pos= self.widget.pos_y
        x_pos = self.widget.pos_x
        for line in widget.content[0:widget.line_count]:
            line.render(x_pos, y_pos)
            y_pos += 1


@implementer(IRenderer)
class SelectRenderer(Renderer):
    __used_for__ = (ISelectWidget,)

    def render(self, pos_x=None, pos_y=None):
        super(SelectRenderer, self).render(pos_x=pos_x, pos_y=pos_y)
        pos_x = self.pos_x
        pos_y = self.pos_y

        if self.widget.selected_idx + pos_y >= self.display.line_count:
            start_idx =  self.widget.selected_idx - (self.display.line_count - pos_y - 1)
            end_idx = self.widget.selected_idx + 1
        else:
            start_idx = 0
            end_idx = self.display.line_count - pos_y
        idx = start_idx
        for line in self.widget.content[start_idx:end_idx]:
            if idx == self.widget.selected_idx:
                self.display.write_at_pos(pos_x, pos_y, '>')
            else:
                self.display.write_at_pos(pos_x, pos_y, ' ')
            line.render(pos_x + 1, pos_y)
            pos_y += 1
            idx += 1

@implementer(IRenderer)
class PageRenderer(Renderer):
    __used_for__ = (IPageWidget,)

    def render(self, pos_x=None, pos_y=None):
        for widget in self.widget.widgets:
            widget.render()


gsm = getGlobalSiteManager()
gsm.registerAdapter(LineRenderer, (ILineWidget, Interface), IRenderer)
gsm.registerAdapter(LinesRenderer, (ILinesWidget, Interface,), IRenderer)
gsm.registerAdapter(SelectRenderer, (ISelectWidget, Interface,), IRenderer)
gsm.registerAdapter(PageRenderer, (IPageWidget, Interface,), IRenderer)
