from gi.repository import Gtk

from thoughts.lib.model import ThoughtModel
from .tag_widget import TagWidget


@Gtk.Template(resource_path="/ir/mirsobhan/apps/Thoughts/ui/thought_widget.ui")
class ThoughtWidget(Gtk.Box):
    __gtype_name__ = "ThoughtWidget"

    _title = Gtk.Template.Child()
    _text = Gtk.Template.Child()
    _tags = Gtk.Template.Child()

    def __init__(self, thought: ThoughtModel = None, *args, **kwargs):
        super().__init__(**kwargs)
        self._thought: ThoughtModel = thought if thought else ThoughtModel(text="safdg")
        self._tags_buffer = []

        self.setup_thought()

        self._text_buffer.connect("changed", self._on_text_changed)
        self._title_buffer.connect("inserted_text", self._on_title_changed)

    @property
    def _text_buffer(self):
        return self._text.get_buffer()

    @property
    def _title_buffer(self):
        return self._title.get_buffer()

    def setup_thought(self):
        self.set_title(self._thought.title)
        self.set_text(self._thought.text)
        self.set_tags()

    def _on_title_changed(self, *args):
        self._thought.title = self._title_buffer.props.text

    def _on_text_changed(self, *args):
        self._thought.text = self._text_buffer.props.text
        self.update_tags()

    def set_title(self, title: str):
        self._title_buffer.set_text(title, -1)
        self._thought.title = title

    def set_text(self, text: str):
        self._text_buffer.set_text(text, -1)
        self._thought.text = text

    def set_tags(self):
        for tag in self._thought.tags:
            tw = TagWidget(tag)
            self._tags.append(tw)
            self._tags_buffer.append(tw)

    def update_tags(self):
        for widget in self._tags_buffer:
            widget.unparent()
        self._tags_buffer.clear()
        self.set_tags()

    @property
    def thought(self):
        return self._thought
