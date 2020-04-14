#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" Simple script to test an URL is valid for use and has wanted permissions """

import sys

from kiwixstorage import KiwixStorage


def test_url_access(url):
    s3 = KiwixStorage(url)
    print(f"testing: {s3.url.geturl()}")

    for test in ("list_buckets", "bucket", "write", "write_and_read"):
        params = {test: True}
        if test == "write_and_read":
            params = {"write": True, "read": True}
        result = s3.check_credentials(failsafe=True, **params)
        print(f"can {test}: {result}")
        if test == "list_buckets":
            print(f"{s3.bucket_names=}")


def test_url():
    if len(sys.argv) < 2:
        print("you must pass an URL to test.")
        sys.exit(1)

    test_url_access(*sys.argv[1:])


if __name__ == "__main__":
    test_url()
