import argparse
import hashlib
import pathlib
from collections import defaultdict

class ProgressPrinter():
  def __init__(self):
    self.last_line_size = 0
  
  def print(self, text):
    l = len(text.encode("utf8"))
    spaces = ""
    if l < self.last_line_size:
      spaces = " " * (self.last_line_size)
    print(text + spaces + "\r", end="")
    self.last_line_size = l

  def end(self):
    print("")

# (base: https://rcmdnk.com/blog/2015/07/18/computer-python/)
def file_sha1(file_path, size=4096):
  m = hashlib.sha1()
  with open(file_path, 'rb') as f:
    for chunk in iter(lambda: f.read(size * m.block_size), b''):
      m.update(chunk)
  return m.hexdigest()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("target-directory", type=str)
  # (from: https://stackoverflow.com/a/16878364/2885946)
  args = vars(parser.parse_args())

  target_dir_path = args['target-directory']

  progress = ProgressPrinter()
  file_size_to_path = defaultdict(lambda: [])

  for path in pathlib.Path(target_dir_path).rglob("*"):
    if not path.is_file():
      continue
    file_path = str(path)
    file_size = path.stat().st_size
    file_size_to_path[file_size].append(file_path)

    # Progress
    progress.print(file_path + "\r")
  print("")

  # Iterate  
  for file_size, paths in file_size_to_path.items():
    if len(paths) == 1:
      continue

    # NOTE: group_by
    hash_to_path = defaultdict(lambda: [])
    for path in paths:
      hash = file_sha1(path)
      hash_to_path[hash].append(path)
    for hash, paths in hash_to_path.items():
      if len(paths) == 1:
        continue
      # Print files which have the same hash
      print(hash, paths)
