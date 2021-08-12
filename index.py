import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import askyesno

listaProductos=[]
listaTiendas=[{"nombreTienda":"Carrefour","listaP":[]}]
carrito=[]
total=0

#Colores
mainBgColor = "#f8f4ff"
blue = "#2a52be"
green = "#00ff7f"
red ="#e32636"
white = "#f2f3f4"
warning="#ffd700"

def cargarDatos():
    dictProducto={"producto":"","precio":0.0,"existencia":0}
    index = 0
    stock = open("stock.txt","r+")
    lines = stock.readlines()
    if(lines):
        for line in lines:
            index+=1       
            if index <= 3:
                if index == 1:
                    contenido = line.split()
                    producto = contenido[0]
                    
                    dictProducto["producto"] = producto
                elif index == 2:
                    contenido = line.split()
                    precio = contenido[1]
                    
                    dictProducto["precio"] = float(precio)
                elif index == 3:
                    contenido = line.split()
                    existencia = contenido[0]
                    
                    dictProducto["existencia"] = int(existencia)
            if dictProducto["producto"] and dictProducto["precio"] and dictProducto["existencia"]:
                for tienda in listaTiendas:           
                    tienda["listaP"].append(dictProducto)
                dictProducto={"producto":"","precio":0.0,"existencia":0}
            if index == 4:
                index = 0
        print("Stock cargado correctamente!",tienda["listaP"])
    stock.close()

def btnVolver(ventana):
    def cerrar(ventana):
        ventana.destroy()
        return
    volver= tk.Button(ventana,text="Volver",font=("Raleway",8,"bold"), background=blue, foreground=white, command=lambda: cerrar(ventana))
    volver.pack(pady=2)
def crearProducto():
    encontrado = False
    global nombre
    global precio
    global existencia
    global ventanaProductos    
    dictProducto={"producto":"","precio":0.0,"existencia":0}  
    dictProducto["producto"]=nombre    
    dictProducto["precio"]=float(precio)    
    dictProducto["existencia"]=int(existencia)
                    
    for t in listaTiendas:        
        for producto in t["listaP"]:          
            if nombre==producto["producto"]:
                producto["existencia"] += int(existencia)
                encontrado = True
    if(encontrado == False):
        for tienda in listaTiendas:           
            tienda["listaP"].append(dictProducto)
            print(tienda["listaP"])

        def destroyLbl():
            exito.pack_forget()
            return
            
        exito = tk.Label(ventanaProductos, text=f"Producto {nombre} agregado con exito!", background=green)
        exito.pack(padx=10, pady=5)

        ventanaProductos.after(1700,destroyLbl)   
    return

def buscarProducto(busqueda):

    global ventanaBuscar
    encontrado=False    
    def destroyLbl():        
        find.pack_forget()
        productoN.pack_forget()
        productoP.pack_forget()
        productoE.pack_forget()
        eliminar.pack_forget()
        return
    for tienda in listaTiendas:                        
        for producto in tienda["listaP"]:            
            if producto['producto'] == busqueda:                   
                encontrado=True
                nombreP = producto['producto']
                precioP = producto['precio']
                existenciaP = producto['existencia'] 
    def eliminarP():
        global busqueda
        for tienda in listaTiendas:                        
            for producto in tienda["listaP"]:            
                if producto['producto'] == busqueda:
                    tienda["listaP"].remove(producto)
                    print(f"{nombreP} eliminado!")
                    eliminado = tk.Label(ventanaBuscar, text="Producto eliminado!", background=red, foreground=white)
                    eliminado.pack(padx=10, pady=5)

        def destroyLbl():            
            eliminado.pack_forget()
            return
        ventanaBuscar.after(500,destroyLbl)   


    if(encontrado):
        find = tk.Label(ventanaBuscar, text=f"Se encontró {busqueda} con exito!", background=green)
        find.pack(padx=10, pady=5)
        productoN = tk.Label(ventanaBuscar, text=nombreP, background=mainBgColor)
        productoP = tk.Label(ventanaBuscar, text=f"${precioP}", background=mainBgColor)
        productoE = tk.Label(ventanaBuscar, text=f"{existenciaP} unidades en stock", background=mainBgColor)
        eliminar= tk.Button(ventanaBuscar, text=" Eliminar ",font=("Raleway",8,"bold"),background=red,foreground=white, command=eliminarP)
        productoN.pack()
        productoP.pack()
        productoE.pack()
        eliminar.pack()
        

    else:
        find = tk.Label(ventanaBuscar, text=f"No se encontró ningún producto {busqueda}", background=red)
        find.pack(padx=10, pady=5)
    ventanaBuscar.after(2700,destroyLbl)
    return

