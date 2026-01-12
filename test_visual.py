"""Direct test with matplotlib - no console output needed."""

from py_xre_tiff import read_xre_tif, write_xre_tif, get_metadata
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Use non-interactive backend
matplotlib.use('Agg')

# Read example file
filepath = 'example data/recon_Al_00389.tif'

# Get metadata
metadata = get_metadata(filepath)

# Read data both ways
data_u16 = read_xre_tif(filepath, rescale=False)
data_float = read_xre_tif(filepath, rescale=True)

# Verify conversion formula
expected_float = data_u16.astype(np.float32) * metadata['slope'] + metadata['offset']
conversion_diff = np.abs(data_float - expected_float)

# Round-trip test
write_xre_tif('test_new_roundtrip.tif', data_float, rescale=True,
              slope=metadata['slope'], offset=metadata['offset'])
data_back = read_xre_tif('test_new_roundtrip.tif', rescale=True)
roundtrip_diff = np.abs(data_float - data_back)

# Create comprehensive visualization
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Title with metadata
fig.suptitle(f'XRE TIFF Test Results - New Example Files\n' +
             f'File: recon_Al_00389.tif | Slope: {metadata["slope"]:.6e} | Offset: {metadata["offset"]:.6e}',
             fontsize=14, fontweight='bold')

# Row 1: Original data
ax1 = fig.add_subplot(gs[0, 0])
im1 = ax1.imshow(data_u16, cmap='gray')
ax1.set_title(f'U16 Data\nRange: [{data_u16.min()}, {data_u16.max()}]')
ax1.axis('off')
plt.colorbar(im1, ax=ax1, fraction=0.046)

ax2 = fig.add_subplot(gs[0, 1])
im2 = ax2.imshow(data_float, cmap='gray')
ax2.set_title(f'Rescaled Float Data\nRange: [{data_float.min():.2f}, {data_float.max():.2f}]')
ax2.axis('off')
plt.colorbar(im2, ax=ax2, fraction=0.046)

ax3 = fig.add_subplot(gs[0, 2])
im3 = ax3.imshow(conversion_diff, cmap='hot')
ax3.set_title(f'Conversion Formula Verification\nMax diff: {conversion_diff.max():.9f}')
ax3.axis('off')
plt.colorbar(im3, ax=ax3, fraction=0.046)

# Row 2: Round-trip test
ax4 = fig.add_subplot(gs[1, 0])
im4 = ax4.imshow(data_back, cmap='gray')
ax4.set_title(f'After Round-trip\nRange: [{data_back.min():.2f}, {data_back.max():.2f}]')
ax4.axis('off')
plt.colorbar(im4, ax=ax4, fraction=0.046)

ax5 = fig.add_subplot(gs[1, 1])
im5 = ax5.imshow(roundtrip_diff, cmap='hot')
max_rt_diff = roundtrip_diff.max()
ax5.set_title(f'Round-trip Difference\nMax: {max_rt_diff:.6f}, Mean: {roundtrip_diff.mean():.6f}')
ax5.axis('off')
plt.colorbar(im5, ax=ax5, fraction=0.046)

# Metadata verification
metadata_back = get_metadata('test_new_roundtrip.tif')
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
ax6.text(0.1, 0.9, 'Metadata Verification:', fontsize=12, fontweight='bold', transform=ax6.transAxes)
ax6.text(0.1, 0.75, f'Original slope: {metadata["slope"]:.6e}', fontsize=10, transform=ax6.transAxes)
ax6.text(0.1, 0.65, f'Written slope:  {metadata_back["slope"]:.6e}', fontsize=10, transform=ax6.transAxes)
ax6.text(0.1, 0.50, f'Original offset: {metadata["offset"]:.6e}', fontsize=10, transform=ax6.transAxes)
ax6.text(0.1, 0.40, f'Written offset:  {metadata_back["offset"]:.6e}', fontsize=10, transform=ax6.transAxes)

slope_match = abs(metadata['slope'] - metadata_back['slope']) < 1e-9
offset_match = abs(metadata['offset'] - metadata_back['offset']) < 1e-9
ax6.text(0.1, 0.25, f'Slope match: {"✓ PASS" if slope_match else "✗ FAIL"}', 
         fontsize=11, fontweight='bold', color='green' if slope_match else 'red', transform=ax6.transAxes)
ax6.text(0.1, 0.15, f'Offset match: {"✓ PASS" if offset_match else "✗ FAIL"}', 
         fontsize=11, fontweight='bold', color='green' if offset_match else 'red', transform=ax6.transAxes)

# Row 3: Histograms and summary
ax7 = fig.add_subplot(gs[2, 0])
ax7.hist(data_u16.flatten(), bins=100, alpha=0.7, color='blue', edgecolor='black')
ax7.set_title('U16 Data Histogram')
ax7.set_xlabel('Value')
ax7.set_ylabel('Frequency')
ax7.grid(True, alpha=0.3)

ax8 = fig.add_subplot(gs[2, 1])
ax8.hist(data_float.flatten(), bins=100, alpha=0.7, color='green', edgecolor='black', label='Original')
ax8.hist(data_back.flatten(), bins=100, alpha=0.5, color='red', edgecolor='black', linestyle='--', label='Round-trip')
ax8.set_title('Float Data Histogram (Overlay)')
ax8.set_xlabel('Value')
ax8.set_ylabel('Frequency')
ax8.legend()
ax8.grid(True, alpha=0.3)

# Summary text
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
ax9.text(0.1, 0.9, 'TEST SUMMARY', fontsize=12, fontweight='bold', transform=ax9.transAxes)

conversion_ok = conversion_diff.max() < 1e-6
roundtrip_ok = max_rt_diff < 0.1
metadata_ok = slope_match and offset_match

ax9.text(0.1, 0.75, f'✓ Metadata extraction', fontsize=10, color='green', transform=ax9.transAxes)
ax9.text(0.1, 0.65, f'✓ U16 reading', fontsize=10, color='green', transform=ax9.transAxes)
ax9.text(0.1, 0.55, f'{"✓" if conversion_ok else "✗"} Conversion formula', 
         fontsize=10, color='green' if conversion_ok else 'red', transform=ax9.transAxes)
ax9.text(0.1, 0.45, f'{"✓" if roundtrip_ok else "✗"} Round-trip test', 
         fontsize=10, color='green' if roundtrip_ok else 'red', transform=ax9.transAxes)
ax9.text(0.1, 0.35, f'{"✓" if metadata_ok else "✗"} Metadata preservation', 
         fontsize=10, color='green' if metadata_ok else 'red', transform=ax9.transAxes)

all_pass = conversion_ok and roundtrip_ok and metadata_ok
ax9.text(0.1, 0.15, f'{"ALL TESTS PASSED!" if all_pass else "SOME TESTS FAILED"}', 
         fontsize=12, fontweight='bold', color='green' if all_pass else 'red', transform=ax9.transAxes)

# Save figure
output_file = 'test_new_example_visual.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"Saved to: {output_file}")
