import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkButton, CTkLabel, CTkEntry, CTkToplevel
import matplotlib.pyplot as plt
import math

from solver import solve_erlang_b, solve_engset


class TeleTrafficApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator Teorii Ruchu")
        self.geometry("450x420")
        self.resizable(False, False)
        ctk.set_appearance_mode("system")

        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tab_erlang = self.notebook.add("Erlang B")
        self.tab_engset = self.notebook.add("Engset")

        self.setup_erlang_ui()
        self.setup_engset_ui()

        btn_help = ctk.CTkButton(self, text="Pomoc", command=self.show_help, fg_color="transparent", border_width=1,
                                 text_color=("black", "white"))
        btn_help.pack(pady=(0, 10))

    def show_message(self, title, message):
        dialog = CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("350x250")
        dialog.resizable(False, False)

        dialog.transient(self)
        dialog.grab_set()

        x = self.winfo_x() + (self.winfo_width() // 2) - (350 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (250 // 2)
        dialog.geometry(f"+{x}+{y}")

        lbl = CTkLabel(dialog, text=message, wraplength=310, justify="left")
        lbl.pack(padx=20, pady=20, expand=True, fill="both")

        btn = CTkButton(dialog, text="OK", command=dialog.destroy, width=100)
        btn.pack(pady=(0, 20))

    def parse_input(self, value_str, type_func):
        value_str = value_str.strip().replace(',', '.')
        if not value_str or value_str.lower() == "wykres":
            return None

        # parsowanie dla przedziałów
        is_range = False
        parts = []

        if '-' in value_str and 'e-' not in value_str.lower():
            parts = value_str.split('-')
        else:
            for sep in [':', ';']:
                if sep in value_str:
                    parts = value_str.split(sep)
                    break

        if len(parts) == 2:
            try:
                start = type_func(parts[0].strip())
                end = type_func(parts[1].strip())
                if start > end:
                    start, end = end, start
                return ("RANGE", start, end, type_func)
            except ValueError:
                pass  # W przypadku błędu przejdź do standardowego parsowania

        try:
            return type_func(value_str)
        except ValueError:
            raise ValueError(f"Nieprawidłowy format danych: {value_str}")

    def generate_range_values(self, start, end, type_func):
        if type_func == int:
            return list(range(int(start), int(end) + 1))
        else:
            steps = 100
            return [start + i * (end - start) / steps for i in range(steps + 1)]

    # ================= ERLANG B =================
    def setup_erlang_ui(self):
        self.tab_erlang.grid_columnconfigure(0, weight=1)
        self.tab_erlang.grid_columnconfigure(1, weight=1)

        info_text = "Zostaw dokładnie jedno pole puste.\nAby narysować wykres, w jednym polu wpisz przedział (np. 1-10)."
        CTkLabel(self.tab_erlang, text=info_text, font=("Arial", 11, "italic")).grid(row=0, column=0, columnspan=2,
                                                                                     pady=10, padx=10)

        self.e_A = ctk.StringVar()
        self.e_V = ctk.StringVar()
        self.e_PB = ctk.StringVar()

        self.create_input_row(self.tab_erlang, "Ruch całkowity (A) [Erl]:", self.e_A, 1)
        self.create_input_row(self.tab_erlang, "Liczba kanałów (V):", self.e_V, 2)
        self.create_input_row(self.tab_erlang, "Prawd. blokady (PB) [0-1]:", self.e_PB, 3)

        btn_calc = CTkButton(self.tab_erlang, text="Oblicz / Rysuj", command=self.calc_erlang)
        btn_calc.grid(row=4, column=0, columnspan=2, pady=20)

    def calc_erlang(self):
        try:
            A = self.parse_input(self.e_A.get(), float)
            V = self.parse_input(self.e_V.get(), int)
            PB = self.parse_input(self.e_PB.get(), float)

            inputs = {'A': A, 'V': V, 'PB': PB}

            empty_vars = [k for k, v in inputs.items() if v is None]
            if len(empty_vars) != 1:
                self.show_message("BŁĄD", "Zostaw DOKŁADNIE JEDNO pole puste!")
                return
            target_var = empty_vars[0]

            # przedziały
            range_vars = [k for k, v in inputs.items() if isinstance(v, tuple) and v[0] == "RANGE"]
            if len(range_vars) > 1:
                self.show_message("BŁĄD", "Możesz podać maksymalnie jeden przedział!")
                return

            # wykres
            if len(range_vars) == 1:
                indep_var = range_vars[0]
                _, start, end, t_func = inputs[indep_var]
                x_vals = self.generate_range_values(start, end, t_func)
                y_vals = []

                for x in x_vals:
                    kwargs = {k: (x if k == indep_var else v) for k, v in inputs.items()}
                    kwargs[target_var] = None
                    y_vals.append(solve_erlang_b(**kwargs))

                plt.figure(figsize=(7, 5))

                # skala logarytmiczna dla PB
                if target_var == 'PB':
                    plt.yscale('log')

                if target_var == 'V':
                    plt.step(x_vals, y_vals, where='post', color='#1f77b4', linewidth=2)
                else:
                    plt.plot(x_vals, y_vals, marker='o' if t_func == int else None, linestyle='-', color='#1f77b4')

                fixed_params = [f"{k}={v}" for k, v in inputs.items() if k != target_var and k != indep_var]
                fixed_str = ", ".join(fixed_params)

                plt.title(f"Zależność {target_var} od {indep_var} (Erlang B) dla: {fixed_str}")
                plt.xlabel(f"Wartość {indep_var}")
                plt.ylabel(f"Szukane {target_var}")
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()
                plt.show()

                getattr(self, f"e_{target_var}").set("Wykres")

            # jedna wartość
            else:
                result = solve_erlang_b(A=A, V=V, PB=PB)
                if target_var == 'A':
                    self.e_A.set(f"{result:.4f}")
                elif target_var == 'V':
                    self.e_V.set(str(result))
                elif target_var == 'PB':
                    self.e_PB.set(f"{result:.6f}")

        except Exception as e:
            self.show_message("BŁĄD", str(e))

    # ================= ENGSET =================
    def setup_engset_ui(self):
        self.tab_engset.grid_columnconfigure(0, weight=1)
        self.tab_engset.grid_columnconfigure(1, weight=1)

        info_text = "Zostaw dokładnie jedno pole puste.\nAby narysować wykres, w jednym polu wpisz przedział (np. 1-10)."
        CTkLabel(self.tab_engset, text=info_text, font=("Arial", 11, "italic")).grid(row=0, column=0, columnspan=2,
                                                                                     pady=10, padx=10)

        self.en_S = ctk.StringVar()
        self.en_V = ctk.StringVar()
        self.en_alpha = ctk.StringVar()
        self.en_PB = ctk.StringVar()

        self.create_input_row(self.tab_engset, "Liczba źródeł (S):", self.en_S, 1)
        self.create_input_row(self.tab_engset, "Liczba kanałów (V):", self.en_V, 2)
        self.create_input_row(self.tab_engset, "Ruch źródła (alpha) [0-1]:", self.en_alpha, 3)
        self.create_input_row(self.tab_engset, "Prawd. blokady (PB) [0-1]:", self.en_PB, 4)

        btn_calc = CTkButton(self.tab_engset, text="Oblicz / Rysuj", command=self.calc_engset)
        btn_calc.grid(row=5, column=0, columnspan=2, pady=20)

    def calc_engset(self):
        try:
            S = self.parse_input(self.en_S.get(), int)
            V = self.parse_input(self.en_V.get(), int)
            alpha = self.parse_input(self.en_alpha.get(), float)
            PB = self.parse_input(self.en_PB.get(), float)

            inputs = {'S': S, 'V': V, 'alpha': alpha, 'PB': PB}

            empty_vars = [k for k, v in inputs.items() if v is None]
            if len(empty_vars) != 1:
                self.show_message("BŁĄD", "Zostaw DOKŁADNIE JEDNO pole puste!")
                return
            target_var = empty_vars[0]

            # przedziały
            range_vars = [k for k, v in inputs.items() if isinstance(v, tuple) and v[0] == "RANGE"]
            if len(range_vars) > 1:
                self.show_message("BŁĄD", "Możesz podać maksymalnie jeden przedział!")
                return

            # tryb wykresu
            if len(range_vars) == 1:
                indep_var = range_vars[0]
                _, start, end, t_func = inputs[indep_var]
                x_vals = self.generate_range_values(start, end, t_func)
                y_vals = []

                for x in x_vals:
                    kwargs = {k: (x if k == indep_var else v) for k, v in inputs.items()}
                    kwargs[target_var] = None
                    try:
                        y_vals.append(solve_engset(**kwargs))
                    except ValueError:
                        y_vals.append(float('nan'))

                if all(math.isnan(y) for y in y_vals):
                    self.show_message("BŁĄD",
                                      "Dla podanych parametrów wygenerowanie wykresu jest matematycznie niemożliwe (zbyt mała liczba źródeł względem kanałów).")
                    return

                plt.figure(figsize=(7, 5))

                # skala logarytmiczna dla PB
                if target_var == 'PB':
                    plt.yscale('log')

                if target_var in ['S', 'V']:
                    plt.step(x_vals, y_vals, where='post', color='#ff7f0e', linewidth=2)
                else:
                    plt.plot(x_vals, y_vals, marker='.' if t_func == int else None, linestyle='-', color='#ff7f0e')

                fixed_params = [f"{k}={v}" for k, v in inputs.items() if k != target_var and k != indep_var]
                fixed_str = ", ".join(fixed_params)

                plt.title(f"Zależność {target_var} od {indep_var} (Engset) dla {fixed_str}")
                plt.xlabel(f"Wartość {indep_var}")
                plt.ylabel(f"Szukane {target_var}")
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()
                plt.show()

                getattr(self, f"en_{target_var}").set("Wykres")

            # jedna wartość
            else:
                result = solve_engset(S=S, V=V, alpha=alpha, PB=PB)
                if target_var == 'S':
                    self.en_S.set(str(result))
                elif target_var == 'V':
                    self.en_V.set(str(result))
                elif target_var == 'alpha':
                    self.en_alpha.set(f"{result:.4f}")
                elif target_var == 'PB':
                    self.en_PB.set(f"{result:.6f}")

        except Exception as e:
            self.show_message("BŁĄD", str(e))

    def create_input_row(self, parent, label_text, text_var, row_idx):
        lbl = CTkLabel(parent, text=label_text)
        lbl.grid(row=row_idx, column=0, sticky=tk.W, padx=15, pady=5)
        entry = CTkEntry(parent, textvariable=text_var, width=120)
        entry.grid(row=row_idx, column=1, sticky=tk.E, padx=15, pady=5)

    def show_help(self):
        curr_tab = self.notebook.get()
        if curr_tab == "Erlang B":
            text = "Erlang B\n\nAby wygenerować wykres podaj przedział zamiast liczby.\nFormat przedziału to: start-koniec (np. 1-15 lub 0.1-0.9)."
            self.show_message("ERLANG B", text)
        elif curr_tab == "Engset":
            text = "Engset\n\nAby wygenerować wykres podaj przedział zamiast liczby.\nFormat przedziału to: start-koniec (np. 1-15 lub 0.1-0.9)."
            self.show_message("ENGSET", text)


if __name__ == "__main__":
    app = TeleTrafficApp()
    app.mainloop()
