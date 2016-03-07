"""
    Two classes for media storage
"""

from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

class FixedS3BotoStorage(S3BotoStorage):
    """
    fix the broken javascript admin resources with S3Boto on Django 1.4
    for more info see http://code.larlet.fr/django-storages/issue/121/s3boto-admin-prefix-issue-with-django-14
    """
    def url(self, name):
        url = super(FixedS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url

class StaticStorage(FixedS3BotoStorage):
    """
    Storage for static files.
    The folder is defined in settings.STATIC_S3_PATH
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.STATIC_S3_PATH
        super(StaticStorage, self).__init__(*args, **kwargs)

    def url(self, name):
        """
        Override static storage to disable credentials that break cache.
        See: http://stackoverflow.com/questions/15668443/
             django-storage-with-s3-boto-break-browser-cache
        """

        name = self._clean_name(name)
        return '{0}{1}'.format(settings.STATIC_URL, name)

class DefaultStorage(FixedS3BotoStorage):
    """
    Storage for uploaded media files.
    The folder is defined in settings.DEFAULT_S3_PATH
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.DEFAULT_S3_PATH
        super(DefaultStorage, self).__init__(*args, **kwargs)
