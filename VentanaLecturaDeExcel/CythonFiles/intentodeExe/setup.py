from cx_Freeze import setup, Executable

base = None


executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "Michel",
    options = options,
    version = "0.1",
    description = '<any description>',
    executables = executables
)
