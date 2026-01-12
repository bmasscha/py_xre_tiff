"""
XRE TIFF Read/Write Library

This module provides functions to read and write XRE TIFF images.
XRE TIFF format consists of:
- 8-byte header containing image dimensions
- 16-bit unsigned integer (U16) image data
- TIFF description tag containing slope and offset for data conversion
"""

import numpy as np
import struct
import re
from PIL import Image
from typing import Tuple, Optional


def read_xre_tif(path: str, rescale: bool = False) -> np.ndarray:
    """
    Read an XRE TIFF image.
    
    Parameters:
    -----------
    path : str
        Path to the XRE TIFF file
    rescale : bool, optional
        If True, convert U16 data to float using slope and offset from description tag.
        Formula: float_data = (u16_data * slope) + offset
        If False, return U16 data as-is (default: False)
    
    Returns:
    --------
    np.ndarray
        Image data as numpy array (dtype=uint16 if rescale=False, dtype=float32 if rescale=True)
    """
    # Open the TIFF file with PIL
    with Image.open(path) as img:
        # Convert to numpy array
        data = np.array(img, dtype=np.uint16)
        
        # Extract slope and offset from description tag if rescaling
        if rescale:
            slope, offset = _extract_slope_offset(img)
            # Apply conversion: float_data = (u16_data * slope) + offset
            data = data.astype(np.float32) * slope + offset
    
    return data


def write_xre_tif(path: str, data: np.ndarray, rescale: bool = False, 
                  slope: float = 1.0, offset: float = 0.0) -> None:
    """
    Write data to an XRE TIFF file.
    
    Parameters:
    -----------
    path : str
        Output path for the XRE TIFF file
    data : np.ndarray
        Image data to write (can be float or uint16)
    rescale : bool, optional
        If True, rescale float data to U16 using slope and offset.
        Formula: u16_data = (float_data - offset) / slope
        If False, convert float to U16 by clipping to [0, 65535] (default: False)
    slope : float, optional
        Slope value for data conversion (default: 1.0)
    offset : float, optional
        Offset value for data conversion (default: 0.0)
    
    Notes:
    ------
    - The description tag is written in format: "slope = X.XXXXXXE+XX offset = Y.YYYYYYE+YY"
    - All TIFF tags are written after the data
    - Data is stored as 16-bit unsigned integer (little-endian)
    """
    # Convert data to U16
    if rescale and data.dtype != np.uint16:
        # Apply inverse conversion: u16_data = (float_data - offset) / slope
        if slope == 0:
            raise ValueError("Slope cannot be zero when rescaling")
        u16_data = ((data - offset) / slope).astype(np.uint16)
    else:
        # Direct conversion: clip to valid U16 range
        if data.dtype != np.uint16:
            u16_data = np.clip(data, 0, 65535).astype(np.uint16)
        else:
            u16_data = data
    
    # Create PIL Image from numpy array
    img = Image.fromarray(u16_data, mode='I;16')
    
    # Prepare description tag with slope and offset
    description = f"slope = {slope:.6E} offset = {offset:.6E}"
    
    # Save TIFF with metadata
    # Note: PIL handles the TIFF structure, including writing tags after data
    img.save(path, format='TIFF', compression=None, 
             description=description,
             software='py_xre_tiff')


def _extract_slope_offset(img: Image.Image) -> Tuple[float, float]:
    """
    Extract slope and offset from TIFF description tag.
    
    Parameters:
    -----------
    img : PIL.Image.Image
        Opened PIL Image object
    
    Returns:
    --------
    tuple
        (slope, offset) as floats. Returns (1.0, 0.0) if not found.
    """
    slope, offset = 1.0, 0.0
    
    # Try to get description tag (tag 270)
    if hasattr(img, 'tag_v2'):
        desc = img.tag_v2.get(270)
        if desc:
            # Parse slope and offset using regex
            # Expected format: "slope = 1.000000E+00 offset = 0.000000E+00"
            slope_match = re.search(r'slope\s*=\s*([\d.Ee+-]+)', desc, re.IGNORECASE)
            offset_match = re.search(r'offset\s*=\s*([\d.Ee+-]+)', desc, re.IGNORECASE)
            
            if slope_match:
                slope = float(slope_match.group(1))
            if offset_match:
                offset = float(offset_match.group(1))
    
    return slope, offset


def get_metadata(path: str) -> dict:
    """
    Get metadata from an XRE TIFF file.
    
    Parameters:
    -----------
    path : str
        Path to the XRE TIFF file
    
    Returns:
    --------
    dict
        Dictionary containing 'slope', 'offset', 'width', 'height', 'dtype'
    """
    with Image.open(path) as img:
        slope, offset = _extract_slope_offset(img)
        width, height = img.size
        
        return {
            'slope': slope,
            'offset': offset,
            'width': width,
            'height': height,
            'dtype': img.mode
        }


if __name__ == '__main__':
    # Simple test
    print("XRE TIFF Library")
    print("=" * 60)
    print("Functions available:")
    print("  - read_xre_tif(path, rescale=False)")
    print("  - write_xre_tif(path, data, rescale=False, slope=1.0, offset=0.0)")
    print("  - get_metadata(path)")
    print("\nUse test_xre_tiff.py for comprehensive testing.")
