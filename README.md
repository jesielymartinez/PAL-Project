# PAL-Project

### MOTIVATION
During the technology era, we have seen a new way to see the media. From drawings digitized, movies, series, clips, live streaming, GIF, etc. We as a group thought that a good way to continue those trends came in one idea: Programing Animation Language (PAL). This programming language is intended to create animations and then export them as a video clip or GIF. Our goal is to create a variety of tools geared for various scenarios, characters, and storylines that the user can create and choose for their pleasure. It is a new way to express your creativity with something simple and fun. One of the main purposes of our project is to improve the world of short animations, making it easier and accessible to create, so that even children can use their imagination to bring their ideas to life with animations. This is done by simplifying the process, not requiring advanced skills in programming and graphic design.



### VIDEO TUTORIAL

- Tap the image to view a simple tutorial to start using PAL

[![WATCH THE VIDEO!](https://github.com/JonathanXSG/PAL-Project/blob/master/PAL_VideoImage.png)](https://youtu.be/_BxfNZoQCqs)



### LANGUAGE FEATURES
- Easy sintax.
- Manipulation of images and sprites by rotation, movement and changing the size of these.
- Manipulation of the background by means of movement and automatic repetition of it.
- Ability to choose the time between the frames.
- The state of the previous frame is copied to the next.



### APPROACH
PAL uses the modules lexer.py and PAL_parser.py. PAL_parser is the main module that runs the application. It contains the main methods of the application. User input is parsed by yacc using the PLY library. These functions define grammar characteristics of the language. The yacc parser must match the functions found in PAL_parser module with the command entered by the user, considering the tokens defined in the lexer file for PAL. The tokens form the regular expression that will be matched and the execute the command. 
PAL uses the following libraries:
Imageio: Imageio is a Python library that provides an easy interface to read and write a wide range of image data, including animated images, video, volumetric data, and scientific formats. It is cross-platform, runs on Python 2.7 and 3.4+, and is easy to install. We will be using this library for exporting the finished animation.
PLY: also referred as Python Lex- Yacc, is a parsing tool written in Python and implements the Lex parsing tool. This tool s divided in both stages, the lexical analyzer( lex) is the one responsible that all the syntax what the user writes follows the rules specified by the Developers. The second one is yac, practically yac is the one that parses de code.
Tkinter: Tkinter is Python's de-facto standard GUI (Graphical User Interface) package, used in pal module to provide the graphics needed. 
PIL: The Python Imaging Library by Fredrik Lundh and Contributors.
_Thread: The thread module provides a basic synchronization data structure called a lock object The synchronization primitives go hand in hand with thread management.



### Language Functions and Commands

- init(width, height) - It initialize the animation with the given width and height passed as parameters.
- show - It displays a preview of the current frame with all its content.
- setBackground(image.jpg) - Sets the background of the frame to the image passed as a parameter.
- createSprite(spriteName, fileName, width, height) - Creates a sprite with the given name and dimensions.
- spriteName moveSprite(R, moveX, moveY) - Moves the sprite relative to it’s position.
- createAsset(assetName, assetImage.png) - Creates an image to add to the frame with the given name.
- assetName resizeAsset absolute(width, height) - Resizes the given asset with the specified dimensions.
- assetName moveAsset(A, moveX, moveY) - Moves the given asset to the specified location in the frame.
- createFrame - Creates a frame that looks exactly the same as the one already created, just to facilitate the flow and development of    the animation.
- moveBackground(moveX) - Moves the background according to the number passed as a parameter.
- changeFrame(index) - Change the frame to the one specified by the index given as a parameter.
- createAnimation(displayTime) - Creates an animation with each of the frames in the order they are created. Each frame will be showed by the time passed as a parameter which are in seconds.



### TEAM
- Jonathan Santiago González
- Adahid Galan Rivera
- Jesiely Martínez Rodríguez
- Gilson Rivera González


