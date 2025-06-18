import os, sys, turtle, datetime
import matplotlib.pyplot as plt

#Define la funcion limpiar_pantalla.
def limpiar_pantalla():
    '''
    Borra la pantalla cuando es llamada.
    No recibe parametros.
    No retorna.
    '''
    #Condicional que analiza el sistema operativo y de acuerdo a ello borra la pantalla.
    if sys.platform.startswith('win'):
        os.system('cls')
    elif sys.platform.startswith('darwin'):
        os.system('clear')
    elif sys.platform.startswith('linux'):
        os.system('clear')

#Define la funcion leer_archivo_productos.
def leer_archivo_productos():
    '''
    Intenta leer "productos.csv", si no existe, lo crea.
    No recibe parametros.
    :return dic productos_diccionario: diccionario con los productos.
    '''

    #Intenta leer el archivo y guardar su contenido en una lista.
    try:
        archivo = open("Archivos/productos.csv", "r")
        productos = archivo.readlines()
        productos = productos[1:]
        archivo.close()

    #Si el archivo no existe, intenta lo que esta en except.
    except:
        #Crea el archivo "productos.csv", escribe el separador y las columnas.
        archivo = open("Archivos/productos.csv", "w")
        archivo.write("sep=,\n")
        archivo.write("codigo,nombre,precio,unidades\n")
        archivo.close()

        #Lee su contenido y lo almacena en una lista.
        archivo = open("Archivos/productos.csv", "r")
        productos = archivo.readlines()
        productos = productos[1:]
        archivo.close()

    #Inicializa un diccionario.
    productos_diccionario = {}

    #Actualiza el diccionario con el contenido de los productos.
    for linea in productos:
        producto = linea.split(",")

        productos_diccionario[producto[0]] = [producto[1], producto[2], producto[3][:len(producto[3]) - 1]]

    #Retorna el diccionario.
    return productos_diccionario

#Define la funcion ver_productos.
def ver_productos(productos):
    '''
    Imprime los productos y sus caractersiticas ordenado por codigo.
    :param dic productos: diccionario con los productos.
    No retorna.
    '''

    limpiar_pantalla()

    #Indica la opcion escogida
    print("Escogio la opcion de ver productos.\n")

    #Determina la longitud del nombre mas largo, esta variable es usada con fines esteticos.
    nombre_mas_largo = max([len(producto[0]) for producto in productos.values()])

    #Guarda los productos en una lista que contiene tuplas.
    productos = list(productos.items())

    #Guarda la primera columna en dos variables.
    columna_codigo, columnas = productos[0]

    #Imprime la primera columna.
    print("{:<8}|{:<{}}|{:<9}|{}".format(columna_codigo, columnas[0], nombre_mas_largo, columnas[1], columnas[2]))

    #Imprime un separador que cambia dependiendo del nombre mas largo.
    print("-" * (26 + nombre_mas_largo))

    #Imprime todos los productos.
    for codigo, producto in productos[1:]:
        print("{:<8} {:<{}} {:<9} {}".format(codigo, producto[0], nombre_mas_largo, producto[1], producto[2]))

    input("\nPresione enter para volver al menu.")
    limpiar_pantalla()

#Define la funcion try_valor.
def try_valor(valor):
    '''
    Prueba que el valor sea un numero.
    :param str valor: valor del operador.
    :return bool True or False: booleano.
    '''
    #Intenta convertir el valor a float, retorna true si puede.
    try:
        valor = float(valor)
        return True

    #Si no puede, retorna False.
    except:
        return False

#Define la funcion agregar_producto.
def agregar_producto(productos):
    '''
    Agrega la cantidad de productos que pida el operador.
    :param dic productos: productos existentes.
    No retorna.
    '''

    #Indica la opcion escogida.
    limpiar_pantalla()
    print("----------------------------------------------")
    print("Escogio la opcion de agregar producto(s)")

    #Opcion del operador.
    agregar = input("Escriba la cantidad de productos que quiere agregar: ")

    #Ciclo que valida la opcion del operador.
    while not try_opcion(agregar) or int(agregar) < 0:
        limpiar_pantalla()
        print("La cantidad de productos a agregar debe ser un numero entero positivo.")
        agregar = input("Escriba la cantidad de productos que quiere agregar: ")
    
    #Convierte la opcion a int.
    agregar = int(agregar)

    #Vuelve al menu porque no hay productos que agregar.
    if agregar == 0:
        print("\nNo se han agregado productos.")
        input("\nPresione cualquier tecla para volver al menú")
        limpiar_pantalla()

        return

    #Ciclo que agrega tantos productos como se pidan.
    while agregar > 0:
        limpiar_pantalla()

        codigos = list(productos.keys())

        #Si es el primer producto, incializa el codigo en 1.
        if "1" not in codigos:
            codigo = "1"

        #Establece el codigo de acuerdo a los productos existentes.
        else:
            codigo = str(int(codigos[len(codigos) - 1]) + 1)

        #Almacena los nombres existentes.
        nombres_existentes = [producto[0] for producto in productos.values()]

        #Nombre escogido por operador.
        nombre = str(input("Ingrese el nombre del producto: ")).lower()

        #Se valida que el nombre tenga informacion y que no sea repetido.
        while nombre == "" or nombre in nombres_existentes or "," in nombre:
            limpiar_pantalla()
            print("Nombre no valido")
            
            #Indica el por que el nombre no es valido.
            if nombre == "":
                print("El nombre debe tener minimo un(1) caracter.")

            elif nombre in nombres_existentes:
                print("No pueden existir nombres repetidos.")

            elif "," in nombre:
                print("Los nombres no pueden tener comas.")

            #Nombre escogido por operador.
            nombre = str(input("\nIngrese el nombre del producto: ")).lower()

        limpiar_pantalla()
        #Mantiene la informacion del producto.
        print("Nombre:", nombre)

        #Valor escogido por operador.
        valor = input("\nIngrese el precio del producto: ")

        #Valida el valor.
        while not try_valor(valor) or float(valor) < 0:
            limpiar_pantalla()

            #Mantiene la informacion del producto.
            print("Nombre:", nombre)

            #Indica el por que el valor puede no ser valido.
            print("\nEl valor tiene que ser un numero positivo.")

            valor = input("\nIngrese el precio del producto: ")

        limpiar_pantalla()

        #Mantiene la informacion del producto.
        print("Nombre:", nombre)
        print("Precio:", valor)

        #Cantidad escogida por operador.
        cantidad = input("\nIngrese la cantidad de unidades del producto: ")

        while not try_opcion(cantidad) or int(cantidad) < 0:
            limpiar_pantalla()

            #Mantiene la informacion del producto.
            print("Nombre:", nombre)
            print("Precio:", valor)

            #Indica el por que la cantidad puede no ser valida.
            print("\nLa cantidad tiene que ser un numero entero positivo.")

            #Cantidad escogida por operador.
            cantidad = input("\nIngrese la cantidad de unidades del producto: ")

        limpiar_pantalla()

        #Mantiene la informacion del producto.
        print("Nombre:", nombre)
        print("Precio:", valor)
        print("Unidades:", cantidad)
            
        #Actualiza el diccionario de productos.
        nuevo_producto = [nombre, valor, cantidad]
        productos[codigo] = nuevo_producto
        
        #Dismninuye la variable agregar, para que el ciclo no sea infinito.
        agregar -= 1

        #Indica cuantos productos quedan por agregar.
        if agregar != 0:
            print("\nProducto agregado exitosamente.")
            print("Queda(n) {} producto(s) por agregar.".format(agregar))
            input("Presione enter para continuar.")

    limpiar_pantalla()

    #Abre el archivo con el fin de escribir sobre el.
    archivo = open("Archivos/productos.csv", "w")
    archivo.write("sep=,\n")

    #Guarda los codigos en una lista.
    codigos = list(productos.keys())

    #Escribe en el archivo.
    for codigo in codigos:
        archivo.write("{},".format(codigo))
        archivo.write("{}\n".format(",".join(productos[codigo])))

    #Cierra el archivo.
    archivo.close()

    #Indica que los productos fueron agregados.
    print("Producto/s agregado/s exitosamente.")

    input("\nPresione cualquier tecla para volver al menu.")
    limpiar_pantalla()

