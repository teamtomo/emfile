# emfile

Basic utility to read tomography data from files in `*.em` format.

## Installation
```bash
pip install emfile
```

## Basic usage
```python
header, data = emfile.read(path, mmap=False, header_only=False)

emfile.write(path, data, overwrite=True)
```
