import os, sys
import Tkinter
import Image, ImageTk
import serial
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class MyHandler(BaseHTTPRequestHandler):
    
     def do_GET(self):
        try:
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
                 
            return
			
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

     def do_POST(self):
       global rootnode
       try:
	  ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
          if ctype == 'multipart/form-data':
              query=cgi.parse_multipart(self.rfile, pdict)
          self.send_response(301)
          self.end_headers()
          l1= query.get('lf')# *1000 sec
          ld= query.get('ld')# *1000 sec
          lh= query.get('layer') #mm layer
          l1[0]=int(l1[0])*1000
	  ld[0]=int(ld[0])*1000
	  lh[0]=float(lh[0])
          print l1[0]
	  print ld[0]
	  print lh[0]
          z=0
          x=1
          ser = serial.Serial('com3', 9600) 
          # ser.write(srting) #invia stringa
          # print ser.readline() # leggi stringa

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
                  if x==1 :
                   root.after(l1[0], lambda: root.quit())
                  else:
                   root.after(ld[0], lambda: root.quit())

                  if old_label_image is not None:
                      old_label_image.destroy()
                  old_label_image = label_image
	          root.mainloop()
        
                  z=z+4
                  ser.write('G1 Z%f'% z)
                  print ('G1 Z%f'% z)
                  z=lh[0]*x
                  ser.write('G1 Z%f'% z)
                  print z

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
            
       except :
         pass

def main():
    try:
        server = HTTPServer(('', 80), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