#Define la funcion modificar_producto.
def modificar_producto(productos):
    '''
    Modifica las caracteristicas de nombre y precio de un producto.
    :param dic productos: diccionario con los productos.
    No retorna.
    '''

    #Indica la opcion que se escogio.
    limpiar_pantalla()
    print("----------------------------------------------")
    print("Escogio la opcion de modificar producto.\n")

    #Indicaciones de eleccion.
    print("A continuacion se le pedira escribir el codigo del producto que desea modificar.")
    print("Si no desea modificar ningun producto, escriba 0.")
    codigo_modificar = str(input("\nIngrese el codigo del producto que modificar: "))

    #Almacena los codigos existentes.
    codigos_existentes = list(productos.keys())

    #Retorna al menu.
    if codigo_modificar == "0":
        input("\nPresione enter para volver al menu.")
        limpiar_pantalla()
        return

    #Valida que el codigo exista.
    while codigo_modificar not in codigos_existentes:

        limpiar_pantalla()

        #Indica el problema.
        print("El codigo a modificar no existe.\n")

        #Indicaciones de eleccion.
        print("A continuacion se le pedira escribir el codigo del producto que desea modificar.")
        print("Si no desea modificar ningun producto, escriba 0.")
        codigo_modificar = str(input("\nIngrese el codigo del producto que modificar: "))

        if codigo_modificar == "0":
            input("\nPresione enter para volver al menu.")
            limpiar_pantalla()
            return

    limpiar_pantalla()

    #Variable usada con fines esteticos.
    if len("Nombre") > len(productos[codigo_modificar][0]):
        n_caracteres = len("Nombre")

    else:
        n_caracteres = len(productos[codigo_modificar][0])

    #Indica el producto seleccionado.
    print("El producto seleccionado es el siguiente:\n")
    print("{:<8}|{:<{}}|{}".format("Codigo", "Nombre", n_caracteres, "Precio"))
    print("{:<8} {:<{}} {}".format(codigo_modificar, productos[codigo_modificar][0], n_caracteres, productos[codigo_modificar][1]))
    print("----------------------------------------------")
    
    #Indicaciones para el operador.
    print("A continuacion se le pedira ingresar el nuevo nombre del producto.")
    print("Si no desea cambiarlo, presione enter sin escribir nada.")

    #Input del operador.    
    nuevo_nombre = input("\nIngrese el nuevo nombre del producto: ").lower()

    #Guarda los nombres existentes en una lista.
    nombres_existentes = [producto[0] for producto in productos.values()]

    #Validacion del cambio de nombre del producto escogido.
    if nuevo_nombre != "":

        #Valida el nuevo_nombre.
        while nuevo_nombre in nombres_existentes or "," in nuevo_nombre:
            limpiar_pantalla()

            #Indica el por que no es valido.
            print("Nombre no valido,  el nombre ya existe o contiene una o mas comas.")

            #Indica el producto seleccionado.
            print("El producto seleccionado es el siguiente:\n")
            print("{:<8}|{:<{}}|{}".format("Codigo", "Nombre", n_caracteres, "Precio"))
            print("{:<8} {:<{}} {}".format(codigo_modificar, productos[codigo_modificar][0], n_caracteres, productos[codigo_modificar][1]))
            print("----------------------------------------------")

            #Indicaciones para el operador.
            print("A continuacion se le pedira ingresar el nuevo nombre del producto.")
            print("Si no desea cambiarlo, presione enter sin escribir nada.")
            
            #Input del operador.
            nuevo_nombre = input("\nIngrese el nuevo nombre del producto: ").lower()
            
        limpiar_pantalla()  

        if nuevo_nombre != "":
            productos[codigo_modificar][0] = nuevo_nombre
            print("El nombre se ha cambiado exitosamente: ")
            print("----------------------------------------------")

    limpiar_pantalla() 

     #Variable usada con fines esteticos.
    if len("Nombre") > len(productos[codigo_modificar][0]):
        n_caracteres = len("Nombre")

    else:
        n_caracteres = len(productos[codigo_modificar][0])

    #Indica el producto seleccionado.
    print("El producto seleccionado es el siguiente:\n")
    print("{:<8}|{:<{}}|{}".format("Codigo", "Nombre", n_caracteres, "Precio"))
    print("{:<8} {:<{}} {}".format(codigo_modificar, productos[codigo_modificar][0], n_caracteres, productos[codigo_modificar][1]))
    print("----------------------------------------------")
    
    #Indicaciones para el operador.
    print("A continuacion se le pedira ingresar el nuevo precio del producto.")
    print("Si no desea cambiarlo, presione enter sin escribir nada.")
            
    nuevo_precio = input("\nIngrese el nuevo precio del producto: ")

    #Validacion del cambio de precio del producto escogido
    if nuevo_precio != "":
        
        #Valida el nuevo precio.
        while (not try_valor(nuevo_precio) or float(nuevo_precio) < 0) and nuevo_precio != "":
            limpiar_pantalla()

            #Indica el por que no es valido.
            print("Precio no valido,  el precio tiene que ser un numero positivo.\n")

            #Indica el producto seleccionado.
            print("El producto seleccionado es el siguiente:\n")
            print("{:<8}|{:<{}}|{}".format("Codigo", "Nombre", n_caracteres, "Precio"))
            print("{:<8} {:<{}} {}".format(codigo_modificar, productos[codigo_modificar][0], n_caracteres, productos[codigo_modificar][1]))
            print("----------------------------------------------")

            #Indicaciones para el operador.
            print("A continuacion se le pedira ingresar el nuevo precio del producto.")
            print("Si no desea cambiarlo, presione enter sin escribir nada.")
            
            #Input del operador.
            nuevo_precio = input("\nIngrese el nuevo precio del producto: ")

        limpiar_pantalla()

        if nuevo_precio != "":
            productos[codigo_modificar][1] = nuevo_precio
            print("El precio se ha cambiado exitosamente: ")
            print("----------------------------------------------")

    limpiar_pantalla()

    #Indica el producto modificado.
    print("\nEste es el producto con las modificaciones:\n")
    print("{:<8}|{:<{}}|{}".format("Codigo", "Nombre", n_caracteres, "Precio"))
    print("{:<8} {:<{}} {}".format(codigo_modificar, productos[codigo_modificar][0], n_caracteres, productos[codigo_modificar][1]))
    print("----------------------------------------------")

    #Abre el archivo con el fin de escribir sobre el.
    archivo = open("Archivos/productos.csv", "w")
    archivo.write("sep=,\n")

    #Escribe en el archivo.
    for codigo in codigos_existentes:
        archivo.write("{},".format(codigo))
        archivo.write("{}\n".format(",".join(productos[codigo])))

    #Cierra el archivo.
    archivo.close()

    input("Presione enter para volver al menu.")
    limpiar_pantalla()

