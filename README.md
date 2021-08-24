kiwixstorage
============

[![CodeFactor](https://www.codefactor.io/repository/github/openzim/python-storagelib/badge)](https://www.codefactor.io/repository/github/openzim/python-storagelib)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version shields.io](https://img.shields.io/pypi/v/kiwixstorage)](https://pypi.org/project/kiwixstorage/)

helpers for S3 storage, autoconf from URL + Wasabi (wasabisys.com) extras

Goal is mainly to provide a configured s3.client and s3.resource from an URL
Users could limit usage to this and use [boto3](https://boto3.amazonaws.com/) directly from there.

A few additional wrappers are in place to simplify common actions.
Also, non-S3, wasabi-specific features are exposed directly.

# Usage

``` sh
pip install kiwixstorage
```

## Connection

``` py
from kiwixstorage import KiwixStorage
url = "https://s3.us-east-1.wasabisys.com/?keyId=x&secretAccessKey=y&bucketName=z"
s3 = KiwixStorage(url)
# test credentials and ensure we can list buckets
if not s3.check_credentials(list_buckets=True, failsafe=True):
    return # bad auth
```

## Scraper use-case

``` py
online_url = "https://xxx"
fpath = "/local/path.ext"
# retrieve origin etag
etag = requests.head(online_url, allow_redirects=True).headers.get("Etag")
# check if we have that very same version in store
if s3.has_matching_object(key=url, etag=etag)
    # lastest version in our store, download from there (using progress output)
    s3.download_file(key=url, fpath=fpath, progress=True)
else:
    # download the origin file using your regular tools
    download_file(url, fpath)
    # upload it our storage
    s3.upload_file(fpath=fpath, key=url)
# now you have a local file of lastest version and the storage is up to date
```

# Other use cases

``` py
# create a bucket
bucket = s3.create_bucket("bucket_name")

# set auto-delete on bucket
s3.set_bucket_autodelete_after(nb_days=7)

# allow public downloads from bucket
s3.allow_public_downloads_on()

# upload a file
s3.upload_file(fpath, "some/path/file.img", meta={"ENCODER_VERSION": "v1"})

# set autodelete on specific file
s3.set_object_autodelete_on(key, datetime.datetime.now())

# download a file
s3.download_file(key, fpath)

# get URL for external download
s3.get_download_url(key)

```

# Resources:

* https://wasabi.com/wp-content/themes/wasabi/docs/API_Guide
* https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
