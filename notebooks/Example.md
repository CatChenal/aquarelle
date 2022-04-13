# Examples
---
---

### Boilerplate cell: if you're running this notebook from within the cloned repo


```python
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from IPython import get_ipython
from IPython.display import Image as Image

import sys
from pathlib import Path


def add_div(div_class='info', div_start='Tip:', 
            div_text='Some tip here', output_string=True):
    """
    Behaviour with default `output_string=True`:
    The cell is overwritten with the output, but the cell mode is still 'code',
    not 'markdown'.
    Workaround: After running the function, click on the new cell, press ESC, 
                type 'm', then run the new cell.
    If `output_string=False`, the output is displayed in an new cell with the 
    code cell visible.
    ```
    [x]
    add_div('alert-warning', 'Tip: ', 'some tip here', output_string=True)
    [x]
    <div class="alert alert-warning"><b>Tip: </b>some tip here</div>
    ```
    """
    accepted = ['info', 'warning', 'danger']
    div_class = div_class.lower()
    if div_class not in accepted:
        msg = f'<div class="alert"><b>Wrong class:&nbsp;</b> `div_start` not in: {accepted}.</div>'
        return Markdown(msg)
    
    div = f"""<div class="alert alert-{div_class}"><b>{div_start}&nbsp;&nbsp;</b>{div_text}</div>"""
    if output_string:
        return get_ipython().set_next_input(div, 'markdown')
    else:
        return Markdown(div)


def add_to_sys_path(this_path, up=False):
    """
    Prepend this_path to sys.path.
    If up=True, path refers to parent folder (1 level up).
    """
    newp = str(Path(this_path))
    if up:
        newp = str(Path(this_path).parent)

    msg = F'Path already in sys.path: {newp}'
    if newp not in sys.path:
        sys.path.insert(1, newp)
        msg = F'Path added to sys.path: {newp}'
    print(msg)

# if notebook inside another folder, eg ./notebooks:
nb_folder = 'notebooks'
add_to_sys_path(Path.cwd(), Path.cwd().name.startswith(nb_folder))

# autoreload extension
if 'autoreload' not in get_ipython().extension_manager.loaded:
    get_ipython().run_line_magic('load_ext', 'autoreload')

%autoreload 2
```

---

## Import this project module:


```python
from aquarelle import process as aqua
print(aqua.__doc__)
```

---

## Reference the path of your image folder w.r.t. the current location (`notebooks` folder):
For simplicity, this folder will also hold the processed files.


```python
image_fld = 'images' # change to your actual folder name/path

img_dir = Path.cwd().parent.joinpath(image_fld)
if not img_dir.exists():
    Path.mkdir(img_dir)
img_dir
```

---
---
# Example 1: Use the sample image


```python
sample = aqua.SAMPLE_FILE
```

## Show using `IPython.display.Image` (aliased as dImage)


```python
dImage(filename=sample)
```

## Show using PIL: this will tell you whether the image is rotated
The sample image is rotated when opened with PIL.  
The `.show()` method uses the system image viewer.


```python
s = aqua.load_sample()
s.size
s.show()
```

# Process the sample image
__Note__: You must provide a non-default output filename for saving the processed __sample file__; i.e. if `save_file=True`, `output_filename` cannot be "default".


```python
rotate = 270
outline, outfile = aqua.image_to_edges(sample, rotate_angle=rotate,
                                       save_file=True, output_filename=img_dir.joinpath("sample_lines.png"))
```

# Show result


```python
#outline.show()  # external viewer. Or:
```


```python
# Outfile is the output filename with the default naming convention:
dImage(filename=outfile)
```

---
---

# Example 2: Fetching multiple files from an Image folder:

## Filter the folder to exclude already processed files (if saved with `default` name)
... or not: you could process a processed file again to see if you like the output better!


```python
input_files = list(f for f in img_dir.glob("*.*g") if '_lines' not in f.name)
input_files
```

## [Optional] Display the input files to discover if rotation is needed.

<div class="alert alert-warning"><b>WARNING:&nbsp;&nbsp;</b>
    Using `IPython.display.Image`, the sample image is displayed properly: it does NOT need rotated. While if it's opened with `pillow.Image` the image is rotated.<br> => Use `pillow.Image` since it is used for processing! (Its rotation angle is 270.)</div>

### If you have several (all?) files that need rotated (AND you do not have too many files in the image folder), you can create a dictionary:


```python
from collections import defaultdict

rotation_params = defaultdict(int)

msg = "Rotation needed? "
msg += "Enter 0 for no rotation or an angle between 0 and 360:"
for i, f in enumerate(input_files):
    aqua.Image.open(f)
    ans = int(input(prompt=msg))
    rotation_params[i] = ans

print("\tDONE setting the rotation parameters!")
rotation_params
```

## Process all files


```python
processed_files = []

for i, f in enumerate(input_files):
    pic = aqua.Image.open(f)
    print(f,'- Size:',pic.size)
    rotate = rotation_params[i]
    _, outfile = aqua.image_to_edges(f, rotate_angle=rotate, save_file=True)
    processed_files.append(outfile)

processed_files
```

## View each output:


```python
dImage(filename=processed_files[0])
```


```python

```