#Define la funcion actualizacion_unidades.
def actualizar_unidades(productos):
    '''
    Actualiza las unidades de un producto.
    :param dic productos: diccionario con los productos.
    No retorna.
    '''

    #Indica la opcion que se escogio.
    limpiar_pantalla()
    print("----------------------------------------------")
    print("Escogio la opcion de actualizar unidades.\n")

    #Indicaciones de eleccion.
    print("A continuacion se le pedira escribir el codigo del producto al que desea actualizar las unidades.")
    print("Si no desea actualizar ningun producto, escriba 0.")
    codigo = str(input("\nIngrese el codigo del producto al que desea actualizar las unidades: "))

    #Almacena los codigos existentes.
    codigos_existentes = list(productos.keys())

    #Retorna al menu.
    if codigo == "0":
        input("\nPresione enter para volver al menu.")
        limpiar_pantalla()
        return

    #Valida que el codigo exista.
    while codigo not in codigos_existentes:

        limpiar_pantalla()

        #Indica el problema.
        print("El codigo no existe.\n")

        #Indicaciones de eleccion.
        print("A continuacion se le pedira escribir el codigo del producto al que desea actualizar las unidades.")
        print("Si no desea actualizar ningun producto, escriba 0.")
        codigo = str(input("\nIngrese el codigo del producto al que desea actualizar las unidades: "))

        if codigo == "0":
            input("\nPresione enter para volver al menu.")
            limpiar_pantalla()
            return

    limpiar_pantalla()

    #Variable usada con fines esteticos.
    if len("Nombre") > len(productos[codigo][0]):
        n_caracteres = len("Nombre")

    else:
        n_caracteres = len(productos[codigo][0])

    #Indica el producto seleccionado.
    print("El producto seleccionado es el siguiente:\n")
    print("{:<8}|{:<{}}|{:<9}|{}".format("Codigo", "Nombre", n_caracteres, "Precio", "Unidades"))
    print("{:<8} {:<{}} {:<9} {}".format(codigo, productos[codigo][0], n_caracteres, productos[codigo][1], productos[codigo][2]))
    print("----------------------------------------------")

    #Opcion del operador.
    print("A continuacion se le pedira cuantas unidades desea aumentar/disminuir.")
    print("Si quiere disminuir las unidades escriba el simbolo '-' antes del valor.")
    print("Si no quiere cambiar el valor actual, escriba 0.")
    cantidad = input("\nEscriba cuantas unidades desea aniadir/quitar: ")

    #Valida la cantidad.
    while not try_opcion(cantidad) or (int(productos[codigo][2]) + int(cantidad)) < 0:
        limpiar_pantalla()
        
        #Indica el error.
        print("Cantidad no valida, tiene que ser un numero entero.\n")

        #Indica el producto seleccionado.
        print("El producto seleccionado es el siguiente:\n")
        print("{:<8}|{:<{}}|{:<9}|{}".format("Codigo", "Nombre", n_caracteres, "Precio", "Unidades"))
        print("{:<8} {:<{}} {:<9} {}".format(codigo, productos[codigo][0], n_caracteres, productos[codigo][1], productos[codigo][2]))
        print("----------------------------------------------")

        #Opcion del operador.
        print("A continuacion se le pedira cuantas unidades desea aumentar/disminuir.")
        print("Si no quiere cambiar el valor actual, escriba 0.")
        cantidad = input("\nEscriba cuantas unidades desea aniadir/quitar: ")

    productos[codigo][2] = str(int(productos[codigo][2]) + int(cantidad))

    #Indica el producto seleccionado.
    print("El producto seleccionado es el siguiente:\n")
    print("{:<8}|{:<{}}|{:<9}|{}".format("Codigo", "Nombre", n_caracteres, "Precio", "Unidades"))
    print("{:<8} {:<{}} {:<9} {}".format(codigo, productos[codigo][0], n_caracteres, productos[codigo][1], productos[codigo][2]))
    print("----------------------------------------------")

    #Abre el archivo con el fin de escribir sobre el.
    archivo = open("Archivos/productos.csv", "w")
    archivo.write("sep=,\n")

    #Escribe en el archivo.
    for codigo_dic in codigos_existentes:
        archivo.write("{},".format(codigo_dic))
        archivo.write("{}\n".format(",".join(productos[codigo_dic])))

    #Cierra el archivo.
    archivo.close()

    input("Presione enter para volver al menu.")
    limpiar_pantalla()
    
