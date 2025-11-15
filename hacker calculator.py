import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Themed Calculator")
        self.root.geometry("320x450")
        self.root.resizable(False, False)
        
        # Theme variables
        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "display_bg": "#ffffff",
                "button_bg": "#e0e0e0",
                "operator_bg": "#FF9500",
                "special_bg": "#A6A6A6",
                "hacker_special": "#4a86e8"
            },
            "dark": {
                "bg": "#2d2d2d",
                "fg": "#ffffff",
                "display_bg": "#3d3d3d",
                "button_bg": "#4d4d4d",
                "operator_bg": "#FF9500",
                "special_bg": "#6d6d6d",
                "hacker_special": "#4a86e8"
            },
            "hacker": {
                "bg": "#000000",
                "fg": "#00ff00",
                "display_bg": "#001a00",
                "button_bg": "#003300",
                "operator_bg": "#00cc00",
                "special_bg": "#006600",
                "hacker_special": "#00ff00"
            }
        }
        
        # Variables
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset_display = False
        
        # Create UI elements
        self.create_widgets()
        self.apply_theme()
        
    def create_widgets(self):
        # Display
        self.display_var = tk.StringVar(value=self.current)
        self.display = tk.Entry(
            self.root, 
            textvariable=self.display_var, 
            font=("Courier", 16), 
            justify="right",
            state="readonly",
            relief="flat"
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=(15, 10), sticky="ew")
        
        # Theme selector
        self.theme_var = tk.StringVar(value="Light")
        theme_frame = tk.Frame(self.root)
        theme_frame.grid(row=1, column=0, columnspan=4, pady=(0, 10))
        
        tk.Label(theme_frame, text="Theme:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(10, 5))
        theme_menu = tk.OptionMenu(
            theme_frame, 
            self.theme_var, 
            "Light", 
            "Dark", 
            "Hacker", 
            command=self.change_theme
        )
        theme_menu.pack(side=tk.LEFT)
        
        # Buttons
        buttons = [
            ("C", 2, 0), ("±", 2, 1), ("%", 2, 2), ("÷", 2, 3),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("×", 3, 3),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3),
            ("0", 6, 0), (".", 6, 2), ("=", 6, 3)
        ]
        
        # Store button references
        self.buttons = {}
        
        for (text, row, col) in buttons:
            if text == "0":
                btn = tk.Button(self.root, text=text, font=("Arial", 14))
                btn.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky="nsew")
            else:
                btn = tk.Button(self.root, text=text, font=("Arial", 14))
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
                
            btn.config(command=lambda t=text: self.button_click(t))
            self.buttons[text] = btn
        
        # Configure grid weights
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
            
    def change_theme(self, selection):
        theme_map = {"Light": "light", "Dark": "dark", "Hacker": "hacker"}
        self.current_theme = theme_map[selection]
        self.apply_theme()
        
    def apply_theme(self):
        theme = self.themes[self.current_theme]
        
        # Apply theme colors
        self.root.config(bg=theme["bg"])
        self.display.config(bg=theme["display_bg"], fg=theme["fg"], insertbackground=theme["fg"])
        
        # Style buttons according to theme
        for text, btn in self.buttons.items():
            if text in ["÷", "×", "-", "+", "="]:
                btn.config(
                    bg=theme["operator_bg"],
                    fg="white" if self.current_theme != "hacker" else theme["fg"],
                    activebackground=theme["operator_bg"]
                )
            elif text in ["C", "±", "%"]:
                btn.config(
                    bg=theme["special_bg"],
                    fg=theme["fg"],
                    activebackground=theme["special_bg"]
                )
            else:
                btn.config(
                    bg=theme["button_bg"],
                    fg=theme["fg"],
                    activebackground=theme["button_bg"]
                )
                
            # Special hacker theme modifications
            if self.current_theme == "hacker":
                btn.config(font=("Courier", 14, "bold"))
                if text in ["C", "±", "%"]:
                    btn.config(fg=theme["hacker_special"])
                    
                # Add subtle glow effect for operators in hacker theme
                if text in ["÷", "×", "-", "+", "="]:
                    btn.config(relief="raised", bd=2)
        
        # Update theme menu
        theme = self.themes[self.current_theme]
        self.root.nametowidget(self.root.children['!frame']._name + '.!optionmenu').config(
            bg=theme["button_bg"],
            fg=theme["fg"],
            activebackground=theme["button_bg"]
        )
        
    def button_click(self, char):
        try:
            if char.isdigit():
                self.input_number(char)
            elif char == ".":
                self.input_decimal()
            elif char in ["÷", "×", "-", "+"]:
                self.input_operator(char)
            elif char == "=":
                self.calculate()
            elif char == "C":
                self.clear()
            elif char == "±":
                self.change_sign()
            elif char == "%":
                self.percentage()
        except Exception as e:
            messagebox.showerror("Error", "Invalid operation")
            self.clear()

    def input_number(self, num):
        if self.should_reset_display or self.current == "0":
            self.current = num
            self.should_reset_display = False
        else:
            self.current += num
        self.update_display()

    def input_decimal(self):
        if self.should_reset_display:
            self.current = "0."
            self.should_reset_display = False
        elif "." not in self.current:
            self.current += "."
        self.update_display()

    def input_operator(self, op):
        if self.operator and not self.should_reset_display:
            self.calculate()
        
        self.previous = self.current
        self.operator = op
        self.should_reset_display = True

    def calculate(self):
        if not self.operator or not self.previous:
            return
            
        try:
            prev = float(self.previous)
            curr = float(self.current)
            
            if self.operator == "+":
                result = prev + curr
            elif self.operator == "-":
                result = prev - curr
            elif self.operator == "×":
                result = prev * curr
            elif self.operator == "÷":
                if curr == 0:
                    messagebox.showerror("Error", "Cannot divide by zero")
                    self.clear()
                    return
                result = prev / curr
                
            # Format result to avoid trailing zeros
            if result.is_integer():
                self.current = str(int(result))
            else:
                self.current = f"{result:.10g}"
                
            self.operator = ""
            self.previous = ""
            self.should_reset_display = True
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def clear(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset_display = False
        self.update_display()

    def change_sign(self):
        if self.current != "0":
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.update_display()

    def percentage(self):
        try:
            value = float(self.current) / 100
            self.current = f"{value:.10g}"
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def update_display(self):
        # Limit display length
        display_text = self.current[:12] if len(self.current) > 12 else self.current
        self.display_var.set(display_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()