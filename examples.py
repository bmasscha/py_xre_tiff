"""
Example usage of py_xre_tiff library.

This script demonstrates common use cases for reading and writing XRE TIFF files.
"""

from py_xre_tiff import read_xre_tif, write_xre_tif, get_metadata
import numpy as np
import matplotlib.pyplot as plt


def example_1_read_and_display():
    """Example 1: Read an XRE TIFF file and display it."""
    print("Example 1: Reading and displaying XRE TIFF file")
    print("=" * 60)
    
    # Read the file
    filepath = 'example data/recon_Al_00389.tif'
    data = read_xre_tif(filepath, rescale=False)
    
    print(f"Loaded: {filepath}")
    print(f"Shape: {data.shape}")
    print(f"Data type: {data.dtype}")
    print(f"Value range: [{data.min()}, {data.max()}]")
    
    # Display
    plt.figure(figsize=(8, 8))
    plt.imshow(data, cmap='gray')
    plt.title('XRE TIFF Image (U16)')
    plt.colorbar(label='Intensity')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('example_1_output.png', dpi=150)
    print("Saved visualization to: example_1_output.png\n")


def example_2_metadata_extraction():
    """Example 2: Extract and display metadata."""
    print("Example 2: Extracting metadata")
    print("=" * 60)
    
    filepath = 'example data/recon_Al_00389.tif'
    metadata = get_metadata(filepath)
    
    print(f"File: {filepath}")
    print(f"Dimensions: {metadata['width']} x {metadata['height']}")
    print(f"Slope: {metadata['slope']}")
    print(f"Offset: {metadata['offset']}")
    print(f"Data type: {metadata['dtype']}\n")


def example_3_rescaling():
    """Example 3: Read with automatic rescaling."""
    print("Example 3: Reading with rescaling")
    print("=" * 60)
    
    filepath = 'example data/recon_Al_00389.tif'
    
    # Read without rescaling
    data_u16 = read_xre_tif(filepath, rescale=False)
    print(f"U16 data range: [{data_u16.min()}, {data_u16.max()}]")
    
    # Read with rescaling
    data_float = read_xre_tif(filepath, rescale=True)
    print(f"Float data range: [{data_float.min():.2f}, {data_float.max():.2f}]")
    
    # Get metadata to show the conversion
    metadata = get_metadata(filepath)
    print(f"\nConversion formula: float = (u16 * {metadata['slope']}) + {metadata['offset']}")
    print(f"Example: {data_u16[0, 0]} -> {data_float[0, 0]:.2f}\n")


def example_4_write_with_metadata():
    """Example 4: Write a TIFF file with custom slope/offset."""
    print("Example 4: Writing with custom slope/offset")
    print("=" * 60)
    
    # Create synthetic data
    data = np.random.rand(512, 512).astype(np.float32) * 1000.0 + 500.0
    print(f"Created synthetic data: {data.shape}, range [{data.min():.2f}, {data.max():.2f}]")
    
    # Write with custom slope and offset
    output_path = 'example_output.tif'
    slope = 0.01
    offset = 500.0
    
    write_xre_tif(output_path, data, rescale=True, slope=slope, offset=offset)
    print(f"Wrote to: {output_path}")
    print(f"Slope: {slope}, Offset: {offset}")
    
    # Verify by reading back
    metadata = get_metadata(output_path)
    print(f"\nVerification - metadata from file:")
    print(f"  Slope: {metadata['slope']}")
    print(f"  Offset: {metadata['offset']}\n")


def example_5_round_trip():
    """Example 5: Round-trip test (read, write, read again)."""
    print("Example 5: Round-trip test")
    print("=" * 60)
    
    # Read original
    original = read_xre_tif('example data/recon_Al_00389.tif', rescale=True)
    print(f"Original data range: [{original.min():.2f}, {original.max():.2f}]")
    
    # Get original metadata
    metadata = get_metadata('example data/recon_Al_00389.tif')
    
    # Write and read back
    write_xre_tif('roundtrip_test.tif', original, rescale=True,
                  slope=metadata['slope'], offset=metadata['offset'])
    readback = read_xre_tif('roundtrip_test.tif', rescale=True)
    
    # Compare
    diff = np.abs(original - readback)
    print(f"Readback data range: [{readback.min():.2f}, {readback.max():.2f}]")
    print(f"Max difference: {diff.max():.6f}")
    print(f"Mean difference: {diff.mean():.6f}")
    print(f"Round-trip successful: {diff.max() < 0.1}\n")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("XRE TIFF Library - Usage Examples")
    print("=" * 60 + "\n")
    
    example_1_read_and_display()
    example_2_metadata_extraction()
    example_3_rescaling()
    example_4_write_with_metadata()
    example_5_round_trip()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