#Define la funcion modificar_contrasenia.
def cambiar_contrasenia():
    '''
    Cambia la contrasenia si se cumplen condiciones basicas.
    No recibe parametros.
    No retorna.
    '''

    limpiar_pantalla()

    #Indica la opcion escogida.
    print("Escogio la opcion de cambiar contrasenia.")
    
    #Almacena los datos existentes en un diccionario.
    usuarios = try_usuarios()
    usuarios = leer_usuarios(usuarios)
    
    #Guarda informacion del acceso.
    ingreso_resultado, usuario = ingreso(usuarios)

    #Si el ingreso fue permitido.
    if ingreso_resultado:
        limpiar_pantalla()

        #Indicaciones para el operador.
        print("A continuacion se le pedira la nueva contrasenia.")
        print("Si no quiere cambiarla, presione enter sin escribir nada.")
        nueva_contrasenia = input("\nEscriba su nueva contrasenia: ")

        #Evita el simbolo ":" en la contrasenia.
        while ":" in nueva_contrasenia:
            limpiar_pantalla()
            #Indica el error.
            print("La contrasenia no puede tener este simolo: ':'.\n")

            #Indicaciones para el operador.
            print("A continuacion se le pedira la nueva contrasenia.")
            print("Si no quiere cambiarla, presione enter sin escribir nada.")
            nueva_contrasenia = input("\nEscriba su nueva contrasenia: ")

        #Opcion de no cambiar la contrasenia.
        if nueva_contrasenia == "":
            limpiar_pantalla()
            print("No se ha cambiado la contrasenia.")
            input("Presione enter para volver al menu.")
            limpiar_pantalla()
            return

        #Pide confirmacion.
        confirmar_contrasenia = input("Confirme su contrasenia: ")

        #Se asegura que ambas contrasenias coincidan.
        while nueva_contrasenia != confirmar_contrasenia:
            limpiar_pantalla()

            #Indica el error.
            print("Las contrasenias no coinciden. Intente de nuevo.\n")

            #Indicaciones para el operador.
            print("A continuacion se le pedira la nueva contrasenia.")
            print("Si no quiere cambiarla, presione enter sin escribir nada.")
            nueva_contrasenia = input("\nEscriba su nueva contrasenia: ")

            #Evita el simbolo ":" en la contrasenia.
            while ":" in nueva_contrasenia:
                limpiar_pantalla()
                #Indica el error.
                print("La contrasenia no puede tener este simolo: ':'.\n")

                #Indicaciones para el operador.
                print("A continuacion se le pedira la nueva contrasenia.")
                print("Si no quiere cambiarla, presione enter sin escribir nada.")
                nueva_contrasenia = input("\nEscriba su nueva contrasenia: ")

            #Opcion de no cambiar la contrasenia.
            if nueva_contrasenia == "":
                limpiar_pantalla()
                print("No se ha cambiado la contrasenia.")
                input("Presione enter para volver al menu.")
                limpiar_pantalla()
                return

            #Pide confirmacion.
            confirmar_contrasenia = input("Confirme su contrasenia: ")

        limpiar_pantalla()

        #Cambia la contrasenia en el diccionario.
        usuarios[usuario] = nueva_contrasenia

        #Abre el archivo y escribe sobre el los nuevos datos, despues cierra el archivo.
        archivo = open("Archivos/usuarios.txt", "w")
        for usuario_nombre, contrasenia in usuarios.items():
            archivo.write("{}:{}\n".format(usuario_nombre, contrasenia))
        archivo.close()

        #Indica el resultado del proceso.
        print("La contrasenia se ha cambiado exitosamente.")
        input("Presion enter para volver al menu.")
        limpiar_pantalla()

    else:
        #Indica el resultado del proceso.
        print("No se pudo cambiar la contrasenia.")
        input("Presion enter para volver al menu.")
        limpiar_pantalla()

#Define la funcion crear usuario.
def crear_usuario():
    limpiar_pantalla()
    
    #Indica la opcion escogida.
    print("Escogio la opcion de crear usuario.")
   
    #Almacena los datos existentes.
    usuarios = try_usuarios()
    usuarios = leer_usuarios(usuarios)

    #Valida el ingreso.
    if ingreso(usuarios):
        #Indicaciones para el operador.
        print("A continuacion se le pedira el nombre de usuario.")
        print("Si desea cancelar el proceso, presione enter sin escribir nada.\n")
        nombre_usuario = input("Escriba el nombre de usuario: ")

        #Da la opcion de cancelar el proceso.
        if nombre_usuario == "":
            limpiar_pantalla()
            print("No se ha creado el usuario.")
            input("Presione enter para volver al menu.")
            return

        while nombre_usuario in usuarios.keys() or ":" in nombre_usuario:
            limpiar_pantalla()
            #Indica el error.
            print("Ese nombre de usuario ya existe y no puede ser usado en la creacion de un nuevo usuario\n o su usuario contiente el siguiente simbolo ':'.")

            #Indicaciones para el operador.
            print("A continuacion se le pedira el nombre de usuario.")
            print("Si desea cancelar el proceso, presione enter sin escribir nada.\n")
            nombre_usuario = input("Escriba el nombre de usuario: ")

            #Da la opcion de cancelar el proceso.
            if nombre_usuario == "":
                limpiar_pantalla()
                print("No se ha creado el usuario.")
                input("Presione enter para volver al menu.")
                return

        limpiar_pantalla()

        archivo = open("Archivos/usuarios.txt", "a+")

        #Realiza checksum del usuario.
        contrasenia = checksum_usuario(nombre_usuario)

        #Escribe el usuario y checksum (contrasenia) en el archivo.
        archivo.write("{}:{}\n".format(nombre_usuario, contrasenia))
        archivo.close()

        #Indica la contrasenia y usuario establecidos.
        print('Su usuario es: {}\nSu contrasenia es: {}\nPuede cambiar la contrasenia con la opción "cambiar contrasenia."\n'.format(nombre_usuario, contrasenia))

        input("Presione enter para volver al menu.")
        limpiar_pantalla()

    else:
        limpiar_pantalla()

        #Indica resultado del proceso.
        print("No se pudo crear el usuario.")
        input("Presione enter para volver al menu.")
        limpiar_pantalla()

