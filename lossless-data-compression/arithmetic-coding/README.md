# Arithmetic coding
## About
Naive [arithmetic coding algorithm](https://en.wikipedia.org/wiki/Arithmetic_coding) implementation.
It doesn't contain value rounding, binary operations, etc.


## Requirements
- Python >= 3.6

## Usage

### Basig usage
```
usage: python3 main.py [-h] [--precision PRECISION] {compress,decompress} input output

positional arguments:
  {compress,decompress}
                        Option for either compressing or decompressing input file
  input                 Name of the input file
  output                Name of the output file

optional arguments:
  -h, --help            show this help message and exit
  --precision PRECISION
                        Number of decimal places for controlling algorithms quality
```

### Details
 
For compressing file run 
```
python3 main.py compress input.txt compressed.txt 
```
where `input.txt` is a file with text and `compressed.txt` is a file with compressed data.

For decompressing file run 
```
python3 main.py decompress compressed.txt decompressed.txt
```
where `compressed.txt` is a file with compressed data and `decompressed.txt` is a file with output text.

All arithmetics is done with pythons `Decimal` class. One can pass optional argument `--precision` with any integer number, that will change number of decimal places in computations. 

By default it is set to 10000. But if one has huge files it is possible 
to control quality of compression and compression output size with this parameter.
