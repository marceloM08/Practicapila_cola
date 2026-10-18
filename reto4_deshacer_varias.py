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


def deshacer_ultima_atencion():
    if not pila_historial:
        return None

    solicitud = pila_historial.pop()
    solicitud["estado"] = "pendiente"
    cola_pendientes.insert(0, solicitud)
    return solicitud


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


def clientes(lista):
    return [solicitud["cliente"] for solicitud in lista]


def comprobar(descripcion, obtenido, esperado):
    correcto = obtenido == esperado
    print(("OK    | " if correcto else "FALLA | ") + descripcion)
    print(f"        esperado: {esperado}")
    print(f"        obtenido: {obtenido}")
    return correcto


def probar():
    print("Reto 4: Deshacer varias atenciones")
    print("Entrada: cola A, B, C, D; se atienden A, B y C; se deshacen dos")
    print("Salida esperada: pendientes B, C, D y solo A permanece atendida\n")

    registrar_solicitud("A", "Asunto A")
    registrar_solicitud("B", "Asunto B")
    registrar_solicitud("C", "Asunto C")
    registrar_solicitud("D", "Asunto D")
    atender_siguiente()
    atender_siguiente()
    atender_siguiente()

    resultados = []
    resultados.append(comprobar("Deshacer dos informa 2 restauradas", deshacer_varias(2), 2))
    resultados.append(comprobar("Quedan pendientes B, C, D", clientes(cola_pendientes), ["B", "C", "D"]))
    resultados.append(comprobar("Solo A permanece atendida", clientes(pila_historial), ["A"]))

    for invalido in [0, -1, "2", 2.5, True]:
        resultados.append(comprobar(f"La cantidad {invalido!r} no es un entero positivo", deshacer_varias(invalido), None))
    resultados.append(comprobar("Las cantidades inválidas no cambian la pila", clientes(pila_historial), ["A"]))

    resultados.append(comprobar("Si pide 5 y solo hay 1, restaura e informa 1", deshacer_varias(5), 1))
    resultados.append(comprobar("La pila queda vacía", pila_historial, []))

    print(f"\nResultado: {sum(resultados)} de {len(resultados)} pruebas correctas")


if __name__ == "__main__":
    probar()
