import sys
import os
print(f"CWD: {os.getcwd()}")
print(f"Sys Path: {sys.path}")
try:
    import app.main
    print(f"App Main File: {app.main.__file__}")
    if hasattr(app.main, 'read_root'):
        import inspect
        print("Source of read_root:")
        print(inspect.getsource(app.main.read_root))
except Exception as e:
    print(f"Error importing: {e}")
