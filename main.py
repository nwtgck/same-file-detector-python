import argparse
import csv
import hashlib
import pathlib

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
  parser.add_argument("out-csv", type=str)
  parser.add_argument("target-directory", type=str)
  # (from: https://stackoverflow.com/a/16878364/2885946)
  args = vars(parser.parse_args())

  out_csv_path = args['out-csv']
  target_dir_path = args['target-directory']

  progress = ProgressPrinter()

  with open(out_csv_path, 'w', newline='') as csvfile:
    w = csv.writer(csvfile)

    for path in pathlib.Path(target_dir_path).rglob("*"):
      if not path.is_file():
        continue

      file_path = str(path)
      hash = file_sha1(file_path)
      w.writerow([hash, file_path])

      # Progress
      progress.print(file_path + "\r")
    print("")