#Define la funcion factura.
def factura(items, precio_total, productos_vendidos, productos):
    '''
    Genera la factura de la compra.
    :param int items: numero de items comprados.
    :param float precio_total: precio total de la compra.
    :param dic productos_vendidos: codigos de los productos y su cantidad vendida.
    :param dic productos: productos existentes.
    No retorna.
    '''
    #Guarda las fechas en una variable.
    archivo_fechas = open("Archivos/Fechas.csv", "r")
    fechas = archivo_fechas.readlines()
    archivo_fechas.close()
    
    #Encuentra el ultimo dia.
    ultimo_dia = fechas[len(fechas) - 1].split(",")[0]

    #El tiempo actual.
    tiempo = str(datetime.datetime.now()).split(" ")[1]
    tiempo = tiempo.replace(":", "-")
    tiempo = tiempo.split(".")[0]

    #Crea un archivo dependiendo del dia y tiempo.
    archivo = open("Archivos/Facturas/{}_{}.txt".format(ultimo_dia, tiempo), "w")

    #Encuentra la fecha de hoy.
    hoy = str(datetime.date.today()).replace("-", "/")
    tiempo = tiempo.replace("-", ":")

    #Escribe la fecha y tiempo de la compra.
    archivo.write("Fecha: {} {}\n\n".format(hoy, tiempo))

    #Escrbie las columnas.
    archivo.write("{:<20} {:<9} {:<4} {}\n".format("Item", "Precio", "Cant", "Valor"))
    archivo.write("-" * 50 + "\n")

    #Escribe la informacion de cada producto.
    for producto in productos_vendidos.keys():
        nombre = productos[producto][0]

        if len(nombre) > 20:
            nombre = nombre[:20]

        precio = productos[producto][1]
        cantidad = productos_vendidos[producto]
        valor_total = int(precio) * cantidad
        archivo.write("{:<20} ${:<9} x{:<4} ${}\n".format(nombre, precio, cantidad, valor_total))
    
    archivo.write("-" * 50 + "\n")
    
    #Escribe las unidades totales compradas y el precio total.
    archivo.write("Items: {}\n".format(items))
    archivo.write("Total: ${}\n".format(precio_total))
    archivo.write("Gracias por su compra!\n")
    archivo.write("-" * 50 + "\n")

    #Cierra el archivo.
    archivo.close()

#Define la funcion vender.
def vender(productos):
    limpiar_pantalla()

    #Variables de venta.
    items = 0
    precio_total = 0
    productos_vendidos = {}

    while True:
        limpiar_pantalla()
        #Indicaciones para el operador.
        print("A continuacion se le pedira el codigo del producto que desea vender.")
        print("Si desea cancelar la operacion de venta, presione enter sin escribir nada. ")

        if items != 0:
            print("Si desea finalizar la venta, escriba 0.")

        codigo_venta = input("\nEscriba el codigo del producto a vender: ")

        #Almacena los codigos existentes.
        codigos_existentes = list(productos.keys())

        #Finaliza la compra.
        if codigo_venta == "0" and items != 0:
            limpiar_pantalla()
            
            #Indica que finaliza la compra y genera una factura.
            print("Se ha finalizado la operacion de venta.")
            factura(items, precio_total, productos_vendidos, productos)
            print("Se ha generado una factura.\n") 

            #Rompe el ciclo para volver.
            break


        #Retorna al menu.
        if codigo_venta == "":
            limpiar_pantalla()
            print("Se ha cancelado la operacion de venta.")
            input("\nPresione enter para volver al menu.")
            limpiar_pantalla()
            return

        #Valida que el codigo exista.
        while codigo_venta not in codigos_existentes:

            limpiar_pantalla()

            #Indica el problema.
            print("El codigo a vender no existe.\n")

            #Indicaciones de eleccion.
            print("A continuacion se le pedira el codigo del producto que desea vender.")
            print("Si desea cancelar la operacion de venta, presione enter sin escribir nada.")

            if items != 0:
                print("Si desea finalizar la venta, escriba 0.")

            codigo_venta = input("\nEscriba el codigo del producto a vender: ")

            #Finaliza la compra.
            if codigo_venta == "0" and items != 0:
                limpiar_pantalla()

                #Indica que finaliza la compra y genera una factura.
                print("Se ha finalizado la operacion de venta.")
                factura(items, precio_total, productos_vendidos, productos)
                print("Se ha generado una factura.\n") 

                #Rompe el ciclo para volver.
                break


            #Retorna al menu.
            if codigo_venta == "":
                limpiar_pantalla()
                print("Se ha cancelado la operacion de venta.")
                input("\nPresione enter para volver al menu.")
                limpiar_pantalla()
                return

        limpiar_pantalla()

        #Variable usada con fines esteticos.
        if len("Nombre") > len(productos[codigo_venta][0]):
            n_caracteres = len("Nombre")

        else:
            n_caracteres = len(productos[codigo_venta][0])

        #Indica el producto seleccionado.
        print("El producto seleccionado es el siguiente:\n")
        print("{:<8}|{:<{}}|{:<9}|{}".format("Codigo", "Nombre", n_caracteres, "Precio", "Unidades"))
        print("{:<8} {:<{}} {:<9} {}".format(codigo_venta, productos[codigo_venta][0], n_caracteres, productos[codigo_venta][1], productos[codigo_venta][2]))
        print("----------------------------------------------")

        #Indicaciones para el operador.
        print("A continuacion se le pedira cuantas unidades desea vender.")
        print("Si no desea vender el producto, escriba 0.")
        unidades_venta = input("\nEscriba cuantas unidades desea vender: ")

        #Valida la cantidad de unidades a vender.
        while not try_opcion(unidades_venta) or int(unidades_venta) > int(productos[codigo_venta][2]) or int(unidades_venta) < 0:
            limpiar_pantalla()
            print("La cantidad introducida no es valida.")
            print("La cantidad tiene que ser un numero entero positivo menor o igual a las unidades disponibles.")

            #Indica el producto seleccionado.
            print("\nEl producto seleccionado es el siguiente:\n")
            print("{:<8}|{:<{}}|{:<9}|{}".format("Codigo", "Nombre", n_caracteres, "Precio", "Unidades"))
            print("{:<8} {:<{}} {:<9} {}".format(codigo_venta, productos[codigo_venta][0], n_caracteres, productos[codigo_venta][1], productos[codigo_venta][2]))
            print("----------------------------------------------")

            #Indicaciones para el operador.
            print("A continuacion se le pedira cuantas unidades desea vender.")
            print("Si no desea vender el producto, escriba 0.")
            unidades_venta = input("\nEscriba cuantas unidades desea vender: ")

        #Indica el estado de venta.
        if unidades_venta == "0":
            print("No se vendio el producto.")

        #Actualiza los datos.
        else:
            productos[codigo_venta][2] = str(int(productos[codigo_venta][2]) - int(unidades_venta))
            items += int(unidades_venta)
            precio_total += int(unidades_venta) * float(productos[codigo_venta][1])
            
            if codigo_venta not in productos_vendidos.keys():
                productos_vendidos[codigo_venta] = int(unidades_venta)

            else:
                productos_vendidos[codigo_venta] += int(unidades_venta) 

    #Abre el archivo con el fin de escribir sobre el.
    archivo = open("Archivos/productos.csv", "w")
    archivo.write("sep=,\n")

    #Escribe en el archivo.
    for codigo_dic in codigos_existentes:
        archivo.write("{},".format(codigo_dic))
        archivo.write("{}\n".format(",".join(productos[codigo_dic])))

    #Cierra el archivo.
    archivo.close()

    input("Presione enter para volver al menu.")
    limpiar_pantalla()

