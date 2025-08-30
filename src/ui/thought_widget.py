# thought_widget.py
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

from thoughts.lib.model import ThoughtModel

from .tag_widget import TagWidget

@Gtk.Template(resource_path='/ir/mirsobhan/apps/Thoughts/ui/thought_widget.ui')
class ThoughtWidget(Gtk.Box):
    __gtype_name__ = "ThoughtWidget"

    _title = Gtk.Template.Child()
    _text = Gtk.Template.Child()
    _tags = Gtk.Template.Child()

    def __init__(self, thought: ThoughtModel, *args,**kwargs):
        super().__init__(**kwargs)
        self._thought ThoughtModel = thought

        self.setup_thought()

    def setup_thought(self):
        print(self._thought.title)
        self.set_title(self._thought.title)
        self.set_text(self._thought.text)
        self.set_tags()

    def set_title(self, title: str):
        self._title.set_label(title)
        self._thought.title = title

    def set_text(self, text: str):
        self._text.set_text(text)
        self._thought.text = text

    def set_tags(self):
        for tag in self._thought.tags:
            self._tags.append(TagWidget(tag))

    @property
    def thought(self):
        return self._thought
