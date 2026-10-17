
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


def cancelar_pendiente(id_solicitud):
    for indice, solicitud in enumerate(cola_pendientes):
        if solicitud["id"] == id_solicitud:
            eliminada = cola_pendientes.pop(indice)
            eliminada["estado"] = "cancelada"
            return eliminada
    return None


def clientes(lista):
    return [solicitud["cliente"] for solicitud in lista]


def comprobar(descripcion, obtenido, esperado):
    correcto = obtenido == esperado
    print(("OK    | " if correcto else "FALLA | ") + descripcion)
    print(f"        esperado: {esperado}")
    print(f"        obtenido: {obtenido}")
    return correcto


def probar():
    print("Reto 3: Cancelar una solicitud pendiente")
    print("Entrada: cola A, B, C; se cancela B; luego se atiende A y se intenta cancelarla")
    print("Salida esperada: quedan A, C en ese orden; la solicitud atendida no se puede cancelar\n")

    registrar_solicitud("A", "Asunto A")
    registrar_solicitud("B", "Asunto B")
    registrar_solicitud("C", "Asunto C")

    resultados = []
    cancelada = cancelar_pendiente(2)
    resultados.append(comprobar("Cancelar el ID 2 devuelve a B", cancelada["cliente"], "B"))
    resultados.append(comprobar("Las demás mantienen su orden relativo", clientes(cola_pendientes), ["A", "C"]))

    atender_siguiente()
    resultados.append(comprobar("Una solicitud atendida no se cancela", cancelar_pendiente(1), None))
    resultados.append(comprobar("La atendida sigue en el historial", clientes(pila_historial), ["A"]))
    resultados.append(comprobar("Un ID inexistente devuelve None", cancelar_pendiente(99), None))

    print(f"\nResultado: {sum(resultados)} de {len(resultados)} pruebas correctas")


if __name__ == "__main__":
    probar()
