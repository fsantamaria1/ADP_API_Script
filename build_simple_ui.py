import PyInstaller.__main__

tkinter_app = "simple_ui.py"
extra_import = "pyodbc"

options = [
    '--onefile',
    '-w',
    '--add-data', '.env;.',
    f'{tkinter_app}',
    f'--hidden-import={extra_import}',
    '--name', 'ADP Script'
]

PyInstaller.__main__.run(options)
