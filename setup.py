from setuptools import setup, find_packages


version = '0.1'

setup(
    name = 'dreamtellers.mailing',
    version = version,
    description = "",
    long_description="""\
    """,
    classifiers = [],
    keywords = '',
    author = 'Alberto Valverde Gonzalez',
    author_email = 'alberto@toscat.net',
    url = 'http://www.dreamtellers.org',
    license = 'GPLv3',
    packages = find_packages(exclude=['ez_setup']),
    include_package_data = True,
    zip_safe = False,
    namespace_packages = ['dreamtellers'],
    test_suite="nose.collector",
    tests_require=["nose", "WebTest", "unittest2"],
    install_requires = [
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
        ],
    entry_points = """
    [console_scripts]
    webmailing = dreamtellers.mailing:main
    [paste.app_factory]
    main = dreamtellers.mailing:app_factory
    """,
    )
