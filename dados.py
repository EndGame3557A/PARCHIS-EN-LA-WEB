import tkinter as tk
import turtle
import random
import time

puntos = {
    1: [(0, 0)],
    2: [(-30, -30), (30, 30)],
    3: [(-30, -30), (0, 0), (30, 30)],
    4: [(-30, -30), (-30, 30), (30, -30), (30, 30)],
    5: [(-30, -30), (-30, 30), (0, 0), (30, -30), (30, 30)],
    6: [(-30, -30), (-30, 0), (-30, 30), (30, -30), (30, 0), (30, 30)],
}

tamaño = 100

def dibujar(tortuga, x, y, value):
    tortuga.penup()
    tortuga.goto(x - tamaño // 2, y + tamaño // 2)
    tortuga.pendown()
    tortuga.fillcolor("white")
    tortuga.begin_fill()
    for _ in range(4):
        tortuga.forward(tamaño)
        tortuga.right(90)
    tortuga.end_fill()
    tortuga.penup()
    for px, py in puntos[value]:
        tortuga.goto(x + px, y + py - 10)
        tortuga.dot(20, "black")


def cerrar_panel_dados():
    if hasattr(crear_panel_dados, "ventana") and crear_panel_dados.ventana.winfo_exists():
        crear_panel_dados.ventana.destroy()
        del crear_panel_dados.ventana
def crear_panel_dados(master, callback, turno):
    # Crear o reutilizar una ventana Toplevel para los dados
    if hasattr(crear_panel_dados, "ventana") and crear_panel_dados.ventana.winfo_exists():
        ventana = crear_panel_dados.ventana
        ventana.deiconify()
        ventana.lift()
        for widget in ventana.winfo_children():
            widget.destroy()
    else:
        ventana = tk.Toplevel(master)
        ventana.title("Lanzar Dados")
        ventana.geometry("420x300+1000+100")
        ventana.resizable(False,False)
        ventana.protocol("WM_DELETE_WINDOW", lambda: None)  # Desactiva la X

        crear_panel_dados.ventana = ventana

    label_turno = tk.Label(ventana, text=f"Turno de: {turno}", font=("Arial", 16, "bold"), fg="blue")
    label_turno.pack(pady=5)

    canvas = tk.Canvas(ventana, width=400, height=200)
    canvas.pack()

    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("lightgreen")
    

    tortuga = turtle.RawTurtle(screen)
    tortuga.hideturtle()
    tortuga.speed(0)


    def lanzar_dados():
        button.config(state="disabled")
        tortuga.clear()
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        dibujar(tortuga, -100, 0, dado1)
        dibujar(tortuga, 100, 0, dado2)
        ventana.update()  # Fuerza a que se dibuje antes de dormir
        time.sleep(1)     # Espera 1 segundo (la ventana no responderá durante este tiempo)
        if callback:
            callback(dado1, dado2, ventana)

        

    button = tk.Button(ventana, text="Lanzar Dados", command=lanzar_dados, font=("Arial", 14), bg="#4CAF50", fg="white")
    button.pack(pady=10)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_panel_dados)
    #ventana.protocol("WM_DELETE_WINDOW", ventana.withdraw)  # Oculta la ventana al cerrar

    return