"""Einfaches GUI-Platzhalterfenster."""

import tkinter as tk


class App(tk.Tk):
    """Hauptfenster."""

    def __init__(self) -> None:
        super().__init__()
        self.title("DeZensur – v0.1")
        label = tk.Label(self, text="GUI Platzhalter")
        label.pack(padx=20, pady=20)


def main() -> None:
    """Startet die GUI."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
