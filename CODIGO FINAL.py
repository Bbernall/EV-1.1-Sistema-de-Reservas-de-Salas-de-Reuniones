# =================================================================
# 1. IMPORTACIÓN DE MÓDULOS
# =================================================================
import os
import datetime

# =================================================================
# 2. VARIABLES GLOBALES
# =================================================================
clientes = {}
salas = {}

reservaciones = []

id_cliente_siguiente = 1
id_sala_siguiente = 1
folio_reservacion_siguiente = 1

# =================================================================
# 3. DEFINICIÓN FUNCIONES DE AYUDA
# =================================================================
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else  'clear')


def mostrar_menu():
    print("*" * 51)
    print("**   SISTEMA DE RESERVA DE SALAS DE REUNIONES    **")
    print("*" * 51)
    print("\n-- MENÚ PRINCIPAL --")
    print("1. Registrar una Reservación")
    print("2. Editar el nombre del evento de una reservación")
    print("3. Consultar las reservaciones para una fecha")
    print("4. Registrar un nuevo cliente")
    print("5. Registrar una nueva sala")
    print("6. Salir")
    print("-" * 51)


def cargar_datos_de_prueba():
    global clientes, salas, id_cliente_siguiente, id_sala_siguiente

    clientes[101] = {'nombre': 'José Carlos', 'apellidos': 'Bernal Medina'}
    clientes[102] = {'nombre': 'Andrea Janet', 'apellidos': 'Mata Araujo'}
    clientes[103] = {'nombre': 'Iván', 'apellidos': 'Meléndez Méndez'}
    clientes[104] = {'nombre': 'Carlos Omar', 'apellidos': 'Tamez Medina'}
    clientes[105] = {'nombre': 'Sara Fernanda', 'apellidos': 'Villarreal Leal'}
    id_cliente_siguiente = 106

    salas[201] = {'nombre': 'Python Programadores', 'cupo': 15}
    salas[202] = {'nombre': 'Marketing', 'cupo': 8}
    salas[203] = {'nombre': 'Diseño Digital', 'cupo': 4}
    salas[204] = {'nombre': 'Java Programadores', 'cupo': 10}
    salas[205] = {'nombre': 'Creatividad Musical', 'cupo': 7}
    id_sala_siguiente = 206

    print("-> ¡Datos de prueba cargados exitosamente! <-")

# =================================================================
# 4. DEFINICIÓN FUNCIONES PRINCIPALES
# =================================================================
def registrar_reservacion():
    limpiar_pantalla()
    print("*"*47)
    print("**         REGISTRO DE RESERVACIÓN           **")
    print("*"*47)

    if not clientes:
        input("ERROR: No hay clientes registrados. Registra un cliente primero.\n\n    -->ENTER para coninuar...")
        return

    print("--- Clientes Registrados ---")

    clientes_ordenados = sorted(clientes.items(), key=lambda item: (item[1]['apellidos'], item[1]['nombre']))

    for id_cliente, datos in clientes_ordenados:
        print(f"  ID: {id_cliente} -> {datos['apellidos']}, {datos['nombre']}")

    while True:
        id_str = input("\nSelecciona el ID del cliente (o escribe 'C' para cancelar): ")

        if id_str.upper() == 'C':
            print("\nOperación cancelada.")
            return

        try:
            cliente_seleccionado_id = int(id_str)
            if cliente_seleccionado_id in clientes:
                break
            else:
                print("ID no válido. Por favor, elige un ID de la lista.")
        except ValueError:
            print("Error: Ingresa solo el número del ID.")

    print("\n--- Selección de Fecha ---")
    fecha_actual = datetime.date.today()
    dos_dias_despues = fecha_actual + datetime.timedelta(days=2)

    while True:
        fecha_str = input(f"Ingresa la fecha de la reservación (dd/mm/aaaa). Debe ser después del {dos_dias_despues.strftime('%d/%m/%Y')}: ")
        try:
            fecha_reservacion = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
            if fecha_reservacion > fecha_actual + datetime.timedelta(days=1):
                break
            else:
                print("La fecha debe ser con al menos dos días de anticipación.")
        except ValueError:
            print("Formato de fecha incorrecto. Usa dd/mm/aaaa.")

    print("\n--- Salas y Turnos Disponibles ---")
    turnos = ["MATUTINO", "VESPERTINO", "NOCTURNO"]
    opciones_disponibles = []
    opcion_num = 1

    for id_sala, datos_sala in salas.items():
        for turno in turnos:

            disponible = True
            for reservacion in reservaciones:
                if reservacion['fecha'] == fecha_reservacion and reservacion['sala_id'] == id_sala and reservacion['turno'] == turno:
                    disponible = False
                    break

            if disponible:
                print(f"{opcion_num}. Sala: {datos_sala['nombre']} ({datos_sala['cupo']} personas) - Turno: {turno}")
                opciones_disponibles.append({'num': opcion_num, 'id_sala': id_sala, 'turno': turno})
                opcion_num += 1

    if not opciones_disponibles:
        print("\nLo sentimos, no hay salas disponibles para la fecha seleccionada.")
        return

    while True:
        try:
            opcion_elegida = int(input("\nSelecciona el número de la opción deseada: "))
            seleccion_final = None
            for opcion in opciones_disponibles:
                if opcion['num'] == opcion_elegida:
                    seleccion_final = opcion
                    break

            if seleccion_final:
                break
            else:
                print("Número de opción no válido. Inténtalo de nuevo.")
        except ValueError:
            print("Error: Ingresa solo un número.")

    while True:
        nombre_evento = input("\nIngresa el nombre del evento: ")
        if nombre_evento.strip():
            break
        else:
            print("El nombre del evento no puede estar vacío.")

    global folio_reservacion_siguiente
    nueva_reservacion = {
        'folio': folio_reservacion_siguiente,
        'cliente_id': cliente_seleccionado_id,
        'sala_id': seleccion_final['id_sala'],
        'fecha': fecha_reservacion,
        'turno': seleccion_final['turno'],
        'evento': nombre_evento
    }

    reservaciones.append(nueva_reservacion)
    folio_reservacion_siguiente += 1

    print("\n***************************************************")
    print(f"    ¡RESERVACIÓN REGISTRADA CON ÉXITO!")
    print(f"     Su folio es el número: {nueva_reservacion['folio']}")
    print("***************************************************")
    input("     -->ENTER para continuar...")


