from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("OpenSavePandasGUI.pyx")
    #ext_modules = cythonize("Verde.pyx")
)
