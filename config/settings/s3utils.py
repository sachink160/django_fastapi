import os
from tempfile import SpooledTemporaryFile

from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3Boto3Storage(S3Boto3Storage):
    """
    This is our custom version of S3Boto3Storage that fixes a bug in
    boto3 where the passed in file is closed upon upload.
    From:
    https://github.com/matthewwithanm/django-imagekit/issues/391#issuecomment-275367006
    https://github.com/boto/boto3/issues/929
    https://github.com/matthewwithanm/django-imagekit/issues/391
    """

    def _save(self, name, content):
        """
        We create a clone of the content file as when this is passed to
        boto3 it wrongly closes the file upon upload where as the storage
        backend expects it to still be open
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified
        # size. This file will be automatically deleted when closed by
        # boto3 or after exiting the `with` statement if the boto3 is fixed
        with SpooledTemporaryFile() as content_autoclose:

            # Write our original content into our copy that will be closed by boto3
            content_autoclose.write(content.read())

            # Upload the object which will auto close the
            # content_autoclose instance
            return super()._save(name, content_autoclose)


MediaRootS3BotoStorage = lambda: CustomS3Boto3Storage(location='food/media', file_overwrite=False)  # NOQA
StaticRootS3BotoStorage = lambda: CustomS3Boto3Storage(location='food/static', file_overwrite=True)  # NOQA