def editar_nombre_evento():
    """Permite al usuario modificar el nombre de un evento existente."""
    limpiar_pantalla()
    print("*"*61)
    print("**           EDICIÓN DE EVENTO DE RESERVACIÓN              **")
    print("*"*61)

    if not reservaciones:
        input("     No hay reservaciones registradas para editar.\n\n    -->ENTER para coninuar...")
        return

    while True:
        try:
            fecha_inicio_str = input("Ingresa la fecha de inicio del rango (dd/mm/aaaa): ")
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Formato de fecha incorrecto. Usa dd/mm/aaaa.")

    while True:
        try:
            fecha_fin_str = input("Ingresa la fecha de fin del rango (dd/mm/aaaa): ")
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, "%d/%m/%Y").date()
            if fecha_fin >= fecha_inicio:
                break
            else:
                print("La fecha de fin no puede ser anterior a la fecha de inicio.")
        except ValueError:
            print("Formato de fecha incorrecto. Usa dd/mm/aaaa.")

    reservaciones_en_rango = []
    for r in reservaciones:
        if fecha_inicio <= r['fecha'] <= fecha_fin:
            reservaciones_en_rango.append(r)

    if not reservaciones_en_rango:
        print("\nNo se encontraron reservaciones en el rango de fechas especificado.")
        return

    print("\n             --- Reservaciones Encontradas ---")
    print(f"{'FOLIO':<8} | {'FECHA':<12} | {'SALA':<20} | {'EVENTO'}")
    print("-" * 60)
    for r in reservaciones_en_rango:
        nombre_sala = salas[r['sala_id']]['nombre']
        print(f"{r['folio']:<8} | {r['fecha'].strftime('%d/%m/%Y'):<12} | {nombre_sala:<20} | {r['evento']}")

    while True:
        folio_str = input("\nIngresa el folio a editar (o escribe 'C' para cancelar): ")

        if folio_str.upper() == 'C':
            print("\nOperación de edición cancelada. Volviendo al menú principal.")
            return

        try:
            folio_a_editar = int(folio_str)
            reservacion_a_modificar = None
            for r in reservaciones_en_rango:
                if r['folio'] == folio_a_editar:
                    reservacion_a_modificar = r
                    break
            
            if reservacion_a_modificar:
                break
            else:
                print("Folio no encontrado en la lista. Inténtalo de nuevo.")
        except ValueError:
            print("Error: Ingresa solo números para el folio (o 'C' para cancelar).")

    while True:
        nuevo_nombre = input(f"\nIngresa el nuevo nombre para el evento '{reservacion_a_modificar['evento']}': ")
        if nuevo_nombre.strip():
            reservacion_a_modificar['evento'] = nuevo_nombre
            break
        else:
            print("El nombre del evento no puede estar vacío.")

    input("\n¡El nombre del evento ha sido actualizado con éxito!\n\n    -->ENTER para coninuar...")


