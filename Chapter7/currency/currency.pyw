import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
    "..")))
import tkinter as tk
import Main
import Utils


def main():
    application = tk.Tk()
    Utils.set_application_icons(application, os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "images"))
    Main.Window(application)
    application.mainloop()


main()