#Define la funcion coordenada_y.
def coordenada_y(dia, codigo):
    '''
    Busca las unidades de un producto en un dia especifico y las retorna.
    :param int dia: dia del archivo.
    :param str codigo: codigo del producto.
    :return int productos[codigo][2]: las unidades del producto en ese dia.
    '''
    #Abre un archivo dependiendo del dia y guarda su contenido.
    archivo_dia = open("Archivos/Cronologia/{}.csv".format(dia), "r")
    contenido = archivo_dia.readlines()
    archivo_dia.close()

    #Guarda la informacion del archivo en un diccionario.
    productos = {}
    for producto in contenido[1:]:
        informacion_producto = producto.split(",")
        productos[informacion_producto[0]] = [informacion_producto[1], informacion_producto[2], informacion_producto[3]]

    #Retorna las unidades de un producto en especifico.
    return int(productos[codigo][2])

#Define la funcion estadisticas
def estadisticas(productos):
    '''
    Ver las ventas de los ultimos 30 dias de un producto.
    :param dic productos: diccionario con los productos.
    No retorna.
    '''
    #Indica la opcion que se escogio.
    limpiar_pantalla()
    print("----------------------------------------------")
    print("Escogio la opcion de estadisticas.\n")

    #Indicaciones de eleccion.
    print("A continuacion se le pedira escribir el codigo del producto al que le desea ver las estadisticas.")
    print("Si no desea ver las estadisticas de ningun producto, escriba 0.")
    codigo_visualizar = str(input("\nIngrese el codigo del producto a visualizar: "))

    #Almacena los codigos existentes.
    codigos_existentes = list(productos.keys())

    #Retorna al menu.
    if codigo_visualizar == "0":
        input("\nPresione enter para volver al menu.")
        limpiar_pantalla()
        return

    #Valida que el codigo exista.
    while codigo_visualizar not in codigos_existentes:

        limpiar_pantalla()

        #Indica el problema.
        print("El codigo a visualizar no existe.\n")

        #Indicaciones de eleccion.
        print("A continuacion se le pedira escribir el codigo del producto al que le desea ver las estadisticas.")
        print("Si no desea ver las estadisticas de ningun producto, escriba 0.")
        codigo_visualizar = str(input("\nIngrese el codigo del producto a visualizar: "))

        if codigo_visualizar == "0":
            input("\nPresione enter para volver al menu.")
            limpiar_pantalla()
            return

    limpiar_pantalla()

    #El dia actual.
    hoy = str(datetime.date.today())

    #Las fechas guardadas en el archivo.
    fechas = try_archivo_fechas(hoy)

    #EL ultimo dia guardado.
    ultimo_dia = int(fechas[len(fechas) - 1].split(",")[0])

    #Coordenadas en x.
    x = [dia for dia in range(1, 31)]

    #Inicializacion de coordenadas en y.
    y = []

    #Si no hay 30 dias en el archivo, se rellena las coordenadas en y con ceros 0.
    if ultimo_dia < 30:
        for dia in range(ultimo_dia + 1):
            y_dia = coordenada_y(dia, codigo_visualizar)
            y.append(y_dia)

        while len(y) < 30:
            y.append(0)

    #Si hay 30 dias o mas, itera en otros dias.
    else:
        for dia in range(ultimo_dia - 30, ultimo_dia + 1):
            y_dia = coordenada_y(dia, codigo_visualizar)
            y.append(y_dia)

    #Encuentra el maximo en y.
    y_maximo = max(y)

    #El titulo del grafico es el nombre del producto.
    plt.title("{}".format(productos[codigo_visualizar][0])) 
 
    #Se establecen los rangos de las variables.
    plt.ylim(0, y_maximo) 
    plt.xlim(1, 30)

    #Se establecen colores y tamanos de la grafica.
    plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='blue', markersize=6) 

    #Se nombran los ejes.
    plt.ylabel("Unidades")
    plt.xlabel("Dias")

    #Se muestra la grafica.
    plt.show()
    
    input("Presione enter para volver al menu.")
    limpiar_pantalla()

#Define la funcion try_archivo_fechas.
def try_archivo_fechas(hoy):
    '''
    Intenta leer el archivo "Fechas.csv", si no puede, lo crea.
    :param str hoy: La fecha actual.
    :return list fechas: retorna una lista con la informacion del archivo "Fechas.csv"
    '''
    #Intenta leer el archivo.
    try:
        archivo = open("Archivos/Fechas.csv", "r")
        fechas = archivo.readlines()
        archivo.close()

        return fechas

    #Si no puede lo crea.
    except:
        #Crea el archivo.
        archivo = open("Archivos/Fechas.csv", "w")

        #Escribe la informacion principal.
        archivo.write("sep=,\n")
        archivo.write("Dia,Fecha\n")
        archivo.write("0,{}\n".format(hoy))
        archivo.close()

        #Guarda la informacion en una lista.
        archivo = open("Archivos/Fechas.csv", "r")
        fechas = archivo.readlines()
        archivo.close()

        #Crea otro archivo para inicializar los dias.
        Dia = open("Archivos/Cronologia/0.csv", "w")
        Dia.close()

        return fechas

#Define la funcion archivos_fechas.
def archivos_fechas(productos):
    '''
    Crea archivos y los actualiza, estos archivos estan relacionado con los dias.
    :param dic productos: diccionario con los productos.
    No retorna.
    '''

    #Dia de hoy.
    hoy = str(datetime.date.today())
    
    #Lista con las fechas.
    fechas = try_archivo_fechas(hoy)

    #Abre un archivo para escribir en el.
    archivo = open("Archivos/Fechas.csv", "a+")

    #Mira cual es el ultimo dia y separa sus columnas
    ultimo_dia = fechas[len(fechas) - 1].split(",")
    dia, fecha = ultimo_dia[0], ultimo_dia[1][:len(ultimo_dia[1]) - 1]

    #Si la fecha es diferente a la de hoy, crea los archivos respectivos para el presente dia.
    if fecha != hoy:
        #Crea ambos archivos.
        archivo.write("{},{}\n".format(int(fechas[len(fechas) - 1].split(",")[0]) + 1, hoy))
        dia = open("Archivos/Cronologia/{}.csv".format(int(fechas[len(fechas)-1].split(",")[0]) + 1), "w")

        #Escribe el separador y la informacion de los productos.
        dia.write("sep=,\n")
        for codigo, producto in productos.items():
            dia.write("{},".format(codigo))
            dia.write("{}\n".format(",".join(producto)))

        #Cierra los archivos.
        dia.close()
        archivo.close()

    #Actualiza la informacion del dia de hoy.
    else:
        #Reescribe el archivo.
        dia = open("Archivos/Cronologia/{}.csv".format(int(fechas[len(fechas)-1].split(",")[0])), "w")

        #Escribe el separador y la informacion de los productos.
        dia.write("sep=,\n")
        for codigo, producto in productos.items():
            dia.write("{},".format(codigo))
            dia.write("{}\n".format(",".join(producto)))
            
        dia.close()

