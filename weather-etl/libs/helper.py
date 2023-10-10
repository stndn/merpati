import os
import errno

"""
Ensure path exists
Ref1: https://stackoverflow.com/questions/32123394/workflow-to-create-a-folder-if-it-doesnt-exist-already
Ref2: https://stackoverflow.com/questions/273192/how-do-i-create-a-directory-and-any-missing-parent-directories
"""
def make_sure_path_exists(path):
  try:
    os.makedirs(path)
  except OSError as exception:
    if exception.errno != errno.EEXIST:
      raise

