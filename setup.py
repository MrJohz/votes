from setuptools import setup

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
    extras_require={
        'dev': list(open('dev-requirements.txt'))
    }
)
