# Mario Kart Escape Time Fractals

A Python project for generating animated visualizations and 3D models of Julia and Mandelbrot sets using escape time algorithms. The project creates pixel matrices representing escape times.  It can then convert them into frame sequences, and assembles them into GIF animations.  It can also convert them directly into 3D printable STLs, where heights represent escape times.

#### Authors

- Eliza Brown
- Gabriel Dorfsman-Hopkins

## Quick Start: 3D Models
To quickly make a 3D model for the Julia set of a complex number you choose, run `wrapperSTL.py` to have all the necessary core scripts run in sequence.
```
python wrapperSTL.py <c> <name>
```
**Arguments:**
- `c`: Complex parameter defining the Julia set.  $a+bi$ is stored as an array `[a,b]`
- `name`: Your GIF will be stored as `name.gif` in the `Gifs` directory

**Example**
Run the following:
```
python wrapperSTL.py [-.75,0] example
```
It will create create a 3D model in STL format for the basilica Julia set for $c=-0.75+0i$ and save it as `/3DModels/example.stl`.

**Optional Arguments**
The wrapper also has some optional arguments:
```
python wrapperSTL.py <c> <name> <mountain --or-- hole> <Resolution> <max_iter>
```
- `mountain --or-- hole`. Choose `mountain` to build a vertical mountain, where height is escape time.  Choose `hole` to dig a hole, where depth is escape time.  Defaults to `mountain`.
- `resolution` is the number of pixels.  It defaults to 1000 (as a 1000x1000 pixel square).
- <max_iter> The escape time bound.  Might want to increase for nice zooms.  Defaults to 100.

**Example**
Run the following:
```
python wrapperSTL.py [-.75,0] holeExample hole
```
As above, it will create create a 3D model in STL format for the basilica Julia set for $c=-0.75+0i$ and save it as `/3DModels/holeExample.stl`, but this time as a hole.

### Mandelbrot Wrapper
There is also a quickstart wrapper to create Mandelbrot set 3D models.  If you run
```
python wrapperSTLMandel.py MandelExample
```
it will create a 3D model for the entire Mandelbrot set and save it as `3DModels/MandelExample.stl`.  There are a lot more optional arguments in this wrapper to make zooming more accessable.  All of these arguments are available in the Julia framework as well, though not accessable from the wrapper.
```
python wrapperMandel.py <name> <mountain --or hole> <center> <xRange> <resolution> <aspect ratio> <bound>
```
**Optional Arguments**
- `center`: Center point of image (Defaults to -.65)
- `mountain --or-- hole`. Choose `mountain` to build a vertical mountain, where height is escape time.  Choose `hole` to dig a hole, where depth is escape time.  Defaults to `mountain`.
- `xRange`: Visible real range of the complex plane (defaults to 3)
- `resolution`: The number of pixels in the x-direction.  Defaults to 1000.
- `Aspect ratio`: Defaults to 4/3
- `bound`: The escape time bound.  Might want to increase for nice zooms.  Defaults to 100.

## Quick Start: Animations
To quickly make a GIF for the Julia set of a complex number you choose, run `wrapper.py` to have all the necessary core scripts run in sequence.
```
python wrapper.py <c> <name>
```
**Arguments:**
- `c`: Complex parameter defining the Julia set.  $a+bi$ is stored as an array `[a,b]`
- `name`: Your GIF will be stored as `name.gif` in the `Gifs` directory

**Example**
Run the following:
```
python wrapper.py [-.75,0] example
```
It will create create a GIF for the basilica Julia set for $c=-0.75+0i$ and save it as `/Gifs/example.gif`.

**Optional Arguments**
The wrapper also has some optional arguments:
```
python wrapper.py <c> <name> <num_frames> <color> <resolution>
```
- `num_frames` is the number of frames.  Defaults to 100.
- `color` is a boolean.  Full color is the default.
- `resolution` is the number of pixels.  It defaults to 1000 (as a 1000x1000 pixel square).