#Define la funcion opciones.
def opciones(opcion):
    '''
    Determina la accion a hacer de acuerdo con la opcion del operador.
    :param int opcion: opcion del operador.
    No retorna.
    '''

    #Guarda los productos (dic) en una variable.
    productos = leer_archivo_productos()
    archivos_fechas(productos)

    #Funcion de acuerdo a la opcion.
    if opcion == 1:
        agregar_producto(productos)

    elif opcion == 2:
        modificar_producto(productos)

    elif opcion == 3:
        ver_productos(productos)

    elif opcion == 4:
        cambiar_contrasenia()

    elif opcion == 5:
        crear_usuario()

    elif opcion == 6:
        actualizar_unidades(productos)

    elif opcion == 7:
        vender(productos)
    
    elif opcion == 8:
        estadisticas(productos)

    else:
        limpiar_pantalla()
        sys.exit()

#Define la funcion try_opcion.
def try_opcion(opcion):
    '''
    Intenta convertir la opcion en entero para verificar que sea una opcion valida.
    :param str opcion: opcion del operador.
    :return bool True or False: Booleano.
    '''

    #Intenta convertir la opcion en entero, si puede, retorna True.
    try:
        opcion = int(opcion)
        return True

    #Si la seccion try no es posible, retorna False.
    except:
        return False

#Define la funcion menu.
def menu():
    '''
    Imprime el menu y valida la opcion del operador
    No recibe parametros.
    '''
    #Ciclo que permite volver al menu despues de acabar una opcion. El ciclo se rompe con la opcion salir en la funcion opciones.
    while True:
        #Imprime el menu.
        print("\tMenu\t\n")
        print("1. Agregar producto(s)")
        print("2. Modificar producto")
        print("3. Ver productos")
        print("4. Cambiar contrasenia")
        print("5. Crear nuevo usuario")
        print("6. Actualizar unidades")
        print("7. Vender")
        print("8. Estadisticas")
        print("9. Salir\n")

        #Opcion del operador (str).
        opcion = input("Elija la opcion que quiere realizar (la opcion debe ser un numero entero entre 1 y 9): ")
        
        #Valida que la opcion sea un numero entero y que este dentro del intervalo de opciones.
        while not try_opcion(opcion) or int(opcion) < 1 or int(opcion) > 9:
            #Limpia la pantalla.
            limpiar_pantalla()

            #Vuelve a imprimir el menu como ayuda visual.
            print("Opcion no valida, la opcion debe ser un numero entero entre 1 y 9.\n")
            print("\tMenu\t\n")
            print("1. Agregar producto(s)")
            print("2. Modificar producto")
            print("3. Ver productos")
            print("4. Cambiar contrasenia")
            print("5. Crear nuevo usuario")
            print("6. Actualizar unidades")
            print("7. Vender")
            print("8. Estadisticas")
            print("9. Salir\n")

            #Permite escoger una opcion.
            opcion = input("Elija la opcion que quiere realizar: ")

        #Determina el proceso a seguir.
        opciones(int(opcion))

#Define la funcion try_usuarios.
def try_usuarios():
    '''
    Intenta leer el archivo "usuarios.txt", si no existe lo crea y crea un usuario con su respectiva contrasenia.
    No recibe parametros.
    :return list usuarios: lista con usuarios y contrasenias.
    '''
    #Intenta leer el archivo "usuarios.txt", si puede, retorna la informacion en forma de lista.
    try:
        archivo = open("Archivos/usuarios.txt", "r")
        usuarios = archivo.readlines()
        archivo.close()

        return usuarios

    #Crea el archivo "usuarios.txt" y crea un usuario con contrasenia.
    #Retorna la informacion en forma de lista.
    except:
        #Crea archivo.
        archivo = open("Archivos/usuarios.txt", "w")

        #Usuario generado por operador.
        usuario = str(input("Creando usuario...\nEscriba el nuevo nombre de usuario: "))

        #Comprueba que se haya escrito un usuario.
        while len(usuario) == 0 or ":" in usuario:
            limpiar_pantalla()
            print("Usuario no valido, el nombre tiene que tener minimo un(1) caracter y no puede contener este simbolo ':'.")
            usuario = str(input("Escriba el nuevo nombre de usuario: "))

        #Realiza checksum del usuario.
        checksum = checksum_usuario(usuario)

        #Escribe el usuario y checksum (contrasenia) en el archivo.
        archivo.write("{}:{}\n".format(usuario, checksum))
        archivo.close()

        limpiar_pantalla()

        #Indica la contrasenia y usuario establecidos.
        print('Su usuario es: {}\nSu contrasenia es: {}\nPuede cambiar la contrasenia con la opcion "cambiar contrasenia."\n'.format(usuario, checksum))

        #Lee el archivo y guarda el usuario en una lista.
        archivo = open("Archivos/usuarios.txt", "r")
        usuarios = archivo.readlines()
        archivo.close()
        
        return usuarios

#Define la funcion peso.
def peso(semilla, palabras):
    '''
    Guarda los pesos del usuario.
    :param int semilla: numero primo para calcular el peso.
    :param list palabras: lista con palabras del usuario.
    :return list pesos: lista con pesos.
    '''
    
    #Inicializa una lista.   
    pesos = []

    #Guarda el peso de cada palabra en una lista.
    for palabra in palabras:
        for letra in range(len(palabra)):
            pesos.append(ord(palabra[letra]) * ( letra + 1) % semilla)

    #retorna la lista de pesos.
    return pesos

#Define la funcion checksum_usuario.
def checksum_usuario(usuario):
    '''
    Calcula el checksum del nombre de usuario.
    :param str usuario: nombre de usuario.
    :return int checksum: checksum calculado.
    '''
    #Establece variables para los calculos.
    limite = 15023006
    semilla = 281

    #Separa el nombre de usuario en palabras.
    palabras = usuario.split(" ")

    #Establece los pesos con la funcion peso.
    pesos = peso(semilla, palabras)

    #Inicializa el checksum
    checksum = 0

    #Actualiza el checksum teniendo en cuenta las variables.
    for palabra in range(len(palabras)):       
        if checksum > limite:
            checksum %= limite
        
        checksum += pesos[palabra]
        checksum *= semilla
        
    if checksum > limite:
        checksum %= limite
        
    #Retorna el checksum
    return checksum

