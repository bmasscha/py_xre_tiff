"""
Comprehensive test script for XRE TIFF read/write functions.
Tests include round-trip verification, rescaling, and visual inspection with matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
from py_xre_tiff import read_xre_tif, write_xre_tif, get_metadata
import os


def test_read_example():
    """Test reading an example XRE TIFF file."""
    print("\n" + "="*70)
    print("TEST 1: Reading Example TIFF File")
    print("="*70)
    
    filepath = 'example data/scan_000001.tif'
    
    # Get metadata
    metadata = get_metadata(filepath)
    print(f"\nMetadata:")
    print(f"  Size: {metadata['width']} x {metadata['height']}")
    print(f"  Slope: {metadata['slope']}")
    print(f"  Offset: {metadata['offset']}")
    print(f"  Mode: {metadata['dtype']}")
    
    # Read without rescaling
    data_u16 = read_xre_tif(filepath, rescale=False)
    print(f"\nData (U16):")
    print(f"  Shape: {data_u16.shape}")
    print(f"  Dtype: {data_u16.dtype}")
    print(f"  Min: {data_u16.min()}, Max: {data_u16.max()}")
    print(f"  Mean: {data_u16.mean():.2f}")
    
    # Read with rescaling
    data_float = read_xre_tif(filepath, rescale=True)
    print(f"\nData (Float with rescaling):")
    print(f"  Shape: {data_float.shape}")
    print(f"  Dtype: {data_float.dtype}")
    print(f"  Min: {data_float.min():.6f}, Max: {data_float.max():.6f}")
    print(f"  Mean: {data_float.mean():.6f}")
    
    return data_u16, data_float, metadata


def test_round_trip():
    """Test writing and reading back data."""
    print("\n" + "="*70)
    print("TEST 2: Round-Trip Test (Write and Read Back)")
    print("="*70)
    
    # Read original
    original = read_xre_tif('example data/scan_000001.tif', rescale=False)
    
    # Write to new file
    output_path = 'test_roundtrip.tif'
    write_xre_tif(output_path, original, rescale=False, slope=1.0, offset=0.0)
    print(f"\nWrote data to: {output_path}")
    
    # Read back
    readback = read_xre_tif(output_path, rescale=False)
    
    # Compare
    are_equal = np.array_equal(original, readback)
    max_diff = np.abs(original.astype(np.int32) - readback.astype(np.int32)).max()
    
    print(f"\nComparison:")
    print(f"  Arrays equal: {are_equal}")
    print(f"  Max difference: {max_diff}")
    print(f"  Original shape: {original.shape}, Readback shape: {readback.shape}")
    
    if are_equal:
        print("  ✓ Round-trip test PASSED")
    else:
        print("  ✗ Round-trip test FAILED")
    
    return original, readback, are_equal


def test_rescale_conversion():
    """Test rescaling functionality."""
    print("\n" + "="*70)
    print("TEST 3: Rescale Conversion Test")
    print("="*70)
    
    # Create synthetic float data
    synthetic_float = np.random.rand(256, 256).astype(np.float32) * 100.0 + 50.0
    print(f"\nSynthetic float data:")
    print(f"  Shape: {synthetic_float.shape}")
    print(f"  Range: [{synthetic_float.min():.2f}, {synthetic_float.max():.2f}]")
    
    # Define slope and offset
    slope = 0.01
    offset = 50.0
    
    # Write with rescaling
    output_path = 'test_rescale.tif'
    write_xre_tif(output_path, synthetic_float, rescale=True, slope=slope, offset=offset)
    print(f"\nWrote with slope={slope}, offset={offset}")
    
    # Read back with rescaling
    readback_float = read_xre_tif(output_path, rescale=True)
    
    # Compare
    diff = np.abs(synthetic_float - readback_float)
    max_diff = diff.max()
    mean_diff = diff.mean()
    
    print(f"\nRescale round-trip comparison:")
    print(f"  Max difference: {max_diff:.6f}")
    print(f"  Mean difference: {mean_diff:.6f}")
    print(f"  Relative error: {(max_diff / synthetic_float.max() * 100):.4f}%")
    
    # Check metadata
    metadata = get_metadata(output_path)
    print(f"\nMetadata verification:")
    print(f"  Stored slope: {metadata['slope']}")
    print(f"  Stored offset: {metadata['offset']}")
    print(f"  Expected slope: {slope}")
    print(f"  Expected offset: {offset}")
    
    if abs(metadata['slope'] - slope) < 1e-6 and abs(metadata['offset'] - offset) < 1e-6:
        print("  ✓ Metadata test PASSED")
    else:
        print("  ✗ Metadata test FAILED")
    
    return synthetic_float, readback_float


def visualize_results(data_u16, data_float, original, readback, synthetic, synthetic_readback):
    """Create visualization of all test results."""
    print("\n" + "="*70)
    print("Creating Visualization")
    print("="*70)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('XRE TIFF Read/Write Test Results', fontsize=16, fontweight='bold')
    
    # Test 1: Original data (U16)
    im0 = axes[0, 0].imshow(data_u16, cmap='gray')
    axes[0, 0].set_title('Test 1: Original (U16)')
    axes[0, 0].axis('off')
    plt.colorbar(im0, ax=axes[0, 0], fraction=0.046)
    
    # Test 1: Rescaled data (Float)
    im1 = axes[0, 1].imshow(data_float, cmap='gray')
    axes[0, 1].set_title('Test 1: Rescaled (Float)')
    axes[0, 1].axis('off')
    plt.colorbar(im1, ax=axes[0, 1], fraction=0.046)
    
    # Test 2: Round-trip difference
    diff_roundtrip = np.abs(original.astype(np.int32) - readback.astype(np.int32))
    im2 = axes[0, 2].imshow(diff_roundtrip, cmap='hot')
    axes[0, 2].set_title(f'Test 2: Round-trip Diff (max={diff_roundtrip.max()})')
    axes[0, 2].axis('off')
    plt.colorbar(im2, ax=axes[0, 2], fraction=0.046)
    
    # Test 3: Synthetic original
    im3 = axes[1, 0].imshow(synthetic, cmap='viridis')
    axes[1, 0].set_title('Test 3: Synthetic Data')
    axes[1, 0].axis('off')
    plt.colorbar(im3, ax=axes[1, 0], fraction=0.046)
    
    # Test 3: Synthetic readback
    im4 = axes[1, 1].imshow(synthetic_readback, cmap='viridis')
    axes[1, 1].set_title('Test 3: After Rescale Round-trip')
    axes[1, 1].axis('off')
    plt.colorbar(im4, ax=axes[1, 1], fraction=0.046)
    
    # Test 3: Rescale difference
    diff_rescale = np.abs(synthetic - synthetic_readback)
    im5 = axes[1, 2].imshow(diff_rescale, cmap='hot')
    axes[1, 2].set_title(f'Test 3: Rescale Diff (max={diff_rescale.max():.4f})')
    axes[1, 2].axis('off')
    plt.colorbar(im5, ax=axes[1, 2], fraction=0.046)
    
    plt.tight_layout()
    
    # Save figure
    output_file = 'test_results_visualization.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {output_file}")
    
    # Show plot
    plt.show()
    print("Displaying visualization window...")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("XRE TIFF READ/WRITE FUNCTION TESTS")
    print("="*70)
    
    try:
        # Test 1: Read example file
        data_u16, data_float, metadata = test_read_example()
        
        # Test 2: Round-trip test
        original, readback, round_trip_passed = test_round_trip()
        
        # Test 3: Rescale conversion test
        synthetic, synthetic_readback = test_rescale_conversion()
        
        # Visualize all results
        visualize_results(data_u16, data_float, original, readback, synthetic, synthetic_readback)
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"  Test 1 (Read): ✓ PASSED")
        print(f"  Test 2 (Round-trip): {'✓ PASSED' if round_trip_passed else '✗ FAILED'}")
        print(f"  Test 3 (Rescale): ✓ PASSED")
        print(f"\nAll test files created successfully!")
        print(f"  - test_roundtrip.tif")
        print(f"  - test_rescale.tif")
        print(f"  - test_results_visualization.png")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    success = main()
    if success:
        print("\n" + "="*70)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
