from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ipython>=6", "numpy>=1", "matplotlib>=3"]

setup(
    name="projetoOraBolas",
    version="0.0.1",
    author="Joao Victor, Pietra Marques, Lucca",
    author_email="safreirejoaov@gmail.com",
    description="Projeto OraBolas FEI",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/JoaoVictor1910/projetoOraBolas/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)