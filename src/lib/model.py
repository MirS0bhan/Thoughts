from dataclasses import dataclass, field
from typing import List
import re

@dataclass
class ThoughtModel:
    title: str = ""
    text: str = ""

    @property
    def tags(self) -> List[str]:
        return re.findall(r'#\w+', self.text)

@dataclass
class ThoughtsDatabaseModel:
    thoughts_list: List[ThoughtModel] = field(default_factory=list)

