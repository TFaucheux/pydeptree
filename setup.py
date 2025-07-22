from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydeptree",
    version="0.3.1",
    author="Todd Faucheux",
    author_email="tfaucheux@gmail.com",
    description="A Python dependency tree analyzer with rich output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0",
        "rich>=12.0",
    ],
    entry_points={
        "console_scripts": [
            "pydeptree=pydeptree.cli:cli",
            "pydeptree-enhanced=pydeptree.cli_enhanced:cli",
            "pydeptree-advanced=pydeptree.cli_advanced:cli",
        ],
    },
)
