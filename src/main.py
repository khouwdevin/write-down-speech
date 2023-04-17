from typing import List

import ttkbootstrap as ttk
from pages.mainpage import MainPage

from utils.util import get_path

page_data = [MainPage]

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename = "journal")
        self.title("speech to Text")

        self.geometry("600x300")
        self.minsize(600, 300)

        self.iconbitmap(get_path("public\\icon.ico"))

        container = ttk.Frame(self)
        container.pack(side = "bottom", fill = "both", expand = 1)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.pages: List[ttk.Frame] = []

        for p in page_data:
            page: ttk.Frame = p(container, self)
            page.grid(row = 0, column = 0, sticky ="nsew")

            self.pages.append(page)

        self.place_window_center()

        self.change_page(0)

        self.mainloop()

    def change_page(self, current_page: int):
        page = self.pages[current_page]
        page.tkraise()

if __name__ == "__main__":
    App()
