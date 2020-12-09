import tkinter as tk
from tkinter import messagebox
    
class LedControlApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.red = tk.IntVar()
        self.green = tk.IntVar()
        self.blue = tk.IntVar()
        self.command = tk.StringVar()
        self.create_widget()
        
        
    def create_widget(self):
        
        
        self.redLbl = tk.Label(self.master, text="Red")
        self.greenLbl = tk.Label(self.master, text="Green")
        self.blueLbl = tk.Label(self.master, text="Blue")
        self.commandLbl = tk.Label(self.master, text="Command")
        
        self.red_text = tk.Entry(self.master, textvariable=self.red)
        self.green_text = tk.Entry(self.master, textvariable=self.green)
        self.blue_text = tk.Entry(self.master, textvariable=self.blue)
        self.command_text = tk.Entry(self.master, textvariable=self.command)
    
        self.confirm_btn = tk.Button(self.master, text="Confirm", command=self.confirmCallBack)
        
        self.redLbl.pack()
        self.red_text.pack()
        
        self.greenLbl.pack()
        self.green_text.pack()
        
        self.blueLbl.pack()
        self.blue_text.pack()
        
        self.commandLbl.pack()
        self.command_text.pack()
        
        self.confirm_btn.pack()
        
    def confirmCallBack(self):
        red = self.red.get()
        green = self.green.get()
        blue = self.blue.get()
        if red < 0 or red > 100\
           or blue < 0 or blue > 100\
           or green < 0 or green > 100:
            messagebox.showinfo( "Warning", "Color should be in range 0 to 100." )
        elif len(self.command.get()) == 0:
            messagebox.showinfo( "Warning", "Please enter a command." )
        else:
            with open( "command_list.txt", "a" ) as file:

                file.write( self.command.get().upper() + "," +str(self.red.get()) +"," + str(self.green.get()) +"," + str(self.blue.get()) + "\n" )
            messagebox.showinfo( "Saved", "Saved color command." )
            self.master.destroy()
        
def call_ui():
    root = tk.Tk()
    root.title("Led Controller App")
    root.geometry("250x300")
    app = LedControlApp(root)
    app.mainloop()