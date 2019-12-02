# same-file-finder
Find duplicate files by message digest (hash)

## Usage

```bash
python3 main.py my/directory/which/may/have/duplicate/files/
```

## Algorithm

* Get all file sizes
* Make a group by the file size
* Find duplicate files in the same file-size group
