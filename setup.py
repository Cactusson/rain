import sys
import os
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

exe = Executable(script='rain.py', base=base)

include_files = [os.path.join('resources', 'fonts'),
                 os.path.join('resources', 'graphics')]
includes = []
excludes = []
packages = []

setup(version='1.0',
      description='A math puzzle game',
      author='cactusson',
      name='Rain',
      options={'build_exe': {'includes': includes,
                             'include_files': include_files,
                             'packages': packages,
                             'excludes': excludes}},
      executables=[exe])
