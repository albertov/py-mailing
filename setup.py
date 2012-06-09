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
    license = 'BSD',
    packages = find_packages(exclude=['ez_setup']),
    include_package_data = True,
    zip_safe = True,
    namespace_packages = ['dreamtellers'],
    test_suite="nose.collector",
    tests_require=["nose"],
    install_requires = [
        "bottle",
        "bottle_sqlalchemy",
        "markdown",
        "genshi",
        "SQLAlchemy",
        "Babel",
        "lxml",
        "cssutils",
        "ftputil",
        ],
    entry_points = """
        """,
    )
