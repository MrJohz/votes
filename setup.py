from setuptools import setup
from setuptools.command.test import test as TestCommand

import sys

USING_35 = sys.version_info[0] == 3 and sys.version_info[1] == 5
SHIM_LIBRARIES = []
try:
    from unittest import mock
except ImportError:
    SHIM_LIBRARIES.append('mock==1.3.0')

class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', 'Arguments to pass to py.test'),
        ('cruel', 'c', 'Run pep8/flake testing with py.test')
    ]
    pytest_args = []
    cruel = False

    def initialise_options(self):
        super().initialise_options()
        self.pytest_args = []
        self.cruel = False

    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        if self.cruel:
            self.pytest_args.extend(('--pep8', '--flakes'))
        if USING_35:
            self.pytest_args.append('--assert=plain')
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='votes',
    version='0.0.1',
    description='Webapp for determining voting preferences',
    long_description=open('README.rst').read(),

    url='https://github.com/MrJohz/votes',
    author='Jonathan Frere',
    license='MIT',
    packages=['votes'],
    install_requires=list(open('requirements.txt')),
    extras_require={'dev': list(open('dev-requirements.txt')) + SHIM_LIBRARIES},
    tests_require = list(open('dev-requirements.txt')) + SHIM_LIBRARIES,
    cmdclass = {'test': PyTest}
)
