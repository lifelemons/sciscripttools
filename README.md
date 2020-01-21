# SciScriptTools

Small set of tools and functions for scientific code and scripts.

## IO Example
An example to get started with the IO tools.
```python
import sciscripttools as st

power = [4,5,6]
st.save_data("power_exp_01", power) # save a value, arrary, or dictionary
```
Load the previous saved data with
```python
import sciscripttools as st

_, power = st.load_data("power_exp_01")
```

## Plot Example
An example to get started with the plotting tools

```python
import numpy as np
import matplotlib.pyplot as plt
import sciscripttools as st

# data
x = np.linspace(0, 2)
y = x + np.random.rand(len(x))
y2 = x + np.random.rand(len(x))

# figure

fig_params = st.figure_parameters() # generate parameters
st.standard_font(font_size = fig_params.font_size) # standarise the font

# normal matplotlib plotting
fig, axes = plt.subplots(1, 2, sharey = True) # create matplotlib figure
ax1, ax2 = axes

# plot data
ax1.plot(x, y)
ax2.plot(x, y2)
for ax in axes:
    ax.set_ylim(0, 3) 

fig.subplots_adjust(wspace = fig_params.adjust_subplot_wspace) # set subplot width spacing
sf = st.standard_figure(fig, axes, fig_params) # create standard_figure
sf.add_subplot_labels()

# add units
ylabel = "Power"; yunit = "\\watt"
sf.ylabel(ax1, ylabel, yunit)
xlabel = "Time"; xunit = "\\second"
sf.xlabel(axes, xlabel, xunit)

fig.savefig("quick_plot.png")
```
![example quick plot](examples/quick_plot.png)