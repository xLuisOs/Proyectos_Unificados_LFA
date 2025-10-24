import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from graph import Graph
from automaton import Automaton
from algorithm import ShortestPath

COLORS = {
    "bg_primary": "#D5E6E6",
    "bg_secondary": "#A7C3C3",
    "accent": "#2E838B",
    "accent_dark": "#29757C",
    "text_primary": "#222222",
    "text_secondary": "#6B7280"
}

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class GraphGUI:
    def __init__(self, master):
        self.master = master
        master.title("Aplicación de Ruta Más Corta")
        master.state('zoomed')
        master.configure(bg=COLORS["bg_primary"])

        self.graph = Graph(directed=True)
        self.automaton = None

        self.frame_main = ctk.CTkFrame(master, fg_color=COLORS["bg_primary"])
        self.frame_main.pack(side="left", fill="both", expand=True)

        self.frame_side = ctk.CTkFrame(master, width=300, fg_color=COLORS["bg_secondary"])
        self.frame_side.pack(side="right", fill="y")

        ctk.CTkLabel(
            self.frame_side, text="Opciones",
            font=("Arial", 18, "bold"),
            text_color=COLORS["text_primary"]
        ).pack(pady=10)

        buttons = [
            ("Agregar Nodo", self.show_add_node),
            ("Agregar Arista", self.show_add_edge),
            ("Definir Autómata", self.show_define_automaton),
            ("Visualizar Grafo", self.show_graph),
            ("Calcular Ruta Más Corta", self.show_shortest_path)
        ]

        for text, command in buttons:
            ctk.CTkButton(
                self.frame_side, text=text, command=command,
                fg_color=COLORS["accent"], hover_color=COLORS["accent_dark"],
                text_color="white", corner_radius=10, height=35
            ).pack(pady=5, fill='x', padx=15)

        self.panel_dynamic = ctk.CTkFrame(self.frame_main, fg_color=COLORS["bg_secondary"])
        self.panel_dynamic.pack(fill="both", expand=True, padx=20, pady=20)

        self.frame_right = ctk.CTkFrame(self.frame_main, fg_color=COLORS["bg_primary"])
        self.frame_right.pack(fill="both", expand=True, padx=20, pady=20)

        self.graph_canvas = None
        self.toolbar = None

    def clear_panel(self):
        for widget in self.panel_dynamic.winfo_children():
            widget.destroy()

    def show_add_node(self):
        self.clear_panel()
        ctk.CTkLabel(self.panel_dynamic, text="Agregar Nodo", font=("Arial", 16, "bold")).pack(pady=10)
        entry_node = ctk.CTkEntry(self.panel_dynamic, placeholder_text="Nombre del nodo")
        entry_node.pack(pady=5)

        def add_node_action():
            nodo = entry_node.get().strip()
            if nodo:
                self.graph.add_node(nodo)
                messagebox.showinfo("Nodo agregado", f"El nodo '{nodo}' ha sido agregado")
                entry_node.delete(0, ctk.END)

        ctk.CTkButton(self.panel_dynamic, text="Agregar", command=add_node_action,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_dark"]).pack(pady=10)

    def show_add_edge(self):
        self.clear_panel()
        ctk.CTkLabel(self.panel_dynamic, text="Agregar Arista", font=("Arial", 16, "bold")).pack(pady=10)
        entry_origen = ctk.CTkEntry(self.panel_dynamic, placeholder_text="Nodo origen")
        entry_origen.pack(pady=5)
        entry_destino = ctk.CTkEntry(self.panel_dynamic, placeholder_text="Nodo destino")
        entry_destino.pack(pady=5)
        entry_peso = ctk.CTkEntry(self.panel_dynamic, placeholder_text="Peso de la arista")
        entry_peso.pack(pady=5)

        def add_edge_action():
            origen = entry_origen.get().strip()
            destino = entry_destino.get().strip()
            try:
                peso = float(entry_peso.get())
            except ValueError:
                peso = 1.0
            self.graph.add_edge(origen, destino, peso)
            messagebox.showinfo("Arista agregada", f"Arista {origen} -> {destino} (peso {peso}) agregada")
            entry_origen.delete(0, ctk.END)
            entry_destino.delete(0, ctk.END)
            entry_peso.delete(0, ctk.END)

        ctk.CTkButton(self.panel_dynamic, text="Agregar", command=add_edge_action,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_dark"]).pack(pady=10)

    def show_define_automaton(self):
        self.clear_panel()
        ctk.CTkLabel(self.panel_dynamic, text="Definir Autómata", font=("Arial", 16, "bold")).pack(pady=10)

        entry_inicial = ctk.CTkEntry(self.panel_dynamic, placeholder_text="Estado inicial")
        entry_inicial.pack(pady=5)

        entry_aceptacion = ctk.CTkEntry(self.panel_dynamic,
                                        placeholder_text="Estados de aceptación separados por coma")
        entry_aceptacion.pack(pady=5)

        def define_automaton_action():
            estado_inicial = entry_inicial.get().strip()
            estados_aceptacion = set(e.strip() for e in entry_aceptacion.get().split(",") if e.strip())

            nodos_grafo = self.graph.get_nodes()
            if estado_inicial not in nodos_grafo:
                messagebox.showerror("Error", f"El nodo inicial '{estado_inicial}' no existe en el grafo")
                return

            invalid_accepting = [e for e in estados_aceptacion if e not in nodos_grafo]
            if invalid_accepting:
                messagebox.showerror("Error", f"Los nodos de aceptación no existen: {', '.join(invalid_accepting)}")
                return

            self.automaton = Automaton(
                self.graph,
                initial_state=estado_inicial,
                accepting_states=estados_aceptacion,
                alphabet=self.graph.get_nodes()
            )
            messagebox.showinfo("Autómata", "Autómata definido correctamente")
            entry_inicial.delete(0, ctk.END)
            entry_aceptacion.delete(0, ctk.END)

        ctk.CTkButton(self.panel_dynamic, text="Definir", command=define_automaton_action,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_dark"]).pack(pady=10)

    def show_shortest_path(self):
        self.clear_panel()
        ctk.CTkLabel(self.panel_dynamic, text="Calcular Ruta Más Corta", font=("Arial", 16, "bold")).pack(pady=10)
        entry_start = ctk.CTkEntry(self.panel_dynamic, placeholder_text="Nodo inicio")
        entry_start.pack(pady=5)
        entry_end = ctk.CTkEntry(self.panel_dynamic, placeholder_text="Nodo destino")
        entry_end.pack(pady=5)

        def calculate_path_action():
            if not self.automaton:
                messagebox.showwarning("Advertencia", "Primero define el autómata")
                return
            start = entry_start.get().strip()
            end = entry_end.get().strip()

            sp = ShortestPath(self.graph)
            distance, path = sp.dijkstra(start, end)

            if not path:
                messagebox.showinfo("Resultado", f"No se encontró ruta válida de {start} a {end}")
            else:
                messagebox.showinfo("Resultado", f"Ruta más corta: {' -> '.join(path)}\nDistancia total: {distance}")
                self.show_graph(path)

        ctk.CTkButton(self.panel_dynamic, text="Calcular", command=calculate_path_action,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_dark"]).pack(pady=10)


    def show_graph(self, path=None):
        try:
            G = nx.DiGraph() if self.graph.directed else nx.Graph()
            for node in self.graph.get_nodes():
                G.add_node(node)
            for node, connections in self.graph.graph.items():
                for neighbor, weight in connections.items():
                    G.add_edge(node, neighbor, weight=weight)

            pos = nx.spring_layout(G, seed=42)
            fig, ax = plt.subplots(figsize=(6, 5))
            fig.patch.set_facecolor(COLORS["bg_primary"])
            ax.set_facecolor(COLORS["bg_secondary"])

            nx.draw(G, pos, with_labels=True, ax=ax,
                    node_color=COLORS["accent"], edgecolors=COLORS["accent_dark"],
                    node_size=900, font_color="white", font_weight="bold")

            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

            if path and len(path) > 1:
                path_edges = list(zip(path, path[1:]))
                nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="#FFD700", node_size=1000, ax=ax)
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="#FFD700", width=3, ax=ax)

            if self.graph_canvas is not None:
                self.graph_canvas.get_tk_widget().destroy()
                self.toolbar.destroy()


            self.graph_canvas = FigureCanvasTkAgg(fig, master=self.frame_right)
            self.graph_canvas.draw()
            self.graph_canvas.get_tk_widget().pack(padx=10, pady=(10, 0), fill="both", expand=True)

            self.toolbar = NavigationToolbar2Tk(self.graph_canvas, self.frame_right, pack_toolbar=False)
            self.toolbar.update()
            self.toolbar.pack(padx=10, pady=(0, 10), fill="x")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el grafo:\n{e}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = GraphGUI(root)
    root.mainloop()
