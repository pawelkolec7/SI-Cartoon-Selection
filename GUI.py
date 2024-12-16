import tkinter as tk
import clips
import configparser


class GiftGuideApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gift Guide")
        self.master.config(bg="#E1E8ED")

        # Ustawienie rozmiaru okna
        window_width, window_height = 800, 600
        screen_width, screen_height = master.winfo_screenwidth(), master.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        master.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
        master.resizable(False, False)

        # Inicjalizacja środowiska CLIPS i konfiguracji
        self.environment = clips.Environment()
        self.environment.load('construct.clp')

        self.config = configparser.ConfigParser()
        self.config.read('properties.properties')

        # Inicjalizacja interfejsu
        self.question_label = None
        self.answer_buttons = []
        self.answer_frame = None
        self.restart_button = None

        # Rozpoczęcie procesu
        self.restart()

    def display_question(self):
        """Wyświetla bieżące pytanie i możliwe odpowiedzi."""
        # Wyczyść wszystkie obecne widżety w oknie
        for widget in self.master.winfo_children():
            widget.destroy()

        # Stwórz główną ramkę aplikacji
        main_frame = tk.Frame(self.master, bg="#E1E8ED")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Gradientowe tło
        canvas = tk.Canvas(main_frame, bg="#FFFFFF", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Panel pytania
        question_frame = tk.Frame(canvas, bg="#FFFFFF", bd=2, relief="groove")
        question_frame.pack(pady=(30, 10), padx=20, fill="x")

        self.question_label = tk.Label(
            question_frame, wraplength=600, font=("Segoe UI", 18, "bold"),
            bg="#fcfcfc", fg="#333333", anchor="center"
        )
        self.question_label.pack(pady=20)

        # Panel odpowiedzi
        self.answer_frame = tk.Frame(canvas, bg="#FFFFFF")
        self.answer_frame.pack(pady=40)

        # Przyciski Restart
        self.restart_button = tk.Button(
            canvas, text="Restart", command=self.restart,
            font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="#FFFFFF",
            activebackground="#45A049", activeforeground="#FFFFFF",
            relief="groove", bd=2, padx=15, pady=8
        )
        self.restart_button.pack(side="bottom", pady=20)

        # Pobierz pytanie i dostępne odpowiedzi
        question, answers = self.extract_question_and_answers()
        self.update_question_and_answers(question, answers)

    def extract_question_and_answers(self):
        """Odczytuje pytanie i odpowiedzi z CLIPS."""
        question = ""
        answers = []
        for fact in self.environment.facts():
            fact_str = str(fact)
            fact_parts = fact_str.split(")")
            for part in fact_parts:
                if "display" in part:  # Znaleziono pytanie
                    question = part.split("display")[1].strip().strip(" ()\"")
                elif "valid-answers" in part:  # Znaleziono odpowiedzi
                    answers = part.split("valid-answers")[1].strip().strip(" ()\"").split(" ")
        return question, answers

    def update_question_and_answers(self, question, answers):
        """Uaktualnia widok pytania i listę dostępnych odpowiedzi."""
        # Pobierz tekst pytania i odpowiedzi z pliku konfiguracyjnego
        question_text = self.config['DEFAULT'].get(question, "Nieznane pytanie")
        valid_answers = [self.config['DEFAULT'].get(answer, answer) for answer in answers]

        # Wyświetl pytanie
        self.question_label.config(text=question_text)

        # Dodaj przyciski odpowiedzi
        for answer, label in zip(answers, valid_answers):
            button = tk.Button(
                self.answer_frame, text=label,
                command=lambda a=answer: self.submit_answer(a),
                font=("Segoe UI", 14), bg="#03A9F4", fg="#FFFFFF",
                activebackground="#0288D1", activeforeground="#FFFFFF",
                relief="groove", bd=2, padx=25, pady=10, wraplength=500
            )
            button.pack(side="top", pady=10, padx=20)

    def submit_answer(self, answer):
        """Wysyła wybraną odpowiedź do środowiska CLIPS i przetwarza następne pytanie."""
        # Znajdź bieżący fakt (nazwa faktu)
        fact_name = ""
        for fact in self.environment.facts():
            fact_str = str(fact)
            fact_parts = fact_str.split(")")
            for part in fact_parts:
                if "fact-name" in part:
                    fact_name = part.split("fact-name")[1].strip().strip(" ()\"")

        # Prześlij odpowiedź
        if fact_name:
            self.environment.assert_string(f"({fact_name} {answer})")
            print(f"Fact asserted: ({fact_name} {answer})")

        # Uruchom CLIPS dla nowego stanu
        self.environment.run()

        # Sprawdź, czy zakończono proces
        if self.is_final_decision_reached():
            self.display_final_message()
            self.restart()
        else:
            self.display_question()

    def is_final_decision_reached(self):
        """Sprawdza, czy osiągnięto ostateczną decyzję."""
        return any("state final" in str(fact) for fact in self.environment.facts())

    def display_final_message(self):
        """Wyświetla końcowe pytanie lub odpowiedź."""
        final_message = ""
        for fact in self.environment.facts():
            fact_str = str(fact)
            fact_parts = fact_str.split(")")
            for part in fact_parts:
                if "display" in part:
                    final_message = part.split("display")[1].strip().strip(" ()\"")
        final_message = self.config['DEFAULT'].get(final_message, "Nieznana odpowiedź")
        self.show_message("Final Decision", final_message)

    def show_message(self, title, message):
        """Wyświetla okienko z wiadomością."""
        top = tk.Toplevel(self.master)
        top.geometry(f"+{self.master.winfo_screenwidth() // 2 - 200}+{self.master.winfo_screenheight() // 2 - 100}")
        top.title(title)
        top.config(bg="#fcfcfc", padx=10, pady=10)

        label = tk.Label(top, text=message, font=("Segoe UI", 14), padx=20, pady=20, bg="#fcfcfc",
                         fg="#333333", wraplength=400)
        label.pack(pady=(10, 10))

        button = tk.Button(
            top, text="OK", command=top.destroy,
            font=("Segoe UI", 12), bg="#0288D1", fg="#FFFFFF",
            activebackground="#02689D", relief="groove", bd=1
        )
        button.pack(pady=(10, 20))

        top.grab_set()
        top.focus_set()
        top.wait_window()

    def restart(self):
        """Restartuje aplikację."""
        self.environment.reset()
        self.environment.run()
        self.display_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = GiftGuideApp(root)
    root.mainloop()