from setuptools import setup
import re
import shutil

_version_re = re.compile(r"(?<=^__version__ = (\"|'))(.+)(?=\"|')")

def get_version(rel_path: str) -> str:
    """
    Searches for the ``__version__ = `` line in a source code file.

    https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
    """
    with open(rel_path, 'r') as f:
        matches = map(_version_re.search, f)
        filtered = filter(lambda m: m is not None, matches)
        version = next(filtered, None)
        if version is None:
            raise RuntimeError(f'Could not find __version__ in {rel_path}')
        return version.group(0)


# add script to $PATH for installing outside of container
scripts = []
if shutil.which('surface_fit_script.pl') is None:
    scripts = ['base/surface_fit_script.pl']


setup(
    name='gifit',
    version=get_version('gifit/__init__.py'),
    description='Outer to inner surface mesh deformation using a radial distance map for human fetal MRI',
    author='FNNDSC',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-gifit',
    packages=['gifit'],
    install_requires=['chris_plugin', 'pandas', 'loguru'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'gifit = gifit.__main__:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1'
        ]
    },
    package_data={
        'gifit': ['models/*']
    },
    scripts=scripts
)
