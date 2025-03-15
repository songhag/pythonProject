import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text
from Profile import *
from ds_messenger import *
from pathlib import Path

class Body(tk.Frame):
    def __init__(self, root, profile, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.profile = profile
        self._contacts = []
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        selected_contact = self._contacts[index]
        self._select_callback(selected_contact)
        self.entry_editor.delete(1.0, tk.END)

        user = self.profile.username

        for sender, recip, msg in reversed(self.profile.conversation):
            if sender == user and recip == selected_contact:
                self.entry_editor.insert(tk.END, f"{selected_contact}: {msg}\n", 'entry-left')
            elif sender == selected_contact and recip == user:
                self.entry_editor.insert(tk.END, f"You: {msg}\n", 'entry-right')


    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None, path=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        self.path = path
        super().__init__(root, title)

    def body(self, frame):
        # self.path_label = tk.Label(frame, width=30, text="Profile path")
        # self.path_label.pack()
        # self.path_entry = tk.Entry(frame, width=30)
        #
        # self.path_entry.insert(tk.END, self.path)
        # self.path_entry.pack()
        self.path_label = tk.Label(frame, width=30, text="Profile path")
        self.path_label.pack()
        self.browse_button = tk.Button(frame, text="Browse", command=self.browse_file)
        self.browse_button.pack()
        self.selected_path_label = tk.Label(frame, width=50, text=self.path or "No file selected")
        self.selected_path_label.pack()

        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        #self.password...
        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("DSM Files", "*.dsu")],
            title="Select Profile File"
        )
        if filepath:
            self.path = filepath
            self.selected_path_label.config(text=self.path)

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.current_file=''
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!

        self.profile = Profile()  # Add Profile instance

        self.direct_messenger = None

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()


    def send_message(self):
        # You must implement this!
        message = self.body.get_text_entry()
        if not message or not self.recipient or not self.direct_messenger:
            self.footer.footer_label.config(text="Error: Missing message or recipient")
            return

        try:
            if self.direct_messenger.send(message, self.recipient):
                display_msg = message
                self.body.insert_user_message(f'You: {message}')
                self.profile.add_conversation(display_msg, self.recipient, self.username)
                self.body.set_text_entry('')
                self.profile.save_profile(self.current_file)
                self.body.profile.save_profile(self.current_file)
                self.footer.footer_label.config(text="Message sent")
            else:
                self.footer.footer_label.config(text="Error: Failed to send message")
        except Exception as e:
            self.footer.footer_label.config(text=f"Error: {str(e)}")

    def add_contact(self):
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        new_contact = tk.simpledialog.askstring("Add Contact", "Enter username:")
        if new_contact:
            self.body.insert_contact(new_contact)
        pass

    def recipient_selected(self, recipient):
        self.recipient = recipient
        self.footer.footer_label.config(text=f"Selected: {recipient}")

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server, self.current_file)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.current_file = ud.path

        filepath = Path(self.current_file)
        if filepath.is_file() and filepath.exists() and filepath.suffix == '.dsu':
            self.profile.load_profile(filepath)
            if self.profile.username is None and self.profile.password is None and self.profile.dsuserver is None:
                self.profile.username = ud.user
                self.profile.password = ud.pwd
                self.profile.dsuserver = ud.server
                self.profile.save_profile(self.current_file)
        else:
            self.footer.footer_label.config(text="File not found")
            return

        if self.profile.username != self.username or self.profile.password != self.password:
            self.footer.footer_label.config(text="Error: Credentials do not match profile")
            return

        # Load contacts into UI
        self.body._contacts.clear()
        self.body.posts_tree.delete(*self.body.posts_tree.get_children())
        dic={}
        for msg, recip, msger in self.profile.conversation:
            if recip not in dic and recip != self.username:
                dic[recip] = 1
                self.body.insert_contact(recip)

        self.footer.footer_label.config(text=f"Opened: {filepath}")

        # self.profile.username = ud.user
        # self.profile.password = ud.pwd
        # self.profile.dsuserver = ud.server
        # self.profile.save_profile(self.current_file)

        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)

        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.

    def publish(self, message: str):
        # You must implement this!
        pass

    def check_new(self):
        # You must implement this!
        if self.direct_messenger:
            new_messages = self.direct_messenger.retrieve_new()
            for msg in new_messages:
                contact = msg.recipient
                if contact not in self.body._contacts:
                    self.body.insert_contact(contact)
                self.profile.add_conversation(msg.message
                                              , self.username, contact)
                if self.recipient == contact:
                    self.body.insert_contact_message(
                        f"{contact}: {msg.message}")
            self.profile.save_profile(self.current_file)
        self.root.after(2000, self.check_new)
        pass

    def new_file(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".dsu",
            filetypes=[("DSM Files", "*.dsu")]
        )
        filepath = Path(filepath)
        if filepath.exists():
            self.footer.footer_label.config(text="Error: "
                                                 "File already "
                                                 "exists. Choose "
                                                 "a new name.")
            return
        else:
            filepath.touch()
        print(Path(filepath))
        self.current_file = filepath
        self.profile = Profile()
        self.profile.save_profile(filepath)


    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_file)
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root, self.profile,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