### Mandelbrot Wrapper
There is also a quickstart wrapper to create Mandelbrot set animations.  If you run
```
python wrapperMandel.py MandelExample
```
it will create a GIF for the entire Mandelbrot set and save it as `Gifs/MandelExample.gif`.  There are a lot more optional arguments in this wrapper to make zooming more accessable.  All of these arguments are available in the Julia framework as well, though not accessable from the wrapper.
```
python wrapperMandel.py <name> <center> <xRange> <NUM_FRAMES> <color> <resolution> <aspect ratio> <bound>
```
**Optional Arguments**
- `center`: Center point of image (Defaults to -.65)
- `xRange`: Visible real range of the complex plane (defaults to 3)
- `NUM_FRAMES`: NUmber of frames in animation (defaults to 100)
- `color` is a boolean.  Full color is the default.
- `resolution`: The number of pixels in the x-direction.  Defaults to 1000.
- `Aspect ratio`: Defaults to 4/3
- `bound`: The escape time bound.  Might want to increase for nice zooms.  Defaults to 100.

## Core Scripts

### Pixel Matrix Creation

#### `EscapeTimeMatrix.py`
Builds a pixel matrix for a Julia set where each entry represents the escape time of a point in the complex plane. Uses a "Mario Kart Finishing Time"-style approximation to convert discrete escape times to continuous values.

**Usage:** 
```
python EscapeTimeMatrix.py <c> <ouptut_dir> <resolution> <escape_time_bound> <xRange> <center> <aspect_ratio>
```

