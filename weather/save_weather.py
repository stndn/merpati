import os
import json
import requests
import shutil
import pandas as pd
from libs import configurator
from libs import helper
from minio import Minio
from minio.commonconfig import Tags


if __name__ == '__main__':

  # Initialize all configurations
  cfg = configurator.init_config()
  log = configurator.init_logger(name='log_app',
                               log_path=os.path.join(cfg.APP_PATH, 'logs')
                              )
  minio_cfg = configurator.init_minio_config()
  helper.make_sure_path_exists(cfg.archive_path)

  files_list = []

  # Get the list of files to be uploaded. We only need the Parquet files
  for f in os.listdir(cfg.output_path):
    if f.endswith(".parquet"):
      # Prints only text file present in My Folder
      files_list.append(os.path.join(cfg.output_path, f))

  files_count = len(files_list)
  log.info("Count of Parquet files to save: {}".format(files_count))


  # Process the files if any
  if files_count:
    # Connect to S3 bucket
    client = Minio(minio_cfg['url'], minio_cfg['access_key'], minio_cfg['secret_key'])
    tags = Tags(for_object=True)
    tags["Content"] = "weather data"

    for f in files_list:
      f_basic = os.path.basename(f)
      result = client.fput_object(minio_cfg['bucket_w_in'], f_basic, f,
                                  tags=tags,
                                 )
      log.info("Created '{0}' with etag '{1}'".format(
                result.object_name, result.etag
              ))

      # Move processed file to archive
      if result.object_name == f_basic:
        shutil.move(f, cfg.archive_path)

    output = { 'total_processed': files_count,
               'target_bucket': minio_cfg['bucket_w_in'] }

  else:
    output = { 'total_processed': 0,
               'target_bucket': minio_cfg['bucket_w_in'] }

  print(json.dumps(output))

