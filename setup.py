from pathlib import Path

import setuptools

VERSION = "0.0.12"  # PEP-440

NAME = "theohe-epias"

INSTALL_REQUIRES = [
  "requests",
  "pandas",
  "pwinput"
]


setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Energy Exchange Istanbul (EXIST) or Enerji Piyasaları İşletme A.Ş. (EPİAŞ) by its Turkish name is an energy exchange company.",
    url="https://github.com/onurhakki/exist",
    project_urls={
        "Source Code": "https://github.com/onurhakki/exist",
    },
    author="Onur Hakkı Eyüboğlu",
    author_email="eyubogluo@itu.edu.tr",
    license="MIT License",
    python_requires=">=3.8",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["theohe_epias"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)