**Arguments:**
- `c`: Complex parameter defining the Julia set.  $a+bi$ is stored as an array [a,b]
- `output_dir`: Directory to save the matrix as JSON
- Optional `resolution`: How many pixels in the x-direction.  Defaults to 1000.
- Optional `escape_time_bound`: An upper bound for how long a pixel has to escape.  Defaults to 500.
- Optional `xRange`: The width of the complex plane viewed (necessary if you'd like to zoom).  Defaults to 4.
- Optional `center`: The complex number at the center of the image (stored as `[a,b]`, necessary if you'd like to zoom).  Defaults to the origin.
- Optional `aspect_ratio`: The aspect ratio of the images produced.  Defaults to 1 (square)


#### `EscapeTimeMatrixMandel.py`
Similar to `EscapeTimeMatrix`, but builds a pixel matrix for the Mandelbrot set.
**Usage:**
```
python EscapeTimeMatrixMandel.py <output_dir> <center> <xRange> <resolution> <aspectRatio> <bound>
```
**Arguments:**
- `output_dir`: Directory to save the matrix as JSON
- Optional `center`: The complex number at the center of the image (stored as `[a,b]`, necessary if you'd like to zoom).  Defaults to the origin.
- Optional `xRange`: The width of the complex plane viewed (necessary if you'd like to zoom).  Defaults to 4.
- Optional `resolution`: How many pixels in the x-direction.  Defaults to 1000.
- Optional `aspect_ratio`: The aspect ratio of the images produced.  Defaults to 4/3.
- Optional `escape_time_bound`: An upper bound for how long a pixel has to escape.  Defaults to 500.

### Creating a 3D model from a Pixel Matrix

#### `MatrixToSTL.py`
Converts an escape time matrix into 3D model as an STL, which is water tight and 3D printable.  It will either be a *mountain* where height corresponds to escape time, or a *hole* where depth corresponds to escape time.  This currently just exports an STL, but you can uncomment `    solid_mesh.show()` to show the 3D model in the built in trimesh viewer rather than exporting the entire model.


**Usage:**
```
python MatrixToSTL.py <input_dir> <output_dir> <mountain --or -- hole> <LpNorm>
```

**Arguments:**
- `input_dir`: Directory containing the escape time matrix JSON
- `output_dir`: Directory to save PNG frames
- Option `mountain --or-- hole`: Choose `mountain` to build a vertical mountain, where height is escape time.  Choose `hole` to dig a hole, where depth is escape time.  Defaults to `mountain`.
- Optional `LpNorm`:  Chooses the norm for the the redistribution/renormalization of escape times.  See redistribution below.  Defaults to 2.


### Creating Frames from a Pixel Matrix

#### `MatrixToFramesBW.py`
Converts an escape time matrix into a sequence of black-and-white frames, showing which pixels have "escaped" at each time step.

**Usage:**
```
python MatrixToFramesBW.py <input_dir> <output_dir> <num_frames> <LpNorm (optional)>
```

**Arguments:**
- `input_dir`: Directory containing the escape time matrix JSON
- `output_dir`: Directory to save PNG frames
- `num_frames`: Number of frames to generate
- Optional `LpNorm`:  Chooses the norm for the the redistribution/renormalization of escape times.  See redistribution below.  Defaults to 2.


#### `MatrixToFramesColor.py`
Similar to `MatrixToFramesBW.py` but generates color frames. Includes an optional parameter for color cycling.

**Usage:**
```
python MatrixToFramesColor.py <input_dir> <output_dir> <num_frames> <LpNorm (optional)> <color_cycles (optional)>
```

**Arguments:**
- `input_dir`: Directory containing the escape time matrix JSON
- `output_dir`: Directory to save PNG frames
- `num_frames`: Number of frames to generate
- Optional `LpNorm`:  Chooses the norm for the the redistribution/renormalization of escape times.  See redistribution below.  Defaults to 2.
- Optional `color_cycles`: (how many times to cycle through the color spectrum)

### Image Creation

#### `SingleFrame.py`
Creates a single colored image from an escape time matrix.  Can be useful for testing with large images.

**Usage:**
```
python SingleFrame.py <input_dir> <output_file> <LpNorm (optional)>
```

**Arguments:**
- `input_dir`: Directory containing the escape time matrix JSON
- `output_file`: Path for the output PNG image
- Optional `LpNorm`:  Chooses the norm for the the redistribution/renormalization of escape times.  See redistribution below.  Defaults to 2.

#### `png_to_gif.py`
Converts a stack of PNG images into a single animated GIF.

**Usage:**
```
python png_to_gif.py <input_dir> <output_gif> <frame_duration>
```

**Arguments:**
- `input_dir`: Directory containing PNG files
- `output_gif`: Name of the output GIF file
- Optional: `frame_duration`: Frame duration in milliseconds.  Defaults to 50.

### Math Helper Functions: `helpers.py`
Here's where helper functions go.  This includes all the complex number algebra and escape time computations in the pixel matrix creation steps.  It also houses the redistribution function:

#### Redistribution

In `MatrixToFrames` (BW and Color) as well as `SingleFrame` there is a redistribution function.  Essentially, the structure of these functions is to first normalize the escape times so they all lie between 0 and 1.  The problem is, many things escape early and as the escape time gets longer and longer the change from frame to frame becomes less visible without zooming.  To make nice animations (or more importantly, nice 3D prints), we want to 'slow down' the beginning time and 'speed up' the end.

**Usage**
```
import helpers
helpers.redsitribute(x,n)
```
The value n is the LpNorm given as an optional argument to `MatrixToFrames` and `SingleFrame`.  These functions default to calling n=2.

This function takes an input $x\in[0,1]$ and maps it to $(1-(1-x)^n)^{1/n}$ where n=LpNorm.  This is used to renormalize the interval `[0,1]`, which we think of as escape times along the circle centered at (1,0) in the specified LpNorm.  `n>1` slows down the beginning of the the animation and speeds up the end.  `0<n<1` speeds up the beginning of the animation and slows down the end.

All called scripts use this function automatically, but if you're trying to create a nice 3D print, you may want to create the JSON file and then experiment with `MatrixToSTL` calling different values of n = LpNorm to get the effect you want.  You will likely want larger values to avoid spikeyness.

**Note:** changing n is inaccessable from the wrapper, you will need to create a json file first and then feed the LpNorm to one of `MatrixToFrames` or `SingleFrame`.

**TODO:**  The circle approach only slows down the beginning or the end.  I'd be interested in writing a redistribution function which allows us to slow down over a particular interval of interest to us.  Maybe control points for a cubic or a sigmoid type thing.

**TODO:**  I introduced a `redistributeSigmoid(x,c,b)` function which can be called by `matrixToFrames`.  This puts a sigmoid on `[0,1]`, whose center (i.e., largest slope) is at `c`.  `b` controls the bound of the sigmoid that gets squeezed into `[0,1]`.  Precisely, we take the usual sigmoid and squeeze `[-b,b]` to `[0,1]`, moving the center to `c`.  A higher `b` will be a more local and steeper slope at `c`.  Right now this function is inaccessable from the command line, you must goe into `matrixToFrames` and comment out the redistribute function you don't want to use.  I will update this soon.

A good way to use `redistributeSigmoid` is to first create 100 frames with `redistribute` with `LpNorm=1` (or just adjust the code to skip redistribution altogether).  Then dig through your frames to find the place you'd like to stretch out vertically, divide this frame number by 100 and that will be a good `c` value for `redistributeSigmoid`.

## Output Directories

- `PixelMatrices/`: JSON files containing escape time matrices.  The wrapper stores outputs of `EscapeTimeMatrix.py` here.  If this doesn't exist, the wrappers will make this directory.
- `Gifs/`: Final GIF animations.  The wrapper stores final outputs here.  If this doesn't exist, the wrappers will make this directory.
- Directories for stacks of PNGs will be created by the wrapper when it runs `MatrixToFramesBW.py` and `MatrixToFrames.py`

## Requirements

- Python 3.8+ (3.10 recommended)
- See [requirements.txt](requirements.txt) for project dependencies (`numpy`, `pillow`, `trimesh`, `scipy`, `pyglet`, `PyOpenGL`).
- The STL generation itself does not require `pyglet` or `PyOpenGL`.  These packages are only needed for the optional `trimesh` viewer (`mesh.show()`).

Installation (pip / venv)

Create and activate a virtual environment, then install dependencies:
```powershell
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Conda alternative

If you prefer conda:
```powershell
conda create -n mke python=3.10
conda activate mke
pip install -r requirements.txt
```

Notes

- The `trimesh` viewer depends on `pyglet` and `PyOpenGL`; if the optional viewer fails to start on Windows, ensure your graphics drivers are up to date.
- If you need accelerated numerical routines, consider installing optimized builds of `numpy`/`scipy` (via conda or wheels).

## Usage Examples

1. Generate an escape time matrix:
```
python EscapeTimeMatrix.py [-0.7,0.27015] PixelMatrices/matrix.json 500
```

2. Generate a single test frame:
```
python SingleFrame.py PixelMatrices/matrix.json Images/test_frame.png
```
3. Generate a 3D model (as a mountain)
```
python MatrixToSTL.py PixelMatrices/matrix.json 3DModels/test_model.stl
```
4. Generate a 3D model (as a hole)
```
python MatrixToSTL.py PixelMatrices/matrix.json 3DModels/test_model_hole.stl hole
```

4. Create black and white frames:
```
python MatrixToFramesBW.py PixelMatrices/matrix.json ExampleBW 100
```

5. Create color frames:
```
python MatrixToFramesColor.py PixelMatrices/matrix.json ExampleColor 100 2
```

6. Convert frames to GIF:
```
python png_to_gif.py ExampleColor Gifs/ExampleColor.gif 50
```


## Performance Notes

- High-resolution matrices (e.g., 5000x5000) and large frame counts can be computationally intensive
- Consider downscaling images or reducing frame numbers for faster processing
- GIF creation is memory-intensive; optimize frame count and resolution accordingly