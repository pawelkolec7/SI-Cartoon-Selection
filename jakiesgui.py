import tkinter as tk
from tkinter import messagebox
from typing import List
import clips

cid = 0
env = clips.Environment()


def polar_question(question: str, fact: str, *answers: List):
    """A simple Yes/No question."""

    def on_next_click():
        for i in answers:
            if var.get() == i:
                env.assert_string(f"({fact} {i})")
                print_c()
        window.destroy()

    window = tk.Tk()
    window.title("Cartoon Finder")
    window.geometry("300x150")

    tk.Label(window, text=question).pack(pady=10)

    var = tk.StringVar(value=" ")

    for answer in answers:
        tk.Radiobutton(window, text=answer, variable=var, value=answer).pack(anchor='w')

    tk.Button(window, text="NEXT", command=on_next_click).pack(pady=10)

    window.mainloop()


def list_result(*results: List[str]):
    def on_reset_click():
        env.reset()
        window.destroy()

    window = tk.Tk()
    window.title("Cartoon Finder")

    tk.Label(window, text="Result of your choices:").pack(pady=10)

    listbox = tk.Listbox(window, height=10, width=50, selectmode=tk.SINGLE)
    for result in results:
        listbox.insert(tk.END, result)
    listbox.pack(pady=10)

    tk.Button(window, text="RESET", command=on_reset_click).pack(pady=10)

    window.mainloop()


def show(text: str):
    def on_start_click():
        window.destroy()

    window = tk.Tk()
    window.title("Cartoon Finder")

    tk.Label(window, text=text).pack(pady=10)
    tk.Button(window, text="Start", command=on_start_click).pack(pady=10)

    window.mainloop()


def print_c():
    for i in env.facts():
        print(i)
    print("------")


def check():
    print("work")


def main():
    env.define_function(polar_question, name='polar-question')
    env.define_function(list_result, name='result')
    env.define_function(show, name="show")
    env.define_function(print_c, name="printc")
    env.define_function(check, name="check")

    env.load("cartoon_rule.clp")
    env.run()


if __name__ == '__main__':
    main()
