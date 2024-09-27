import customtkinter
import tkinter
import tkinter.messagebox
import shutil
import os

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("FileArchiver")

        self.iconbitmap("icon.ico")
        self.geometry("800x600")
        self.resizable(False, False)

        self.grid_columnconfigure(
            index = 1,
            weight = 1
        )
        self.grid_columnconfigure(
            index = (2, 3),
            weight = 0
        )
        self.grid_rowconfigure(
            index = (0, 1, 2),
            weight = 1
        )



        self.sidebar_frame = customtkinter.CTkFrame(
            master = self,
            height = 600,
            corner_radius = 0
        )
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.title_label = customtkinter.CTkLabel(
            master = self.sidebar_frame,
            text = "FileArchiver",
            font = customtkinter.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=24, pady=24)



        self.tabview = customtkinter.CTkTabview(
            master = self,
            width = 512,
            height = 256
        )
        self.tabview.grid(row=0, column=1, padx=32, pady=32, sticky="nsew")

        self.tabview.add("Archive")
        self.tabview.add("Unpack")

        self.path_setting = customtkinter.CTkEntry(
            master = self.tabview.tab("Archive"),
            width = 512,
            placeholder_text = "Insert folder path to archive",
            font = customtkinter.CTkFont(size=16)
        )
        self.path_setting.grid(row=0, column=0, padx=8, pady=8)

        self.delete_setting = customtkinter.CTkCheckBox(
            master = self.tabview.tab("Archive"),
            text = "Delete original files when archived",
            width = 512,
            font = customtkinter.CTkFont(size=16)
        )
        self.delete_setting.grid(row=1, column=0, padx=8, pady=8)



        self.archive_button = customtkinter.CTkButton(
            master = self.tabview.tab("Archive"),
            text = "ARCHIVE",
            font = customtkinter.CTkFont(size=16),
            command = lambda: self.archive_files(self.path_setting.get(), self.delete_setting.get())
        )
        self.archive_button.grid(row=2, column=0, padx=8, pady=(320, 8))





        self.path_setting1 = customtkinter.CTkEntry(
            master = self.tabview.tab("Unpack"),
            width = 512,
            placeholder_text = "Insert archive path to unpack",
            font = customtkinter.CTkFont(size=16)
        )
        self.path_setting1.grid(row=0, column=0, padx=8, pady=8)

        self.path2_setting = customtkinter.CTkEntry(
            master = self.tabview.tab("Unpack"),
            width = 512,
            placeholder_text = "Insert path for extracted files",
            font = customtkinter.CTkFont(size=16)
        )
        self.path2_setting.grid(row=1, column=0, padx=8, pady=8)



        self.delete_setting1 = customtkinter.CTkCheckBox(
            master = self.tabview.tab("Unpack"),
            text = "Delete archive when unpacked",
            width = 512,
            font = customtkinter.CTkFont(size=16)
        )
        self.delete_setting1.grid(row=2, column=0, padx=8, pady=8)



        self.unpack_button = customtkinter.CTkButton(
            master = self.tabview.tab("Unpack"),
            text = "UNPACK",
            font = customtkinter.CTkFont(size=16),
            command = lambda: self.unpack_files(self.path_setting1.get(), self.path2_setting.get(), self.delete_setting1.get())
        )
        self.unpack_button.grid(row=3, column=0, padx=8, pady=(320, 8))
    




    def archive_files(self, path, delete_when_archived):
        if path:
            try:
                try:
                    shutil.make_archive(
                        base_name = rf"{path}",
                        root_dir = rf"{path}",
                        format = "zip"
                    )
                except NotADirectoryError:
                    tkinter.messagebox.showerror(
                        title = "Error",
                        message = f"\"{path}\" isn't a directory"
                    )

                    return
                
                if delete_when_archived == True:
                    try:
                        shutil.rmtree(rf"{path}")
                    except NotADirectoryError:
                        os.remove(rf"{path}")
                    except FileNotFoundError:
                        tkinter.messagebox.showerror(
                            title = "Error",
                            message = "File not found"
                        )

                        return
                
                tkinter.messagebox.showinfo(
                    title = "Info",
                    message = "Successfully archived your file"
                )
            except FileNotFoundError:
                tkinter.messagebox.showerror(
                    title = "Error",
                    message = "File not found"
                )

                return
        else:
            tkinter.messagebox.showerror(
                title = "Error",
                message = "Folder path shouldn't be empty"
            )

            return
    
    def unpack_files(self, path, path2, delete_when_unpacked):
        if path:
            try:
                shutil.unpack_archive(
                    filename = rf"{path}",
                    extract_dir = rf"{path2}",
                    format = "zip"
                )

                if delete_when_unpacked == True:
                    try:
                        os.remove(rf"{path}")
                    except FileNotFoundError:
                        tkinter.messagebox.showerror(
                            title = "Error",
                            message = "File not found"
                        )

                        return

                tkinter.messagebox.showinfo(
                    title = "Info",
                    message = "Successfully unpacked your archive"
                )
            except shutil.ReadError:
                tkinter.messagebox.showerror(
                    title = "Error",
                    message = f"\"{path}\" isn't an archive"
                )

                return
            except FileNotFoundError:
                tkinter.messagebox.showerror(
                    title = "Error",
                    message = "File not found"
                )

                return
        else:
            tkinter.messagebox.showerror(
                title = "Error",
                message = "Folder path shouldn't be empty"
            )

            return

if __name__ == "__main__":
    app = App()
    app.mainloop()
