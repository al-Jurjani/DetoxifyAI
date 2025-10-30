# import evidently
# import pkgutil

# print(f"Evidently version: {evidently.__version__}")
# print(f"Evidently location: {evidently.__file__}")
# print("\n=== Available modules in evidently ===")

# for importer, modname, ispkg in pkgutil.iter_modules(evidently.__path__):
#     print(f"  {modname} {'(package)' if ispkg else ''}")

# # Try to see what's actually importable
# print("\n=== Attempting common imports ===")

# imports_to_try = [
#     "from evidently.report import Report",
#     "from evidently.metric_preset import DataDriftPreset",
#     "from evidently.metrics import ColumnDriftMetric",
#     "from evidently.test_suite import TestSuite",
#     "from evidently.ui.workspace import Workspace",
# ]

# for imp in imports_to_try:
#     try:
#         exec(imp)
#         print(f"✓ {imp}")
#     except Exception as e:
#         print(f"✗ {imp}")
#         print(f"  Error: {e}")

# from evidently.ui.workspace import Workspace
# from evidently.presets import DataDriftPreset
# Try finding what's available instead of DataQualityPreset
# import evidently.presets

# List what you got
# import evidently.presets as presets
# print("Available presets:", [x for x in dir(presets) if 'Preset' in x])