def AgregarACarrito(busqueda):
    global ventanaAgregarCarrito
    encontrado=False

    for tienda in listaTiendas:                        
        for producto in tienda["listaP"]:           
            if producto['producto'] == busqueda:                   
                encontrado=True
                nombreP = producto['producto']
                precioP = producto['precio']
                existenciaP = producto['existencia']
    if(encontrado):
        find = tk.Label(ventanaAgregarCarrito, text=f"Se encontró {busqueda} con exito!", background=green)
        find.pack(padx=10, pady=5)
        productoN = tk.Label(ventanaAgregarCarrito, text=nombreP, background=mainBgColor)
        productoP = tk.Label(ventanaAgregarCarrito, text=f"${precioP}", background=mainBgColor)
        productoE = tk.Label(ventanaAgregarCarrito, text=f"{existenciaP} unidades en stock", background=mainBgColor)
        productoN.pack()
        productoP.pack()
        productoE.pack()
        cantCompraLbl=tk.Label(ventanaAgregarCarrito,text=f"¿Cuantas unidades de {nombreP} quiere comprar? ({existenciaP} en stock)", background=mainBgColor)
        cantCompraLbl.pack(pady=1)
        cantCompraEntry=tk.Entry(ventanaAgregarCarrito, background=white, border=0, foreground=blue,font="8")
        cantCompraEntry.pack(pady=1)           
        
        def confirmar():
            uCompra =int(cantCompraEntry.get())
            def destroyLbl():        
                find.pack_forget()
                productoN.pack_forget()
                productoP.pack_forget()
                productoE.pack_forget()
                alert.pack_forget()
                cantCompraLbl.pack_forget()
                cantCompraEntry.pack_forget()
                carritoBtn.pack_forget()
                return
            try:               
                
                if uCompra <= existenciaP:
                    carritoP={"producto":"","precio":0.0,"unidades":0}
                    carritoP["producto"]=nombreP
                    carritoP["precio"]=precioP
                    carritoP["unidades"]=uCompra
                    carrito.append(carritoP)
                    alert= tk.Label(ventanaAgregarCarrito, text=f"Se agregó {nombreP} al carrito con exito!", background=green)
                    alert.pack(padx=10, pady=5)
                    print(carrito)          
                    ventanaAgregarCarrito.after(1500,destroyLbl)
                else:
                    alert = tk.Label(ventanaAgregarCarrito, text="No hay suficiente existencia para agregar esa cantidad a carrito!", background=red)
                    alert.pack(padx=10, pady=5)
                    def destroyLbl():
                        alert.pack_forget()
                        return
                    ventanaAgregarCarrito.after(1500,destroyLbl)
            except:        
                alert = tk.Label(ventanaAgregarCarrito, text="Algo salio mal!", background=red)
                alert.pack(padx=10, pady=5)
                def destroyLbl():
                    alert.pack_forget()
                    return
                ventanaAgregarCarrito.after(1500,destroyLbl)
                
  
        carritoBtn = tk.Button(ventanaAgregarCarrito, text="Confirmar",font=("Raleway",8,"bold"), background=blue,foreground=white,command=confirmar)
        carritoBtn.pack()

    else:
        find = tk.Label(ventanaAgregarCarrito, text=f"No se encontró ningún producto {busqueda}", background=red)
        find.pack(padx=10, pady=5)
    
    return      


cargarDatos()
ventana = tk.Tk()
ventana.geometry("800x550")
ventana.title("Supermercado")
ventana.config(background=mainBgColor)
logo = tk.PhotoImage(file="carrefour.png")    
btnCrear = tk.PhotoImage(file="crearProd.png")
btnBuscar = tk.PhotoImage(file="buscarProd.png")
btnAgCarrito = tk.PhotoImage(file="agCarrito.png")
btnCarrito = tk.PhotoImage(file="carrito.png")
btnStock = tk.PhotoImage(file="stock.png")


