from cartopy import crs as ccrs
from matplotlib import pyplot as plt
import shapely

import iris
from iris import quickplot as qplt
from iris.util import mask_cube_from_shape

wgs84 = ccrs.PlateCarree()
line = shapely.LineString([(-45, 40), (-28, 53), (-2, 55), (19, 45)])

cube = iris.load_cube(iris.sample_data_path("toa_brightness_stereographic.nc"))
masked_cube = mask_cube_from_shape(cube, line, wgs84)

fig, axes = plt.subplots(
    1, 2, figsize=(12, 5),
    subplot_kw={'projection': cube.coord_system().as_cartopy_crs()}
)

plt.sca(axes[0])
qplt.pcolormesh(cube)
axes[0].coastlines()
axes[0].add_geometries(
    [line], crs=wgs84, edgecolor='red', facecolor='none', linewidth=2
)
axes[0].set_title("Original Cube")

plt.sca(axes[1])
qplt.pcolormesh(masked_cube)
axes[1].coastlines()
axes[1].set_title("Masked Cube")

plt.tight_layout()
plt.savefig("iris_314.png")
