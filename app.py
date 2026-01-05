import tkinter as tk
from tkinter import messagebox
from urllib import request

TITLE = "Name Popularity"
BASE_URL = "https://cs.stcc.edu/~silvestri/csc220/names"
CACHE_FILENAME = "NameCache.txt"
NAMES = {}

class NamePopularityApp:
    
    def __init__(self):
        self.root = tk.Tk()
        self.is_caching = False
        
        self.root.bind("<Return>", self.processSearch)
        self.root.bind("<Destroy>", self.saveCache)

        self.loadCache()
        self.buildGui()

    def buildGui(self):
        self.root.title(TITLE)
        
        # Frames
        frame0 = tk.Frame(self.root)
        frame1 = tk.Frame(frame0)
        frame1_1 = tk.Frame(frame1)
        frame1_2 = tk.Frame(frame1)
        frame2 = tk.Frame(frame0)
        frame3 = tk.Frame(frame0)
        frame4 = tk.Frame(frame0)
        frame4_1 = tk.Frame(frame4)
        frame4_2 = tk.Frame(frame4)

        frame0.pack(padx = 10, pady = 10)
        frame1.pack()
        frame1_1.pack(side = "left", padx = 5)
        frame1_2.pack(side = "right", padx = 5)
        frame2.pack()
        frame3.pack(pady = 5)
        frame4.pack(pady = 5)
        frame4_1.pack(side = "left", padx = 5)
        frame4_2.pack(side = "right", padx = 5)

        # Input
        # / Frame 1 - Name & Year
        tk.Label(frame1_1, text = "Name").pack(pady = 5)
        tk.Label(frame1_1, text = "Year").pack(pady = 5)
        
        self.name_entry = tk.Entry(frame1_2)
        self.name_entry.pack(pady = 5)
        
        self.year_entry = tk.Entry(frame1_2)
        self.year_entry.pack(pady = 5)

        # / Frame 2 - Sex
        self.sex = tk.StringVar(value = 'M')

        tk.Radiobutton(
            frame2, text = "Male",
            variable = self.sex, value = 'M'
        ).pack(side = "left")

        tk.Radiobutton(
            frame2, text = "Female",
            variable = self.sex, value = 'F'
        ).pack()

        # Frame 3 - Search Button
        tk.Button(
            frame3, text = "Search Rank",
            command = self.processSearch
        ).pack()

        # Output
        # / Frame 4 - Ranking
        tk.Label(frame4_1, text = "Popularity:").pack()
        
        self.ranking_entry = tk.Entry(frame4_2)
        self.ranking_entry.pack()
        
    def processSearch(self, event = None):
        name = self.name_entry.get().strip().title()
        year = self.year_entry.get().strip()
        sex = self.sex.get()
        if not (name and year):
            messagebox.showerror("Error!", "Entry cannot be empty")
            return
        if not year.isdecimal():
            messagebox.showerror("Error!", "Year must be an integer")
            return
        year = int(year)
        if not 1880 <= year <= 2023:
            messagebox.showerror("Error!", "Year must be within 1880 - 2023")
            return
        self.ranking_entry.delete(0, tk.END)
        self.ranking_entry.insert(0, "Searching...")
        self.fetchNames(year)
        self.search(year, name, sex)
        
    def fetchNames(self, year):
        if year in NAMES:
            return
        url = f"{BASE_URL}/{year}"
        name_data = {}
        try:
            with request.urlopen(url) as response:
                for line in response:
                    name, sex, count, rank = line.decode("utf-8").strip().split(',')
                    name_data[(name, sex)] = (int(count), int(rank))
            NAMES[year] = name_data
        except Exception as e:
            messagebox.showerror("Error!", f"Failed to fetch names: {e}")
        
    def search(self, year, name, sex):
        sex_word = "female" if sex == 'F' else "male"
        if (name, sex) not in NAMES[year]:
            self.ranking_entry.delete(0, tk.END)
            messagebox.showwarning("Unfortunate!", "Name not found")
            return
        count, rank = NAMES[year][(name, sex)]
        self.ranking_entry.delete(0, tk.END)
        self.ranking_entry.insert(0, f"{rank}")

    def loadCache(self):
        try:
            with open(CACHE_FILENAME, 'r') as file:
                for line in file:
                    year, name, sex, count, rank = line.strip().split(',')
                    year = int(year)
                    if year not in NAMES:
                        NAMES[year] = {}
                    NAMES[year][(name, sex)] = (int(count), int(rank))
        except Exception as e:
            #messagebox.showerror("Error!", f"Failed to load cache: {e}")

    def saveCache(self, event = None):
        if self.is_caching:
            return
        self.is_caching = True
        with open(CACHE_FILENAME, 'w') as file:
            for year in NAMES:
                for entry in NAMES[year]:
                    name, sex = entry
                    count, ranking = NAMES[year][entry]
                    line = f"{year},{name},{sex},{count},{ranking}\n"
                    file.write(line)

    def run(self):
        self.root.mainloop()
