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
  log = configurator.init_logger(name='save_weather',
                               log_path=os.path.join(cfg.APP_PATH, 'logs')
                              )
  minio_cfg = configurator.init_minio_config()
  helper.make_sure_path_exists(cfg.archive_path)

  files_list = []

  # Get the list of files to be uploaded. We only process Parquet and JSON files
  for f in os.listdir(cfg.output_path):
    if f.endswith(".parquet") or f.endswith(".json"):
      files_list.append(os.path.join(cfg.output_path, f))


  total_files = len(files_list)
  log.info("Count of files to save: {}".format(total_files))


  # Process the files if any
  if total_files:
    # Connect to S3 bucket
    client = Minio(minio_cfg['url'], minio_cfg['access_key'], minio_cfg['secret_key'])
    tags = Tags(for_object=True)
    tags["Content"] = "Weather data"

    for f in files_list:
      if f.endswith(".parquet"):
        f_basic = "{}/{}".format('parquet', os.path.basename(f))
      elif f.endswith(".json"):
        f_basic = "{}/{}".format('json', os.path.basename(f))
      else:
        f_basic = os.path.basename(f)
      w, lat, long, ts  = f_basic.split('_')
      tags['latitude']  = lat
      tags['longitude'] = long
      tags['timestamp'] = ts.split('.')[0]

      result = client.fput_object(minio_cfg['bucket_w_in'], f_basic, f, tags=tags)
      log.info("Created '{0}' with etag '{1}'".format(
                result.object_name, result.etag
              ))

      # Move processed file to archive
      if result.object_name == f_basic:
        # Create archive directory based on file's date
        py, pm, pd = ts[0:4], ts[4:6], ts[6:8]
        target_path = os.path.join(cfg.archive_path, py, pm, pd)
        helper.make_sure_path_exists(target_path)
        shutil.move(f, target_path)

    output = { 'total_files': total_files,
               'total_processed': total_files,
               'target_bucket': minio_cfg['bucket_w_in'] }

  else:
    output = { 'total_files': total_files,
               'total_processed': 0,
               'target_bucket': minio_cfg['bucket_w_in'] }

  print(json.dumps(output))
