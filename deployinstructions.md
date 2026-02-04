


## Update version
Update version in `setup.py > setup > vesion`

## Build
```
cd /path/to/pimpmyplot
python -m build
```



## Publish
```
twine upload dist/*
```

Note: Set your PyPI token in .pypirc or use `twine upload --skip-existing dist/*`