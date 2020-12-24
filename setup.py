from setuptools import setup
from setuptools import find_packages

with open("./README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="rdmfileselector",
    description="Randomly selects files and copies them to a destination, in a way that's less likely to pick previous files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0.0",
    url="https://github.com/Vinesma/rdm-file-selector",
    author="Otavio Cornelio",
    author_email="vinesma.work@gmail.com",
    license="GPL",
    scripts=["scripts/rdmfileselector"],
    packages=find_packages("src"),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL 3.0 License"
    ],
    install_requires=[]
)
