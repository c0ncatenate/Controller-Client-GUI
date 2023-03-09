'''
This code in this file combines the UI and the Controller together.
'''

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
        self.stopped = True
        self.conn = None
        self.addr = None
        
        self.id = 0
        self.ids = []
        self.clients = []
        
        self.load_first_frame()
        
        self.sock = None
        
        
    # GUI Functions

    def load_second_frame(self):
        
        self.title(f'Controller - {self.ip_address} : {self.port}')
        # create the second frame with the layout from your provided code
        self.second_frame = tk.Frame(self)

        # create the Connections label
        self.connections_label = tk.Label(self.second_frame, text='Connections', font=('Arial', 16))
        self.connections_label.pack(pady=10)
        
        self.server_status_frame = tk.Frame(self.second_frame)
        self.server_status_frame.pack(pady=10)
        
        self.server_status_label = tk.Label(self.server_status_frame, text='Server Status: Stopped', font=('Arial', 12), borderwidth=2, relief='groove')
        self.server_status_label.grid(row=0, column=1, pady=10)
        
        self.server_start_button = tk.Button(self.server_status_frame, width=10, text="Start", command=self.start_server_thread, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        self.server_start_button.grid(row=1, column=0)
        
        self.server_stop_button = tk.Button(self.server_status_frame, width=10, text="Stop", command=self.stop_server, state=tk.DISABLED, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        self.server_stop_button.grid(row=1, column=2)

        # create the treeview with two columns
        self.treeview_frame = tk.Frame(self.second_frame)
        self.treeview_frame.pack()

        self.treeview = ttk.Treeview(self.treeview_frame, columns=('IP', 'datetime'), height=5)
        self.treeview.heading('#0', text='ID')
        self.treeview.heading('IP', text='IP')
        self.treeview.heading('datetime', text='datetime')

        self.treeview.column('#0', width=50)

        self.treeview.pack(side='left', fill='both', expand=True)
        
        self.output_box_frame = tk.Frame(self.second_frame)
        self.output_box_frame.pack(pady=10)
        
        self.output_box = tk.scrolledtext.ScrolledText(self.output_box_frame, state='disabled', width=54, height=5)
        self.output_box.pack(side='left', fill='both', expand=True)
        self.output_box.config(state='normal', font=('Consolas', 10))
        self.output_box.insert(tk.END, 'This textbox shows you the message log.\n\n')
        self.output_box.config(state='disabled')
            

        # create a frame for the ID label and dropdown menu and Command label and textbox
        self.id_command_frame = tk.Frame(self.second_frame)
        self.id_command_frame.pack(pady=10)

        # create the ID label and dropdown menu
        self.id_label = tk.Label(self.id_command_frame, text='ID')
        self.id_label.pack(side='left')

        # self.id_dropdown = ttk.Combobox(id_command_frame, values=options)
        self.id_dropdown = ttk.Combobox(self.id_command_frame)
        self.id_dropdown.pack(side='left', padx=10)

        # create the Command label and textbox
        self.command_label = tk.Label(self.id_command_frame, text='Command')
        self.command_label.pack(side='left', padx=10)

        self.command_entry = tk.Entry(self.id_command_frame)
        self.command_entry.pack(side='left')

        # create the Send Command button
        self.buttons_frame = tk.Frame(self.second_frame)
        self.buttons_frame.pack(pady=10)

        self.send_command_button = tk.Button(self.buttons_frame, text='Execute', command=self.execute_command,  font=('Arial', 12, 'bold'), width=10, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        self.send_command_button.pack(side='left', padx=10)

        self.back_button = tk.Button(self.buttons_frame, text='Back', command=lambda: [ self.second_frame.destroy(), self.load_first_frame()], font=('Arial', 12, 'bold'), width=10, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        self.back_button.pack(side='right', padx=10)

        # pack the second frame and forget the first frame
        self.second_frame.pack(fill='both', expand=True)
        self.first_frame.pack_forget()

    def load_first_frame(self):
        # create the first frame with a button in the middle
        self.first_frame = tk.Frame(self)

        heading = tk.Label(self.first_frame, text='Please provide the IP address and port for the controller.', font=('Arial', 14, 'bold'))
        heading.grid(row=0, column=0, columnspan=2, padx=50, pady=20)
        self.ip_label = tk.Label(self.first_frame, text='IP:', font=('Consolas', 20), width=5)
        self.ip_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.ip_entry = tk.Entry(self.first_frame, width=20, font=('Consolas', 20))
        self.ip_entry.insert(tk.END, socket.gethostname())
        self.ip_entry.grid(row=1, column=1, padx=10, pady=10)
        self.ip_entry.bind('<Return>', lambda event: self.port_entry.focus())

        self.port_label = tk.Label(self.first_frame, text='Port:', font=('Consolas', 20), width=5)
        self.port_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.port_entry = tk.Entry(self.first_frame, width=20, font=('Consolas', 20))
        self.port_entry.insert(tk.END, '9999')
        self.port_entry.grid(row=2, column=1, padx=10, pady=10)
        self.port_entry.bind('<Return>', lambda event: self.save_values())

        self.status_label = tk.Label(self. first_frame, text='')
        self.status_label.grid(row=3, column=1, pady=10)

        self.save_button = tk.Button(self.first_frame, text='Save', command=self.save_values, font=('Arial', 16, 'bold'), width=10, relief='raised', highlightbackground='#007acc',  highlightcolor='white')
        self.save_button.grid(row=4, column=1, pady=50)

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



    # Functions for the socket connection        
        
    def start_server_thread(self):
        self.stopped = False
        self.server_start_button.config(state=tk.DISABLED)
        self.server_stop_button.config(state=tk.NORMAL)
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, '[i] Starting server...\n')
        self.output_box.config(state='disabled')
        self.treeview.delete(*self.treeview.get_children())

        # create a new thread to run the start_server method
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        
    def start_server(self):
        # self.stopped = False
        # self.bind_server()
        # self.server_start_button.config(state=tk.DISABLED)
        # self.server_stop_button.config(state=tk.NORMAL)
        # self.server_status_label.config(text='Server Status: Running')
        # self.listen_thread = threading.Thread(target=self.listen)
        # self.listen_thread.start()
        

        self.server_start_button.config(state=tk.DISABLED)
        self.server_stop_button.config(state=tk.NORMAL)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind((self.ip_address, self.port))
            self.stopped = False
            self.listen_thread = threading.Thread(target=self.listen())
            self.listen_thread.start()

        except OSError as e:
            print(e)
            self.output_box.config(state='normal')
            self.output_box.insert(tk.END, f'Error: {e}\n')
            self.output_box.config(state='disabled')
            self.output_box.yview_moveto(1.0)
            self.server_start_button.config(state=tk.NORMAL)
            self.server_stop_button.config(state=tk.DISABLED)


    # Socket connection functions
            
    def listen(self):
        print("Server is now listening...")
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, f'[i] Server is now listening for connections:\n')
        self.output_box.insert(tk.END, f'    {self.ip_address}:{self.port}\n')
        self.output_box.config(state='disabled')
        self.output_box.yview_moveto(1.0)
        self.sock.listen(1)
        self.sock.settimeout(1.0)
        while not self.stopped:
            try:
                self.conn, self.addr = self.sock.accept()
                self.clients.append((self.conn, self.addr))
                thread = threading.Thread(target=self.handle_client, args=(self.conn, self.addr))
                thread.start()
            except socket.timeout:
                pass
            except OSError as e:
                if not self.stopped:
                    print(f"Error accepting connection: {e}")
                    break

        

    def handle_client(self, conn, addr):
        print(f'Connection has been established from: {addr}')
        self.id += 1
        self.ids.append(self.id)
        self.id_dropdown.config(values=self.ids)
        self.id_dropdown.current(len(self.ids)-1)
        
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, f'[i] Connection has been established from: {addr[0]}\n')
        self.output_box.config(state='disabled')
        self.output_box.yview_moveto(1.0)
            
            
    def execute_command(self):
        self.command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        current = self.id_dropdown.current()
        
        print(current)
        print(self.ids)
        
        if current+1 in self.ids:
            self.conn, self.addr = self.clients[current]
            if self.command != 'bye':
                self.conn.send(self.command.encode())
                out = self.conn.recv(2048)
                print(out.decode())
                self.output_box.config(state='normal')
                self.output_box.insert(tk.END, f'Client {current+1} says: {out.decode()}\n')
                self.output_box.config(state='disabled')
                self.output_box.yview_moveto(1.0)
            else:
                self.conn.send(self.command.encode())
                out = self.conn.recv(2048)
                self.output_box.config(state='normal')
                self.output_box.insert(tk.END, f'Client {current+1} says: {out.decode()}\n')
                self.output_box.insert(tk.END, f'Client {current+1} has disconnected!\n')
                self.output_box.config(state='disabled')
                self.output_box.yview_moveto(1.0)
                self.id_dropdown.delete(current)
                self.ids.pop(current)
                self.id_dropdown.config(values=self.ids)
                
                
        else:
            print('Invalid ID')
            
            

    def stop_server(self):
        self.stopped = True
        if self.conn is not None:
            self.conn.send('bye'.encode())
            self.conn.close()
        if hasattr(self, 'listen_thread'):
            self.listen_thread.join()
        self.sock.close()
        self.sock = None
        print("Server has closed!")
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, '[i] The server\'s connection has been closed.\n')
        self.output_box.config(state='disabled')
        self.output_box.yview_moveto(1.0)
        self.server_stop_button.config(state=tk.DISABLED)
        self.server_start_button.config(state=tk.NORMAL)
        self.server_status_label.config(text='Server Status: Stopped')


        
if __name__ == '__main__':
    app = ControllerApp()
    app.protocol('WM_DELETE_WINDOW', app.destroy)
    app.mainloop()
