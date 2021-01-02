from setuptools import setup
from setuptools import find_packages

with open("./README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="rdm-file-selector",
    description="Randomly selects files and copies them to a destination, in a way that's less likely to pick previous files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0.5",
    url="https://github.com/Vinesma/rdm-file-selector",
    author="Otavio Cornelio",
    author_email="vinesma.work@gmail.com",
    license="MIT",
    scripts=["scripts/rdm-file-selector"],
    packages=find_packages("src"),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[]
)
