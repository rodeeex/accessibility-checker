import importlib
from pathlib import Path

from .base import WCAGRule, Issue

rules_dir = Path(__file__).parent

for file in rules_dir.glob("*.py"):
    if file.name not in ["__init__.py", "base.py"]:
        module_name = file.stem
        try:
            importlib.import_module(f"rules.{module_name}")
        except Exception as e:
            print(f"Предупреждение: не удалось загрузить правило {module_name}: {e}")

__all__ = ["WCAGRule", "Issue"]