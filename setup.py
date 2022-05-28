import setuptools

LICENSE = "ISC"
DIR = "adoc_math"
VERSION = "1.0.0"
NAME = "adoc-math"
SETUP_DIR = "_setup"
README = "README.adoc"
AUTHOR = "Dominik Teiml"
PYTHON_REQUIRES = ">=3.7"
DESCRIPTION = """Use MathJax (Latex or AsciiMath) in your AsciiDoc projects!"""


extras_require = dict(
    tests=[
        "pytest >= 6.2.5, < 7.0.0",
    ]
)

packages = [
    f"{DIR}." + some_dir
    for some_dir in setuptools.find_namespace_packages(DIR)
    if "tests" not in some_dir.split(".")
] + [DIR]

entry_points = dict(
    console_scripts=[
        f"{NAME} = {DIR}.__main__:main",
        f"{NAME}-link = {DIR}.{SETUP_DIR}.link:main",
        f"{NAME}-install = {DIR}.{SETUP_DIR}.install:main",
        f"{NAME}-setup = {DIR}.{SETUP_DIR}.__main__:main",
    ]
)

with open(README) as f:
    long_description = f.read()

setuptools.setup(
    name=NAME,
    author=AUTHOR,
    version=VERSION,
    license=LICENSE,
    packages=packages,
    description=DESCRIPTION,
    entry_points=entry_points,
    extras_require=extras_require,
    python_requires=PYTHON_REQUIRES,
    long_description=long_description,
)
