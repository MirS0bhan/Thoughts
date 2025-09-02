from pathlib import Path
from json import loads as json_load, dumps as json_dumps
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
    def __init__(self, database: Path):
        self.path = database
        self._is_database_locked = False
        self._database = ThoughtsDatabaseModel()

    def add(self, thought: ThoughtModel):
        self._database.thoughts_list.append(thought)

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
