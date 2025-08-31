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

    path: Path
    thoughts_manager: ThoughtsManager

    _scrolled_window = Gtk.Template.Child()
    _canvas = Gtk.Template.Child()
    _viewport = Gtk.Template.Child()
    _headerbar = Gtk.Template.Child()
    _new_brain = Gtk.Template.Child()
    _open_brain = Gtk.Template.Child()
    _stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.application = self.get_application()

        self.setup_pan_gesture()

        self.application.create_action("zen-mode", self.toggle_zen_mode_action, ["<Ctrl><Shift>z"])
        self.application.create_action("new-thought", self.new_thought_action, ["<Ctrl>t"])
        self.application.create_action("open-file", self.open_file_action, ["<Ctrl>o"])
        self.application.create_action("save-file", self.save_file_action, ["<Ctrl>s"])

        self._new_brain.connect("clicked", self.create_new_file)
        self._open_brain.connect("clicked", self.open_file)

    def open_file_action(self, *args):
        fd = Gtk.FileDialog()
        fd.open(callback=self._on_file_opened)

    def _on_file_opened(self, dialog, result):
        file = dialog.open_finish(result)
        if file:
            self.path = Path(file.get_path())
            self._load_thoughts()
            self.transmision_to_canvas()

    def _load_thoughts(self):
        self.thoughts_manager = ThoughtsManager(self.path)
        self.thoughts_manager.load()

    def _dump_thoughts(self):
        self.thoughts_manager = ThoughtsManager(self.path)
        self.thoughts_manager.load()

    def create_new_file(self, *args):
        dialog = Gtk.FileDialog()
        dialog.save(parent=None, cancellable=None, callback=self._on_file_saved)

    def _on_file_saved(self, dialog, result):
        file = dialog.save_finish(result)
        if file:
            self.path = Path(file.get_path())
            if not self.path.exists():
                self.path.touch()
            self._dump_thoughts()

        self.transmision_to_canvas()

    def open_file(self, *args):
        self.open_file_action()

    def transmision_to_canvas(self, *args):
        self._stack.set_visible_child(self._scrolled_window)
        self.setup_thoughts()


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
        for thought in self.thoughts_manager.thoughts_list:
            self.insert_thought(ThoughtWidget(thought))


    def insert_thought(self, thought_widget):
        x,y = thought_widget.thought.position
        self._canvas.put(thought_widget, x, y)

    def new_thought_action(self, *args):
        thought_widget = ThoughtWidget()
        self.thoughts_manager.add(thought_widget.thought)
        padding = 200
        x,y = random.choice(range(padding,3200-padding)), random.choice(range(padding,1800-padding))
        thought_widget.thought.position = (x,y)

        self.insert_thought(thought_widget)

        self._scroll_to_widget(thought_widget, (x,y))

    # header

    def toggle_zen_mode_action(self, *args):
        self._headerbar.set_visible(not self._headerbar.is_visible())

    def save_file_action(self, *args):
        self.thoughts_manager.dump()

    def _scroll_to_widget(self,widget, xy = None):
        # FIXME: scroll to center of widget
        x,y = xy if xy else None
        vadjustment = self._scrolled_window.get_vadjustment()
        hadjustment = self._scrolled_window.get_hadjustment()

        vadjustment.set_value(y)
        hadjustment.set_value(x)
