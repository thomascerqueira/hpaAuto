from cx_Freeze import setup, Executable

base = None    

executables = [Executable("test.py", base=base)]

packages = ["idna", "os", "pynput"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "autoPoint",
    options = options,
    version = "0.5",
    description = 'For pointing thing for HPA',
    executables = executables
)