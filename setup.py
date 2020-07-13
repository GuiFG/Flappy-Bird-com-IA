import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("flappy.py", base=base)
]

buildOptions = dict(
        packages = [],
        includes = ["pygame", "random", "sys", "os", "time", "sqlite3"],
        include_files = ["flappy.ico", "assets/", "Network.txt"],
        excludes = []
)


setup(
    name = "Flappy Bird",
    version = "1.0",
    description = "Game Flappy Bird",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
