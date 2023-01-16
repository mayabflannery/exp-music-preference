# Music preference experiment
This is an experiment designed using Python and [Kivy](https://kivy.org) (for GUI) and is intended for in-person use.
The experiment progresses through:
 1. a demographic questionnaire
 2. a personality assessment ([BFI-44](https://www.ocf.berkeley.edu/~johnlab/bfi.htm))
 3. a listening task (rating music preference)

## Note
Program designed following tutorials and referencing
 * https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6

# Dependencies
## Install Kivy in virtual environment
* python -m pip install --upgrade pip wheel setuptools virtualenv
* python -m virtualenv kivy_venv
* kivy_venv\Scripts\activate
* python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
* python -m pip install kivy_deps.gstreamer==0.1.*
* pip install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/

# Optional Examples
* python -m pip install kivy_examples==1.11.1

# Reference
* https://kivy.org/doc/stable/guide/lang.html
*