#Define la funcion leer_usuarios.
def leer_usuarios(usuarios):
    '''
    Guarda la informacion de los usuarios en un diccionario.
    :param list usuarios: recibe una lista con los usuarios.
    :return dic usuarios_diccionario: Informacion de los usuarios organizada en un diccionario.
    '''
    #Inicializa un diccionario.
    usuarios_diccionario = {}

    #Actualiza el diccionario.
    for usuario in usuarios:
        lista_usuario = usuario.split(":")
        usuarios_diccionario[lista_usuario[0]] = lista_usuario[1][:len(lista_usuario[1]) - 1]

    #Retorna el diccionario.
    return usuarios_diccionario

#Define la funcion ingreso.
def ingreso(usuarios):
    '''
    Analiza los inputs del operador y establece su estado de ingreso.
    :param dic usuarios: diccionario con informacion de los usuarios.
    :return bool True or False: Booleano. 
    :return str usuario: nombre de usuario aceptado.
    '''
    
    #Pide el usuario.
    usuario = str(input("Ingrese su usuario: "))

    #Si el usuario es incorrecto, puede corregirlo con 5 intentos.
    intentos_restantes = 5
    while usuario not in usuarios.keys() and intentos_restantes != 0:
        
        #El ciclo no es infinito.
        intentos_restantes -= 1

        #Se acaban los intentos.
        if intentos_restantes == 0:
            break

        limpiar_pantalla()
        print("Usuario inexistente. Intentos restantes: ", intentos_restantes)
        usuario = str(input("Ingrese su usuario: "))

    #Si se acabaron los intentos, se niega el acceso y finaliza el programa.
    if intentos_restantes == 0:
        limpiar_pantalla()
        input("Acceso denegado, presione enter para salir: ")
        return False        

    #Pide la contrasenia.
    limpiar_pantalla()
    contrasenia = str(input("Ingrese su contrasenia: "))

    #Si la contrasenia es incorrecta, puede corregirla con 3 intentos.
    intentos_restantes = 3
    while intentos_restantes != 0 and contrasenia != usuarios[usuario]:
        intentos_restantes -= 1
        limpiar_pantalla()

        #Se acaban los intentos.
        if intentos_restantes == 0:
            break

        print("Contrasenia equivocada. Intentos restantes: ", intentos_restantes)
        contrasenia = str(input("Ingrese su contrasenia: "))
        
    #Si se acabaron los intentos, se niega el acceso y finaliza el programa.
    if intentos_restantes == 0:
        limpiar_pantalla()
        input("Acceso denegado, presione enter para salir: ")
        return False

    #Retorna true, es decir, permite el acceso.
    return True, usuario

#Defina la funcion dibujar_s.
def dibujar_s(tortuga):
    '''
    Dibuja una "s".
    :param class Turtle: Tortuga de la liberia Turtle.
    No retorna.
    '''
    tortuga.forward(80)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.right(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(40)
    tortuga.right(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.right(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.right(90)
    tortuga.forward(40)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.right(90)
    tortuga.backward(80)
    tortuga.right(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.right(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.right(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.right(90)
    tortuga.backward(20)
    tortuga.right(90)
    tortuga.backward(60)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.right(90)

#Defina la funcion dibujar_i.
def dibujar_i(tortuga):
    '''
    Dibuja una "i".
    :param class Turtle: Tortuga de la liberia Turtle.
    No retorna.
    '''
    tortuga.forward(80)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.right(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.forward(80)
    tortuga.right(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(80)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.backward(80)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)

#Define la funcion dibujar_m
def dibujar_m(tortuga):
    '''
    Dibuja una "m".
    :param class Turtle: Tortuga de la liberia Turtle.
    No retorna.
    '''
    tortuga.forward(40)
    tortuga.left(90)
    tortuga.forward(80)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.forward(80)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(120)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.backward(20)
    tortuga.left(90)
    tortuga.forward(20)
    tortuga.left(90)
    tortuga.forward(40)
    tortuga.left(90)
    tortuga.forward(120)
    tortuga.left(90)

#Define la funcion dibujar_iniciales
def dibujar_iniciales(tortuga):
    '''
    Dibuja las iniciales del proyecto.
    :param class Turtle: Tortuga de la liberia Turtle.
    No retorna.
    '''
    tortuga.up()
    tortuga.goto(-250, -385)
    tortuga.down()

    dibujar_s(tortuga)

    tortuga.up()
    tortuga.goto(-100, -385)
    tortuga.down()

    dibujar_i(tortuga)

    tortuga.up()
    tortuga.goto(10, -385)
    tortuga.down()

    dibujar_m(tortuga)

    tortuga.up()
    tortuga.goto(180, -385)
    tortuga.down()

    dibujar_i(tortuga)

#Define la funcion dibujar_copo
def dibujar_logo(longitud, copos, tortuga):
    '''
    :param int longitud: longitud de la linea de cada copo.
    :param int copos: copos restantes.
    :param class turtle: Tortuga que hace el dibujo.
    No retorna
    '''

    #Caso Base.
    if copos > 0:
        #Dibuja el copo.
        copo = 6
        while copo > 0:
            tortuga.forward(longitud)

            #Se llama asimisma y se acerca al caso base.
            dibujar_logo(longitud//3, copos-1, tortuga)

            tortuga.backward(longitud)
            tortuga.left(60)
            
            #Evita un ciclo infinito.
            copo -= 1

#Define la funcion main.
def main():
    '''
    Arranca el programa.
    No recibe parametros.
    No retorna.
    '''
    limpiar_pantalla()

    #Establece parametros de turtle como la pantalla, tortuga, color, velocidad, entre otros.
    pantalla = turtle.Screen()
    tortuga = turtle.Turtle()
    tortuga.ht()
    tortuga.speed(90000)
    tortuga.color("green")
    pantalla.bgcolor("black")

    #Establece variables y llama la funcion de crear el logo con iniciales
    longitud = 200
    dibujar_logo(longitud, 4,tortuga)
    dibujar_iniciales(tortuga)
    pantalla.exitonclick()

    #Guarda los usuarios en un diccionario.
    usuarios = try_usuarios()
    usuarios = leer_usuarios(usuarios)
    
    #Valida el ingreso.
    if ingreso(usuarios):
        limpiar_pantalla()
        print("Acceso concedido.")
        print("----------------------------------------------")
        print("\tBienvenido\t")
        print("----------------------------------------------")

        menu()

#Llama la funcion main.
main()