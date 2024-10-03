"""
This module contains the main function for the application.
"""
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import threading
import os
import sys
from main import main

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainApplication(tk.Frame):
    """
        Creates and displays the main window of the application.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.parent.title("ADP Script")
        self.parent.resizable(width=False, height=False)

        # # Center window
        self.window_width = 250
        self.window_height = 100
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        self.x_coordinate = (screen_width / 2) - (self.window_width / 2)
        self.y_coordinate = (screen_height / 2) - (self.window_height / 2)

        self.parent.geometry(
            f"{self.window_width}x{self.window_height}+"
            f"{int(self.x_coordinate)}+{int(self.y_coordinate)}")

        # Create a nice and big button
        self.style = ttk.Style()
        self.style.configure("TButton", padding=10, font=("Helvetica", 14))

        self.run_button = ttk.Button(root, text="Run Script", command=self.button_clicked)
        self.run_button.pack(pady=20)

        self.wait_message = None

    def button_clicked(self):
        """
            Event handler for when the user clicks on the "Run Script" button.
            Disables the button, displays a "Please wait" message box, and runs the main function.
        """
        # Disable the button to prevent multiple runs
        self.run_button.config(state=tk.DISABLED)

        # Display a "Please wait" message box
        self.wait_message = tk.Toplevel(self.parent)
        self.wait_message.title("Wait")
        self.wait_message.geometry(f"{root.winfo_width()}x"
                                   f"{root.winfo_height()}+"
                                   f"{int(self.x_coordinate)}+"
                                   f"{int(self.y_coordinate)}")

        wait_label = ttk.Label(self.wait_message, text="Please wait...")
        wait_label.pack(padx=20, pady=10)

        # Set focus on the "Please wait" window and make it modal
        self.wait_message.grab_set()

        # Create a thread to run the main() function
        progress_thread = threading.Thread(target=self.run_main)
        progress_thread.start()

    def run_main(self):
        """
        Runs the main function defined in the main module.
        Displays a message after the function is done running.
        """
        try:
            main()
            messagebox.showinfo(title="Done", message="The ADP hours have been updated")
        except Exception as exception:
            messagebox.showerror(title="Error", message=f"An error occurred: {str(exception)}")
        finally:
            # Close the wait window
            self.wait_message.destroy()

            # Show the root window
            self.parent.deiconify()

            # Enable the button after completion
            self.run_button.config(state=tk.NORMAL)


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)

    # Set the icon for the root window
    icon = resource_path("clock.ico")
    root.iconbitmap(default=icon)

    root.mainloop()
