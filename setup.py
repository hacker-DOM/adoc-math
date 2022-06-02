import setuptools

LICENSE = "ISC"
DIR = "adoc_math"
VERSION = "1.0.8"
NAME = "adoc-math"
SETUP_DIR = "_setup"
README = "README.adoc"
AUTHOR = "Dominik Teiml"
PYTHON_REQUIRES = ">=3.7"
INCLUDE_PACKAGE_DATA = True
HOMEPAGE = "https://github.com/hacker-dom/adoc-math"
DESCRIPTION = """Use MathJax (Latex or AsciiMath) in your AsciiDoc projects!"""
# text/asciidoc is not supported
# Ref: https://packaging.python.org/en/latest/specifications/core-metadata/#description-content-type
LONG_DESCRIPTION_CONTENT_TYPE = "text/plain"

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

data_files = [
    ("", [README]),
    (DIR, [f"{DIR}/d_mathjax_wrapper.js"]),
]

package_data = dict(DIR=["*.js"], NAME=["*.js"])

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
    homepage=HOMEPAGE,
    data_files=data_files,
    description=DESCRIPTION,
    entry_points=entry_points,
    package_data=package_data,
    extras_require=extras_require,
    python_requires=PYTHON_REQUIRES,
    long_description=long_description,
    include_package_data=INCLUDE_PACKAGE_DATA,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
)
