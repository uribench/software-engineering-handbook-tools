from subprocess import call
from setuptools import Command, setup, find_packages
from handbook_tools import __version__

class RunTests(Command):
    """Run all tests"""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests"""
        errno = call(['pytest', '--cov-report=term-missing', '--cov=handbook_tools'])
        raise SystemExit(errno)

setup(
    name='handbook-tools',
    version=__version__,
    description='Tools for maintaining the Software Engineering Handbook',
    url='https://github.com/uribench/software-engineering-handbook-tools',
    author_email='uribench@gmail.com',
    license = 'UNLICENSE',
    packages=['handbook_tools'],
    # packages = find_packages(exclude=['docs', 'tests*']),
    zip_safe=False,
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'handbook=handbook_tools.handbook:main',
        ],
    },
    cmdclass = {'test': RunTests},
)