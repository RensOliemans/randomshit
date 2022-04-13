from setuptools import setup, find_packages

setup(
    name="wordle-parse",
    version="0.1.0",
    description="Parse worlde and wordle clones from WhatsApp chat export",
    url="https://github.com/RensOliemans/randomshit",
    license="GPLv3",
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)