label = tk.Label(ventana, text="Bienvenido al supermercado", bg=blue, foreground= white, font="Raleway")
label.pack(fill=tk.X, pady=5)

labelLogo= tk.Label(ventana, image=logo, background=mainBgColor)
labelLogo.pack()

label1 = tk.Label(ventana, text="2021 ® ", bg=blue, foreground= white, font="Raleway")
label1.pack(fill=tk.X, side=tk.BOTTOM)

def vProducto():
    global ventanaProductos
    label1.config(text="Ventana crear producto ejecutada con exito!",background=green, foreground="black")
    ventanaProductos = tk.Tk()    
    ventanaProductos.geometry("500x500")
    ventanaProductos.title("Crear producto")
    ventanaProductos.config(background=mainBgColor)
    titulo = tk.Label(ventanaProductos, text="INGRESE EL PRODUCTO",font=("Raleway",12,"bold"), background=mainBgColor)
    titulo.pack(pady=5)
    spacer = tk.Label(ventanaProductos,height=2, background=mainBgColor)
    spacer.pack(fill=tk.X)
    txtNombre = tk.Label(ventanaProductos,text="Ingrese el nombre del producto", background=mainBgColor)
    nombreEntry = tk.Entry(ventanaProductos, background=white, border=0, foreground=blue,font="8")
    txtNombre.pack()
    nombreEntry.pack()
    txtPrecio = tk.Label(ventanaProductos,text="Ingrese el precio del producto", background=mainBgColor)
    precioEntry = tk.Entry(ventanaProductos, background=white, border=0, foreground=blue,font="8")
    txtPrecio.pack()
    precioEntry.pack()
    txtExistencia = tk.Label(ventanaProductos,text="Ingrese la cantidad en stock", background=mainBgColor)
    existenciaEntry = tk.Entry(ventanaProductos, background=white, border=0, foreground=blue ,font="8")
    txtExistencia.pack()
    existenciaEntry.pack()
    def data():
        global precio
        global nombre
        global existencia
        global exito
        existencia = existenciaEntry.get()
        nombre = nombreEntry.get()
        precio = precioEntry.get()
        print(nombre,precio,existencia)
        if(nombre and precio and existencia):
            try:
                crearProducto()               
            except:
                exito = tk.Label(ventanaProductos, text="Algo salió mal!", background=red, foreground="#f2f3f4")
                exito.pack(padx=10, pady=5)
            nombreEntry.delete('0', tk.END)
            precioEntry.delete('0', tk.END )
            existenciaEntry.delete('0', tk.END)
        else:
            exito = tk.Label(ventanaProductos, text="Algo salió mal!", background=red, foreground="#f2f3f4")
            exito.pack(padx=10, pady=5)

        def destroyLbl():            
            exito.pack_forget()
            return
        ventanaProductos.after(1700,destroyLbl)     

        return existencia, nombre, precio
    
    confirmar = tk.Button(ventanaProductos,text="Agregar producto",font=("Raleway",8,"bold"), background=blue,foreground=white, command=data)
    confirmar.pack(pady = 10)

def vBuscar():
    global ventanaBuscar
    label1.config(text="Ventana buscar producto ejecutada con exito!",background=green)
    ventanaBuscar = tk.Tk()
    ventanaBuscar.title("Buscar producto")
    ventanaBuscar.geometry("500x500")
    ventanaBuscar.config(background=mainBgColor)
    titulo = tk.Label(ventanaBuscar, text="BUSCAR PRODUCTO",font=("Raleway",12,"bold"), background=mainBgColor)
    titulo.pack(pady=5)
    spacer = tk.Label(ventanaBuscar,height=2, background=mainBgColor)
    spacer.pack(fill=tk.X)
    txtBusqueda = tk.Label(ventanaBuscar,text="Ingrese el nombre del producto", background=mainBgColor)
    busquedaEntry = tk.Entry(ventanaBuscar, background=white, border=0, foreground=blue,font="8")
    txtBusqueda.pack()
    busquedaEntry.pack()
    
    def search():
        global busqueda        
        busqueda=busquedaEntry.get()       
        try:
            buscarProducto(busqueda)
        except:
            find = tk.Label(ventanaBuscar, text="Algo salió mal!", background=red, foreground="#f2f3f4")
            find.pack(padx=10, pady=5)
        def destroyLbl():
            find.pack_forget()
            return
        ventanaBuscar.after(1700,destroyLbl)
        return busqueda   
    buscarBtn = tk.Button(ventanaBuscar, text = 'Buscar producto',font=("Raleway",8,"bold"), background=blue,foreground=white, command=search)
    buscarBtn.pack(side = tk.TOP, pady = 10)

