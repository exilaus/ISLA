import os, sys
import Tkinter
import Image, ImageTk
import serial

lt1= 40*1000 #sec
lt2= 20*1000 #sec
lt3= 20*1000 #sec
lt4= 20*1000 #sec
lt5= 20*1000 #sec
ldefault = 20*1000
lh=0.4  # mm layer

z=0
x=1
ser = serial.Serial('com3', 9600) # Establish the connection on a specific port
#counter = 32 # Below 32 everything in ASCII is gibberish
#     ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
#     print ser.readline() # Read the newest output from the Arduino

dirlist = os.listdir('.\slices')

root = Tkinter.Tk()
#root.geometry('+%d+%d' % (3100,100))
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
old_label_image = None

ser.write('G28')

image1 = Image.open('black.jpg')
root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
tkpi = ImageTk.PhotoImage(image1)
label_image = Tkinter.Label(root, image=tkpi)
label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
root.after(100, lambda: root.quit())
root.mainloop()
if old_label_image is not None:
            old_label_image.destroy()
old_label_image = label_image
for f in dirlist:
    

    try:
        image1 = Image.open('.\slices\%d.png' % x)
        root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
        tkpi = ImageTk.PhotoImage(image1)
        label_image = Tkinter.Label(root, image=tkpi)
        label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
        root.after(10, lambda: root.quit())
        if old_label_image is not None:
            old_label_image.destroy()
        old_label_image = label_image
	root.mainloop()
        
        z=z+4
        ser.write('G1 Z%d'% z)
        z=lh*x
        ser.write('G1 Z%d'% z)
        
        image1 = Image.open('black.jpg')
        root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
        tkpi = ImageTk.PhotoImage(image1)
        label_image = Tkinter.Label(root, image=tkpi)
        label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
        root.after(500, lambda: root.quit())
	x=x+1
        if old_label_image is not None:
            old_label_image.destroy()
        old_label_image = label_image
        root.mainloop()
    except Exception, e:  # This is used to end print process. if file no exist we have finish a print.
        pass
   
    