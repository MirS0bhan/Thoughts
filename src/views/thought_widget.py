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


@Gtk.Template(resource_path='/ir/mirsobhan/apps/Thoughts/views/thought_widget.ui')
class ThoughtWidget(Gtk.Box):
    __gtype_name__ = "ThoughtWidget"

    def __init__(self,*args,**kwargs):
        super().__init__(**kwargs)

    def setup_thought():
        pass