def vAgregarCarrito():
    global ventanaAgregarCarrito
    label1.config(text="Ventana agregar producto a carrito ejecutada con exito!",background=green)
    ventanaAgregarCarrito = tk.Tk()
    ventanaAgregarCarrito.title("Agregar a carrito")
    ventanaAgregarCarrito.geometry("500x500")
    ventanaAgregarCarrito.config(background=mainBgColor)
    titulo = tk.Label(ventanaAgregarCarrito, text="AGREGAR A CARRITO",font=("Raleway",12,"bold"), background=mainBgColor)
    titulo.pack(pady=5)
    spacer = tk.Label(ventanaAgregarCarrito,height=2, background=mainBgColor)
    spacer.pack(fill=tk.X)
    txtCarrito = tk.Label(ventanaAgregarCarrito,text="Ingrese el nombre del producto", background=mainBgColor)
    carritoEntry = tk.Entry(ventanaAgregarCarrito, background=white, border=0, foreground=blue,font="8")
    txtCarrito.pack()
    carritoEntry.pack()
    def search():
        global busqueda        
        busqueda=carritoEntry.get()       
        try:
            AgregarACarrito(busqueda)
        except:
            find = tk.Label(ventanaAgregarCarrito, text="Algo salió mal!", background=red, foreground=white)
            find.pack(padx=10, pady=5)
        def destroyLbl():
            find.pack_forget()
            return
        ventanaAgregarCarrito.after(1700,destroyLbl)
        return busqueda 
    carritoBtn = tk.Button(ventanaAgregarCarrito, text = 'Buscar producto',font=("Raleway",8,"bold"), background=blue,foreground=white, command=search)
    carritoBtn.pack(side = tk.TOP, pady = 10)
def vCarrito():
    global total
    label1.config(text="Ventana Carrito ejecutada con exito!",background=green)
    ventanaCarrito = tk.Tk()
    ventanaCarrito.geometry("500x500")
    ventanaCarrito.title("Carrito")
    ventanaCarrito.config(background=mainBgColor)
    titulo = tk.Label(ventanaCarrito, text="PRODUCTOS EN CARRITO",font=("Raleway",12,"bold"), background=mainBgColor)
    titulo.pack(pady=2)
    if(carrito==[]):
        msg= tk.Label(ventanaCarrito, text="No hay productos en carrito!", background=warning)
        msg.pack(pady=10, padx=5)
        btnVolver(ventanaCarrito)
    else:
        for producto in carrito:      
            
            labelNombre = tk.Label(ventanaCarrito, text=producto['producto'], background=mainBgColor)
            labelNombre.pack()
            labelPrecio = tk.Label(ventanaCarrito, text=f"${producto['precio']}", background=mainBgColor)
            labelPrecio.pack()
            labelPrecio = tk.Label(ventanaCarrito, text=f"{producto['unidades']} unidades", background=mainBgColor)
            labelPrecio.pack()
            
            subtotal=producto['unidades'] * producto['precio']
            total+=subtotal

        lblTotal = tk.Label(ventanaCarrito, text=f"TOTAL A PAGAR :$ {total:,.2f} ", background=white, foreground=blue )
        lblTotal.pack(fill=tk.X, pady=3)
        total=0
        def vaciarCarrito():
            global carrito            
            carrito=[]

            alert = tk.Label(ventanaCarrito, text="El carrito ha sido vaciado!", background=green)
            alert.pack(padx=10, pady=5)
            def destroyLbl():
                alert.pack_forget()                    
                return
            def destroyWindow():
                ventanaCarrito.destroy()
                return
            ventanaCarrito.after(1700,destroyLbl)
            ventanaCarrito.after(1900,destroyWindow)          
            return
        def comprar():            
            global carrito
            for productoC in carrito:
                nomProducto = productoC['producto']     
                precioProducto = productoC['precio']
                unidadesProducto = productoC['unidades']
                    
            for t in listaTiendas:        
                for producto in t["listaP"]:          
                    if nomProducto==producto["producto"]:
                        totalU = producto["existencia"]-unidadesProducto
                        producto["existencia"] = totalU            
                        if totalU == 0:
                            t["listaP"].remove(producto)
            alert = tk.Label(ventanaCarrito, text="Compra exitosa!", background=green)
            alert.pack(padx=10, pady=5)
            def destroyLbl():
                alert.pack_forget()                    
                return
            def destroyWindow():
                ventanaCarrito.destroy()
                return
            ventanaCarrito.after(1700,destroyLbl)
            ventanaCarrito.after(1900,destroyWindow)

            vaciarCarrito()            
            return
        comprarBtn= tk.Button(ventanaCarrito,text="Comprar",font=("Raleway",8,"bold"), background=blue,foreground=white, command=comprar)
        comprarBtn.pack(pady=2)
        vaciarBtn= tk.Button(ventanaCarrito,text="Vaciar Carrito",font=("Raleway",8,"bold"), background=blue,foreground=white, command=vaciarCarrito)
        vaciarBtn.pack(pady=2)
            
