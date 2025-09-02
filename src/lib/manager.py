from pathlib import Path
from json import loads as json_load, dumps as json_dumps

from typing import List

from .model import ThoughtModel, ThoughtsDatabaseModel


def _atomic(func):
    def wrapper(self, *args, **kwargs):
        if self._is_database_locked:
            return False
        self._is_database_locked = True
        try:
            return func(self, *args, **kwargs)
        finally:
            self._is_database_locked = False

    return wrapper


class ThoughtsManager:
    def __init__(self, database: Path, index: bool = True):
        self.path = database
        self._is_database_locked = False
        self._database = ThoughtsDatabaseModel()

        self._index: Dict[str, List[ThoughtModel]] = {}
        if index:
            self._build_index()

    def _build_index(self):
        self._index.clear()
        for thought in self._database.thoughts_list:
            for tag in thought.tags:
                self._index.setdefault(tag, []).append(thought)

    def add(self, thought: ThoughtModel):
        self._database.thoughts_list.append(thought)
        for tag in thought.tags:
            self._index.setdefault(tag, []).append(thought)

    def filter(self, *tags: str) -> List[ThoughtModel]:
        if not tags:
            return self._database.thoughts_list[:]

        sets_of_thoughts: List[Set[ThoughtModel]] = []
        for tag in tags:
            thoughts_for_tag = set(self._index.get(tag, []))
            sets_of_thoughts.append(thoughts_for_tag)

        if not sets_of_thoughts:
            return []

        filtered_thoughts = set.intersection(*sets_of_thoughts)

        return list(filtered_thoughts)

    def new(self):
        new_thought = ThoughtModel()
        self._database.thoughts_list.append(new_thought)

        return new_thought

    @_atomic
    def load(self):
        with self.path.open(mode="r", encoding="utf-8") as file:
            content = json_load(file.read())
            self._database = ThoughtsDatabaseModel(
                thoughts_list=[
                    ThoughtModel(**t) for t in content.get("thoughts_list", [])
                ]
            )
        return True

    @_atomic
    def dump(self):
        with self.path.open(mode="w", encoding="utf-8") as file:
            content = json_dumps(
                {"thoughts_list": [t.__dict__ for t in self._database.thoughts_list]}
            )
            file.write(content)
        return True

    @property
    def thoughts_list(self):
        return self._database.thoughts_list