def consultar_reservaciones():
    limpiar_pantalla()
    print("*"*46)
    print("**        CONSULTA DE RESERVACIONES         **")
    print("*"*46)

    if not reservaciones:
        print("No hay reservaciones registradas en el sistema.")
        input("\n\n    -->ENTER para coninuar...")
        return

    while True:
        fecha_str = input("Ingresa la fecha a consultar (dd/mm/aaaa): ")
        try:
            fecha_consulta = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Formato de fecha incorrecto. Usa dd/mm/aaaa.")

    reservaciones_encontradas = []
    for reservacion in reservaciones:
        if reservacion['fecha'] == fecha_consulta:
            reservaciones_encontradas.append(reservacion)

    limpiar_pantalla()
    print("*"*95)
    print(f"**                      REPORTE DE RESERVACIONES PARA EL DÍA {fecha_consulta.strftime('%d/%m/%Y')}                      **")
    print("*"*95)

    if not reservaciones_encontradas:
        print("\n         No se encontraron reservaciones para esta fecha.         ")
    else:

        print(f"\n{'SALA':<20} | {'CLIENTE':<25} | {'EVENTO':<30} | {'TURNO'}")
        print("-" * 90)
        for reservacion in reservaciones_encontradas:

            nombre_sala = salas[reservacion['sala_id']]['nombre']
            cliente_info = clientes[reservacion['cliente_id']]
            nombre_cliente = f"{cliente_info['nombre']} {cliente_info['apellidos']}"

            print(f"{nombre_sala:<20} | {nombre_cliente:<25} | {reservacion['evento']:<30} | {reservacion['turno']}")

    print("\n")
    print("*"*95)
    print("**                                  FIN DEL REPORTE                                          **")
    print("*"*95)
    input("\n\n                   -->ENTER para coninuar...")


def registrar_cliente():
    global id_cliente_siguiente

    limpiar_pantalla()
    print("*"*28)
    print("REGISTRO DE UN NUEVO CLIENTE")
    print("*"*28)

    while True:
        nombre = input("Nombre del cliente: ")
        if nombre.strip():
            break
        else:
            print("El nombre no puede estar vacío.")

    while True:
        apellidos = input("Apellidos del cliente: ")
        if apellidos.strip():
            break
        else:
            print("Los apellidos no pueden estar vacíos.")

    clientes[id_cliente_siguiente] = {'nombre': nombre, 'apellidos': apellidos}
    id_cliente_siguiente += 1

    input(f"\n¡Cliente '{nombre} {apellidos}' registrado con éxito!\nEl ID único del cliente es: {id_cliente_siguiente - 1}\n\n   -->ENTER para continuar.")


def registrar_sala():
    global id_sala_siguiente

    limpiar_pantalla()

    print("*"*28)
    print("    REGISTRO DE LA SALA")
    print("*"*28)

    while True:
        nombre = input("Dame el nombre de la sala: ")
        if nombre:
            break
        else:
            print("El nombre de la sala no puede estar vacío, intente de nuevo.")

    while True:
        try:
            cupo = int(input("Dame el cupo de la sala: "))
            if cupo > 0:
                break
            else:
                print("La sala tiene que tener un cupo mayor a 0")
        except ValueError:
            print("Error: Ingrese solo números para el cupo.")

    salas[id_sala_siguiente] = {'nombre':nombre,'cupo':cupo}
    id_sala_siguiente += 1

    input(f"\n¡¡Sala '{nombre}' registrada con exitosamente!!\nEl ID de tu sala es: {id_sala_siguiente - 1}!\n\n   -->ENTER para continuar.")

# =================================================================
# 5. DEFINICIÓN DE LA FUNCION PRINCIPAL "main()"
# =================================================================
def main():
    while True:
        respuesta = input("¿Deseas cargar datos de prueba? (S/N): ").upper()
        if respuesta == 'S':
            cargar_datos_de_prueba()
            input("--> Datos de prueba cargados. Presiona Enter para iniciar el menú...")
            break
        elif respuesta == 'N':
            print("\nIniciando el programa con datos vacíos.")
            input("--> Presiona Enter para iniciar el menú...")
            break
        else:
            print("Opción no válida. Por favor, responde 'S' para sí o 'N' para no.")

    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input("   > Selecciona una opción: ")

        if opcion == '1':
            registrar_reservacion()
        elif opcion == '2':
            editar_nombre_evento()
        elif opcion == '3':
            consultar_reservaciones()
        elif opcion == '4':
            registrar_cliente()
        elif opcion == '5':
            registrar_sala()
        elif opcion == '6':
            print("\nGracias por usar el sistema. ¡Hasta pronto!")
            break
        else:
            input("\nOpción no válida. Por favor, intenta de nuevo. (ENTER)")

# =================================================================
# 6. INICIO DE LA EJECUCIÓN DEL PROGRAMA
# =================================================================
main()