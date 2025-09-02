# window.py
#
# Copyright 2025 sobhan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk, Gdk

from . import utils
from .thought_widget import ThoughtWidget

@Gtk.Template(resource_path='/ir/mirsobhan/apps/Thoughts/ui/canvas_screen.ui')
class CanvasScreen(Gtk.ScrolledWindow):
    __gtype_name__ = 'CanvasScreen'

    _canvas = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setup_pan_gesture()

    # Canvas gesture

    def setup_pan_gesture(self):
        gesture = Gtk.GestureDrag()

        gesture.set_button(Gdk.BUTTON_PRIMARY)

        self.drag_start_x = 0
        self.drag_start_y = 0

        gesture.connect("drag-begin", self.on_pan_drag_begin)
        gesture.connect("drag-update", self.on_pan_drag_update)
        gesture.connect("drag-end", self.on_pan_drag_end)

        self.add_controller(gesture)

    def on_pan_drag_begin(self, gesture, start_x, start_y):
        grabbing_cursor = Gdk.Cursor.new_from_name("grabbing")
        self.set_cursor(grabbing_cursor)

        self.drag_start_x = self.get_hadjustment().get_value()
        self.drag_start_y = self.get_vadjustment().get_value()

    def on_pan_drag_update(self, gesture, offset_x, offset_y):
        hadj = self.get_hadjustment()
        vadj = self.get_vadjustment()

        hadj.set_value(self.drag_start_x - offset_x)
        vadj.set_value(self.drag_start_y - offset_y)

    def on_pan_drag_end(self, gesture, offset_x, offset_y):
        grab_cursor = Gdk.Cursor.new_from_name("grab")
        self.set_cursor(grab_cursor)


    # thoughts

    def insert_thought(self, thought_widget, scroll: bool =False):
        x,y = thought_widget.thought.position
        self._canvas.put(thought_widget, x, y)

        if scroll:
            self._scroll_to_thought(thought_widget)

    def _scroll_to_thought(self, thought_widget: ThoughtWidget):
        tought = thought_widget.thought
        utils._scroll_to_widget(self, tought.position)
