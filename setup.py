from setuptools import setup, find_packages

setup(
    name="xadrezmaster",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "click>=8.0.0",
        "pyyaml>=6.0.0",
        "rich>=10.0.0",
        "python-chess>=1.9.0",
        "stockfish>=3.28.0",
        "spacy>=3.5.0",
        "nltk>=3.8.1",
        "transformers>=4.30.0",
        "tracery>=0.1.1",
        "markovify>=0.9.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "sqlalchemy>=2.0.0",
        "pymongo>=4.3.0",
        "pygame>=2.5.0",
        "plotly>=5.14.0",
        "networkx>=3.1.0"
    ],
)
