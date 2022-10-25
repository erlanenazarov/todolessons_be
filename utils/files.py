import uuid

from django.utils.deconstruct import deconstructible


def normalize_filename(filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return '{0}'.format(filename)


@deconstructible
class SetUploadPath(object):

    def __init__(self, path=''):
        self.path = path

    def __call__(self, _, filename):
        if self.path:
            return '{path}/{filename}'.format(path=self.path, filename=normalize_filename(filename))
        return normalize_filename(filename)
