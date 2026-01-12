"""Simple test without matplotlib to check slope/offset values."""

from py_xre_tiff import read_xre_tif, write_xre_tif, get_metadata
import numpy as np

print("="*70)
print("TESTING NEW EXAMPLE FILES - Simple Test")
print("="*70)

# Test with first example file
filepath = 'example data/recon_Al_00389.tif'

try:
    # Get metadata
    print(f"\nReading: {filepath}")
    metadata = get_metadata(filepath)
    print(f"\nMetadata:")
    print(f"  Size: {metadata['width']} x {metadata['height']}")
    print(f"  Slope: {metadata['slope']}")
    print(f"  Offset: {metadata['offset']}")
    
    # Read U16
    data_u16 = read_xre_tif(filepath, rescale=False)
    print(f"\nU16 Data:")
    print(f"  Shape: {data_u16.shape}")
    print(f"  Range: [{data_u16.min()}, {data_u16.max()}]")
    print(f"  Mean: {data_u16.mean():.2f}")
    
    # Read with rescaling
    data_float = read_xre_tif(filepath, rescale=True)
    print(f"\nRescaled Float Data:")
    print(f"  Shape: {data_float.shape}")
    print(f"  Range: [{data_float.min():.6f}, {data_float.max():.6f}]")
    print(f"  Mean: {data_float.mean():.6f}")
    
    # Verify conversion
    print(f"\nVerifying conversion formula:")
    print(f"  Formula: float = (u16 * slope) + offset")
    expected_min = data_u16.min() * metadata['slope'] + metadata['offset']
    expected_max = data_u16.max() * metadata['slope'] + metadata['offset']
    print(f"  Expected min: {expected_min:.6f}")
    print(f"  Actual min: {data_float.min():.6f}")
    print(f"  Match: {abs(expected_min - data_float.min()) < 1e-5}")
    
    # Round-trip test
    print(f"\nRound-trip test:")
    write_xre_tif('test_simple_roundtrip.tif', data_float, rescale=True,
                  slope=metadata['slope'], offset=metadata['offset'])
    data_back = read_xre_tif('test_simple_roundtrip.tif', rescale=True)
    
    max_diff = np.abs(data_float - data_back).max()
    print(f"  Max difference: {max_diff:.6f}")
    print(f"  Success: {max_diff < 0.1}")
    
    print("\n" + "="*70)
    print("TEST PASSED!")
    print("="*70)
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
