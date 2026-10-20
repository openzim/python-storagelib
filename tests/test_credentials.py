# pyright: strict, reportPrivateUsage=false
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from kiwixstorage import KiwixStorage

URL = "s3://example.com/?keyId=key&secretAccessKey=secret&bucketName=dev"
URL_WITHOUT_BUCKET = "s3://example.com/?keyId=key&secretAccessKey=secret"


def make_storage() -> KiwixStorage:
    return KiwixStorage(URL)


def test_check_credentials_requires_a_test():
    with pytest.raises(ValueError, match="Nothing to test"):
        make_storage().check_credentials()


def test_check_credentials_delete_without_list_buckets():
    storage = make_storage()
    client = MagicMock()
    with patch.object(
        KiwixStorage, "client", new_callable=PropertyMock, return_value=client
    ):
        assert storage.check_credentials(delete=True) is True

    client.list_buckets.assert_not_called()
    client.put_object.assert_called_once()
    client.delete_object.assert_called_once()

    put_kwargs = client.put_object.call_args.kwargs
    delete_kwargs = client.delete_object.call_args.kwargs
    assert put_kwargs["Bucket"] == "dev"
    assert put_kwargs["Key"].startswith(".tests_access_delete/")
    assert delete_kwargs == {"Bucket": "dev", "Key": put_kwargs["Key"]}


def test_test_access_delete_with_key_does_not_write():
    storage = make_storage()
    client = MagicMock()
    with patch.object(
        KiwixStorage, "client", new_callable=PropertyMock, return_value=client
    ):
        key = storage.test_access_delete(key="some/key", bucket_name="other")

    assert key == "some/key"
    client.put_object.assert_not_called()
    client.delete_object.assert_called_once_with(Bucket="other", Key="some/key")


def test_test_access_delete_requires_bucket_name():
    with pytest.raises(ValueError):
        KiwixStorage(URL_WITHOUT_BUCKET).test_access_delete()


def test_check_credentials_delete_reuses_write_key():
    storage = make_storage()
    with (
        patch.object(storage, "test_access_write", return_value="written/key") as write,
        patch.object(storage, "test_access_delete") as delete,
    ):
        assert storage.check_credentials(write=True, delete=True) is True

    write.assert_called_once_with(key=None, bucket_name=None, check_read=False)
    delete.assert_called_once_with(key="written/key", bucket_name=None)


def test_check_credentials_delete_with_explicit_bucket():
    storage = make_storage()
    with (
        patch.object(storage, "test_access_bucket") as bucket,
        patch.object(storage, "test_access_delete") as delete,
    ):
        assert storage.check_credentials(delete=True, bucket="other") is True

    bucket.assert_called_once_with(bucket_name="other")
    delete.assert_called_once_with(key=None, bucket_name="other")


def test_check_credentials_delete_failure_is_failsafe():
    storage = make_storage()
    with patch.object(
        storage, "test_access_delete", side_effect=RuntimeError("denied")
    ):
        assert storage.check_credentials(delete=True, failsafe=True) is False

        with pytest.raises(RuntimeError, match="denied"):
            storage.check_credentials(delete=True)
