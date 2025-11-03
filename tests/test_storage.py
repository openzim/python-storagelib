# pyright: strict, reportPrivateUsage=false
from kiwixstorage import KiwixStorage


def test_init_storage():
    url = "s3://example.com/?keyId=key&secretAccessKey=secret&bucketName=dev"
    storage = KiwixStorage(url)
    assert storage.url is not None
    assert "keyid" in storage._params
    assert storage._params["keyid"] == "key"
    assert "secretaccesskey" in storage._params
    assert storage._params["secretaccesskey"] == "secret"
    assert "bucketname" in storage._params
    assert storage._params["bucketname"] == "dev"
