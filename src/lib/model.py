from dataclasses import dataclass, field
from typing import List, Optional
import re

@dataclass
class ThoughtModel:
    title: str = ""
    text: str = ""
    position = [0,0]

    @property
    def tags(self) -> List[str]:
        return re.findall(r'#\w+', self.text)

@dataclass
class ThoughtsDatabaseModel:
    thoughts_list: List[ThoughtModel] = field(default_factory=list)

