# JAP_OCR_Client
## Preparations
>+ ETL8G Dataset  <a href="http://etlcdb.db.aist.go.jp">Download</a>
>+ TKDND2  <a href="https://sourceforge.net/projects/tkdnd/files/">Download</a>
>+ vgg16.npy

### Train Your Model
First use `pip install -r requirements.txt` to install requirements, then extract the dataset in your project folder, use  `python image_enhance.py`  to extract the images into their label named folders.

Use `python create_tfrecords.py` to create a `.tfrecords` form dataset that `train.py` needed and it will also create a `label.txt` file.

Use `python train.py` to train your model.

### Install TKDnD2

Copy the `TKinterDnD2` folder to your python lib directory.  
Copy the `tkdnd2.8` binary folder to your python tcl directory.  

## How To Use
If using Windows, just double click the `run.bat` to start the GUI.
If using Linux `python3 GUI.py` to start.  
Finally draged a picture contens Japanese characters into the left box, the result will be shown in the right one.

>**Current program can only split and recgonize a simple picture without other interference, and if the character contens two parts ( left and right ), it will split into two parts.