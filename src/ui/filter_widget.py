# filter-widget.py
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

from gi.repository import Gtk

from .tag_widget import TagWidget
from .thought_widget import ThoughtWidget


@Gtk.Template(resource_path="/ir/mirsobhan/apps/Thoughts/ui/filter_widget.ui")
class FilterWidget(Gtk.Box):
    __gtype_name__ = "FilterWidget"

    _filter_tags = Gtk.Template.Child()
    _thoughts_list = Gtk.Template.Child()

    def __init__(self, on_click_filter_tag_add, on_click_filter_tag_delete, tags = [], thought_list = [], **kwargs):
        super().__init__(**kwargs)

        for tag in set(tags):
            self._filter_tags.append(TagWidget(tag, on_click_filter_tag_delete))

        for thought in thought_list:
            self._thoughts_list.append(ThoughtWidget(thought, on_click_filter_tag_add))

