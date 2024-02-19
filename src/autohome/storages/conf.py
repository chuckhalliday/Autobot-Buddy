from autohome.env import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_ID", default=None)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS", default=None)
AWS_STORAGE_BUCKET_NAME = "autoadvisorbucket"
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'us-west-2'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True

DEFAULT_FILE_STORAGE = 'autohome.storages.backends.MediaStorage'

STATICFILES_STORAGE = 'autohome.storages.backends.StaticFileStorage'