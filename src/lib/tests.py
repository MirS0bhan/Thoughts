import pytest
import tempfile
from pathlib import Path

from . import ThoughtsManager, ThoughtModel


@pytest.fixture
def sample_thought():
    return ThoughtModel(title="Test", text="This is a #test thought.")


@pytest.fixture
def temp_db_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "test_db.json"


def test_add_and_thoughts_list(sample_thought, temp_db_file):
    mgr = ThoughtsManager()
    mgr.init(temp_db_file)
    mgr.add(sample_thought)
    assert len(mgr.thoughts_list) == 1
    assert mgr.thoughts_list.title == "Test"


def test_dump_and_load(sample_thought, temp_db_file):
    mgr = ThoughtsManager()
    mgr.init(temp_db_file)
    mgr.add(sample_thought)
    # Dump database to file
    dumped = mgr.dump()
    assert dumped is True
    assert temp_db_file.exists()

    # Create new manager instance and load from file
    mgr2 = ThoughtsManager()
    mgr2.init(temp_db_file)
    loaded = mgr2.load()
    assert loaded is True
    assert len(mgr2.thoughts_list) == 1
    assert mgr2.thoughts_list.title == sample_thought.title


def test_atomic_locking(sample_thought, temp_db_file):
    mgr = ThoughtsManager()
    mgr.init(temp_db_file)

    # Manually lock database
    mgr._is_database_locked = True

    # load and dump should return False when locked
    assert mgr.load() is False
    assert mgr.dump() is False

    # Unlock and test again
    mgr._is_database_locked = False
    assert mgr.dump() is True
