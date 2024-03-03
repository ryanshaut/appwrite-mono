import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyappwriteutils",
    version="0.0.1",
    author="ryan@shaut.us",
    author_email="ryan@shaut.us",
    description="Utilities for working with Appwrite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryanshaut/appwrite-mono/tree/main/shared",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)