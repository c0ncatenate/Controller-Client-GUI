import tkinter as tk
from tkinter import ttk, scrolledtext, font
import socket
import threading

class ControllerApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('600x500')
        self.title('Controller - Setup')
        
        self.ip_entry = None
        self.ip_address = None
        self.port_entry = None
        self.port = None
        self.status_label = ''
        self.server_status_label = None
        self.server_start_button = None
        self.server_stop_button = None
        
        self.load_first_frame()
        
        self.sock = None
        
        
    # GUI Functions

    def load_second_frame(self):
        # create the second frame with the layout from your provided code
        self.second_frame = tk.Frame(self)

        # create the Connections label
        connections_label = tk.Label(self.second_frame, text='Connections', font=('Arial', 16))
        connections_label.pack(pady=10)
        
        server_status_frame = tk.Frame(self.second_frame)
        server_status_frame.pack(pady=10)
        
        self.server_status_label = tk.Label(server_status_frame, text='Server Status: Stopped', font=('Arial', 12), borderwidth=2, relief='groove')
        self.server_status_label.grid(row=0, column=1, pady=10)
        
        self.server_start_button = tk.Button(server_status_frame, width=10, text="Start", command=self.start_server, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        self.server_start_button.grid(row=1, column=0)
        
        self.server_stop_button = tk.Button(server_status_frame, width=10, text="Stop", command=self.stop_server, state=tk.DISABLED, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        self.server_stop_button.grid(row=1, column=2)

        # create the treeview with two columns
        treeview_frame = tk.Frame(self.second_frame)
        treeview_frame.pack()

        treeview = ttk.Treeview(treeview_frame, columns=('IP', 'datetime'), height=5)
        treeview.heading('#0', text='ID')
        treeview.heading('IP', text='IP')
        treeview.heading('datetime', text='datetime')

        treeview.column('#0', width=50)

        treeview.pack(side='left', fill='both', expand=True)
        
        self.output_box_frame = tk.Frame(self.second_frame)
        self.output_box_frame.pack(pady=10)
        
        self.output_box = tk.scrolledtext.ScrolledText(self.output_box_frame, state='disabled', width=54, height=5)
        self.output_box.pack(side='left', fill='both', expand=True)
        self.output_box.config(state='normal', font=('Consolas', 10))
        self.output_box.insert(tk.END, 'This textbox shows you the message log.\n\n')
        self.output_box.config(state='disabled')
            

        # create a frame for the ID label and dropdown menu and Command label and textbox
        id_command_frame = tk.Frame(self.second_frame)
        id_command_frame.pack(pady=10)

        # create the ID label and dropdown menu
        id_label = tk.Label(id_command_frame, text='ID')
        id_label.pack(side='left')

        # options = ['Option 1', 'Option 2', 'Option 3']
        # id_dropdown = ttk.Combobox(id_command_frame, values=options)
        id_dropdown = ttk.Combobox(id_command_frame)
        id_dropdown.pack(side='left', padx=10)

        # create the Command label and textbox
        command_label = tk.Label(id_command_frame, text='Command')
        command_label.pack(side='left', padx=10)

        command_textbox = tk.Text(id_command_frame, width=30, height=1)
        command_textbox.pack(side='left')

        # create the Send Command button
        buttons_frame = tk.Frame(self.second_frame)
        buttons_frame.pack(pady=10)

        send_command_button = tk.Button(buttons_frame, text='Execute', font=('Arial', 12, 'bold'), width=10, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        send_command_button.pack(side='left', padx=10)

        back_button = tk.Button(buttons_frame, text='Back', command=lambda: [ self.second_frame.destroy(), self.load_first_frame()], font=('Arial', 12, 'bold'), width=10, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        back_button.pack(side='right', padx=10)

        # pack the second frame and forget the first frame
        self.second_frame.pack(fill='both', expand=True)
        self.first_frame.pack_forget()

    def load_first_frame(self):
        # create the first frame with a button in the middle
        self.first_frame = tk.Frame(self)

        heading = tk.Label(self.first_frame, text='Please provide the IP address and port for the controller.', font=('Arial', 14, 'bold'))
        heading.grid(row=0, column=0, columnspan=2, padx=50, pady=20)
        ip_label = tk.Label(self.first_frame, text='IP:', font=('Consolas', 20), width=5)
        ip_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.ip_entry = tk.Entry(self.first_frame, width=20, font=('Consolas', 20))
        self.ip_entry.grid(row=1, column=1, padx=10, pady=10)
        self.ip_entry.bind('<Return>', lambda event: self.port_entry.focus())

        port_label = tk.Label(self.first_frame, text='Port:', font=('Consolas', 20), width=5)
        port_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.port_entry = tk.Entry(self.first_frame, width=20, font=('Consolas', 20))
        self.port_entry.grid(row=2, column=1, padx=10, pady=10)
        self.port_entry.bind('<Return>', lambda event: self.save_values())

        self.status_label = tk.Label(self.first_frame, text='')
        self.status_label.grid(row=3, column=1, pady=10)

        save_button = tk.Button(self.first_frame, text='Save', font=('Arial', 16, 'bold'), width=10, command=self.save_values, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        save_button.grid(row=4, column=1, pady=50)

        self.help_frame = tk.Frame(self.first_frame)
        self.help_frame.grid(row=5, column=0)

        help_section = tk.Label(self, text='This IP address and port will be used to bind the controller.', font=('Arial', 14, 'bold'))
        help_section.place(relx=0.5, rely=1.0, anchor='s')
        # center the frame contents
        self.first_frame.place(relx=0.5, rely=0.5, anchor='center')


        
    def save_values(self):
        
        try:
            self.ip_address = self.ip_entry.get()
            self.port = int(self.port_entry.get())
        except ValueError:
            self.status_label.config(text="Please enter a valid ip address and port number.", font=('Arial', 12, 'bold'))
            
        if not self.ip_address or not self.port:
            self.status_label.config(text="Please enter a valid ip address and port number.", font=('Arial', 12, 'bold'), fg='red')
            self.after(3000, lambda: self.status_label.config(text=""))
            return
        
        self.load_second_frame()
        
    def start_server(self):
        self.bind_server()
        self.server_start_button.config(state=tk.DISABLED)
        self.server_stop_button.config(state=tk.NORMAL)
        self.server_status_label.config(text='Server Status: Running')
    
    def stop_server(self):
        self.unbind_server()
        self.server_stop_button.config(state=tk.DISABLED)
        self.server_start_button.config(state=tk.NORMAL)
        self.server_status_label.config(text='Server Status: Stopped')
        
    # Socket connection functions
    
    def bind_server(self):
        
        self.sock = socket.socket()
        self.sock.bind((self.ip_address, self.port))
        print("Server binding has completed!")
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, '[i] Server binding has completed!\n')
        self.output_box.config(state='disabled')
        self.output_box.yview_moveto(1.0)
        
    def unbind_server(self):
        self.sock.close()
        self.sock = None
        print("Server has closed!")
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, '[i] Server has closed!\n')
        self.output_box.config(state='disabled')
        self.output_box.yview_moveto(1.0)
if __name__ == '__main__':
    app = ControllerApp()
    app.protocol('WM_DELETE_WINDOW', app.destroy)
    app.mainloop()
