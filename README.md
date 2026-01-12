# py_xre_tiff

A Python library for reading and writing XRE TIFF images with slope/offset metadata.

## Overview

XRE TIFF is a TIFF format variant that stores 16-bit unsigned integer image data along with slope and offset values in the TIFF description tag for data conversion. This library provides simple functions to read and write these files with optional automatic rescaling.

## Features

- **Read XRE TIFF files** with optional slope/offset conversion
- **Write XRE TIFF files** with custom slope/offset metadata
- **Extract metadata** (slope, offset, dimensions) from existing files
- **Automatic data type conversion** between U16 and float
- **Round-trip preservation** with minimal quantization error

## Installation

### Requirements

```bash
pip install numpy pillow matplotlib
```

## Quick Start

```python
from py_xre_tiff import read_xre_tif, write_xre_tif

# Read a file
data = read_xre_tif('image.tif', rescale=True)

# Write a file
write_xre_tif('output.tif', data, rescale=True, slope=0.001, offset=100.0)
```

## Examples

See [`examples.py`](examples.py) for comprehensive usage examples including:

- Reading and displaying images
- Extracting metadata
- Automatic rescaling
- Writing with custom slope/offset
- Round-trip verification

Run examples:

```bash
python examples.py
```

### Usage

```python
from py_xre_tiff import read_xre_tif, write_xre_tif, get_metadata

# Read TIFF file without rescaling (returns U16 data)
data_u16 = read_xre_tif('image.tif', rescale=False)

# Read with automatic rescaling (returns float data)
# Formula: float_data = (u16_data * slope) + offset
data_float = read_xre_tif('image.tif', rescale=True)

# Get metadata
metadata = get_metadata('image.tif')
print(f"Slope: {metadata['slope']}, Offset: {metadata['offset']}")

# Write TIFF file with custom slope/offset
write_xre_tif('output.tif', data_float, rescale=True, slope=0.001, offset=100.0)
```

## API Reference

### `read_xre_tif(path, rescale=False)`

Read an XRE TIFF image.

**Parameters:**

- `path` (str): Path to the XRE TIFF file
- `rescale` (bool): If True, convert U16 data to float using slope/offset

**Returns:**

- `numpy.ndarray`: Image data (uint16 or float32)

### `write_xre_tif(path, data, rescale=False, slope=1.0, offset=0.0)`

Write data to an XRE TIFF file.

**Parameters:**

- `path` (str): Output path for the XRE TIFF file
- `data` (numpy.ndarray): Image data to write
- `rescale` (bool): If True, rescale float data to U16 using slope/offset
- `slope` (float): Slope value for metadata (default: 1.0)
- `offset` (float): Offset value for metadata (default: 0.0)

### `get_metadata(path)`

Get metadata from an XRE TIFF file.

**Parameters:**

- `path` (str): Path to the XRE TIFF file

**Returns:**

- `dict`: Dictionary with 'slope', 'offset', 'width', 'height', 'dtype'

## Testing

Run the comprehensive test suite:

```bash
python test_xre_tiff.py
```

This will:

- Test reading example files
- Verify round-trip preservation
- Test rescaling functionality
- Generate visualization of results

## Format Details

XRE TIFF files are standard TIFF files with:

- 16-bit unsigned integer data (little-endian)
- Slope and offset stored in TIFF description tag (tag 270)
- Format: `"slope = X.XXXXXXE+XX offset = Y.YYYYYYE+YY"`

**Conversion formulas:**

- U16 to float: `float_data = (u16_data * slope) + offset`
- Float to U16: `u16_data = (float_data - offset) / slope`

## License

MIT License

## Author

Created for handling XRE TIFF format images with metadata preservation.
