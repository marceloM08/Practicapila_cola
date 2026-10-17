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


def consultar_siguiente():
    if not cola_pendientes:
        return None
    return cola_pendientes[0]


def comprobar(descripcion, obtenido, esperado):
    correcto = obtenido == esperado
    print(("OK    | " if correcto else "FALLA | ") + descripcion)
    print(f"        esperado: {esperado}")
    print(f"        obtenido: {obtenido}")
    return correcto


def probar():
    print("Reto 1: Consultar el siguiente turno sin extraerlo")
    print("Entrada: cola vacía; luego se registran Ana, Luis y Sofía y se consulta dos veces")
    print("Salida esperada: None con la cola vacía; después ID 1 en ambas consultas y la cola sigue con 3\n")

    resultados = []
    resultados.append(comprobar("Con la cola vacía devuelve None", consultar_siguiente(), None))

    registrar_solicitud("Ana", "No conecta a Wi-Fi")
    registrar_solicitud("Luis", "Impresora sin papel")
    registrar_solicitud("Sofía", "Equipo lento")

    primera = consultar_siguiente()
    segunda = consultar_siguiente()
    resultados.append(comprobar("La primera consulta devuelve el ID 1", primera["id"], 1))
    resultados.append(comprobar("La segunda consulta devuelve el mismo ID", segunda["id"], primera["id"]))
    resultados.append(comprobar("La longitud de la cola no varía", len(cola_pendientes), 3))

    print(f"\nResultado: {sum(resultados)} de {len(resultados)} pruebas correctas")


if __name__ == "__main__":
    probar()
