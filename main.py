import configparser
import os
import sys
import datetime
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox

def get_game_id():
    while True:
        root = tk.Tk()
        root.withdraw()  # hide the root window
        game_id = simpledialog.askstring("Game ID", "Enter the game ID (CODEX only works):")
        root.destroy()  # destroy the root window

        if game_id is None:
            sys.exit(0)  # exit the program without showing error message

        achievements_file = rf'C:\Users\Public\Documents\Steam\CODEX\{game_id}\achievements.ini'

        if not os.path.isfile(achievements_file):
            messagebox.showerror("Error", "Invalid game ID")
            continue

        return game_id

root = tk.Tk()
root.withdraw()  # hide the root window

while True:
    game_id = get_game_id()

    if game_id:
        achievements_file = rf'C:\Users\Public\Documents\Steam\CODEX\{game_id}\achievements.ini'

        config = configparser.ConfigParser()
        config.read(achievements_file)

        achievements = []
        for section in config.sections():
            if section != 'SteamAchievements':
                achievement = {'name': section.replace('_', ' ').title()}  # Modify the name here
                for key, value in config[section].items():
                    if key == 'UnlockTime':
                        value = datetime.datetime.fromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        value = config[section][key]
                    achievement[key.lower()] = value

                achievements.append(achievement)


        def sort_by_name():
            tree.delete(*tree.get_children())
            for achievement in sorted(achievements, key=lambda x: x['name']):
                unlock_time = datetime.datetime.fromtimestamp(int(achievement['unlocktime'])).strftime('%Y-%m-%d %H:%M:%S')
                tree.insert('', 'end', values=(
                achievement['name'], achievement['achieved'], achievement['curprogress'], achievement['maxprogress'],
                unlock_time))


        def sort_by_time():
            tree.delete(*tree.get_children())
            for achievement in sorted(achievements, key=lambda x: x['unlocktime']):
                unlock_time = datetime.datetime.fromtimestamp(int(achievement['unlocktime'])).strftime('%Y-%m-%d %H:%M:%S')
                tree.insert('', 'end', values=(
                achievement['name'], achievement['achieved'], achievement['curprogress'], achievement['maxprogress'],
                unlock_time))


        root.deiconify()  # show the root window
        root.title("Achievements")
        root.wm_attributes("-topmost", True)

        tree = ttk.Treeview(root, columns=('Name', 'Achieved', 'CurProgress', 'MaxProgress', 'UnlockTime'), show='headings')
        tree.column('Name', width=200, anchor='w')
        tree.column('Achieved', width=100, anchor='center')
        tree.column('CurProgress', width=100, anchor='center')
        tree.column('MaxProgress', width=100, anchor='center')
        tree.column('UnlockTime', width=200, anchor='center')
        tree.heading('Name', text='Name', command=sort_by_name)
        tree.heading('Achieved', text='Achieved')
        tree.heading('CurProgress', text='CurProgress')
        tree.heading('MaxProgress', text='MaxProgress')
        tree.heading('UnlockTime', text='Unlock Time', command=sort_by_time)

        for achievement in achievements:
            unlock_time = datetime.datetime.fromtimestamp(int(achievement['unlocktime'])).strftime('%Y-%m-%d %H:%M:%S')
            tree.insert('', 'end', values=(
            achievement['name'], achievement['achieved'], achievement['curprogress'], achievement['maxprogress'],
            unlock_time))

        tree.pack(fill='both', expand=True)

        root.mainloop()

    else:
        messagebox.showerror("Error", "Invalid game ID")