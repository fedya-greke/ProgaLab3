import tkinter as tk
from tkinter import messagebox, ttk
import random
import traceback

class MemoryTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренажер памяти: Запомни число")
        # Возможность изменения размера
        self.root.resizable(width=True, height=True)

        # Переменные для хранения данных игры
        self.main_number = ""
        self.current_level = 1
        self.score = 0
        self.is_test_active = False

        self.create_menu()
        self.create_widgets()
        self.center_window()
        # Фокус на кнопке начать для запуска по Entr
        self.start_button.focus_set()

        # Глобальная привязка Enter
        root.bind('<Return>', self.enter_logic)

    def enter_logic(self, event):
        """Обработка Enter"""
        focused_widget = self.root.focus_get()
        if self.check_button.cget('state') == 'normal' and self.answer_entry.winfo_ismapped():
            self.check_answer(event)
        # Иначе если активна кнопка Начать
        elif self.start_button.cget('state') == 'normal':
            self.start_round()

    def create_menu(self):
        """Меню сверху слева - меню + настройки справка"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Меню - новая игра + выход
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Меню", menu=file_menu)
        file_menu.add_command(label="Новая игра", command=self.start_new_game)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # Настройки - сброс очков + сложность
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Настройки", menu=settings_menu)
        # Подменю для сложности
        settings_menu.add_command(label="Сбросить очки", command=self.reset_score)
        file_menu.add_separator()
        settings_menu.add_command(label="Сложность", command=self.set_up_difficulty_level)

        # Справка - о проге
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_widgets(self):
        """Основной фрейм для содержимого"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Информационная панель
        info_frame = ttk.LabelFrame(main_frame, text="Статистика", padding="20")
        info_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="we")

        self.level_label = ttk.Label(info_frame, text=f"Уровень: {self.current_level}")
        self.level_label.grid(row=0, column=0, padx=20)

        self.score_label = ttk.Label(info_frame, text=f"Очков: {self.score}")
        self.score_label.grid(row=0, column=1, padx=20)

        # Поле для показа числа
        self.number_display = tk.Label(main_frame, text="Начнём?", font=("Arial", 16), bg="white", relief="solid", width=30, height=3)
        self.number_display.grid(row=1, column=0, columnspan=2, pady=20)

        # Кнопки управления
        self.start_button = ttk.Button(main_frame, text="Начать раунд", command=self.start_round)
        self.start_button.grid(row=2, column=0, pady=5)
        self.start_button.bind('<Return>', lambda e: self.start_round())

        self.check_button = ttk.Button(main_frame, text="Проверить", command=self.check_answer, state="disabled")
        self.check_button.grid(row=2, column=1, pady=5)
        self.check_button.bind('<Return>', lambda e: self.check_answer())

        # Поле для ввода ответа
        self.input_label = ttk.Label(main_frame, text="", font=("Arial", 10))
        self.input_label.grid(row=3, column=0, columnspan=2, pady=(20,5))

        self.answer_entry = ttk.Entry(main_frame, font=("Arial", 24), justify="center")
        self.answer_entry.grid(row=4, column=0, columnspan=2, pady=(0,20))
        self.answer_entry.config(state="disabled")

        # Метка для результата
        self.result_label = ttk.Label(main_frame, text="", font=("Arial", 14))
        self.result_label.grid(row=5, column=0, columnspan=2)

    def center_window(self):
        """Центрируем окно"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def start_new_game(self):
        self.current_level = 1
        self.score = 0
        self.update_stats()
        self.result_label.config(text="Новая игра!")
        self.answer_entry.config(state="normal")
        self.answer_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.number_display.config(text="Начнём новую игру!")
        if self.input_label.winfo_ismapped():  # Если метка видима
            self.input_label.grid_forget()
        if self.answer_entry.winfo_ismapped():  # Если поле ввода видимо
            self.answer_entry.grid_forget()
        self.start_button.config(state="normal")
        self.check_button.config(state="disabled")
        messagebox.showinfo("Новая игра", "Игра сброшена. Начните новый раунд.")

        self.start_button.focus_set()

    def start_round(self):
        """Начинает новый раунд"""
        # Очистка предыдущего результата
        self.result_label.config(text="")
        self.answer_entry.config(state="normal") # для отчистки поля ввода оно должно быть активно
        self.answer_entry.delete(0, tk.END)
        self.start_button.config(state="disabled")
        # Возвращаем текст обратно
        self.input_label.config(text="Введите запомненное число:", font=("Arial", 10))
        self.answer_entry.config(state="normal")
        self.check_button.config(state="normal")
        self.input_label.grid(row=3, column=0, columnspan=2, pady=(20, 5))
        self.answer_entry.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        self.answer_entry.focus()
        # Привязка клавиши Enter к проверке
        self.answer_entry.bind('<Return>', lambda event: self.check_answer())

        # Генерируем число длиной, зависит от уровня - 1 уровень 3 цифры
        if self.current_level <= 5:
            num_length = self.current_level + 2
        else:
            num_length = self.current_level + 1

        # Генератор списка чисел
        self.main_number = ''.join([str(random.randint(0, 9)) for _ in range(num_length)])

        self.number_display.config(text=self.main_number)
        # Число пропадёт через 2 - 3 секунды
        if self.current_level <= 4:
            self.root.after(2000, self.hide_number)
        elif self.current_level <= 6:
            self.root.after(2500, self.hide_number)
        else:
            self.root.after(3000, self.hide_number)

    def hide_number(self):
        self.number_display.config(text="???")

    def check_answer(self, event=None):
        user_answer = self.answer_entry.get()
        # Обработка исключения
        # Если строка пустая или только пробелы - предупреждение
        if not user_answer.strip():
            messagebox.showwarning("Пустой ввод", "Пожалуйста, введите число!")
            self.answer_entry.focus()  # Возвращаем фокус на поле ввода
            return
        try:
            # В строке не только цифры - ошибка
            int(user_answer)
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, вводите только цифры!")
            return

        # Проверяем ответ
        if user_answer == self.main_number:
            self.result_label.config(text="Правильно! +10 очков", foreground="green")
            self.score += 10
            self.current_level += 1
        else:
            self.result_label.config(text=f"Неверно! Было: {self.main_number}", foreground="red")
            self.score = max(0, self.score - 5)  # Штраф, но не ниже нуля

        # Отдельно обновляем уровень и очки
        self.update_stats()

        # Подготовка к следующему раунду
        self.start_button.config(state="normal")
        self.check_button.config(state="disabled")
        self.answer_entry.config(state="disabled")
        self.answer_entry.delete(0, tk.END)
        self.input_label.config(text="Введите запомненное число:", font=("Arial", 10))

        self.start_button.focus_set()

    def update_stats(self):
        self.level_label.config(text=f"Уровень: {self.current_level}")
        self.score_label.config(text=f"Очков: {self.score}")

    def reset_score(self):
        self.score = 0
        self.update_stats()
        self.result_label.config(text="Очки сброшены")

    def set_up_difficulty_level(self):
        pass

    def show_about(self):
        messagebox.showinfo("О программе", "Тренажер для памяти. Разработал Греке Фёдор, группа ИДБ-24-14.")

# Точка входа
if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryTestApp(root)

    # Глобальная обработка исключений
    def handle_exception(exc_type, exc_value, exc_traceback):
        messagebox.showerror("Критическая ошибка",
                             f"Произошла непредвиденная ошибка:\n{exc_value}\n\nПрограмма будет закрыта.")
        # Записываем ошибку в лог-файл
        with open("error_log.txt", "w") as f:
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        root.quit()

    # Устанавливаем обработчик
    root.report_callback_exception = handle_exception

    try:
        root.mainloop()
    except Exception as e:
        handle_exception(type(e), e, e.__traceback__)