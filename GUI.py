import tkinter as tk
from tkinter import ttk, messagebox
from solver import solve_erlang_b, solve_engset

class TeleTrafficApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator Teorii Ruchu")
        self.geometry("380x350")
        self.resizable(False, False)

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tab_erlang = ttk.Frame(notebook)
        self.tab_engset = ttk.Frame(notebook)

        notebook.add(self.tab_erlang, text='Erlang B')
        notebook.add(self.tab_engset, text='Engset')

        self.setup_erlang_ui()
        self.setup_engset_ui()

    def parse_input(self, value_str, type_func):
        if not value_str.strip():
            return None
        try:
            return type_func(value_str)
        except ValueError:
            raise ValueError(f"Nieprawidłowy format danych: {value_str}")

    # erlang b
    def setup_erlang_ui(self):
        ttk.Label(self.tab_erlang, text="Zostaw dokładnie jedno pole puste do obliczenia.",
                  font=("Arial", 9, "italic")).grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.e_A = tk.StringVar()
        self.e_V = tk.StringVar()
        self.e_PB = tk.StringVar()

        self.create_input_row(self.tab_erlang, "Ruch całkowity (A) [Erl]:", self.e_A, 1)
        self.create_input_row(self.tab_erlang, "Liczba kanałów (V):", self.e_V, 2)
        self.create_input_row(self.tab_erlang, "Prawd. blokady (PB) [0-1]:", self.e_PB, 3)

        btn_calc = ttk.Button(self.tab_erlang, text="Oblicz", command=self.calc_erlang)
        btn_calc.grid(row=4, column=0, columnspan=2, pady=20)

    def calc_erlang(self):
        try:
            A = self.parse_input(self.e_A.get(), float)
            V = self.parse_input(self.e_V.get(), int)
            PB = self.parse_input(self.e_PB.get(), float)

            if [A, V, PB].count(None) != 1:
                messagebox.showwarning("Błąd", "Zostaw DOKŁADNIE JEDNO pole puste!")
                return

            result = solve_erlang_b(A=A, V=V, PB=PB)

            if A is None: self.e_A.set(f"{result:.4f}")
            elif V is None: self.e_V.set(str(result))
            elif PB is None: self.e_PB.set(f"{result:.6f}")

        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    # engset
    def setup_engset_ui(self):
        ttk.Label(self.tab_engset, text="Zostaw dokładnie jedno pole puste do obliczenia.",
                  font=("Arial", 9, "italic")).grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.en_S = tk.StringVar()
        self.en_V = tk.StringVar()
        self.en_alpha = tk.StringVar()
        self.en_PB = tk.StringVar()


        self.create_input_row(self.tab_engset, "Liczba źródeł (S):", self.en_S, 1)
        self.create_input_row(self.tab_engset, "Liczba kanałów (V):", self.en_V, 2)
        self.create_input_row(self.tab_engset, "Ruch źródła (alpha) [0-1]:", self.en_alpha, 3)
        self.create_input_row(self.tab_engset, "Prawd. blokady (PB) [0-1]:", self.en_PB, 4)


        btn_calc = ttk.Button(self.tab_engset, text="Oblicz", command=self.calc_engset)
        btn_calc.grid(row=5, column=0, columnspan=2, pady=20)

    def calc_engset(self):
        try:
            S = self.parse_input(self.en_S.get(), int)
            V = self.parse_input(self.en_V.get(), int)
            alpha = self.parse_input(self.en_alpha.get(), float)
            PB = self.parse_input(self.en_PB.get(), float)


            if [S, V, alpha, PB].count(None) != 1:
                messagebox.showwarning("Błąd", "Zostaw DOKŁADNIE JEDNO pole puste!")
                return


            result = solve_engset(S=S, V=V, alpha=alpha, PB=PB)

            if S is None: self.en_S.set(str(result))
            elif V is None: self.en_V.set(str(result))
            elif alpha is None: self.en_alpha.set(f"{result:.4f}")
            elif PB is None: self.en_PB.set(f"{result:.6f}")

        except Exception as e:
            messagebox.showerror("Błąd obliczeń", str(e))

    def create_input_row(self, parent, label_text, text_var, row_idx):
        lbl = ttk.Label(parent, text=label_text)
        lbl.grid(row=row_idx, column=0, sticky=tk.W, padx=15, pady=5)
        entry = ttk.Entry(parent, textvariable=text_var, width=15)
        entry.grid(row=row_idx, column=1, sticky=tk.E, padx=15, pady=5)


if __name__ == "__main__":
    app = TeleTrafficApp()
    app.mainloop()