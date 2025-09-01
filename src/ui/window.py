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
from .intro_page import IntroPage
from .canvas_screen import CanvasScreen

from thoughts.lib import ThoughtModel, ThoughtsManager

@Gtk.Template(resource_path='/ir/mirsobhan/apps/Thoughts/ui/window.ui')
class ThoughtsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ThoughtsWindow'

    path: Path
    thoughts_manager: ThoughtsManager

    _headerbar = Gtk.Template.Child()
    _stack = Gtk.Template.Child()
    _canvas_screen = Gtk.Template.Child()
    _intro_page = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.application = self.get_application()

        self.application.create_action("new-file", self.new_file_action, ["<Ctrl>n"])
        self.application.create_action("open-file", self.open_file_action, ["<Ctrl>o"])
        self.application.create_action("save-file", self.save_file_action, ["<Ctrl>s"])
        self.application.create_action("zen-mode", self.toggle_zen_mode_action, ["<Ctrl><Shift>z"])
        self.application.create_action("new-thought", self.new_thought_action, ["<Ctrl>t"])


    # actions
    def new_thought_action(self, *args):
        new_thought = self.thoughts_manager.new()
        thought_widget = ThoughtWidget(new_thought)

        padding = 200
        x,y = random.choice(range(padding,3200-padding)), random.choice(range(padding,1800-padding))
        thought_widget.thought.position = [x,y]

        self._canvas_screen.insert_thought(thought_widget, scroll = True)


    def toggle_zen_mode_action(self, *args):
        self._headerbar.set_visible(not self._headerbar.is_visible())

    def save_file_action(self, *args):
        self.thoughts_manager.dump()

    def new_file_action(self, *args):
        dialog = Gtk.FileDialog()
        dialog.save(parent=None, cancellable=None, callback=self._on_file_saved)

    def open_file_action(self, *args):
        fd = Gtk.FileDialog()
        fd.open(callback=self._on_file_opened)

    def _on_file_opened(self, dialog, result):
        file = dialog.open_finish(result)
        if file:
            self.path = Path(file.get_path())
            self._load_thoughts()
            self.transmision_to_canvas()

    def _on_file_saved(self, dialog, result):
        file = dialog.save_finish(result)
        if file:
            self.path = Path(file.get_path())
            if not self.path.exists():
                self.path.touch()
            self._dump_thoughts()

        self.transmision_to_canvas()

    def _load_thoughts(self):
        self.thoughts_manager = ThoughtsManager(self.path)
        self.thoughts_manager.load()

    def _dump_thoughts(self):
        self.thoughts_manager = ThoughtsManager(self.path)
        self.thoughts_manager.dump()

    def transmision_to_canvas(self, *args):
        self._stack.set_visible_child(self._canvas_screen)
        self.setup_thoughts()


    # Thoughts section

    def setup_thoughts(self):
        for thought in self.thoughts_manager.thoughts_list:
            self._canvas_screen.insert_thought(ThoughtWidget(thought))


