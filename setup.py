import sys
from setuptools import setup, find_packages

VERSION = '0.8a1'

INSTALL_REQUIRES = [
"bottle",
"PIL",
"formencode",
"markdown",
"mako",
"genshi",
"SQLAlchemy",
"Babel",
"lxml",
"cssutils",
"ftputil",
"pastescript",
"cssselect",
]

TESTS_REQUIRE = [
"nose",
"WebTest",
"unittest2",
]

if sys.version_info[:2] < (2, 6):
    INSTALL_REQUIRES.append('simplejson')
    TESTS_REQUIRE.insert(0, 'WebOb==1.1.1')

setup(
    name = 'pyMailing',
    version = VERSION,
    description = "",
    long_description="""\
    """,
    classifiers = [],
    keywords = '',
    author = 'Alberto Valverde Gonzalez',
    author_email = 'alberto@toscat.net',
    url = 'http://github.com/albertov/pyMailing',
    license = 'GPLv3',
    packages = find_packages(exclude=['ez_setup']),
    include_package_data = True,
    zip_safe = False,
    test_suite="nose.collector",
    tests_require=TESTS_REQUIRE,
    install_requires = INSTALL_REQUIRES,
    entry_points = """
    [console_scripts]
    mailing = mailing:main
    [paste.app_factory]
    main = mailing:app_factory
    """,
    )
