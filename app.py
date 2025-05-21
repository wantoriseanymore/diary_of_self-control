import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os


class SimpleDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Дневник достижений")
        self.root.geometry("500x350")
        self.data_file = "diary.json"
        self.load_data()
        self.create_widgets()

    def load_data(self):
        try:
            with open(self.data_file, "r") as f:
                self.entries = json.load(f)
        except:
            self.entries = []

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.entries, f, indent=2)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        #код вкладки добавления
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Новая запись")
        ttk.Label(self.add_tab, text="Дата:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.add_tab)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ttk.Label(self.add_tab, text="Оценка дня (1-10):").grid(row=1, column=0, padx=5, pady=5)
        self.rating_var = tk.IntVar(value=5)
        ttk.Scale(self.add_tab, from_=1, to=10, variable=self.rating_var).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.add_tab, text="Что сделал:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_text = tk.Text(self.add_tab, width=40, height=10)
        self.entry_text.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.add_tab, text="Сохранить", command=self.save_entry).grid(row=3, column=1, pady=10)

        #код вкладки просмотра
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_tab, text="Мои записи")
        self.tree = ttk.Treeview(self.view_tab, columns=("date", "rating"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("rating", text="Оценка")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.details = tk.Text(self.view_tab, state=tk.DISABLED)
        self.details.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Button(self.view_tab, text="Удалить", command=self.delete_entry).pack(pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.show_details)
        self.update_list()

    def save_entry(self):
        entry = {
            "date": self.date_entry.get(),
            "rating": self.rating_var.get(),
            "text": self.entry_text.get("1.0", tk.END).strip()
        }
        self.entries.append(entry)
        self.save_data()
        self.entry_text.delete("1.0", tk.END)
        messagebox.showinfo("Сохранено", "Запись добавлена!")
        self.update_list()

    def update_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for entry in sorted(self.entries, key=lambda x: x["date"], reverse=True):
            self.tree.insert("", tk.END, values=(entry["date"], entry["rating"]))

    def show_details(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected)
        date = item["values"][0]

        for entry in self.entries:
            if entry["date"] == date:
                self.details.config(state=tk.NORMAL)
                self.details.delete("1.0", tk.END)
                self.details.insert("1.0", f"Дата: {entry['date']}\nОценка: {entry['rating']}/10\n\n{entry['text']}")
                self.details.config(state=tk.DISABLED)
                break

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            return
        if messagebox.askyesno("Удалить", "Удалить запись?"):
            date = self.tree.item(selected)["values"][0]
            self.entries = [e for e in self.entries if e["date"] != date]
            self.save_data()
            self.update_list()
            self.details.config(state=tk.NORMAL)
            self.details.delete("1.0", tk.END)
            self.details.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleDiary(root)
    root.mainloop()