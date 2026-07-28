"""Regression tests for verse IDs referenced by static server collections."""
import ast
import json
import sys
import unittest
from collections import defaultdict
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
SERVER_PATH = BACKEND_DIR / "server.py"
APP_DATA_PATH = PROJECT_ROOT / "dharmasearch-handoff" / "app_data.json"
sys.path.insert(0, str(BACKEND_DIR))

from scripture_data import get_all_verses  # noqa: E402


def static_assignment(function_name, variable_name):
    """Read a literal assignment from a server function without importing it."""
    tree = ast.parse(SERVER_PATH.read_text(encoding="utf-8"))
    function = next(
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    )
    assignments = [
        statement
        for statement in function.body
        if isinstance(statement, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == variable_name
            for target in statement.targets
        )
    ]
    assert len(assignments) == 1, (
        f"Expected exactly one direct assignment to {variable_name!r} "
        f"in {function_name!r}, found {len(assignments)}"
    )
    return ast.literal_eval(assignments[0].value)


class TestStaticVerseReferences(unittest.TestCase):
    def test_sample_and_prebuilt_plan_verse_ids_exist_in_seed_sources(self):
        sample_ids = static_assignment("get_sample_verses", "sample_ids")
        plans = static_assignment("seed_reading_plans", "plans")
        pipeline = json.loads(APP_DATA_PATH.read_text(encoding="utf-8"))
        available_ids = {
            verse["verse_id"] for verse in get_all_verses()
        } | {
            verse["id"] for verse in pipeline["verses"]
        }

        reference_locations = defaultdict(list)
        for verse_id in sample_ids:
            reference_locations[verse_id].append("sample_ids")
        for plan in plans:
            for day in plan["days"]:
                for verse_id in day["verse_ids"]:
                    reference_locations[verse_id].append(
                        f'{plan["plan_id"]} day {day["day"]}'
                    )

        missing = {
            verse_id: locations
            for verse_id, locations in reference_locations.items()
            if verse_id not in available_ids
        }
        self.assertFalse(missing, f"Static verse references are missing: {missing}")
