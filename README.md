Resize and crop all images stored in the folder.

By designating a specific folder, resize and crop all images in the sub folders of the specified folder according to settings that you specify. Also save them in the other or the originally designated folder as you specified.

# Install
    pip install batch_resize

# Basic usage
1. The images to be converted are organized by folder as shown below.
    ~~~ 
    +- folder-a 
      +- subfolder-a
      |  +- image-1.jpg
      |  +- image-2.jpg
      +- subfolder-b
          +- image-3.jpg
          +- image-4.jpg
    ~~~

2. Create a config.json file under the destination folder as follows:
    ~~~
    {
        "dest": "../resized",
        "sizes": [
            {"size": [1000, 1500]},
            {"size": [960, 1280]}
        ]
    }
    ~~~

3. Execute the following command in the console environment.
    ~~~
    python -m batch_resize folder-a
    ~~~

4. As a result, you can see that the "resized" folder is created in the same path as the "folder-a" folder as shown below.
    ~~~
    +- folder-a
    +- resized 
      +- subfolder-a
      |  +- 1000x1500
      |  |  +- image-1.jpg
      |  |  +- image-2.jpg
      |  +- 960x1280
      |     +- image-1.jpg
      |     +- image-2.jpg
      +- subfolder-b
         +- 1000x1500
         |  +- image-3.jpg
         |  +- image-4.jpg
         +- 960x1280
            +- image-3.jpg
            +- image-4.jpg
    ~~~