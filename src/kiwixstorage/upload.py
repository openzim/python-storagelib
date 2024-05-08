#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" Simple script to upload a file to a bucket, reusing S3_URL environ

    Optional dependencies:
    - humanfriendly
    - progressbar2 """

import argparse
import os
import pathlib
import sys

from kiwixstorage import KiwixStorage, __version__, format_size

try:
    import progressbar
except ImportError:
    progressbar = None

NAME = "s3upload"
FULLNAME = f"{NAME} v{__version__}"


class CustomProgressBar:
    def __init__(self, total: int = None):
        widgets = [
            " [",
            progressbar.Timer(),
            "] ",
            progressbar.DataSize(),
            progressbar.Bar(),
            progressbar.AdaptiveTransferSpeed(),
            " (",
            progressbar.ETA(),
            ") ",
        ]
        self.bar = progressbar.ProgressBar(max_value=total, widgets=widgets)
        self.seen_so_far = 0

    def callback(self, bytes_amount: int):
        self.seen_so_far += bytes_amount
        self.bar.update(self.seen_so_far)


def do_upload_file(url: str, fpath: pathlib.Path, key: str = None):
    if not fpath.exists():
        raise IOError(f"{fpath} missing.")
    fsize = fpath.stat().st_size
    if not key:
        key = fpath.name

    s3 = KiwixStorage(url)
    dest = f"s3://{s3.url.netloc}/{s3.bucket_name}"

    if s3.has_object(key):
        raise ValueError(f"Key `{key}` already exists at {dest}. Specify another one.")
    print(f"Uploading {fpath.name} ({format_size(fsize)}) to {dest}/{key}", flush=True)

    progress = CustomProgressBar(fsize).callback if progressbar else True
    s3.upload_file(fpath=fpath, key=key, progress=progress)


def upload_file():
    parser = argparse.ArgumentParser(
        prog="s3upload",
        description="KiwixStorage-based S3 single file uploader",
    )

    parser.add_argument(
        help="File to upload",
        dest="fpath",
    )

    parser.add_argument(
        "--key",
        help="Key to upload to. Defaults to fpath's name",
        default=None,
        dest="key",
    )

    parser.add_argument(
        "--url",
        help="S3 URL with credentials and bucketName. "
        "Defaults to `S3URL` environment variable",
        default=os.getenv("S3URL"),
        dest="url",
    )

    parser.add_argument(
        "--version",
        help="Display builder script version and exit",
        action="version",
        version=FULLNAME,
    )

    parser.set_defaults(url=os.getenv("S3URL"))
    kwargs = dict(parser.parse_args()._get_kwargs())
    kwargs["fpath"] = pathlib.Path(kwargs["fpath"]).expanduser().resolve()

    if not kwargs.get("url"):
        parser.error("the following arguments are required: --url")

    try:
        sys.exit(do_upload_file(**kwargs))
    except Exception as exc:
        print(f"FAILED. An error occurred: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    upload_file()
