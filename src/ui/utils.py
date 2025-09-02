from gi.repository import Gtk

from typing import Tuple

def _scroll_to_widget(scrolled_window: Gtk.ScrolledWindow, xy: Tuple[int]):
    # FIXME: scroll to center of widget
    x,y = xy
    vadjustment = scrolled_window.get_vadjustment()
    hadjustment = scrolled_window.get_hadjustment()

    vadjustment.set_value(y)
    hadjustment.set_value(x)
