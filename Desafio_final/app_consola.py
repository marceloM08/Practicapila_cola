cola_pendientes = []
pila_historial = []
siguiente_id = 1


def reiniciar():
    global siguiente_id
    cola_pendientes.clear()
    pila_historial.clear()
    siguiente_id = 1


def describir(solicitud):
    if solicitud is None:
        return "Ninguna"
    return f"ID {solicitud['id']} | {solicitud['cliente']} | {solicitud['asunto']} | {solicitud['estado']}"


def mostrar_estado():
    print("\nPendientes (FIFO, el primero es el siguiente turno):")
    if not cola_pendientes:
        print("  Sin pendientes")
    for turno, solicitud in enumerate(cola_pendientes, start=1):
        print(f"  {turno}. {describir(solicitud)}")

    print("Historial (LIFO, el primero es la cima de la pila):")
    if not pila_historial:
        print("  Sin atenciones")
    for posicion, solicitud in enumerate(reversed(pila_historial), start=1):
        print(f"  {posicion}. {describir(solicitud)}")


def normalizar(texto):
    return texto.strip().lower()


def buscar_duplicado(cliente, asunto):
    cliente_normal = normalizar(cliente)
    asunto_normal = normalizar(asunto)
    for solicitud in cola_pendientes:
        mismo_cliente = normalizar(solicitud["cliente"]) == cliente_normal
        mismo_asunto = normalizar(solicitud["asunto"]) == asunto_normal
        if mismo_cliente and mismo_asunto:
            return solicitud
    return None


def registrar_solicitud(cliente, asunto):
    global siguiente_id
    if not cliente.strip() or not asunto.strip():
        return None
    if buscar_duplicado(cliente, asunto):
        return None

    solicitud = {
        "id": siguiente_id,
        "cliente": cliente.strip(),
        "asunto": asunto.strip(),
        "estado": "pendiente"
    }
    cola_pendientes.append(solicitud)
    siguiente_id += 1
    return solicitud


def atender_siguiente():
    if not cola_pendientes:
        return None

    solicitud = cola_pendientes.pop(0)
    solicitud["estado"] = "atendida"
    pila_historial.append(solicitud)
    return solicitud


def deshacer_ultima_atencion():
    if not pila_historial:
        return None

    solicitud = pila_historial.pop()
    solicitud["estado"] = "pendiente"
    cola_pendientes.insert(0, solicitud)
    return solicitud


def consultar_siguiente():
    if not cola_pendientes:
        return None
    return cola_pendientes[0]


def buscar_solicitud(id_solicitud):
    for indice, solicitud in enumerate(cola_pendientes):
        if solicitud["id"] == id_solicitud:
            return {
                "solicitud": solicitud,
                "ubicacion": "pendientes",
                "posicion": indice + 1
            }

    for indice, solicitud in enumerate(pila_historial):
        if solicitud["id"] == id_solicitud:
            return {
                "solicitud": solicitud,
                "ubicacion": "historial",
                "posicion": len(pila_historial) - indice
            }

    return None


def cancelar_pendiente(id_solicitud):
    for indice, solicitud in enumerate(cola_pendientes):
        if solicitud["id"] == id_solicitud:
            eliminada = cola_pendientes.pop(indice)
            eliminada["estado"] = "cancelada"
            return eliminada
    return None


def es_entero_positivo(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def deshacer_varias(cantidad):
    if not es_entero_positivo(cantidad):
        return None

    restauradas = 0
    for _ in range(cantidad):
        if deshacer_ultima_atencion() is None:
            break
        restauradas += 1
    return restauradas


def obtener_estadisticas():
    ids_unicos = set()
    for solicitud in cola_pendientes:
        ids_unicos.add(solicitud["id"])
    for solicitud in pila_historial:
        ids_unicos.add(solicitud["id"])

    return {
        "pendientes": len(cola_pendientes),
        "atendidas": len(pila_historial),
        "total_unicas": len(ids_unicos)
    }


def leer_entero(mensaje):
    texto = input(mensaje).strip()
    if texto.isdecimal():
        return int(texto)
    return None


def ejecutar_menu():
    while True:
        print("\n1. Registrar solicitud")
        print("2. Atender siguiente")
        print("3. Deshacer última atención")
        print("4. Mostrar estado")
        print("5. Consultar siguiente turno")
        print("6. Buscar solicitud por ID")
        print("7. Cancelar solicitud pendiente")
        print("8. Deshacer varias atenciones")
        print("9. Ver estadísticas")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            cliente = input("Cliente: ")
            asunto = input("Asunto: ")
            resultado = registrar_solicitud(cliente, asunto)
            if resultado:
                print("Registrada:", describir(resultado))
            elif buscar_duplicado(cliente, asunto):
                print("Ya existe una solicitud pendiente con el mismo cliente y asunto")
            else:
                print("Datos inválidos")

        elif opcion == "2":
            atendida = atender_siguiente()
            if atendida:
                print("Atendida:", describir(atendida))
            else:
                print("No hay solicitudes pendientes")

        elif opcion == "3":
            restaurada = deshacer_ultima_atencion()
            if restaurada:
                print("Restaurada:", describir(restaurada))
            else:
                print("No hay atenciones para deshacer")

        elif opcion == "4":
            mostrar_estado()

        elif opcion == "5":
            siguiente = consultar_siguiente()
            if siguiente:
                print("Siguiente turno:", describir(siguiente))
            else:
                print("No hay solicitudes en espera")

        elif opcion == "6":
            id_solicitud = leer_entero("ID a buscar: ")
            if id_solicitud is None:
                print("ID inválido")
            else:
                resultado = buscar_solicitud(id_solicitud)
                if resultado is None:
                    print("No existe una solicitud con ese ID")
                elif resultado["ubicacion"] == "pendientes":
                    print(f"Pendiente, turno {resultado['posicion']}:", describir(resultado["solicitud"]))
                else:
                    print(f"Atendida, posición {resultado['posicion']} desde la cima:", describir(resultado["solicitud"]))

        elif opcion == "7":
            id_solicitud = leer_entero("ID a cancelar: ")
            if id_solicitud is None:
                print("ID inválido")
            else:
                cancelada = cancelar_pendiente(id_solicitud)
                if cancelada:
                    print("Cancelada:", describir(cancelada))
                else:
                    print("Solo se pueden cancelar solicitudes que sigan pendientes")

        elif opcion == "8":
            cantidad = leer_entero("Cantidad de atenciones a deshacer: ")
            restauradas = deshacer_varias(cantidad)
            if restauradas is None:
                print("La cantidad debe ser un entero positivo")
            else:
                print(f"Se restauraron {restauradas} de {cantidad} solicitadas")

        elif opcion == "9":
            estadisticas = obtener_estadisticas()
            print("Pendientes:", estadisticas["pendientes"])
            print("Atenciones en el historial:", estadisticas["atendidas"])
            print("Total de solicitudes únicas:", estadisticas["total_unicas"])

        elif opcion == "0":
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    ejecutar_menu()
