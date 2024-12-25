import tkinter as tk
import winreg

class RegistryBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("Обозреватель Реестра")
        self.listbox = tk.Listbox(self.root, width=80, height=30)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.history = []
        self.current_root = None
        self.root_keys()
        self.listbox.bind("<Double-1>", self.double_click)
    def root_keys(self):
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, "HKEY_CLASSES_ROOT")
        self.listbox.insert(tk.END, "HKEY_CURRENT_USER")
        self.listbox.insert(tk.END, "HKEY_LOCAL_MACHINE")
        self.listbox.insert(tk.END, "HKEY_USERS")
        self.listbox.insert(tk.END, "HKEY_CURRENT_CONFIG")
        self.current_root = None
    def double_click(self, event):
        selected = self.listbox.get(self.listbox.curselection())
        if self.current_root is not None:
            self.history.append((self.current_root, selected))
        self.listbox.delete(0, tk.END)

        try:
            if selected == "HKEY_CLASSES_ROOT":
                self.keys(winreg.HKEY_CLASSES_ROOT)
            elif selected == "HKEY_CURRENT_USER":
                self.keys(winreg.HKEY_CURRENT_USER)
            elif selected == "HKEY_LOCAL_MACHINE":
                self.keys(winreg.HKEY_LOCAL_MACHINE)
            elif selected == "HKEY_USERS":
                self.keys(winreg.HKEY_USERS)
            elif selected == "HKEY_CURRENT_CONFIG":
                self.keys(winreg.HKEY_CURRENT_CONFIG)
            else:
                self.subkeys(self.current_root, selected)
        except Exception as e:
            self.listbox.insert(tk.END, f"Error: {e}")

    def keys(self, root_key):
        self.current_root = root_key
        try:
            with winreg.OpenKey(root_key, "") as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    self.listbox.insert(tk.END, winreg.EnumKey(key, i))
        except Exception as e:
            self.listbox.insert(tk.END, f"Error: {e}")

    def subkeys(self, root_key, subkey):
        try:
            with winreg.OpenKey(root_key, subkey) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    self.listbox.insert(tk.END, winreg.EnumKey(key, i))
        except Exception as e:
            self.listbox.insert(tk.END, f"Error: {e}")

    def go_back(self):
        if not self.history:
            self.root_keys()
            return

        last_root, last_subkey = self.history.pop()
        self.listbox.delete(0, tk.END)

        if last_root is None:
            self.root_keys()
        else:
            self.current_root = last_root
            self.subkeys(last_root, last_subkey)


root = tk.Tk()
app = RegistryBrowser(root)
root.mainloop()
