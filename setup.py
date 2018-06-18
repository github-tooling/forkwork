from setuptools import setup

setup(
    name='forkwork',
    version='0.2',
    py_modules=['forkwork'],
    install_requires=['click', 'requests', 'github3.py', 'cachecontrol', 'tabulate', 'python-dotenv'],
    entry_points='''
        [console_scripts]
        forkwork=forkwork.forkwork:cli
    ''',
)
