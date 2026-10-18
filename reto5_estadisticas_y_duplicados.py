cola_pendientes = []
pila_historial = []
siguiente_id = 1


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


def comprobar(descripcion, obtenido, esperado):
    correcto = obtenido == esperado
    print(("OK    | " if correcto else "FALLA | ") + descripcion)
    print(f"        esperado: {esperado}")
    print(f"        obtenido: {obtenido}")
    return correcto


def probar():
    print("Reto 5: Estadísticas y control de duplicados")
    print("Entrada: se registra dos veces «Ana / Wi-Fi» y una vez « ana / wi-fi »; luego Luis y Sofía; se atiende una")
    print("Salida esperada: solo un pendiente de Ana; estadísticas con 2 pendientes, 1 atendida y 3 únicas\n")

    resultados = []
    primera = registrar_solicitud("Ana", "Wi-Fi")
    segunda = registrar_solicitud("Ana", "Wi-Fi")
    tercera = registrar_solicitud(" ana ", " wi-fi ")
    resultados.append(comprobar("La primera vez sí se registra", primera["id"], 1))
    resultados.append(comprobar("La repetida exacta no se registra", segunda, None))
    resultados.append(comprobar("La repetida con mayúsculas y espacios no se registra", tercera, None))
    resultados.append(comprobar("Solo hay un pendiente", len(cola_pendientes), 1))

    registrar_solicitud("Luis", "Impresora sin papel")
    registrar_solicitud("Sofía", "Equipo lento")
    atender_siguiente()

    estadisticas = obtener_estadisticas()
    resultados.append(comprobar("Cantidad de pendientes", estadisticas["pendientes"], 2))
    resultados.append(comprobar("Atenciones en el historial", estadisticas["atendidas"], 1))
    resultados.append(comprobar("Total de solicitudes únicas", estadisticas["total_unicas"], 3))

    otra = registrar_solicitud("Ana", "Wi-Fi")
    resultados.append(comprobar("Si la anterior ya fue atendida, se acepta una nueva igual", otra is not None, True))

    print(f"\nResultado: {sum(resultados)} de {len(resultados)} pruebas correctas")


if __name__ == "__main__":
    probar()
