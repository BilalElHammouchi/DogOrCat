from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from ttkthemes import ThemedStyle
import configparser
from PIL import ImageTk, Image
from threading import Thread

class DogOrCat( Tk ):
    def __init__(self) -> None:
        super().__init__()
        self.title("Dog or Cat?")
        program_menu = Menu(self)
        self.config(menu=program_menu)
        file_menu =Menu(program_menu)
        program_menu.add_cascade(label="Theme", menu=file_menu )
        self.preferences_menu = Menu(program_menu)
        self.configuration()
        self.theme = ThemedStyle(self)
        self.switch_theme(self.theme_found)
        self.theme_names = self.theme.theme_names()
        self.theme_names.sort()
        for theme in self.theme_names:
            file_menu.add_command(label= theme , command = lambda theme = theme:self.switch_theme(theme) )
        self.main_menu = ttk.Frame(self)
        self.main_menu.pack( expand = True, fill = "both")
        self.dog_img = ImageTk.PhotoImage( Image.open( "lib/dog.png") )
        self.cat_img = ImageTk.PhotoImage( Image.open( "lib/cat.png") )
        self.robot_img = ImageTk.PhotoImage( Image.open( "lib/robot.png") )
        self.main_label = ttk.Label(self.main_menu, text = "Dog or Cat?", font = ("Orelega One", 25) )
        self.main_label.pack()
        self.img_frame = ttk.Frame(self.main_menu )
        self.img_frame.pack()
        self.dog_label = ttk.Label(self.img_frame, image = self.dog_img )
        self.dog_label.pack( side = "left", padx = 20, pady = 20 )
        self.cat_label = ttk.Label(self.img_frame, image = self.cat_img )
        self.cat_label.pack( side = "left", padx = 20, pady = 20 )
        self.stats_frame = ttk.Frame(self.main_menu )
        self.stats_frame.pack()
        self.accuracy_label = ttk.Label(self.stats_frame )
        self.accuracy_label.pack( side = "left", padx = 20, pady = 20 )
        if int(self.configparser['Stats']['tries']):
            self.accuracy_label.configure( text = f"Accuracy: {(int(self.configparser['Stats']['success'])/int(self.configparser['Stats']['tries']))*100}%" )
        else:
            self.accuracy_label.configure( text = f"Accuracy: TBD" )
        self.tries_label = ttk.Label(self.stats_frame, text = f"Tries: {self.configparser['Stats']['tries']}" )
        self.tries_label.pack( side = "left", padx = 20, pady = 20 )
        self.success_label = ttk.Label(self.stats_frame, text = f"Success: {self.configparser['Stats']['success']}" )
        self.success_label.pack( side = "left", padx = 20, pady = 20 )
        self.failure_label = ttk.Label(self.stats_frame, text = f"Failure: {self.configparser['Stats']['failure']}" )
        self.failure_label.pack( side = "left", padx = 20, pady = 20 )
        self.buttons_frame = ttk.Frame(self.main_menu )
        self.buttons_frame.pack( pady = 10 )
        self.insert_button = ttk.Button(self.buttons_frame, text = "Upload a picture", command = self.upload_pic )
        self.insert_button.pack( side = "left", padx = 20 )
        self.reset_button = ttk.Button(self.buttons_frame, text = "Reset stats", command = self.reset_stats )
        self.reset_button.pack( side = "left", padx = 20 )
        self.model = load_model('lib/final_model.h5')
        self.model_button = ttk.Button(self.buttons_frame, text = "Select model", command = self.select_model )
        self.model_button.pack( side = "left", padx = 20 )
        self.center()

    def select_model(self):
        try:
            self.model = load_model( fd.askopenfilename() )
            messagebox.showinfo('Success','Model successfully selected!')
        except:
            messagebox.showerror('Error','Model was not recognized!')

    def reset_stats(self):
        self.configparser['Stats']['tries'] = self.configparser['Stats']['success'] = self.configparser['Stats']['failure'] = '0'
        with open('lib/configuration.ini', 'w') as configfile:
            self.configparser.write(configfile)
        self.update_stats()

    def update_stats(self):
        if int(self.configparser['Stats']['tries']):
            self.accuracy_label.configure( text = f"Accuracy: {(int(self.configparser['Stats']['success'])/int(self.configparser['Stats']['tries']))*100}%" )
        else:
            self.accuracy_label.configure( text = f"Accuracy: TBD" )
        self.tries_label.configure( text = f"Tries: {self.configparser['Stats']['tries']}" )
        self.success_label.configure( text = f"Success: {self.configparser['Stats']['success']}" )
        self.failure_label.configure( text = f"Failure: {self.configparser['Stats']['failure']}" )

    def upload_pic(self):
        self.filename = fd.askopenfilename()
        if self.filename:
            self.answer_window = Toplevel()
            #self.answer_window.geometry("300x300")
            self.answer_frame = ttk.Frame(self.answer_window )
            self.answer_frame.pack()
            self.answer_window.overrideredirect(True)
            self.answer_window.deiconify()
            thread = Thread( target = self.predict )
            self.answer_img = ttk.Label(self.answer_frame, image = self.robot_img )
            thread.start()
            self.answer_img.pack( padx = 20, pady = 20 )
            self.answer_buttons = ttk.Frame(self.answer_frame )
            self.answer_buttons.pack( pady = 20 )
            self.correct_button = ttk.Button(self.answer_buttons, text = "Correct", command = lambda: self.answer(1) )
            self.correct_button.pack( side = "left", padx = 20 )
            self.wrong_button = ttk.Button(self.answer_buttons, text = "Wrong", command = lambda: self.answer(0) )
            self.wrong_button.pack( side = "left", padx = 20 )
            self.center(self.answer_window)

    def predict(self):
        self.load_image()
        self.result = self.model.predict(self.img)
        if self.result[0][0] == 1:
            self.answer_img.configure( image = self.dog_img )
        else:
            self.answer_img.configure( image = self.cat_img )
        print(f"{self.result[0][0] = }")
        self.center(self.answer_window)

    def answer(self, value ):
        self.configparser['Stats']['tries'] = str( 1 + int(self.configparser['Stats']['tries']) )
        if value:
            self.configparser['Stats']['success'] = str( 1 + int(self.configparser['Stats']['success']) )
        else:
            self.configparser['Stats']['failure'] = str( 1 + int(self.configparser['Stats']['failure']) )
        with open('lib/configuration.ini', 'w') as configfile:
            self.configparser.write(configfile)
        self.answer_window.destroy()
        self.update_stats()

    def switch_theme(self,theme):
        self.theme.set_theme(theme)
        self.configparser['Options']['theme'] = theme
        with open('lib/configuration.ini', 'w') as configfile:
            self.configparser.write(configfile)

    def configuration(self):
        self.configparser = configparser.ConfigParser()
        self.configparser.read('lib/configuration.ini')
        self.theme_found = self.configparser['Options']['theme']

    def load_image(self):
        # load the image
        img = load_img(self.filename, target_size=(224, 224))
        # convert to array
        img = img_to_array(img)
        # reshape into a single sample with 3 channels
        img = img.reshape(1, 224, 224, 3)
        # center pixel data
        img = img.astype('float32')
        self.img = img - [123.68, 116.779, 103.939]

    def center(self, *args):
        if not args:
            window = self
        else:
            window = args[0]

        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        window.geometry("+%d+%d" % (x, y))
        
if __name__ == '__main__':
    app = DogOrCat()
    app.mainloop()