import tkinter as tk
from turtle import RawTurtle, ScrolledCanvas
import dados
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
ventana = tk.Tk()
ventana.title("PARCHIS")
ventana.geometry("780x780")
ventana.resizable(False, False)

canvas = ScrolledCanvas(ventana)
canvas.pack(fill=tk.BOTH, expand=True)

# Ventana de control externa
ventana_control = tk.Toplevel()
ventana_control.geometry("180x80+850+200")
ventana_control.title("...")
ventana_control.resizable(False, False)
ventana_control.attributes('-topmost', True)  # Siempre encima

ventana_control.protocol("WM_DELETE_WINDOW", lambda: None)
def bloquear_cierre(event=None):
        return "break"
        ventana_control.bind("<Alt-F4>", bloquear_cierre)
        ventana_control.bind("<Escape>", bloquear_cierre)
        ventana_control.bind("<Control-w>", bloquear_cierre)
        ventana_control.bind("<Control-q>", bloquear_cierre)
    

def cerrar_parchis():
    ventana.destroy()

btn_salir_control = tk.Button(
    ventana_control,
    text="Salir del Parchís",
    font=("Arial", 11, "bold"),
    bg="#e53935",
    fg="white",
    width=14,
    command=cerrar_parchis
)
btn_salir_control.pack(pady=18)

# Si cierran la ventana de control, solo se oculta esa ventana (no el parchís)
ventana_control.protocol("WM_DELETE_WINDOW", ventana_control.withdraw)


turtle_screen = RawTurtle(canvas)
turtle_screen.speed(0)
turtle_screen.screen.colormode(255) 



def dibujar_cuadro():
    turtle_screen.up()
    turtle_screen.goto(-385,-600)
    turtle_screen.down()
    turtle_screen.fillcolor((238, 208, 157))  
    turtle_screen.begin_fill()               
    turtle_screen.setheading(90)
    turtle_screen.forward(990)
    turtle_screen.right(90)
    turtle_screen.forward(770)
    turtle_screen.right(90)
    turtle_screen.forward(990)
    turtle_screen.right(90)
    turtle_screen.forward(770)
    turtle_screen.end_fill()


def dibujar_cuadrado_redondeado(t, x, y, lado, color, radio_esquina):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(lado - 2 * radio_esquina)  
        t.circle(radio_esquina, 90) 
    t.end_fill()


def agregar_imagenes():
    from PIL import Image

    img = Image.open("Atletico-nacional-logo.png")  
    img = img.resize((150, 200))  
    img.save("Atletico-nacional-logo.gif")  

    img = Image.open("R.png")
    img = img.resize((200, 200))  
    img.save("R.gif") 

    img = Image.open("once_caldas.png")  
    img = img.resize((135, 200))  
    img.save("once_caldas.gif")

    img = Image.open("Millonarios FC.png")  
    img = img.resize((200, 200))  
    img.save("Millonarios FC.gif")

    # Registrar y colocar la imagen verde
    turtle_screen.screen.register_shape("Atletico-nacional-logo.gif")
    turtle_screen.shape("Atletico-nacional-logo.gif")
    turtle_screen.penup()
    turtle_screen.goto(-255, -255)
    turtle_screen.stamp()

    # Registrar y colocar la imagen roja
    turtle_screen.screen.register_shape("R.gif")
    turtle_screen.shape("R.gif")
    turtle_screen.penup()
    turtle_screen.goto(-255, 255)
    turtle_screen.stamp()
    
    # Registrar y colocar la imagen blanca
    turtle_screen.screen.register_shape("once_caldas.gif")
    turtle_screen.shape("once_caldas.gif")
    turtle_screen.penup()
    turtle_screen.goto(255, 255)
    turtle_screen.stamp()

    # Registrar y colocar la imagen azul
    turtle_screen.screen.register_shape("Millonarios FC.gif")
    turtle_screen.shape("Millonarios FC.gif")
    turtle_screen.penup()
    turtle_screen.goto(255, -255)
    turtle_screen.stamp()

    # Vuelve a la forma estándar para seguir dibujando
    turtle_screen.shape("classic")
    turtle_screen.pendown()


def dibujar_verde():
    turtle_screen.penup()
    turtle_screen.goto(-125, -125)
    turtle_screen.pendown()
    dibujar_cuadrado_redondeado(turtle_screen, -255, -130, 250, "green", 125)

def dibujar_rojo():
    turtle_screen.penup()
    turtle_screen.goto(-125, 125)
    turtle_screen.pendown()
    dibujar_cuadrado_redondeado(turtle_screen, -255, 385, 250, "red", 125)

def dibujar_blanco():
    turtle_screen.penup()
    turtle_screen.goto(125, 125)
    turtle_screen.pendown()
    dibujar_cuadrado_redondeado(turtle_screen, 255, 385, 250, "white", 125)

def dibujar_azul():
    turtle_screen.penup()
    turtle_screen.goto(125, -125)
    turtle_screen.pendown()
    dibujar_cuadrado_redondeado(turtle_screen, 255, -130, 250, "blue", 125)


def casillas_verde():
    turtle_screen.pensize(8)
    turtle_screen.up()
    turtle_screen.goto(-125,50)
    turtle_screen.setheading(0)

    turtle_screen.down()
    turtle_screen.color("black")
    longi=35.714285714285714285714285714286
    casilla=83.333333333333333333
    turtle_screen.left(90)
    turtle_screen.forward(75)
    turtle_screen.backward(250)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(250)

    turtle_screen.backward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)

    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.begin_fill()
    turtle_screen.color("green")
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()
    turtle_screen.color("black")
    turtle_screen.backward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(180)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250-longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250-longi)
    turtle_screen.backward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)    
    turtle_screen.forward(longi)
    turtle_screen.backward(longi)
    turtle_screen.right(90)

    turtle_screen.begin_fill()
    turtle_screen.color("green")
    turtle_screen.forward(casilla/2)
    turtle_screen.backward(170)
    turtle_screen.right(45)
    turtle_screen.forward(casilla+(casilla/2))
    turtle_screen.left(90)
    turtle_screen.forward(casilla+(casilla/2))
    turtle_screen.end_fill()
    turtle_screen.color("green")
    turtle_screen.left(135)
    turtle_screen.forward(174.8)
    turtle_screen.left(135)
    turtle_screen.forward(122.7)
    turtle_screen.left(90)
    turtle_screen.forward(125)




def casillas_rojo():
    turtle_screen.pensize(8)
    turtle_screen.setheading(270)
    turtle_screen.up()
    turtle_screen.goto(50,125)
    turtle_screen.down()
    turtle_screen.color("black")
    longi=35.714285714285714285714285714286
    casilla=83.333333333333333333
    turtle_screen.left(90)
    turtle_screen.forward(75)
    turtle_screen.backward(250)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(250)

    turtle_screen.backward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)

    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.begin_fill()
    turtle_screen.color("red")
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()
    turtle_screen.color("black")
    turtle_screen.backward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(180)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250-longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250-longi)
    turtle_screen.backward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)    
    turtle_screen.forward(longi)
    turtle_screen.backward(longi)
    turtle_screen.right(90)

    turtle_screen.begin_fill()
    turtle_screen.color("red")
    turtle_screen.forward(casilla/2)
    turtle_screen.backward(170)
    turtle_screen.right(45)
    turtle_screen.forward(casilla+(casilla/2))
    turtle_screen.left(90)
    turtle_screen.forward(casilla+(casilla/2))
    turtle_screen.end_fill()
    turtle_screen.color("red")
    turtle_screen.left(135)
    turtle_screen.forward(174.8)
    turtle_screen.left(135)
    turtle_screen.forward(122.7)
    turtle_screen.left(90)
    turtle_screen.forward(125)


