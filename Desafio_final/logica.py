cola_pendientes = []
pila_historial = []
siguiente_id = 1


def reiniciar():
    global siguiente_id
    cola_pendientes.clear()
    pila_historial.clear()
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
