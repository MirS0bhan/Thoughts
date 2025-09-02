from dataclasses import dataclass, field
from typing import List
import re


@dataclass
class ThoughtModel:
    title: str = ""
    text: str = ""
    position: List[int] = field(default_factory=list)

    @property
    def tags(self) -> List[str]:
        return re.findall(r"#\w+", self.text)

    def __eq__(self, other):
        if not isinstance(other, ThoughtModel):
            return False
        return self.title == other.title and self.text == other.text and set(self.tags) == set(other.tags)

    def __hash__(self):
        return hash((self.title, self.text, tuple(sorted(self.tags))))

@dataclass
class ThoughtsDatabaseModel:
    thoughts_list: List[ThoughtModel] = field(default_factory=list)
