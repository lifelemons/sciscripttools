# Plot

The plotting module heavily relies on the `figure_parameters` class.
`plot_defaults.py` holds a default `figure_parameters` python dictionary, which 
is used when no other one is provided.
It would best to create your own dictionary that would best match your document requirements.

## Create Your Own
### Latex Font Sizes
Check which font size you want to use, [here](https://tex.stackexchange.com/questions/24599/what-point-pt-font-size-are-large-etc).
The default is this package is 12pt. For latex documents such as `\documentclass[12pt]{article}`

### Figure Dimensions
The defaults in this package were calculated form using these margins in a latex document.
```
\documentclass[12pt,a4paper]{report}
\usepackage[left=4.25cm, right=3.10cm, top=3.5cm, bottom=3.5cm, textwidth=5.25in]{geometry}
```
It was measured using `\the\textwidth`, read [this](https://tex.stackexchange.com/questions/39383/determine-text-width) for more information.
`\textwidth` gave a measurement of `5.37506 inches` or `13.64806 cm`.
Thus, a figure width of `5.315 inches`, `13.5001 cm` was used as the default,
This leaves `0.14796 cm` or `0.74 mm` on each side, and thus the figure should never be squashed to be fitted in.

Measure your own document and pick a good size for your figures.
The ratio of 3:2, is the `matplotlib` default ratio.

### Rest of the Variables
The rest of the variables were chosen by trail and error to see which values 
looks nice for the given figure size.

### Load and Save
The `figure_parameters` class can be saved and loaded back in for easy reusability 
of your own choice of parameters.
To save, use
```python
fig_params = st.plot.figure_parameters()
# your own changes
fig_params.save_data("my_params")
```
To load it back in, use
```python
fig_params = st.plot.figure_parameters("my_params")
```