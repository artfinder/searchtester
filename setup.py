# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

PACKAGE = 'searchtester'
VERSION = '0.1'

setup(
    name=PACKAGE, version=VERSION,
    description="Simple system for testing search results, and using that to measure effectiveness of your current search ranking",
    packages=[ 'searchtester' ],
    license='MIT',
    author='Art Dicovery Ltd',
    install_requires=[
        'lxml',
        'eventlet',
        'unittest2',
    ],
    url = 'http://code.artfinder.com/projects/searchtester/',
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
    ],
    entry_points= {
        'console_scripts': [
            'searchtest = searchtester:runtest',
        ],
    },
    test_suite="unittest2.collector",
)
