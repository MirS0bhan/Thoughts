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

import random
from pathlib import Path

from gi.repository import Adw
from gi.repository import Gtk, Gdk

from .thought_widget import ThoughtWidget

from thoughts.lib import ThoughtModel, ThoughtsManager

@Gtk.Template(resource_path='/ir/mirsobhan/apps/Thoughts/ui/window.ui')
class ThoughtsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ThoughtsWindow'

    _scrolled_window = Gtk.Template.Child()
    _canvas = Gtk.Template.Child()
    _viewport = Gtk.Template.Child()
    _headerbar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = Path("test.t.json")

        self.thoughts_manager = ThoughtsManager(self.path)
        # self.thoughts_manager.load()

        self.application = self.get_application()

        self.setup_pan_gesture()
        self.setup_thoughts()

        self.application.create_action("zen-mode", self.toggle_zen_mode_action, ["<Ctrl><Shift>z"])
        self.application.create_action("new-thought", self.new_thought_action, ["<Ctrl>t"])
        self.application.create_action("open-file", self.open_file_action, ["<Ctrl>o"])
        self.application.create_action("save-file", self.save_file_action, ["<Ctrl>s"])

    # Canvas gesture

    def setup_pan_gesture(self):
        gesture = Gtk.GestureDrag()

        gesture.set_button(Gdk.BUTTON_PRIMARY)

        self.drag_start_x = 0
        self.drag_start_y = 0

        gesture.connect("drag-begin", self.on_pan_drag_begin)
        gesture.connect("drag-update", self.on_pan_drag_update)
        gesture.connect("drag-end", self.on_pan_drag_end)

        self._scrolled_window.add_controller(gesture)

    def on_pan_drag_begin(self, gesture, start_x, start_y):
        grabbing_cursor = Gdk.Cursor.new_from_name("grabbing")
        self._scrolled_window.set_cursor(grabbing_cursor)

        self.drag_start_x = self._scrolled_window.get_hadjustment().get_value()
        self.drag_start_y = self._scrolled_window.get_vadjustment().get_value()

    def on_pan_drag_update(self, gesture, offset_x, offset_y):
        hadj = self._scrolled_window.get_hadjustment()
        vadj = self._scrolled_window.get_vadjustment()

        hadj.set_value(self.drag_start_x - offset_x)
        vadj.set_value(self.drag_start_y - offset_y)

    def on_pan_drag_end(self, gesture, offset_x, offset_y):
        grab_cursor = Gdk.Cursor.new_from_name("grab")
        self._scrolled_window.set_cursor(grab_cursor)

    # Thoughts section

    def setup_thoughts(self):
        pass


    def add_thought(self, thought, x,y):
        self._canvas.put(thought,x,y)

    def new_thought_action(self, *args):
        # FIXME: scroll to center of widget
        tw = ThoughtWidget()
        self.thoughts_manager.add(tw.thought)
        x,y = random.choice(range(3200)), random.choice(range(1800))
        self._canvas.put(tw, x, y)

        vadjustment = self._scrolled_window.get_vadjustment()
        hadjustment = self._scrolled_window.get_hadjustment()

        vadjustment.set_value(y)
        hadjustment.set_value(x)

    # header

    def toggle_zen_mode_action(self, *args):
        self._headerbar.set_visible(not self._headerbar.is_visible())

    def open_file_action(self, *args):
        fd = Gtk.FileDialog()
        fd.open(callback=self.init_x)

    def init_x(self, dialog, result):
        file = dialog.open_finish(result)
        if file:
            self.path = Path(file.get_path())

        self.thoughts_manager = ThoughtsManager(self.path)
        self.thoughts_manager.load()

    def save_file_action(self, *args):
        self.thoughts_manager.dump()
        print(2435)
