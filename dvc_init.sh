dvc init
dvc remote add -d my_storage s3://$(S3_BUCKET_NAME)
dvc remote modify my_storage endpointurl https://storage.yandexcloud.net
dvc remote modify --local my_storage credentialpath '.env'
dvc remote modify my_storage version_aware true