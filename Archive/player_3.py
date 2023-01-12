# import pyglet # pip3 install pyglet and pip3 install GLU and sudo apt-get install freeglut3-dev
# 
# vidPath = '/home/andrewdmarques/Desktop/TV/Mister.Rogers.Neighborhood.S14E07.Work.1527.A.Visit.to.a.Dairy.Farm.480p.AMZN.WEB-DL.DD+2.0.x264-RTN.mp4'
# window= pyglet.window.Window()
# player = pyglet.media.Player()
# source = pyglet.media.StreamingSource()
# MediaLoad = pyglet.media.load(vidPath)
#  
# player.queue(MediaLoad)
# player.play()
# 
# @window.event
# def on_draw():
#     if player.source and player.source.video_format:
#         player.get_texture().blit(50,50)
#         
# pyglet.app.run()





# importing pyglet module
import pyglet
 
# width of window
width = 500
   
# height of window
height = 500
   
# caption i.e title of the window
title = "Geeksforgeeks"
   
# creating a window
window = pyglet.window.Window(width, height, title)
 
 
# video path
vidPath ="sample-mp4-file.mp4"
 
# creating a media player object
player = pyglet.media.Player()
 
# creating a source object
source = pyglet.media.StreamingSource()
 
# load the media from the source
MediaLoad = pyglet.media.load(vidPath)
 
# add this media in the queue
player.queue(MediaLoad)
 
# play the video
player.play()
 
# on draw event
@window.event
def on_draw():
     
    # clea the window
    window.clear()
     
    # if player source exist
    # and video format exist
    if player.source and player.source.video_format:
         
        # get the texture of video and
        # make surface to display on the screen
        player.get_texture().blit(0, 0)
         
         
# key press event    
@window.event
def on_key_press(symbol, modifier):
   
    # key "p" get press
    if symbol == pyglet.window.key.P:
         
        # printing the message
        print("Key : P is pressed")
         
        # pause the video
        player.pause()
         
        # printing message
        print("Video is paused")
         
         
    # key "r" get press
    if symbol == pyglet.window.key.R:
         
        # printing the message
        print("Key : R is pressed")
         
        # resume the video
        player.play()
         
        # printing message
        print("Video is resumed")
 
# run the pyglet application
pyglet.app.run()