def casillas_blanco():
    turtle_screen.pensize(8)
    turtle_screen.setheading(180)
    turtle_screen.up()
    turtle_screen.goto(125,-49)
    turtle_screen.down()
    turtle_screen.color("black")
    longi=35.714285714285714285714285714286
    casilla=83.333333333333333333
    turtle_screen.left(90)
    turtle_screen.forward(75)
    turtle_screen.backward(250)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(250)

    turtle_screen.backward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)

    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.begin_fill()
    turtle_screen.color("white")
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()
    turtle_screen.color("black")
    turtle_screen.backward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(180)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250-longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250-longi)
    turtle_screen.backward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)    
    turtle_screen.forward(longi)
    turtle_screen.backward(longi)
    turtle_screen.right(90)

    turtle_screen.begin_fill()
    turtle_screen.color("white")
    turtle_screen.forward(casilla/2)
    turtle_screen.backward(170)
    turtle_screen.right(45)
    turtle_screen.forward(casilla+(casilla/2))
    turtle_screen.left(90)
    turtle_screen.forward(casilla+(casilla/2))
    turtle_screen.end_fill()
    turtle_screen.color("white")
    turtle_screen.left(135)
    turtle_screen.forward(174.8)
    turtle_screen.left(135)
    turtle_screen.forward(122.7)
    turtle_screen.left(90)
    turtle_screen.forward(125)

    


def casillas_azul():
    turtle_screen.pensize(8)
    turtle_screen.setheading(90)
    turtle_screen.up()
    turtle_screen.goto(-50,-125)
    turtle_screen.down()
    turtle_screen.color("black")
    longi=35.714285714285714285714285714286
    casilla=83.333333333333333333
    turtle_screen.left(90)
    turtle_screen.forward(75)
    turtle_screen.backward(250)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(250)

    turtle_screen.backward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(longi)

    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.begin_fill()
    turtle_screen.color("blue")
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()
    turtle_screen.color("black")
    turtle_screen.backward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(180)
    turtle_screen.forward(250)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250-longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(250-longi)
    turtle_screen.backward(250)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)    
    turtle_screen.forward(longi)
    turtle_screen.backward(longi)
    turtle_screen.right(90)

    turtle_screen.begin_fill()
    turtle_screen.color("blue")
    turtle_screen.forward(casilla/2)
    turtle_screen.backward(170)
    turtle_screen.right(45)
    turtle_screen.forward(casilla+(casilla/2))
    turtle_screen.left(90)
    turtle_screen.forward(casilla+(casilla/2))
    turtle_screen.end_fill()
    turtle_screen.color("blue")
    turtle_screen.left(135)
    turtle_screen.forward(174.8)
    turtle_screen.left(135)
    turtle_screen.forward(122.7)
    turtle_screen.left(90)
    turtle_screen.forward(125)

    
