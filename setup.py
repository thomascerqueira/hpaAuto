from cx_Freeze import setup, Executable

base = None    

executables = [Executable("pointageHPA.py", base=base)]

packages = ["idna", "os", "pynput"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "<first_ever>",
    options = options,
    version = "0.5",
    description = 'For pointing thing for HPA',
    executables = executables
)