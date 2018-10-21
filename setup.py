import setuptools
from pyrat import name, version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=version,
    author="Marek Miller",
    author_email="marek.l.miller@gmail.com",
    description="Raw tools for raw audio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitmarek/pyrat",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "scipy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
