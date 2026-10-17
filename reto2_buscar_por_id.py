cola_pendientes = []
pila_historial = []
siguiente_id = 1


def registrar_solicitud(cliente, asunto):
    global siguiente_id
    if not cliente.strip() or not asunto.strip():
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


def ids(lista):
    return [solicitud["id"] for solicitud in lista]


def comprobar(descripcion, obtenido, esperado):
    correcto = obtenido == esperado
    print(("OK    | " if correcto else "FALLA | ") + descripcion)
    print(f"        esperado: {esperado}")
    print(f"        obtenido: {obtenido}")
    return correcto


def probar():
    print("Reto 2: Buscar una solicitud por ID")
    print("Entrada: Ana, Luis y Sofía registrados; se atiende a Ana; se buscan los ID 3, 1 y 99")
    print("Salida esperada: ID 3 en pendientes, ID 1 en historial, ID 99 devuelve None, sin cambiar el orden\n")

    registrar_solicitud("Ana", "No conecta a Wi-Fi")
    registrar_solicitud("Luis", "Impresora sin papel")
    registrar_solicitud("Sofía", "Equipo lento")
    atender_siguiente()

    orden_cola = ids(cola_pendientes)
    orden_pila = ids(pila_historial)

    resultados = []
    en_cola = buscar_solicitud(3)
    resultados.append(comprobar("El ID 3 se encuentra en pendientes", en_cola["ubicacion"], "pendientes"))
    resultados.append(comprobar("El ID 3 es de Sofía", en_cola["solicitud"]["cliente"], "Sofía"))

    en_pila = buscar_solicitud(1)
    resultados.append(comprobar("El ID 1 se encuentra en el historial", en_pila["ubicacion"], "historial"))
    resultados.append(comprobar("El ID 1 es de Ana", en_pila["solicitud"]["cliente"], "Ana"))

    resultados.append(comprobar("Un ID inexistente devuelve None", buscar_solicitud(99), None))
    resultados.append(comprobar("El orden de la cola no cambió", ids(cola_pendientes), orden_cola))
    resultados.append(comprobar("El orden de la pila no cambió", ids(pila_historial), orden_pila))

    print(f"\nResultado: {sum(resultados)} de {len(resultados)} pruebas correctas")


if __name__ == "__main__":
    probar()
