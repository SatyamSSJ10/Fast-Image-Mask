# Fast-Image-Mask
Used to Quickly Make Rectangle White Mask in Images. My purpose in making this was to Delete Watermark or Text from Images to Train AI.

## Requirements
Tkinter, Pillow
```pip install tk pillow```

## Working 

1. Put the INPUT_PATH and PROCESSED PATH.
2. Run the Code
3. Image Dialog box will appear, do not resize it. The default height is 1080px, if your screen is smaller you can make changes in ```line 13```.
4. Draw Rectangle and Press ```TAB``` on keyboard. The Image will be saved in Processed Image folder. The Area of the rectangle will be masked.
5. There are no popups telling if it has happened or not because it is meant to be fast I didn't want to be bothered by a popup telling me that my image has been succesfully saved.
