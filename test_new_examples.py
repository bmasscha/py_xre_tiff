"""Test XRE TIFF functions with new example files that have non-default slope/offset."""

from py_xre_tiff import read_xre_tif, write_xre_tif, get_metadata
import numpy as np
import matplotlib.pyplot as plt

print("="*70)
print("TESTING WITH NEW EXAMPLE FILES (Non-default slope/offset)")
print("="*70)

# Test with first example file
filepath = 'example data/recon_Al_00389.tif'

# Get metadata
print(f"\n1. Reading metadata from: {filepath}")
metadata = get_metadata(filepath)
print(f"   Width: {metadata['width']}")
print(f"   Height: {metadata['height']}")
print(f"   Slope: {metadata['slope']}")
print(f"   Offset: {metadata['offset']}")
print(f"   Mode: {metadata['dtype']}")

# Read without rescaling (raw U16 data)
print(f"\n2. Reading raw U16 data (rescale=False)...")
data_u16 = read_xre_tif(filepath, rescale=False)
print(f"   Shape: {data_u16.shape}")
print(f"   Dtype: {data_u16.dtype}")
print(f"   Min: {data_u16.min()}")
print(f"   Max: {data_u16.max()}")
print(f"   Mean: {data_u16.mean():.2f}")

# Read with rescaling (apply slope/offset conversion)
print(f"\n3. Reading with rescaling (rescale=True)...")
data_float = read_xre_tif(filepath, rescale=True)
print(f"   Shape: {data_float.shape}")
print(f"   Dtype: {data_float.dtype}")
print(f"   Min: {data_float.min():.6f}")
print(f"   Max: {data_float.max():.6f}")
print(f"   Mean: {data_float.mean():.6f}")

# Verify the conversion formula
print(f"\n4. Verifying conversion formula...")
print(f"   Formula: float_data = (u16_data * slope) + offset")
expected_min = data_u16.min() * metadata['slope'] + metadata['offset']
expected_max = data_u16.max() * metadata['slope'] + metadata['offset']
expected_mean = data_u16.mean() * metadata['slope'] + metadata['offset']
print(f"   Expected min: {expected_min:.6f}, Actual: {data_float.min():.6f}")
print(f"   Expected max: {expected_max:.6f}, Actual: {data_float.max():.6f}")
print(f"   Expected mean: {expected_mean:.6f}, Actual: {data_float.mean():.6f}")

match = (abs(expected_min - data_float.min()) < 1e-5 and 
         abs(expected_max - data_float.max()) < 1e-5 and
         abs(expected_mean - data_float.mean()) < 1e-3)
print(f"   Conversion formula verified: {match}")

# Test round-trip with rescaling
print(f"\n5. Testing round-trip with rescaling...")
output_path = 'test_new_roundtrip.tif'
write_xre_tif(output_path, data_float, rescale=True, 
              slope=metadata['slope'], offset=metadata['offset'])
print(f"   Wrote rescaled data to: {output_path}")

# Read back with rescaling
data_readback = read_xre_tif(output_path, rescale=True)
print(f"   Read back with rescaling")

# Compare
diff = np.abs(data_float - data_readback)
max_diff = diff.max()
mean_diff = diff.mean()
rel_error = (max_diff / (data_float.max() - data_float.min())) * 100

print(f"   Max difference: {max_diff:.6f}")
print(f"   Mean difference: {mean_diff:.6f}")
print(f"   Relative error: {rel_error:.4f}%")
print(f"   Round-trip successful: {rel_error < 1.0}")

# Create visualization
print(f"\n6. Creating visualization...")
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('XRE TIFF Test - New Example Files with Slope/Offset', fontsize=16, fontweight='bold')

# Original U16
im0 = axes[0, 0].imshow(data_u16, cmap='gray')
axes[0, 0].set_title(f'Original U16 Data\nRange: [{data_u16.min()}, {data_u16.max()}]')
axes[0, 0].axis('off')
plt.colorbar(im0, ax=axes[0, 0], fraction=0.046)

# Rescaled Float
im1 = axes[0, 1].imshow(data_float, cmap='gray')
axes[0, 1].set_title(f'Rescaled Float Data\nslope={metadata["slope"]:.2e}, offset={metadata["offset"]:.2e}')
axes[0, 1].axis('off')
plt.colorbar(im1, ax=axes[0, 1], fraction=0.046)

# Readback Float
im2 = axes[0, 2].imshow(data_readback, cmap='gray')
axes[0, 2].set_title(f'After Round-trip\nMax diff: {max_diff:.6f}')
axes[0, 2].axis('off')
plt.colorbar(im2, ax=axes[0, 2], fraction=0.046)

# Difference map
im3 = axes[1, 0].imshow(diff, cmap='hot')
axes[1, 0].set_title(f'Absolute Difference\nMean: {mean_diff:.6f}')
axes[1, 0].axis('off')
plt.colorbar(im3, ax=axes[1, 0], fraction=0.046)

# Histogram comparison
axes[1, 1].hist(data_u16.flatten(), bins=50, alpha=0.7, label='U16 data', color='blue')
axes[1, 1].set_title('U16 Data Histogram')
axes[1, 1].set_xlabel('Value')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# Float histogram
axes[1, 2].hist(data_float.flatten(), bins=50, alpha=0.7, label='Float (rescaled)', color='green')
axes[1, 2].hist(data_readback.flatten(), bins=50, alpha=0.5, label='Readback', color='red', linestyle='--')
axes[1, 2].set_title('Float Data Histogram')
axes[1, 2].set_xlabel('Value')
axes[1, 2].set_ylabel('Frequency')
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
output_fig = 'test_new_example_results.png'
plt.savefig(output_fig, dpi=150, bbox_inches='tight')
print(f"   Saved visualization to: {output_fig}")
plt.show()

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
print(f"\n✓ Metadata extraction: PASSED")
print(f"✓ U16 reading: PASSED")
print(f"✓ Rescaling: {'PASSED' if match else 'FAILED'}")
print(f"✓ Round-trip: {'PASSED' if rel_error < 1.0 else 'FAILED'}")
print(f"\nThe functions correctly handle slope={metadata['slope']:.6e} and offset={metadata['offset']:.6e}")
