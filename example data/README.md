# Example Data

This directory contains sample XRE TIFF files for testing and demonstration purposes.

## Files

- `recon_Al_00389.tif` - Aluminum reconstruction slice
- `recon_Al_00390.tif` - Aluminum reconstruction slice
- `recon_Al_00391.tif` - Aluminum reconstruction slice
- `recon_Al_00392.tif` - Aluminum reconstruction slice

## Metadata

These files contain:

- **Format**: 16-bit unsigned integer TIFF
- **Dimensions**: 1024 x 1024 pixels
- **Slope and Offset**: Stored in TIFF description tag for data conversion

## Usage

```python
from py_xre_tiff import read_xre_tif, get_metadata

# Read example file
data = read_xre_tif('example data/recon_Al_00389.tif', rescale=True)

# Get metadata
metadata = get_metadata('example data/recon_Al_00389.tif')
print(f"Slope: {metadata['slope']}, Offset: {metadata['offset']}")
```

## Attribution

These example files are provided for demonstration and testing of the py_xre_tiff library.
