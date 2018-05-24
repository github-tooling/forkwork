from setuptools import setup

setup(
    name='forkwork',
    version='0.1',
    py_modules=['forkwork'],
    install_requires=['click', 'github', 'requests'],
    entry_points='''
        [console_scripts]
        forkwork=forkwork.forkwork:cli
    ''',
)
