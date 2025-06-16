import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os


class AchievementDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Дневник самоконтроля и личных достижений")
        self.root.geometry("600x700")

        #создаем файл для хранения данных
        self.data_file = "achievements.json"
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump([], f)

        #загружаем данные
        self.load_data()

        #создаем интерфейс
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
        #основные вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        #вкладка для новой записи
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Добавить запись")
        self.create_add_tab()

        #вкладка для просмотра записей
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_tab, text="Просмотр записей")
        self.create_view_tab()

        #вкладка статистики
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Статистика")
        self.create_stats_tab()

    def create_add_tab(self):
        #дата
        ttk.Label(self.add_tab, text="Дата:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.date_entry = ttk.Entry(self.add_tab)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))

        #категория
        ttk.Label(self.add_tab, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.add_tab, textvariable=self.category_var,
                                              values=["Здоровье", "Работа", "Учеба", "Спорт", "Личное развитие",
                                                      "Другое"])
        self.category_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.category_combobox.current(0)

        #оценка дня
        ttk.Label(self.add_tab, text="Оценка дня (1-10):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.rating_var = tk.IntVar(value=5)
        self.rating_scale = ttk.Scale(self.add_tab, from_=1, to=10, variable=self.rating_var,
                                      command=lambda v: self.rating_var.set(round(float(v))))
        self.rating_scale.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.rating_label = ttk.Label(self.add_tab, textvariable=self.rating_var)
        self.rating_label.grid(row=2, column=2, padx=5, pady=5)

        #достижения
        ttk.Label(self.add_tab, text="Достижения:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.NW)
        self.achievements_text = tk.Text(self.add_tab, width=50, height=10)
        self.achievements_text.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        #проблемы/затруднения
        ttk.Label(self.add_tab, text="Проблемы/затруднения:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.NW)
        self.problems_text = tk.Text(self.add_tab, width=50, height=10)
        self.problems_text.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        #планы на завтра
        ttk.Label(self.add_tab, text="Планы на завтра:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.NW)
        self.plans_text = tk.Text(self.add_tab, width=50, height=10)
        self.plans_text.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        #кнопка сохранения
        self.save_button = ttk.Button(self.add_tab, text="Сохранить запись", command=self.save_entry)
        self.save_button.grid(row=6, column=1, padx=5, pady=10, sticky=tk.E)

    def save_entry(self):
        entry = {
            "date": self.date_entry.get(),
            "category": self.category_var.get(),
            "rating": self.rating_var.get(),
            "achievements": self.achievements_text.get("1.0", tk.END).strip(),
            "problems": self.problems_text.get("1.0", tk.END).strip(),
            "plans": self.plans_text.get("1.0", tk.END).strip()
        }

        self.entries.append(entry)
        self.save_data()

        #очищаем поля после сохранения
        self.achievements_text.delete("1.0", tk.END)
        self.problems_text.delete("1.0", tk.END)
        self.plans_text.delete("1.0", tk.END)

        messagebox.showinfo("Успех", "Запись успешно сохранена!")

        #обновляем список записей
        self.update_entries_list()
        self.update_stats()

    def create_view_tab(self):
        #список записей
        self.entries_frame = ttk.Frame(self.view_tab)
        self.entries_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        #дерево для отображения записей
        self.tree = ttk.Treeview(self.entries_frame, columns=("date", "category", "rating"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("category", text="Категория")
        self.tree.heading("rating", text="Оценка")
        self.tree.column("date", width=150)
        self.tree.column("category", width=100)
        self.tree.column("rating", width=50)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #полоса прокрутки
        scrollbar = ttk.Scrollbar(self.entries_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        #область для просмотра деталей записи
        self.details_frame = ttk.LabelFrame(self.view_tab, text="Детали записи")
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.details_text = tk.Text(self.details_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        #кнопка удаления записи
        self.delete_button = ttk.Button(self.view_tab, text="Удалить запись", command=self.delete_entry)
        self.delete_button.pack(pady=5)

        #привязываем событие выбора записи
        self.tree.bind("<<TreeviewSelect>>", self.show_entry_details)

        #обновляем список записей
        self.update_entries_list()

    def update_entries_list(self):
        #очищаем текущий список
        for item in self.tree.get_children():
            self.tree.delete(item)

        #сортируем записи по дате (новые сверху)
        sorted_entries = sorted(self.entries, key=lambda x: x["date"], reverse=True)

        #добавляем записи в дерево
        for entry in sorted_entries:
            self.tree.insert("", tk.END, values=(entry["date"], entry["category"], entry["rating"]))

    def show_entry_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        date = item["values"][0]

        #находим запись с соответствующей датой
        for entry in self.entries:
            if entry["date"] == date:
                self.details_text.config(state=tk.NORMAL)
                self.details_text.delete("1.0", tk.END)

                details = f"Дата: {entry['date']}\n"
                details += f"Категория: {entry['category']}\n"
                details += f"Оценка дня: {entry['rating']}/10\n\n"
                details += "Достижения:\n" + entry['achievements'] + "\n\n"
                details += "Проблемы/затруднения:\n" + entry['problems'] + "\n\n"
                details += "Планы на завтра:\n" + entry['plans']

                self.details_text.insert("1.0", details)
                self.details_text.config(state=tk.DISABLED)
                break

    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите запись для удаления")
            return

        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту запись?"):
            return

        item = self.tree.item(selected_item)
        date = item["values"][0]

        #удаляем запись из списка
        self.entries = [entry for entry in self.entries if entry["date"] != date]
        self.save_data()

        #обновляем интерфейс
        self.update_entries_list()
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)
        self.details_text.config(state=tk.DISABLED)
        self.update_stats()

        messagebox.showinfo("Успех", "Запись успешно удалена")

    def create_stats_tab(self):
        #график оценок
        self.ratings_frame = ttk.LabelFrame(self.stats_tab, text="Оценки дней")
        self.ratings_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.ratings_text = tk.Text(self.ratings_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.ratings_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        #статистика по категориям
        self.categories_frame = ttk.LabelFrame(self.stats_tab, text="Статистика по категориям")
        self.categories_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.categories_text = tk.Text(self.categories_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.categories_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        #обновляем статистику
        self.update_stats()

    def update_stats(self):
        if not self.entries:
            self.ratings_text.config(state=tk.NORMAL)
            self.ratings_text.delete("1.0", tk.END)
            self.ratings_text.insert("1.0", "Нет данных для отображения")
            self.ratings_text.config(state=tk.DISABLED)

            self.categories_text.config(state=tk.NORMAL)
            self.categories_text.delete("1.0", tk.END)
            self.categories_text.insert("1.0", "Нет данных для отображения")
            self.categories_text.config(state=tk.DISABLED)
            return

        #статистика по оценкам
        ratings = [entry["rating"] for entry in self.entries]
        avg_rating = sum(ratings) / len(ratings)
        min_rating = min(ratings)
        max_rating = max(ratings)

        ratings_info = f"Всего записей: {len(self.entries)}\n"
        ratings_info += f"Средняя оценка: {avg_rating:.1f}/10\n"
        ratings_info += f"Минимальная оценка: {min_rating}/10\n"
        ratings_info += f"Максимальная оценка: {max_rating}/10\n\n"

        #гистограмма оценок
        ratings_info += "Распределение оценок:\n"
        rating_counts = {i: 0 for i in range(1, 11)}
        for rating in ratings:
            rating_counts[rating] += 1

        max_count = max(rating_counts.values())
        for rating in range(10, 0, -1):
            count = rating_counts[rating]
            bar = "■" * int(count / max_count * 30) if max_count > 0 else ""
            ratings_info += f"{rating:2d}: {bar} {count}\n"

        self.ratings_text.config(state=tk.NORMAL)
        self.ratings_text.delete("1.0", tk.END)
        self.ratings_text.insert("1.0", ratings_info)
        self.ratings_text.config(state=tk.DISABLED)

        #статистика по категориям
        categories = {}
        for entry in self.entries:
            cat = entry["category"]
            if cat not in categories:
                categories[cat] = {"count": 0, "total_rating": 0}
            categories[cat]["count"] += 1
            categories[cat]["total_rating"] += entry["rating"]

        categories_info = "Статистика по категориям:\n\n"
        for cat, data in categories.items():
            avg = data["total_rating"] / data["count"]
            categories_info += f"{cat}:\n"
            categories_info += f"  Количество записей: {data['count']}\n"
            categories_info += f"  Средняя оценка: {avg:.1f}/10\n\n"

        self.categories_text.config(state=tk.NORMAL)
        self.categories_text.delete("1.0", tk.END)
        self.categories_text.insert("1.0", categories_info)
        self.categories_text.config(state=tk.DISABLED)

#все вроде))

if __name__ == "__main__":
    root = tk.Tk()
    app = AchievementDiary(root)
    root.mainloop()