def seguros():
    longi=35.714285714285714285714285714286
    casilla=83.333333333333333333

    #azul

    turtle_screen.up()
    turtle_screen.goto(125,-196)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("blue")
    turtle_screen.setheading(270)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

    turtle_screen.up()
    turtle_screen.goto(196,-125)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("blue")
    turtle_screen.setheading(0)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

    turtle_screen.up()
    turtle_screen.goto(0+(casilla/2),-304-longi)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("blue")
    turtle_screen.setheading(270)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()


    #blanco

    turtle_screen.up()
    turtle_screen.goto(304+longi,(-125+casilla))
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("white")
    turtle_screen.setheading(0)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

    turtle_screen.up()
    turtle_screen.goto(196,125)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("white")
    turtle_screen.setheading(0)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

    turtle_screen.up()
    turtle_screen.goto(125,196)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("white")
    turtle_screen.setheading(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()


    #rojo 

    turtle_screen.up()
    turtle_screen.goto(-196,125)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("red")
    turtle_screen.setheading(0)
    turtle_screen.backward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

    turtle_screen.up()
    turtle_screen.goto(-125,196)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("red")
    turtle_screen.setheading(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

    turtle_screen.up()
    turtle_screen.goto(0+(casilla/2),304+longi)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("red")
    turtle_screen.setheading(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

    #verde

    turtle_screen.up()
    turtle_screen.goto(-304-longi,(-125+casilla))
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("green")
    turtle_screen.setheading(180)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

    turtle_screen.up()
    turtle_screen.goto(-196,-125)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("green")
    turtle_screen.setheading(0)
    turtle_screen.backward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.right(90)
    turtle_screen.forward(longi)
    turtle_screen.right(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

    turtle_screen.up()
    turtle_screen.goto(-125,-196)
    turtle_screen.down()
    turtle_screen.begin_fill()
    turtle_screen.color("green")
    turtle_screen.setheading(270)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.left(90)
    turtle_screen.forward(longi)
    turtle_screen.left(90)
    turtle_screen.forward(casilla)
    turtle_screen.end_fill()

def delinear():
    turtle_screen.up()
    turtle_screen.goto(90,90)
    turtle_screen.color("black")
    turtle_screen.pensize(9)
    turtle_screen.down()
    turtle_screen.right(45)
    turtle_screen.forward(180)
    turtle_screen.left(90)
    turtle_screen.forward(180)
    turtle_screen.left(90)
    turtle_screen.forward(180)
    turtle_screen.left(90)
    turtle_screen.forward(180)
    turtle_screen.left(134.5)
    turtle_screen.backward(50)
    turtle_screen.forward(350)
    turtle_screen.up()
    turtle_screen.goto(-90,90)
    turtle_screen.down()
    turtle_screen.setheading(315)
    turtle_screen.backward(50)
    turtle_screen.forward(350)  

    crear_fichas_objeto() 


def etiquetar_casillas():
    etiquetas_salida = [
        # Salidas horizontales
        {"x": -215, "y": -60, "texto": "SALIDA", "color": "black", "direccion": "vertical"},  # Salida verde
        {"x": 215, "y": 106, "texto": "SALIDA", "color": "black", "direccion": "vertical"},  # Salida naranja

        # Salidas verticales
        {"x": -84, "y": 205, "texto": "SALIDA", "color": "black", "direccion": "horizontal"},  # Salida roja
        {"x": 85, "y": -223, "texto": "SALIDA", "color": "black", "direccion": "horizontal"},  # Salida azul
    
        
    ]

    etiquetas_seguras = [
        {"x": -85, "y": -223, "texto": "SEGURO", "color": "black", "direccion": "horizontal"},  # Seguro verde
        {"x": 84, "y": 205, "texto": "SEGURO", "color": "black", "direccion": "horizontal"},  # Seguro naranja

        {"x": -215, "y": 106, "texto": "SEGURO", "color": "black", "direccion": "vertical"},  # Seguro rojo
        {"x": 215, "y": -60, "texto": "SEGURO", "color": "black", "direccion": "vertical"},  # Seguro azul
    
        {"x": 358, "y": 23, "texto": "SEGURO", "color": "black", "direccion": "vertical"},  # Seguro esquina naranja
        {"x": -358, "y": 23, "texto": "SEGURO", "color": "black", "direccion": "vertical"}, # Seguro esquina verde

        {"x": -2, "y": 350, "texto": "SEGURO", "color": "black", "direccion": "horizontal"},  # Seguro esquina rojo
        {"x": -2, "y": -363, "texto": "SEGURO", "color": "black", "direccion": "horizontal"}, # Seguro esquina azul
    ]

    # Función para escribir texto con dirección
    def escribir_texto(etiqueta):
        turtle_screen.penup()
        turtle_screen.goto(etiqueta["x"], etiqueta["y"])
        turtle_screen.color(etiqueta["color"])

        # Ajustar la dirección del texto
        if etiqueta["direccion"] == "horizontal":
            # Escribir texto horizontalmente
            turtle_screen.write(etiqueta["texto"], align="center", font=("Arial", 10, "bold"))
        elif etiqueta["direccion"] == "vertical":
            # Escribir texto verticalmente (carácter por carácter)
            for i, char in enumerate(etiqueta["texto"]):
                turtle_screen.write(char, align="center", font=("Arial", 10, "bold"))
                turtle_screen.sety(turtle_screen.ycor() - 12)  # Mover hacia abajo para el siguiente carácter

    for etiqueta in etiquetas_salida:
        escribir_texto(etiqueta)

    for etiqueta in etiquetas_seguras:
        escribir_texto(etiqueta)

    
posiciones_salida = {
    "V": [(-214, -65),(-214, -105)],
    "R": [(-65, 213),(-105, 213)],
    "B": [(214, 70),(214, 105)],
    "AZ": [(65, -213),(105, -213)]
}

posiciones_carcel = {
    "V1": (-225, -230), "V2": (-315, -310), "V3": (-315, -230), "V4": (-225, -310),
    "R1": (-225, 210), "R2": (-315, 290), "R3": (-315, 210), "R4": (-225, 290),
    "B1": (195, 210), "B2": (285, 290), "B3": (285, 210), "B4": (195, 290),
    "AZ1": (195, -230), "AZ2": (285, -310), "AZ3": (285, -230), "AZ4": (195, -310)
}

fichas_obj = {}
fichas_numeros = {}

def crear_fichas_objeto():
    posiciones = posiciones_carcel
    colores = {
        "V": (137, 255, 0), "R": (255, 180, 0), "B": (182, 182, 182), "AZ": (0, 179, 255)
    }
    for nombre, (x, y) in posiciones.items():
        ficha = RawTurtle(canvas)
        ficha.penup()
        ficha.shape("circle")
        ficha.shapesize(1.3)
        if nombre.startswith("V"):
            ficha.color(colores["V"])
        elif nombre.startswith("R"):
            ficha.color(colores["R"])
        elif nombre.startswith("B"):
            ficha.color(colores["B"])
        elif nombre.startswith("AZ"):
            ficha.color(colores["AZ"])
        ficha.pencolor("black")
        ficha.pensize(1)
        ficha.goto(x, y)
        ficha.speed(0)
        ficha.hideturtle()
        ficha.showturtle()
        fichas_obj[nombre] = ficha

        # Crea el turtle para el número
        num_turtle = RawTurtle(canvas)
        num_turtle.hideturtle()
        num_turtle.penup()
        num_turtle.goto(x, y - 9)  # Ajusta -5 para centrar el número
        num_turtle.pencolor("black")
        num_turtle.write(nombre[-1], align="center", font=("Arial", 12, "bold"))
        fichas_numeros[nombre] = num_turtle


colores_turno = ["V", "R", "B", "AZ"]



def elegir_color_inicial(ventana):
    try:
        if not ventana.winfo_exists():
            return None
    except tk.TclError:
        return None
    
    seleccion = {"color": None}

    top = tk.Toplevel(ventana)
    top.title("Elige el equipo que va a iniciar")
    top.geometry("550x250+850+400")
    top.resizable(False, False)
    top.configure(bg="#f0f4c3")
    top.grab_set()

    # Botón salir arriba a la derecha
    btn_salir = tk.Button(top, text="Salir", font=("Arial", 10, "bold"), bg="#e53935", fg="white", command=ventana.destroy)
    btn_salir.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)

    tk.Label(top, text="¿Qué equipo va a iniciar?", font=("Arial", 16, "bold"), bg="#f0f4c3").pack(pady=10)

    frame = tk.Frame(top, bg="#f0f4c3")
    frame.pack(pady=10)

    def set_color(color):
        seleccion["color"] = color
        top.destroy()

    colores = [
        ("Verde", "V", "#43a047"),
        ("Rojo", "R", "#e53935"),
        ("Blanco", "B", "#fafafa"),
        ("Azul", "AZ", "#1e88e5"),
    ]

    for nombre, valor, color_hex in colores:
        tk.Button(
            frame,
            text=nombre,
            width=12,
            height=2,
            font=("Arial", 12, "bold"),
            bg=color_hex,
            fg="black" if valor != "B" else "#333",
            command=lambda v=valor: set_color(v)
        ).pack(side=tk.LEFT, padx=10)

    def on_close():
        tk.messagebox.showinfo("Aviso", "Debes elegir un equipo para iniciar la partida o salir.")
    top.protocol("WM_DELETE_WINDOW", on_close)

    ventana.wait_window(top)
    return seleccion["color"]

color_inicial = None
while color_inicial not in colores_turno:
    color_inicial = elegir_color_inicial(ventana)
turno_actual = [colores_turno.index(color_inicial)]
longi=35.714285714285714285714285714286
camino_blanco = {
    "0": [(214, 70), (214, 105)], "1": [(179, 70),(179, 105)], "2": [(144,70),(144,105)], "3": [(109,60),(109,85)],
    "4": [(60, 110), (85,110)], "5": [(65,145),(100,145)], "6": [(65,180),(100,180)], "7": [(65,215),(100,215)], 
    "8": [(65,250),(100,250)], "9": [(65,285),(100,285)], "10": [(65,320),(100,320)], "11": [(65,358),(100,358)], 
    "12": [(-17,358),(17,358)], "13": [(-65,358),(-100,358)], "14": [(-65,320),(-100,320)], "15": [(-65,285),(-100,285)], 
    "16": [(-65,250),(-100,250)], "17": [(-65,215),(-100,215)], "18": [(-65,180),(-100,180)], "19": [(-65,145),(-100,145)], 
    "20": [(-60,110),(-85,110)], "21": [(-109,60),(-109,85)], "22": [(-144,70),(-144,105)], "23": [(-180, 70),(-180, 105)], 
    "24": [(-215, 70), (-215, 105)], "25": [(-250,70),(-250,105)], "26": [(-285,70),(-285,105)], "27": [(-320,70),(-320,105)], 
    "28": [(-358, 70),(-358,105)], "29": [(-358,-15),(-358,15)], "30": [(-358, -70),(-358,-105)], "31": [(-320,-70),(-320,-105)], 
    "32": [(-285,-70),(-285,-105)], "33": [(-250,-70),(-250,-105)], "34": [(-215, -70), (-215, -105)], "35": [(-180, -70),(-180, -105)], 
    "36": [(-144,-70),(-144,-105)], "37": [(-109,-60),(-109,-85)], "38": [(-60,-110),(-85,-110)], "39": [(-65,-145),(-100,-145)], 
    "40": [(-65,-180),(-100,-180)], "41": [(-65,-215),(-100,-215)], "42": [(-65,-250),(-100,-250)], "43": [(-65,-285),(-100,-285)], 
    "44": [(-65,-320),(-100,-320)], "45": [(-65,-358),(-100,-358)], "46": [(-17,-358),(17,-358)], "47": [(65,-358),(100,-358)], 
    "48": [(65,-320),(100,-320)], "49": [(65,-285),(100,-285)], "50": [(65,-250),(100,-250)], "51": [(65,-215),(100,-215)], 
    "52": [(65,-180),(100,-180)], "53": [(65,-145),(100,-145)], "54": [(60, -110), (85,-110)], "55": [(109,-60),(109,-85)], 
    "56": [(144,-70),(144,-105)], "57": [(179, -70),(179, -105)], "58": [(214, -70), (214, -105)], "59": [(250,-70),(250,-105)], 
    "60": [(285,-70),(285,-105)], "61": [(320,-70),(320,-105)], "62": [(358, -70),(358,-105)], "63": [(358,-15),(358,15)], "64": [(320,-15),(320,15)], "65": [(285,-15),(285,15)], 
    "66":[(250,-15),(285,15)], "67":[(215,-15),(215,15)], "68":[(180,-15),(180,15)], "69":[(144,-15),(144,15)], 
    "70":[(109,-15),(109,15)], "71":[(60,-15),(60,15)],
}

camino_rojo={
    "0": [(-65,215),(-100,215)], "1": [(-65,180),(-100,180)], "2": [(-65,145),(-100,145)], 
    "3": [(-60,110),(-85,110)], "4": [(-109,60),(-109,85)], "5": [(-144,70),(-144,105)], "6": [(-180, 70),(-180, 105)], 
    "7": [(-215, 70), (-215, 105)], "8": [(-250,70),(-250,105)], "9": [(-285,70),(-285,105)], "10": [(-320,70),(-320,105)], 
    "11": [(-358, 70),(-358,105)], "12": [(-358,-15),(-358,15)], "13": [(-358, -70),(-358,-105)], "14": [(-320,-70),(-320,-105)], 
    "15": [(-285,-70),(-285,-105)], "16": [(-250,-70),(-250,-105)], "17": [(-215, -70), (-215, -105)], "18": [(-180, -70),(-180, -105)], 
    "19": [(-144,-70),(-144,-105)], "20": [(-109,-60),(-109,-85)], "21": [(-60,-110),(-85,-110)], "22": [(-65,-145),(-100,-145)], 
    "23": [(-65,-180),(-100,-180)], "24": [(-65,-215),(-100,-215)], "25": [(-65,-250),(-100,-250)], "26": [(-65,-285),(-100,-285)], 
    "27": [(-65,-320),(-100,-320)], "28": [(-65,-358),(-100,-358)], "29": [(-17,-358),(17,-358)], "30": [(65,-358),(100,-358)], 
    "31": [(65,-320),(100,-320)], "32": [(65,-285),(100,-285)], "33": [(65,-250),(100,-250)], "34": [(65,-215),(100,-215)], 
    "35": [(65,-180),(100,-180)], "36": [(65,-145),(100,-145)], "37": [(60, -110), (85,-110)], "38": [(109,-60),(109,-85)], 
    "39": [(144,-70),(144,-105)], "40": [(179, -70),(179, -105)], "41": [(214, -70), (214, -105)], "42": [(250,-70),(250,-105)], 
    "43": [(285,-70),(285,-105)], "44": [(320,-70),(320,-105)], "45": [(358, -70),(358,-105)], "46": [(358,-15),(358,15)], 
    "47": [(358, 70),(358,105)], "48": [(320,70),(320,105)], "49": [(285,70),(285,105)], "50": [(250,70),(250,105)],
    "51": [(214, 70), (214, 105)], "52": [(179, 70),(179, 105)], "53": [(144,70),(144,105)], "54": [(109,60),(109,85)],
    "55": [(60, 110), (85,110)], "56": [(65,145),(100,145)], "57": [(65,180),(100,180)], "58": [(65,215),(100,215)], 
    "59": [(65,250),(100,250)], "60": [(65,285),(100,285)], "61": [(65,320),(100,320)], "62": [(65,358),(100,358)], 
    "63": [(-17,358),(17,358)], "64": [(-17,320),(17,320)], "65": [(-17,285),(17,285)], 
    "66":[(-17,250),(17,250)], "67":[(-17,215),(17,215)], "68":[(-17,180),(17,180)], "69":[(-17,145),(17,145)], 
    "70":[(-17,110),(17,110)], "71":[(-17,85),(17,85)],
}

camino_verde={
    "0": [(-215, -70), (-215, -105)], "1": [(-180, -70),(-180, -105)], 
    "2": [(-144,-70),(-144,-105)], "3": [(-109,-60),(-109,-85)], "4": [(-60,-110),(-85,-110)], "5": [(-65,-145),(-100,-145)], 
    "6": [(-65,-180),(-100,-180)], "7": [(-65,-215),(-100,-215)], "8": [(-65,-250),(-100,-250)], "9": [(-65,-285),(-100,-285)], 
    "10": [(-65,-320),(-100,-320)], "11": [(-65,-358),(-100,-358)], "12": [(-17,-358),(17,-358)], "13": [(65,-358),(100,-358)], 
    "14": [(65,-320),(100,-320)], "15": [(65,-285),(100,-285)], "16": [(65,-250),(100,-250)], "17": [(65,-215),(100,-215)], 
    "18": [(65,-180),(100,-180)], "19": [(65,-145),(100,-145)], "20": [(60, -110), (85,-110)], "21": [(109,-60),(109,-85)], 
    "22": [(144,-70),(144,-105)], "23": [(179, -70),(179, -105)], "24": [(214, -70), (214, -105)], "25": [(250,-70),(250,-105)], 
    "26": [(285,-70),(285,-105)], "27": [(320,-70),(320,-105)], "28": [(358, -70),(358,-105)], "29": [(358,-15),(358,15)], 
    "30": [(358, 70),(358,105)], "31": [(320,70),(320,105)], "32": [(285,70),(285,105)], "33": [(250,70),(250,105)],
    "34": [(214, 70), (214, 105)], "35": [(179, 70),(179, 105)], "36": [(144,70),(144,105)], "37": [(109,60),(109,85)],
    "38": [(60, 110), (85,110)], "39": [(65,145),(100,145)], "40": [(65,180),(100,180)], "41": [(65,215),(100,215)], 
    "42": [(65,250),(100,250)], "43": [(65,285),(100,285)], "44": [(65,320),(100,320)], "45": [(65,358),(100,358)], 
    "46": [(-17,358),(17,358)], "47": [(-65,358),(-100,358)], "48": [(-65,320),(-100,320)], "49": [(-65,285),(-100,285)], 
    "50": [(-65,250),(-100,250)], "51": [(-65,215),(-100,215)], "52": [(-65,180),(-100,180)], "53": [(-65,145),(-100,145)], 
    "54": [(-60,110),(-85,110)], "55": [(-109,60),(-109,85)], "56": [(-144,70),(-144,105)], "57": [(-180, 70),(-180, 105)], 
    "58": [(-215, 70), (-215, 105)], "59": [(-250,70),(-250,105)], "60": [(-285,70),(-285,105)], "61": [(-320,70),(-320,105)], 
    "62": [(-358, 70),(-358,105)], "63": [(-358,-15),(-358,15)], "64": [(-320,-15),(-320,15)], "65": [(-285,-15),(-285,15)], 
    "66":[(-250,-15),(-285,15)], "67":[(-215,-15),(-215,15)], "68":[(-180,-15),(-180,15)], "69":[(-144,-15),(-144,15)], 
    "70":[(-109,-15),(-109,15)], "71":[(-60,-15),(-60,15)],
}

camino_azul={
    "0": [(65,-215),(100,-215)], 
    "1": [(65,-180),(100,-180)], "2": [(65,-145),(100,-145)], "3": [(60, -110), (85,-110)], "4": [(109,-60),(109,-85)], 
    "5": [(144,-70),(144,-105)], "6": [(179, -70),(179, -105)], "7": [(214, -70), (214, -105)], "8": [(250,-70),(250,-105)], 
    "9": [(285,-70),(285,-105)], "10": [(320,-70),(320,-105)], "11": [(358, -70),(358,-105)], "12": [(358,-15),(358,15)], 
    "13": [(358, 70),(358,105)], "14": [(320,70),(320,105)], "15": [(285,70),(285,105)], "16": [(250,70),(250,105)],
    "17": [(214, 70), (214, 105)], "18": [(179, 70),(179, 105)], "19": [(144,70),(144,105)], "20": [(109,60),(109,85)],
    "21": [(60, 110), (85,110)], "22": [(65,145),(100,145)], "23": [(65,180),(100,180)], "24": [(65,215),(100,215)], 
    "25": [(65,250),(100,250)], "26": [(65,285),(100,285)], "27": [(65,320),(100,320)], "28": [(65,358),(100,358)], 
    "29": [(-17,358),(17,358)], "30": [(-65,358),(-100,358)], "31": [(-65,320),(-100,320)], "32": [(-65,285),(-100,285)], 
    "33": [(-65,250),(-100,250)], "34": [(-65,215),(-100,215)], "35": [(-65,180),(-100,180)], "36": [(-65,145),(-100,145)], 
    "37": [(-60,110),(-85,110)], "38": [(-109,60),(-109,85)], "39": [(-144,70),(-144,105)], "40": [(-180, 70),(-180, 105)], 
    "41": [(-215, 70), (-215, 105)], "42": [(-250,70),(-250,105)], "43": [(-285,70),(-285,105)], "44": [(-320,70),(-320,105)], 
    "45": [(-358, 70),(-358,105)], "46": [(-358,-15),(-358,15)], "47": [(-358, -70),(-358,-105)], "48": [(-320,-70),(-320,-105)], 
    "49": [(-285,-70),(-285,-105)], "50": [(-250,-70),(-250,-105)],"51": [(-215, -70), (-215, -105)], "52": [(-180, -70),(-180, -105)], 
    "53": [(-144,-70),(-144,-105)], "54": [(-109,-60),(-109,-85)], "55": [(-60,-110),(-85,-110)], "56": [(-65,-145),(-100,-145)], 
    "57": [(-65,-180),(-100,-180)], "58": [(-65,-215),(-100,-215)], "59": [(-65,-250),(-100,-250)], "60": [(-65,-285),(-100,-285)], 
    "61": [(-65,-320),(-100,-320)], "62": [(-65,-358),(-100,-358)], "63": [(-17,-358),(17,-358)], 
    "64": [(-17,-320),(17,-320)], "65": [(-17,-285),(17,-285)], 
    "66":[(-17,-250),(17,-250)], "67":[(-17,-215),(17,-215)], "68":[(-17,-180),(17,-180)], "69":[(-17,-145),(17,-145)], 
    "70":[(-17,-110),(17,-110)], "71":[(-17,-85),(17,-85)],
}

def caminos():
    camino_verde=[
    ]
    turtle_screen.up()
    turtle_screen.fillcolor("orange")
    turtle_screen.pensize(10)
    turtle_screen.goto(-70,30)
    #sacar_de_carcel("B")
    #mover_ficha_pista("B1", 71 - posicion_fichas["B1"], posi=0) 
    #mover_ficha_pista("B2",  - posicion_fichas["B2"], posi=0)  # B1 en casilla 5, posición 0
 # B1 en casilla 5, posición 0
    sacar_de_carcel("R")
    sacar_de_carcel("AZ")
    mover_ficha_pista("AZ1", 16 - posicion_fichas["AZ1"], posi=0)  # AZ1 en casilla 5, posición 0    
    mover_ficha_pista("AZ2", 16 - posicion_fichas["AZ2"], posi=0)  # AZ1 en casilla 5, posición 0    

    #colocar que los dados den 6 y 6
    dado1 = 6
    dado2 = 6
    # sacar_de_carcel("AZ")
    # sacar_de_carcel("V")



meta_verde = [(-25,0),(-70,0),(-70,30),(-70,-30)]
meta_rojo  = [(0,25),(0,70),[30,70],(-30,70)]
meta_blanco =[(25,0),(70,0),(70,30),(70,-30)]
meta_azul  = [(0,-25),(0,-70),(30,-70),(-30,-70)]

salida_fichas = {
    "V": 0,    
    "R": 17,   
    "B": 34,   
    "AZ": 51   
}

posicion_fichas = {
    "V1": None, "V2": None, "V3": None, "V4": None,
    "R1": None, "R2": None, "R3": None, "R4": None,
    "B1": None, "B2": None, "B3": None, "B4": None,
    "AZ1": None, "AZ2": None, "AZ3": None, "AZ4": None,
}

def coords_cerca(coord1, coord2, i=2):
    """Devuelve True si coord1 y coord2 están a menos de 'tolerancia' píxeles de distancia."""
    return abs(coord1[0] - coord2[0]) <= i and abs(coord1[1] - coord2[1]) <= i

def sacar_de_carcel(color):
    fichas_color = [f"{color}{i}" for i in range(1, 5)]
    posiciones_salida_color = posiciones_salida[color]
    salidas = 0

    if color == "V":
        camino = camino_verde
    elif color == "R":
        camino = camino_rojo
    elif color == "B":
        camino = camino_blanco
    elif color == "AZ":
        camino = camino_azul
    else:
        raise ValueError(f"Color de ficha desconocido: {color}")

    for nombre_ficha in fichas_color:
        if posicion_fichas[nombre_ficha] is None:
            if salidas < 2:
                ficha = fichas_obj.get(nombre_ficha)
                if ficha:
                    salida_coord = posiciones_salida_color[salidas]
                    # Buscar TODAS las fichas rivales en la salida (sin importar si es casilla segura)
                    fichas_en_salida = []
                    for otra_ficha, pos in posicion_fichas.items():
                        if otra_ficha != nombre_ficha and pos is not None and not fichas_en_meta[otra_ficha]:
                            color_otra = otra_ficha[:2] if otra_ficha[:2] == "AZ" else otra_ficha[0]
                            if color_otra != color:
                                # Busca la coordenada de la ficha rival
                                if color_otra == "V":
                                    camino_otra = camino_verde
                                elif color_otra == "R":
                                    camino_otra = camino_rojo
                                elif color_otra == "B":
                                    camino_otra = camino_blanco
                                elif color_otra == "AZ":
                                    camino_otra = camino_azul
                                else:
                                    continue
                                coord_otra = camino_otra[str(pos)][0]
                                # CAMBIO: usar coords_cerca en vez de ==
                                if coords_cerca(coord_otra, salida_coord):
                                    fichas_en_salida.append(otra_ficha)
                    # Mandar a la cárcel todas las fichas rivales encontradas (aunque sea casilla segura)
                    for ficha_rival in fichas_en_salida:
                        mandar_carcel(ficha_rival)

                    ficha.goto(salida_coord)
                    num_turtle = fichas_numeros[nombre_ficha]
                    num_turtle.clear()
                    x, y = salida_coord
                    num_turtle.goto(x, y - 9)
                    num_turtle.write(nombre_ficha[-1], align="center", font=("Arial", 12, "bold")) 
                    lugar = None
                    for k, v in camino.items():
                        if salida_coord in v:
                            lugar = int(k)
                            break
                    if lugar is None:
                        lugar = salida_fichas[color]
                    posicion_fichas[nombre_ficha] = lugar
                    pasos_fichas[nombre_ficha] = 0
                    salidas += 1
            else:
                break

def sacar_una_ficha_de_carcel(color):
    fichas_color = [f"{color}{i}" for i in range(1, 5)]
    posiciones_salida_color = posiciones_salida[color]

    if color == "V":
        camino = camino_verde
    elif color == "R":
        camino = camino_rojo
    elif color == "B":
        camino = camino_blanco
    elif color == "AZ":
        camino = camino_azul
    else:
        raise ValueError(f"Color de ficha desconocido: {color}")

    for i, nombre_ficha in enumerate(fichas_color):
        if posicion_fichas[nombre_ficha] is None:
            ficha = fichas_obj[nombre_ficha]
            ficha.goto(posiciones_salida_color[0])  # Solo la primera posición
            for k, v in camino.items():
                if posiciones_salida_color[0] in v:
                    lugar = int(k)
                    break
            else:
                lugar = salida_fichas[color]

            posicion_fichas[nombre_ficha] = lugar
            pasos_fichas[nombre_ficha] = 0
            break  # Solo saca una ficha



pasos_fichas = {
    "V1": 0, "V2": 0, "V3": 0, "V4": 0,
    "R1": 0, "R2": 0, "R3": 0, "R4": 0,
    "B1": 0, "B2": 0, "B3": 0, "B4": 0,
    "AZ1": 0, "AZ2": 0, "AZ3": 0, "AZ4": 0,
}

def mandar_carcel(nombre_ficha):
    ficha = fichas_obj[nombre_ficha]
    destino = posiciones_carcel[nombre_ficha]
    pasos = 10
    x0, y0 = ficha.pos()
    x1, y1 = destino
    for i in range(1, pasos + 1):
        ficha.goto(x0 + (x1 - x0) * i / pasos, y0 + (y1 - y0) * i / pasos)
        ventana.update()
    ficha.goto(destino)
    posicion_fichas[nombre_ficha] = None
    pasos_fichas[nombre_ficha] = 0
    num_turtle = fichas_numeros[nombre_ficha]
    num_turtle.clear()
    num_turtle.goto(x1, y1 - 9)
    num_turtle.write(nombre_ficha[-1], align="center", font=("Arial", 12, "bold"))
    posicion_fichas[nombre_ficha] = None
    pasos_fichas[nombre_ficha] = 0

fichas_en_meta = {
    "V1": False, "V2": False, "V3": False, "V4": False,
    "R1": False, "R2": False, "R3": False, "R4": False,
    "B1": False, "B2": False, "B3": False, "B4": False,
    "AZ1": False, "AZ2": False, "AZ3": False, "AZ4": False,
}

CASILLAS_SEGURAS = [0, 7, 12, 17, 24, 29, 34, 41, 46, 51, 58, 63]  
def mover_ficha_pista(nombre_ficha, pasos, posi=0):
    # Si ya está en meta, no se mueve
    if fichas_en_meta[nombre_ficha]:
        return False

    captura = False
    color = nombre_ficha.rstrip("1234")
    if color == "V":
        camino = camino_verde
        meta_coord = meta_verde
    elif color == "R":
        camino = camino_rojo
        meta_coord = meta_rojo
    elif color == "B":
        camino = camino_blanco
        meta_coord = meta_blanco
    elif color == "AZ":
        camino = camino_azul
        meta_coord = meta_azul
    else:
        raise ValueError(f"Color de ficha desconocido: {color}")

    if posicion_fichas[nombre_ficha] is None:
        return False

    casilla_actual = pasos_fichas[nombre_ficha]
    casillas_restantes = 71 - casilla_actual

    # Solo llega si saca exactamente lo necesario
    if pasos == casillas_restantes:
        # Busca la primera posición libre en meta para ese color
        for i, libre in enumerate(meta_coord):
            ocupada = False
            for ficha, en_meta in fichas_en_meta.items():
                if en_meta and fichas_obj[ficha].pos() == libre:
                    ocupada = True
                    break
            if not ocupada:
                fichas_obj[nombre_ficha].goto(libre)
                # Mueve el número junto con la ficha a la meta
                num_turtle = fichas_numeros[nombre_ficha]
                num_turtle.clear()
                x, y = libre
                num_turtle.goto(x, y - 9)
                num_turtle.write(nombre_ficha[-1], align="center", font=("Arial", 12, "bold"))
                fichas_en_meta[nombre_ficha] = True
                posicion_fichas[nombre_ficha] = 71
                pasos_fichas[nombre_ficha] = 71
                print(f"¡Felicidades! {nombre_ficha} ha llegado a la meta.")
                # --- NUEVO: Revisar si todas las fichas de ese color están en meta ---
                fichas_color = [f"{color}{i}" for i in range(1, 5)]
                if all(fichas_en_meta[f] for f in fichas_color):
    # Ventana de ganador personalizada
                    ventana_ganador = tk.Toplevel(ventana)
                    ventana_ganador.title("¡Fin del juego!")
                    ventana_ganador.geometry("400x200+1000+500")
                    ventana_ganador.resizable(False, False)
                    ventana_ganador.configure(bg={
                        "V": "#a8ff60",   # Verde claro
                        "R": "#ffb3b3",   # Rojo claro
                        "B": "#f5f5f5",   # Blanco
                        "AZ": "#b3e5fc"   # Azul claro
                    }[color])
                    colores_texto = {
                        "V": "#006400",
                        "R": "#b71c1c",
                        "B": "#333333",
                        "AZ": "#01579b"
                    }
                    tk.Label(
                        ventana_ganador,
                        text=f"¡FELICIDADES!\nEl equipo {color} ha ganado",
                        font=("Arial", 22, "bold"),
                        fg=colores_texto[color],
                        bg=ventana_ganador["bg"]
                    ).pack(expand=True, fill="both", pady=30)
                    tk.Button(
                        ventana_ganador,
                        text="Salir",
                        font=("Arial", 14, "bold"),
                        bg="#ffd600",
                        fg="#333",
                        command=ventana.quit
                    ).pack(pady=10)
                    ventana_ganador.grab_set()
                return True
        # Si no hay espacio en meta, no se mueve
        return False
    elif pasos > casillas_restantes:
        # No puede moverse, se pasa de meta
        return False

    # Movimiento normal
    pasos_fichas[nombre_ficha] += pasos
    total_casillas = len(camino)
    lugar = pasos_fichas[nombre_ficha] % total_casillas

    destino_coord = camino[str(lugar)][0]

    # Buscar todas las fichas rivales en la casilla destino (si no es segura)
    fichas_enemigas = []
    if lugar not in CASILLAS_SEGURAS:
        for ficha, pos in posicion_fichas.items():
            if ficha != nombre_ficha and pos is not None and not fichas_en_meta[ficha]:
                color_ficha = ficha[:2] if ficha[:2] == "AZ" else ficha[0]
                if color_ficha != color:
                    if color_ficha == "V":
                        camino_ficha = camino_verde
                    elif color_ficha == "R":
                        camino_ficha = camino_rojo
                    elif color_ficha == "B":
                        camino_ficha = camino_blanco
                    elif color_ficha == "AZ":
                        camino_ficha = camino_azul
                    else:
                        continue
                    coord_ficha = camino_ficha[str(pos)][0]
                    if coord_ficha == destino_coord:
                        fichas_enemigas.append(ficha)
        # Mandar todas a la cárcel
        for ficha_enemiga in fichas_enemigas:
            mandar_carcel(ficha_enemiga)
        if fichas_enemigas:
            captura = True

    posicion_fichas[nombre_ficha] = lugar

    posi_destino = 0
    for ficha, pos in posicion_fichas.items():
        if ficha != nombre_ficha and pos is not None and not fichas_en_meta[ficha]:
            color_ficha = ficha[:2] if ficha[:2] == "AZ" else ficha[0]
            if color_ficha == "V":
                camino_ficha = camino_verde
            elif color_ficha == "R":
                camino_ficha = camino_rojo
            elif color_ficha == "B":
                camino_ficha = camino_blanco
            elif color_ficha == "AZ":
                camino_ficha = camino_azul
            else:
                continue
            coord_ficha = camino_ficha[str(pos)][0]
            if coord_ficha == destino_coord:
                posi_destino = 1
                break

    fichas_obj[nombre_ficha].goto(destino_coord if posi_destino == 0 else camino[str(lugar)][1])
    # Mueve el número junto con la ficha
    num_turtle = fichas_numeros[nombre_ficha]
    num_turtle.clear()
    x, y = fichas_obj[nombre_ficha].pos()
    num_turtle.goto(x, y - 9)  
    num_turtle.write(nombre_ficha[-1], align="center", font=("Arial", 12, "bold"))
    return captura
def Juego():
    dibujar_cuadro()
    dibujar_verde()
    dibujar_rojo()
    dibujar_blanco()
    dibujar_azul()
    agregar_imagenes()
    seguros()
    casillas_verde()
    casillas_rojo()
    casillas_blanco()
    casillas_azul()
    delinear()
    etiquetar_casillas()
    #caminos()
    
intentos_iniciales = {
    "R": 0,
    "V": 0,
    "B": 0,
    "AZ": 0
}
colores_ya_jugaron = {
    "R": False,
    "V": False,
    "B": False,
    "AZ": False
}

turno_ficha = {
    "V": [0],
    "R": [0],
    "B": [0],
    "AZ": [0]
}














def siguiente_ficha_fuera(color):
    """Devuelve el nombre de la siguiente ficha fuera de la cárcel para mover, o None si todas están en la cárcel."""
    fichas = [f"{color}{i}" for i in range(1, 5)]
    # Empieza desde el turno actual de ficha
    start = turno_ficha[color][0]
    for i in range(4):
        lugar = (start + i) % 4
        nombre = fichas[lugar]
        if posicion_fichas[nombre] is not None:
            turno_ficha[color][0] = (lugar + 1) % 4  # Avanza el turno para la próxima vez
            return nombre
    return None  # Todas en la cárcel
def seleccionar_movimiento(fichas_fuera, dado1, dado2, callback):
    ventana_sel = tk.Toplevel(ventana)
    ventana_sel.title("Selecciona movimiento")
    ventana_sel.geometry("400x300+1000+500")
    ventana_sel.resizable(False, False)
    ventana_sel.grab_set()
    
    # Mensaje emergente al intentar cerrar
    def on_close():
        messagebox.showinfo("Aviso", "Debes seleccionar un movimiento para continuar.")
    ventana_sel.protocol("WM_DELETE_WINDOW", on_close)

    # Bloquear cierre por la X y atajos de teclado
    ventana_sel.protocol("WM_DELETE_WINDOW", lambda: None)
    def bloquear_cierre(event=None):
        return "break"
    ventana_sel.bind("<Alt-F4>", bloquear_cierre)
    ventana_sel.bind("<Escape>", bloquear_cierre)
    ventana_sel.bind("<Control-w>", bloquear_cierre)
    ventana_sel.bind("<Control-q>", bloquear_cierre)
    
    def limpiar_seleccion():
        seleccion["ficha_total"].set("")
        seleccion["ficha1"].set("")
        seleccion["ficha2"].set("")

    tk.Button(ventana_sel, text="Limpiar selección", command=limpiar_seleccion, bg="#b2ebf2", fg="#004d40").pack(pady=5)

    
    ventana_sel.configure(bg="#e0f7fa")  # Celeste claro, puedes cambiar el color

    # Fijar la ventana para que no se pueda mover
      # Misma posición que arriba

    

    tk.Label(ventana_sel, text=f"Dados: {dado1} y {dado2}", font=("Arial", 12, "bold"), bg="#e0f7fa", fg="#006064").pack(pady=5)

    seleccion = {"ficha1": tk.StringVar(), "ficha2": tk.StringVar(), "ficha_total": tk.StringVar()}

    tk.Label(ventana_sel, text="Mover ambos dados con una ficha:", bg="#e0f7fa", fg="#004d40").pack()
    menu_total = tk.OptionMenu(ventana_sel, seleccion["ficha_total"], *fichas_fuera)
    menu_total.configure(bg="#b2ebf2", fg="#004d40", activebackground="#4dd0e1")
    menu_total.pack()

    tk.Label(ventana_sel, text="O repartir los dados entre dos fichas:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
    frame = tk.Frame(ventana_sel, bg="#e0f7fa")
    frame.pack()
    tk.Label(frame, text=f"Ficha para {dado1} pasos:", bg="#e0f7fa", fg="#00695c").grid(row=0, column=0)
    op1 = tk.OptionMenu(frame, seleccion["ficha1"], *fichas_fuera)
    op1.configure(bg="#b2ebf2", fg="#004d40", activebackground="#4dd0e1")
    op1.grid(row=0, column=1)
    tk.Label(frame, text=f"Ficha para {dado2} pasos:", bg="#e0f7fa", fg="#00695c").grid(row=1, column=0)
    op2 = tk.OptionMenu(frame, seleccion["ficha2"], *fichas_fuera)
    op2.configure(bg="#b2ebf2", fg="#004d40", activebackground="#4dd0e1")
    op2.grid(row=1, column=1)

    def confirmar():
        ficha_total = seleccion["ficha_total"].get()
        ficha1 = seleccion["ficha1"].get()
        ficha2 = seleccion["ficha2"].get()
        movimientos = []

        # Si selecciona mover todo con una ficha, no debe haber nada en los otros
        if ficha_total:
            if ficha1 or ficha2:
                messagebox.showerror("Error", "No puedes seleccionar ambas opciones a la vez.")
                return
            movimientos.append((ficha_total, dado1 + dado2))
        else:
            # Si el usuario selecciona repartir, debe elegir dos fichas distintas y ambas deben estar seleccionadas
            if ficha1 and ficha2 and ficha1 != ficha2:
                movimientos.append((ficha1, dado1))
                movimientos.append((ficha2, dado2))
            else:
                messagebox.showerror("Error", "¡Debes seleccionar dos fichas distintas para repartir!")
                return

        if not movimientos:
            messagebox.showerror("Error", "¡Debes seleccionar al menos una opción!")
            return

        ventana_sel.destroy()
        callback(movimientos)

    tk.Button(ventana_sel, text="Confirmar", command=confirmar, bg="#00838f", fg="white", activebackground="#4dd0e1").pack(pady=10)













def enviar_ficha_mas_lejana_a_meta(color):
    """
    Envía la ficha de 'color' más lejana a la meta directamente a la meta.
    """
    # Lista de fichas de ese color que no están en la cárcel ni en meta
    fichas_color = [f"{color}{i}" for i in range(1, 5)]
    fichas_fuera = [
        ficha for ficha in fichas_color
        if posicion_fichas[ficha] is not None and not fichas_en_meta[ficha]
    ]
    if not fichas_fuera:
        return  # No hay fichas para mover

    # Buscar la ficha con menor avance (más lejos de la meta)
    ficha_mas_lejana = min(fichas_fuera, key=lambda f: pasos_fichas[f])
    # Llevarla a la meta (elige la primera posición libre)
    if color == "V":
        meta_coord = meta_verde
    elif color == "R":
        meta_coord = meta_rojo
    elif color == "B":
        meta_coord = meta_blanco
    elif color == "AZ":
        meta_coord = meta_azul
    else:
        return

    for pos_meta in meta_coord:
        ocupada = False
        for ficha, en_meta in fichas_en_meta.items():
            if en_meta and fichas_obj[ficha].pos() == pos_meta:
                ocupada = True
                break
        if not ocupada:
            fichas_obj[ficha_mas_lejana].goto(pos_meta)
            num_turtle = fichas_numeros[ficha_mas_lejana]
            num_turtle.clear()
            x, y = pos_meta
            num_turtle.goto(x, y - 9)
            num_turtle.write(ficha_mas_lejana[-1], align="center", font=("Arial", 12, "bold"))
            fichas_en_meta[ficha_mas_lejana] = True
            posicion_fichas[ficha_mas_lejana] = 71
            pasos_fichas[ficha_mas_lejana] = 71
            break

dobles_consecutivos = {
    "V": 0,
    "R": 0,
    "B": 0,
    "AZ": 0
}



def mover_por_dados(dado1, dado2, frame_dados):
    color = colores_turno[turno_actual[0] % 4]
    todas_en_carcel = all(
        posicion_fichas[f"{color}{i}"] is None or fichas_en_meta[f"{color}{i}"]
        for i in range(1, 5)
    )
    if todas_en_carcel:
        intentos_iniciales[color] += 1
        print(f"{color}: intento {intentos_iniciales[color]} para sacar dobles.")

        if dado1 == dado2:
            dobles_consecutivos[color] += 1
            if dobles_consecutivos[color] == 3:
                enviar_ficha_mas_lejana_a_meta(color)
                messagebox.showinfo("¡Regla de 3 dobles!", f"¡{color} sacó 3 veces dobles! Su ficha más lejana va a la meta.")
                dobles_consecutivos[color] = 0
            sacar_de_carcel(color)
            print(f"{color}: ¡Sacó dobles! Fichas liberadas.")
            intentos_iniciales[color] = 0
            # Si aún quedan fichas en la cárcel, puede volver a tirar
            if any(posicion_fichas[f"{color}{i}"] is None for i in range(1, 5)):
                print(f"{color}: aún quedan fichas en la cárcel, puede volver a tirar.")
                # No cambies el turno, vuelve a lanzar dados
            else:
                turno_actual[0] += 1
        else:
            dobles_consecutivos[color] = 0
            if intentos_iniciales[color] >= 3:
                print(f"{color}: no logró sacar dobles en 3 intentos. Pierde el turno.")
                intentos_iniciales[color] = 0
                turno_actual[0] += 1
            else:
                print(f"{color}: sigue intentando sacar dobles (turno adicional).")
        frame_dados.destroy()
        siguiente_color = colores_turno[turno_actual[0] % 4]
        dados.crear_panel_dados(ventana, mover_por_dados, turno=siguiente_color)
    else:
        fichas_fuera = [f"{color}{i}" for i in range(1, 5) if posicion_fichas[f"{color}{i}"] is not None and not fichas_en_meta[f"{color}{i}"]]
        def aplicar_movimientos(movimientos):
            for ficha, pasos in movimientos:
                mover_ficha_pista(ficha, pasos)
                print(f"{color}: mueve {ficha} {pasos} pasos.")
            # Lógica de dobles y turnos:
            if dado1 == dado2:
                dobles_consecutivos[color] += 1
                if dobles_consecutivos[color] == 3:
                    enviar_ficha_mas_lejana_a_meta(color)
                    messagebox.showinfo("¡Regla de 3 dobles!", f"¡{color} sacó 3 veces dobles! Su ficha más lejana va a la meta.")
                    dobles_consecutivos[color] = 0
                if any(posicion_fichas[f"{color}{i}"] is None for i in range(1, 5)):
                    sacar_de_carcel(color)
                    print(f"{color}: sacó dobles y aún quedan fichas en la cárcel, puede volver a tirar.")
                else:
                    print(f"{color}: sacó dobles pero ya no quedan fichas en la cárcel, juega de nuevo.")
            else:
                dobles_consecutivos[color] = 0
                turno_actual[0] += 1
            frame_dados.destroy()
            siguiente_color = colores_turno[turno_actual[0] % 4]
            dados.crear_panel_dados(ventana, mover_por_dados, turno=siguiente_color)

        if len(fichas_fuera) == 1:
            ficha = fichas_fuera[0]
            color_ficha = ficha[:2] if ficha[:2] == "AZ" else ficha[0]
            if color_ficha == "V":
                tramo_final = range(63, 72)
            elif color_ficha == "R":
                tramo_final = range(63, 72)
            elif color_ficha == "B":
                tramo_final = range(63, 72)
            elif color_ficha == "AZ":
                tramo_final = range(63, 72)
            else:
                tramo_final = []

            # Verifica si la ficha está en el tramo final
            if posicion_fichas[ficha] in tramo_final:
                # Mostrar ventana para elegir dado1, dado2 o suma
                def elegir_dado():
                    ventana_dado = tk.Toplevel(ventana)
                    ventana_dado.title("Elige el dado a usar")
                    ventana_dado.geometry("300x200+1000+500")
                    ventana_dado.resizable(False, False)
                    ventana_dado.grab_set()
                    tk.Label(ventana_dado, text=f"¿Con qué dado quieres mover la ficha {ficha}?", font=("Arial", 12, "bold")).pack(pady=10)
                    def mover_con(pasos):
                        ventana_dado.destroy()
                        aplicar_movimientos([(ficha, pasos)])
                    tk.Button(ventana_dado, text=f"Usar dado 1 ({dado1})", command=lambda: mover_con(dado1)).pack(pady=5)
                    tk.Button(ventana_dado, text=f"Usar dado 2 ({dado2})", command=lambda: mover_con(dado2)).pack(pady=5)
                    tk.Button(ventana_dado, text=f"Usar suma ({dado1 + dado2})", command=lambda: mover_con(dado1 + dado2)).pack(pady=5)
                elegir_dado()
            else:
                aplicar_movimientos([(ficha, dado1 + dado2)])
        else:
            seleccionar_movimiento(fichas_fuera, dado1, dado2, aplicar_movimientos)    # Cerrar el panel y preparar siguiente
    frame_dados.destroy()
    siguiente_color = colores_turno[turno_actual[0] % 4]
    dados.crear_panel_dados(ventana, mover_por_dados, turno=siguiente_color)







try:
    Juego()
    siguiente_color = colores_turno[turno_actual[0] % 4]
    dados.crear_panel_dados(ventana, mover_por_dados, turno=color_inicial)
    ventana.mainloop()
except Exception:
    pass  # Oculta cualquier error al cerrar rápido