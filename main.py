import threading
import time
import pyautogui as pg
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import ctypes


idk = {"48":"z","49":"z","50":"x","51":"x","52":"c","53":"v","54":"v","55":"b","56":"b","57":"n","58":"n","59":"m","60":"a","61":"a","62":"s","63":"s","64":"d","65":"f","66":"f","67":"g","68":"g","69":"h","70":"h","71":"j","72":"q","73":"q","74":"w","75":"w","76":"e","77":"r","78":"r","79":"t","80":"t","81":"y","82":"y","83":"u"}

exit_flag = False

class keytip(threading.Thread):
      def __init__(self, msg):
            threading.Thread.__init__(self)
            self.msg = msg
      def run(self):
            try:
                  self.msg.note -=12
            except:
                  pass
            try:              
                  if self.msg.type == 'note_on':
                        pg.keyDown(idk[str(self.msg.note)])
                       
                        #print(f"keydown{idk[str(self.msg.note)]}")
                  elif self.msg.type == 'note_off':
                        pg.keyUp(idk[str(self.msg.note)])
                        
                        #print(f"keyUp{idk[str(self.msg.note)]}")
            except:
                  pass

class play(threading.Thread):

      def __init__(self,file_name):
            threading.Thread.__init__(self)
            self.file_name = file_name
            

      def run(self):
            global exit_flag
            time.sleep(3)
            import mido
            mid = mido.MidiFile(self.file_name, clip=True)
            self.wait_label = Label(text = f"playing").grid()
            for msg in mid:
                  time.sleep(msg.time)
                  if not msg.is_meta: 
                        thread_keytip = keytip(msg)
                        thread_keytip.start()
                  if exit_flag:
                        break
            exit_flag = False
            

class Application(ttk.Frame):

      def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.file_name = ""
        self.createWidgets(self.file_name) 
        
      def createWidgets(self,file_name):
            self.select_btn=Button(text='select file', command=self.select_file).grid()
            self.file_label = Label(text = f"file:{file_name}").grid(column=1 , row=1)
            self.play_btn=Button(text='play', command=self.play).grid()
            self.stop_btn=Button(text='stop', command=self.stop).grid()

      def select_file(self):
            self.file_name = askopenfilename(title='Open a file',initialdir='./',filetypes=(('midi', '*.mid'),))
            self.file_label = Label(text = f"file:{self.file_name}").grid(column=1 , row=1)

      def stop(self):
            global exit_flag
            exit_flag=True

      def play(self):
            self.wait_label=Label(text=f"wait:{3}sec").grid(column=1 , row=1) 
            thread_play = play(self.file_name)
            thread_play.start()

            
  
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False    

if __name__ == '__main__':
      if is_admin():
            window = Tk()
            window.geometry('500x350')
            window.wm_attributes('-topmost',1)
            app = Application(window)
            window.mainloop()
      else:
            print("%15s" % "沒有權限")
            print('%20s'%'*** 需要以管理員身份執行 ***')
