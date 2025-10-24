import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import webbrowser

class MintyTheme:
    COLORS = {
        'primary': '#1E3D34',       
        'secondary': '#27AE60',      
        'accent': '#A3E4D7',         
        'background': '#F5F7F6',     
        'text_main': '#2E4053',    
        'text_soft': '#7D8A8F',    
        'hover': '#ABEBC6',       
        'card_bg': '#FFFFFF',       
        'border': '#D5DBDB'   
    }

    FONTS = {
        'title': ('Calibri', 34, 'bold'),
        'subtitle': ('Calibri', 18, 'italic'),
        'card_title': ('Calibri', 20, 'bold'),
        'card_text': ('Calibri', 14, 'normal'),
        'button': ('Calibri', 15, 'bold')
    }

class ProjectTile(ctk.CTkFrame):
    def __init__(self, parent, title, description, command, emoji="💻", is_url=False, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.title_text = title
        self.is_url = is_url

        self.configure(
            fg_color=MintyTheme.COLORS['card_bg'],
            corner_radius=12,
            border_color=MintyTheme.COLORS['border'],
            border_width=2
        )

        self.icon = ctk.CTkLabel(self, text=emoji, font=('Segoe UI Emoji', 44))
        self.icon.pack(pady=(15, 5))

        self.title_label = ctk.CTkLabel(
            self, text=title,
            font=MintyTheme.FONTS['card_title'],
            text_color=MintyTheme.COLORS['primary']
        )
        self.title_label.pack(pady=(0, 4))

        self.desc_label = ctk.CTkLabel(
            self, text=description,
            font=MintyTheme.FONTS['card_text'],
            text_color=MintyTheme.COLORS['text_soft'],
            wraplength=260, justify="center"
        )
        self.desc_label.pack(pady=(0, 15))

        button_text = "🌐 Abrir Web" if is_url else "▶ Ejecutar"
        self.launch_button = ctk.CTkButton(
            self,
            text=button_text,
            fg_color=MintyTheme.COLORS['secondary'],
            hover_color=MintyTheme.COLORS['hover'],
            text_color="white",
            font=MintyTheme.FONTS['button'],
            corner_radius=8,
            command=self.run_project
        )
        self.launch_button.pack(pady=(0, 10))

        self.bind_hover_effects()

    def bind_hover_effects(self):
        """Efecto hover"""
        def on_enter(e): self.configure(border_color=MintyTheme.COLORS['secondary'])
        def on_leave(e): self.configure(border_color=MintyTheme.COLORS['border'])
        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)

    def run_project(self):
        """Ejecuta el proyecto o abre el enlace"""
        try:
            if self.is_url:
                webbrowser.open(self.command)
                messagebox.showinfo("Proyecto Abierto", f"🌐 {self.title_text} se está abriendo en tu navegador.")
            else:
                subprocess.Popen([sys.executable] + self.command, cwd=os.path.dirname(self.command[0]))
                messagebox.showinfo("Proyecto Iniciado", f"✅ {self.title_text} se está ejecutando.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir {self.title_text}:\n{e}")

class UnifiedLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Centro de Proyectos 2025 - Lanzador")
        self.configure(fg_color=MintyTheme.COLORS['background'])

        self.after(100, lambda: self.state('zoomed'))

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.create_layout()
        self.load_projects()

    def create_layout(self):
        """Diseño visual"""
        self.header = ctk.CTkFrame(self, fg_color=MintyTheme.COLORS['primary'], height=120, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.main_title = ctk.CTkLabel(
            self.header,
            text="Proyectos - Lenguajes y Autómatas ",
            font=MintyTheme.FONTS['title'],
            text_color="white"
        )
        self.main_title.pack(pady=(25, 5))

        self.subtitle = ctk.CTkLabel(
            self.header,
            text="Selecciona un módulo para ejecutar ",
            font=MintyTheme.FONTS['subtitle'],
            text_color=MintyTheme.COLORS['accent']
        )
        self.subtitle.pack()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=40, pady=40)

        for i in range(2):
            self.container.grid_columnconfigure(i, weight=1, uniform="col")
            self.container.grid_rowconfigure(i, weight=1, uniform="row")

    def load_projects(self):

        projects = [
            {
                'title': 'Tablas de Verdad',
                'description': 'Evalúa proposiciones y genera tablas de verdad automáticamente.',
                'command': [os.path.join(os.getcwd(), 'tablas-de-vdd', 'main.py')],
                'emoji': '🧮',
                'is_url': False
            },
            {
                'title': 'Simplificador Booleano',
                'description': 'Reduce expresiones booleanas con pasos visuales.',
                'command': [os.path.join(os.getcwd(), 'simplificador', 'main.py')],
                'emoji': '⚙️',
                'is_url': False
            },
            {
                'title': 'Proyecto 03 - LFA (Web)',
                'description': 'Aplicación web sobre autómatas y expresiones regulares.',
                'command': 'https://expresiones-regex.vercel.app/',
                'emoji': '🌐',
                'is_url': True
            },
            {
                'title': 'Analizador de Grafos',
                'description': 'Explora grafos dirigidos y encuentra rutas óptimas visualmente.',
                'command': [os.path.join(os.getcwd(), 'Grafos', 'main.py')],
                'emoji': '🕸️',
                'is_url': False
            }
        ]

        for i, project in enumerate(projects):
            row, col = divmod(i, 2)
            tile = ProjectTile(
                self.container,
                title=project['title'],
                description=project['description'],
                command=project['command'],
                emoji=project['emoji'],
                is_url=project['is_url'],
                width=300,
                height=300
            )
            tile.grid(row=row, column=col, padx=40, pady=40, sticky="nsew")

        footer = ctk.CTkFrame(self, fg_color=MintyTheme.COLORS['primary'], height=60, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        footer_label = ctk.CTkLabel(
            footer,
            text="Luis Granados 1506124",
            font=('Calibri', 13),
            text_color="white"
        )
        footer_label.pack(pady=15)

def main():
    try:
        app = UnifiedLauncher()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error crítico", f"No se pudo iniciar el launcher:\n{e}")

if __name__ == "__main__":
    main()
