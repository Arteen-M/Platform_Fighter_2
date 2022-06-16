import cx_Freeze
import sys

name = "Platform Fighter"
ver = "1.0.0"

base = None
# Conversion to EXE doesn't support other OS' for now
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {"packages": ["os", "pygame"]}

cx_Freeze.setup(
    name=name,
    version=ver,
    options={"build_exe": build_exe_options},
    executables=[cx_Freeze.Executable("Fighter.py", base=base)]
)

# python setup.py build
