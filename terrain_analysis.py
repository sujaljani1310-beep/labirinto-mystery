import rasterio
import numpy as np
import matplotlib.pyplot as plt


# Change this to the name of your downloaded GeoTIFF file
FILE_PATH = "labirinto_dem.tif"


# Open the elevation raster
with rasterio.open(FILE_PATH) as src:
    elevation = src.read(1).astype(float)

    # Replace NoData values with NaN
    if src.nodata is not None:
        elevation[elevation == src.nodata] = np.nan

    transform = src.transform


# -----------------------------
# 1. Elevation Map
# -----------------------------

plt.figure(figsize=(10, 7))
plt.imshow(elevation)
plt.title("Elevation Map - Labirinto Study Area")
plt.colorbar(label="Elevation")
plt.xlabel("X Pixel")
plt.ylabel("Y Pixel")
plt.tight_layout()
plt.show()


# -----------------------------
# 2. Calculate Slope
# -----------------------------

# Approximate pixel size in map units
x_res = abs(transform.a)
y_res = abs(transform.e)

# Calculate elevation gradients
gradient_y, gradient_x = np.gradient(
    elevation,
    y_res,
    x_res
)

# Calculate slope in degrees
slope = np.degrees(
    np.arctan(
        np.sqrt(
            gradient_x ** 2 +
            gradient_y ** 2
        )
    )
)


plt.figure(figsize=(10, 7))
plt.imshow(slope)
plt.title("Slope Map - Labirinto Study Area")
plt.colorbar(label="Slope (degrees)")
plt.xlabel("X Pixel")
plt.ylabel("Y Pixel")
plt.tight_layout()
plt.show()


# -----------------------------
# 3. Roughness
# -----------------------------

roughness = np.zeros_like(elevation)

rows, cols = elevation.shape

for row in range(1, rows - 1):
    for col in range(1, cols - 1):

        neighborhood = elevation[
            row - 1:row + 2,
            col - 1:col + 2
        ]

        roughness[row, col] = (
            np.nanmax(neighborhood)
            - np.nanmin(neighborhood)
        )


plt.figure(figsize=(10, 7))
plt.imshow(roughness)
plt.title("Terrain Roughness - Labirinto Study Area")
plt.colorbar(label="Elevation Difference")
plt.xlabel("X Pixel")
plt.ylabel("Y Pixel")
plt.tight_layout()
plt.show()
