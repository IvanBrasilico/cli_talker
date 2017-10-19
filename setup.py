import ast
import re
from setuptools import find_packages, setup
import setuptools.command.test


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('cli_talker/__init__.py', encoding='utf8') as f:
    # Search for `__version__` on bottery/__init__.py and get its values
    version = ast.literal_eval(_version_re.search(f.read()).group(1))


setup(
    name='cli_talker',
    description='A CLI talker',
    version=version,
    url='https://github.com/IvanBrasilico',
    license='MIT',
    author='Ivan Brasilico',
    author_email='brasilico.ivan@gmail.com',
    packages=find_packages(),
    install_requires=[
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
    package_data={
        'cli_talker': ['/locale/*'],
    },
    extras_require={
        'dev': [
            'coverage',
            'flake8',
            'isort',
            'pytest',
            'pytest-cov',
            'pytest-mock',
            'sphinx',
            'testfixtures',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.5',
    ],
)
