#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import pathlib
from setuptools import setup, find_packages

root_dir = pathlib.Path(__file__).parent


def read(*names, **kwargs):
    with open(root_dir.joinpath(*names), "r") as fh:
        return fh.read()


setup(
    name="kiwixstorage",
    version=read("src", "kiwixstorage", "VERSION").strip(),
    description="Kiwix S3 Cache wrapper to use within Kiwix/OpenZIM projects",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="kiwix",
    author_email="reg@kiwix.org",
    url="https://github.com/kiwix/python_storagelib",
    keywords="kiwix zim offline aws s3",
    license="GPLv3+",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        line.strip()
        for line in read("requirements.txt").splitlines()
        if not line.strip().startswith("#")
    ],
    setup_requires=["pytest-runner"],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "s3_test_url=kiwixstorage.test_credentials:test_url",
            "s3upload=kiwixstorage.upload:upload_file",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    python_requires=">=3.8",
)
