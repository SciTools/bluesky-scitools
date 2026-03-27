import iris
from iris.analysis import MEAN
from iris.cube import CubeList
from iris import quickplot as qplt
from iris.util import new_axis
from matplotlib import pyplot as plt
import nc_time_axis

file_path = "/data/users/martin.yeo/Wholesale_data/202603270900_u1096_ng_umqv_Wholesale2.grib"

# Masks in coord bounds confuse merge(). Need to manually control cube combination.
#  https://scitools-iris.readthedocs.io/en/latest/user_manual/tutorial/controlling_merge.html#how-to-merge-cubes-when-coordinates-differ
cubes = iris.load_raw(file_path, "altitude")
processed_cubes = CubeList([new_axis(c, scalar_coord="time", expand_extras=["forecast_period"]) for c in cubes])
cube = processed_cubes.concatenate_cube()

mean_cube = cube.collapsed(["projection_x_coordinate", "projection_y_coordinate"], MEAN)
mean_cube.rename("mean height-above-surface of the 0C isotherm")

fig, ax = plt.subplots(figsize=(15, 5))
qplt.plot(mean_cube)
formatter = nc_time_axis.CFTimeFormatter("%d/%m %Hhr", mean_cube.coord("time").units.calendar)
ax.xaxis.set_major_formatter(formatter)
plt.savefig("isotherm_altitude.png")