def vStock():
    label1.config(text="Ventana Stock ejecutada con exito!",background=green)
    ventanaStock = tk.Tk()
    ventanaStock.geometry("500x500")
    ventanaStock.title("Stock")
    ventanaStock.config(background=mainBgColor)
    titulo = tk.Label(ventanaStock, text="PRODUCTOS EN STOCK",font=("Raleway",12,"bold"), background=mainBgColor)
    titulo.pack(pady=2)
    for tienda in listaTiendas:
        if (tienda["listaP"]==[]):    
            msg= tk.Label(ventanaStock, text="No hay productos en stock!", background=warning)
            msg.pack(pady=10, padx=5)
            btnVolver(ventanaStock)
    for tienda in listaTiendas:                    
        for producto in tienda["listaP"]:
            labelNombre = tk.Label(ventanaStock, font="bold", text=producto['producto'], background=mainBgColor)
            labelNombre.pack()
            labelPrecio = tk.Label(ventanaStock, font="bold", text=f"$ {producto['precio']}", background=mainBgColor)
            labelPrecio.pack()
            labelExistencia = tk.Label(ventanaStock, font="bold", text=f"{producto['existencia']} unidades", background=mainBgColor)
            labelExistencia.pack()
            spacer = tk.Label(ventanaStock, height=1, background=mainBgColor)
            spacer.pack()
    if tienda["listaP"]!=[]:        
        btnVolver(ventanaStock)

boton = tk.Button(ventana,image=btnCrear,border=0, font="Raleway",background=mainBgColor, command=vProducto)
boton.pack(pady=5)

boton1 = tk.Button(ventana, image=btnBuscar,border=0, font="Raleway",background=mainBgColor, command=vBuscar)
boton1.pack(pady=5)

boton2 = tk.Button(ventana,image=btnAgCarrito,border=0, font="Raleway",background=mainBgColor, command=vAgregarCarrito)
boton2.pack(pady=5)

boton3 = tk.Button(ventana, image=btnCarrito,border=0, font="Raleway",background=mainBgColor, command=vCarrito)
boton3.pack(pady=5)

boton4 = tk.Button(ventana, image=btnStock,border=0, font="Raleway",background=mainBgColor, command=vStock)

boton4.pack(pady=5)

tk.mainloop()

stock=open("stock.txt", "w")
for tienda in listaTiendas:
    for producto in tienda["listaP"]:
        stock.write(f"{producto['producto']} \n")
        stock.write(f"$ {producto['precio']} \n")
        stock.write(f"{producto['existencia']} unidades \n")
        stock.write("----------------------------- \n")
stock.close()
print("se creó un archivo de texto con el stock")
print("PROGRAMA FINALIZADO")

        