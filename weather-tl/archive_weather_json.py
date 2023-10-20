import os
import json
from libs import configurator
from minio import Minio
from minio.commonconfig import CopySource
from minio.deleteobjects import DeleteObject


if __name__ == '__main__':

  # Initialize all configurations
  cfg = configurator.init_config()
  log = configurator.init_logger(name='move_json_to_backup',
                               log_path=os.path.join(cfg.APP_PATH, 'logs')
                              )
  minio_cfg = configurator.init_minio_config()

  # Get the list of JSON files from MinIO bucket
  client = Minio(minio_cfg['url'], minio_cfg['access_key'], minio_cfg['secret_key'])

  # Object specifics
  total_object = 0
  total_copied = 0
  obj_list = del_list = failed_list = []

  object_list_file = os.path.join(cfg.tmp_path, 'weather-json-objects.txt')
  try:
    with open(object_list_file, 'r') as fp:
      lines = fp.readlines()
      obj_list = [ x.strip() for x in lines ]
  except IOError:
    log.error("Weather json objects not found. Exiting")
    raise

  obj_list = set(obj_list)
  total_object = len(obj_list)

  if client:
    log.info("Connected to S3 bucket at {}".format(minio_cfg['url']))

    for obj in obj_list:
      # Since MinIO does not support `move`, we need to first `copy_object`
      # before proceeding with `remove_object`

      total_object += 1
      basename = obj.split('/')[-1]
      log.info("Copying object {} from {} to {}".format(obj,
                                                    minio_cfg['bucket_w_in'],
                                                    minio_cfg['bucket_w_out']
                                                  ))

      result = client.copy_object(minio_cfg['bucket_w_out'], obj,
                                  CopySource(minio_cfg['bucket_w_in'], obj))

      if client.stat_object(minio_cfg['bucket_w_out'], result.object_name):
        del_list.append(DeleteObject(obj))
      else:
        failed_list.append(obj)

    total_copied = len(del_list)
    log.info("Copied total of {} files. Proceed to remove the files from original bucket", total_copied)

    remove_errors = client.remove_objects(minio_cfg['bucket_w_in'], del_list)
    for err in remove_errors:
      log.error("Error occured when deleting object: ", error)

    log.info("Copy/move {} objects/files from {} to {} completed".format(
                  total_copied, minio_cfg['bucket_w_in'], minio_cfg['bucket_w_out']))


    # Remove the list file object
    os.remove(object_list_file)
    log.info("Removed weather json object file: {}", object_list_file)

    output = { 'total_object': total_object,
               'total_moved': total_copied,
               'source_bucket': minio_cfg['bucket_w_in'],
               'target_bucket': minio_cfg['bucket_w_in']}


  else:
    log.error("Cannot connect to S3 bucket. Exiting.")
    output = { 'total_object': 0,
               'total_moved': 0,
               'source_bucket': minio_cfg['bucket_w_in'],
               'target_bucket': minio_cfg['bucket_w_in']}

  print(json.dumps(output))
