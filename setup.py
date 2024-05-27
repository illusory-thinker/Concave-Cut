import os
import numpy
from Cython.Build import cythonize

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    # config = Configuration('pycppfuns', parent_package, top_path)
    config = Configuration()

    if os.name == "nt":
        ext_comp_args = ['/']
        ext_link_args = []

        library_dirs = []
        libraries = []
    else:
        #                                                                      for each par
        ext_comp_args = ['-fopenmp', '-O3', '-std=c++23', '-DNDEBUG', '-mfma', '-m64', '-DPARALLEL', '-DHAVE_FMA']
        ext_link_args = ['-fopenmp']

        library_dirs = []
        libraries = ["m"]

    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]

    cyname = "cppfuns_"
    config.add_extension(cyname,
                         sources=[f'{cyname}.pyx'],
                         include_dirs = [numpy.get_include()],
                         language="c++",

                         extra_compile_args=ext_comp_args,
                         extra_link_args=ext_link_args,

                         library_dirs=library_dirs,
                         libraries=libraries,
                         depends=[f"{cyname}.pxd", f"{cyname}.pyx"]
                         #  define_macros=cg.define_macros,
                         )

    config.ext_modules = cythonize(config.ext_modules, compiler_directives={'language_level': 3})

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())