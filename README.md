# This is a project for my paper

----------------------------

TODO list


----------------------------

## Steps

`processSvs.py` => `main.py`

### processSvs.py

Accepts meta data (Download meta) of TCGA Svs files.
The svs files and the meta data should place in the same directory.
This script will crop all svs to patches and filter patches by color,
based on Lab color space.
The patches are stored in a specific directory in the form \<TCGAID\>\_pos.jpg.

### main.py

Process all patches by Cellprofiler, count cell number of all patches.
Select top 20 (default, can be set) patches with the highest cell density.
Resultes are stored in a specific directory.

## Records

run pipeline command:

`python run_pipeline.py data/20x/hand-select-nosplit/ data/pipeline tangbo.cpproj -b 100`

The cellprofiler project `tangbo.cpproj` has more features. Using a measurement
generate by our script. Which could be easily change to the default method from
cellprofiler.
