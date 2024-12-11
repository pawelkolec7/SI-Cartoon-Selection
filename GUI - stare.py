import tkinter as tk
import clips
import configparser

environment = clips.Environment()
environment.load('construct.clp')

config = configparser.ConfigParser()
config.read('properties.properties')


def display_question():
    global question_label, answer_buttons, environment, answer_frame, restart_button

    # Czyszczenie ekranu
    for widget in root.winfo_children():
        widget.destroy()

    # Główna ramka
    main_frame = tk.Frame(root, bg="#E1E8ED")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Gradientowe tło
    canvas = tk.Canvas(main_frame, bg="#FFFFFF", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Pytanie (na górze z obramowaniem)
    question_frame = tk.Frame(canvas, bg="#FFFFFF", bd=2, relief="groove")
    question_frame.pack(pady=(30, 10), padx=20, fill="x")

    question_label = tk.Label(
        question_frame, wraplength=600, font=("Segoe UI", 18, "bold"),
        bg="#fcfcfc", fg="#333333", anchor="center"
    )
    question_label.pack(pady=20)

    # Ramka z przyciskami (odpowiedzi)
    answer_frame = tk.Frame(canvas, bg="#FFFFFF")
    answer_frame.pack(pady=40)

    # Restart Button (na dole)
    restart_button = tk.Button(
        canvas, text="Restart", command=restart,
        font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="#FFFFFF",
        activebackground="#45A049", activeforeground="#FFFFFF",
        relief="groove", bd=2, padx=15, pady=8
    )
    restart_button.pack(side="bottom", pady=20)

    # Odczytaj pytanie i odpowiedzi ze środowiska
    for fact in environment.facts():
        fact_str = str(fact)
        fact_parts = fact_str.split(")")
        question = ""
        answers = []
        for part in fact_parts:
            if "display" in part:
                question = part.split("display")[1].strip().strip(" ()\"")
            elif "valid-answers" in part:
                answers = part.split("valid-answers")[1].strip().strip(" ()\"").split(" ")

    # Pobierz tekst pytania oraz odpowiedzi z pliku konfiguracyjnego
    question_text = config['DEFAULT'].get(question, "Nieznane pytanie")
    valid_answers = [config['DEFAULT'].get(answer, answer) for answer in answers]

    # Wyświetl pytanie
    if question_text:
        question_label.config(text=question_text)

    # Tworzenie przycisków odpowiedzi z nowoczesnym designem
    if valid_answers:
        for answer, label in zip(answers, valid_answers):
            button = tk.Button(
                answer_frame, text=label,
                command=lambda a=answer: submit_answer(a),
                font=("Segoe UI", 14), bg="#03A9F4", fg="#FFFFFF",
                activebackground="#0288D1", activeforeground="#FFFFFF",
                relief="groove", bd=2, padx=25, pady=10, wraplength=500
            )
            button.pack(side="top", pady=10, padx=20)


def submit_answer(answer):
    global environment

    # Znajdź bieżącą nazwę faktu i przypisz odpowiedź
    fact_name = ""
    for fact in environment.facts():
        fact_str = str(fact)
        fact_parts = fact_str.split(")")
        for part in fact_parts:
            if "fact-name" in part:
                fact_name = part.split("fact-name")[1].strip().strip(" ()\"")

    if fact_name:
        environment.assert_string(f"({fact_name} {answer})")
        print(f"Fact asserted: ({fact_name} {answer})")

    # Wykonaj środowisko CLIPS
    environment.run()
    if any("state final" in str(fact) for fact in environment.facts()):
        # Wyświetl wiadomość końcową
        final_message = ""
        for fact in environment.facts():
            fact_str = str(fact)
            fact_parts = fact_str.split(")")
            for part in fact_parts:
                if "display" in part:
                    final_message = part.split("display")[1].strip().strip(" ()\"")
        final_message = config['DEFAULT'].get(final_message, "Nieznana odpowiedź")
        show_custom_message("Final Decision", final_message)
        restart()
    else:
        display_question()


def show_custom_message(title, message):
    top = tk.Toplevel(root)
    top.title(title)
    top.config(bg="#fcfcfc", padx=10, pady=10)

    label = tk.Label(top, text=message, font=("Segoe UI", 14), padx=20, pady=20, bg="#fcfcfc", wraplength=400,
                     fg="#333333")
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


def restart():
    global environment
    environment.reset()
    environment.run()
    display_question()


# Główne okno aplikacji
root = tk.Tk()
root.title("Gift Guide")
root.config(bg="#E1E8ED")

# Rozmiary okna
window_width, window_height = 800, 600
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_left = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
root.resizable(False, False)

# Rozpoczęcie aplikacji
environment.reset()
environment.run()
display_question()

root.mainloop()
