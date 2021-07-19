from cx_Freeze import setup, Executable

base = None    

executables = [Executable("pointageHPA.py", base=base)]

packages = ["idna", "os", "pynput", "pyperclip", "tkinter", "time", "xlsxwriter"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Automatique",
    options = options,
    version = "2",
    description = 'For pointing thing for HPA',
    executables = executables
)