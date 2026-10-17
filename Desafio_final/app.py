import secrets

from flask import Flask, flash, redirect, render_template, request, url_for

import logica

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def mostrar_pagina(busqueda=None):
    return render_template(
        "index.html",
        pendientes=logica.cola_pendientes,
        historial=logica.pila_historial,
        siguiente=logica.consultar_siguiente(),
        estadisticas=logica.obtener_estadisticas(),
        busqueda=busqueda
    )


@app.get("/")
def inicio():
    return mostrar_pagina()


@app.post("/registrar")
def registrar():
    cliente = request.form.get("cliente", "")
    asunto = request.form.get("asunto", "")
    nueva = logica.registrar_solicitud(cliente, asunto)

    if nueva:
        flash(f"Solicitud ID {nueva['id']} registrada para {nueva['cliente']}.", "success")
    else:
        duplicada = logica.buscar_duplicado(cliente, asunto)
        if duplicada:
            flash(f"Esa solicitud ya se encuentra pendiente con el ID {duplicada['id']}. No se registró otra vez.", "warning")
        else:
            flash("Cliente y asunto son obligatorios.", "danger")

    return redirect(url_for("inicio"))


@app.post("/atender")
def atender():
    atendida = logica.atender_siguiente()
    if atendida:
        flash(f"Se atendió la solicitud ID {atendida['id']} de {atendida['cliente']}.", "success")
    else:
        flash("No hay solicitudes pendientes para atender.", "warning")
    return redirect(url_for("inicio"))


@app.post("/deshacer")
def deshacer():
    restaurada = logica.deshacer_ultima_atencion()
    if restaurada:
        flash(f"La solicitud ID {restaurada['id']} de {restaurada['cliente']} volvió al inicio de la cola.", "success")
    else:
        flash("No hay atenciones en el historial para deshacer.", "warning")
    return redirect(url_for("inicio"))


@app.get("/buscar")
def buscar():
    id_solicitud = request.args.get("id", type=int)
    if id_solicitud is None or id_solicitud <= 0:
        flash("Escribe un ID válido: debe ser un entero positivo.", "danger")
        return redirect(url_for("inicio"))

    busqueda = {
        "id": id_solicitud,
        "resultado": logica.buscar_solicitud(id_solicitud)
    }
    return mostrar_pagina(busqueda)


@app.post("/cancelar/<int:id_solicitud>")
def cancelar(id_solicitud):
    cancelada = logica.cancelar_pendiente(id_solicitud)
    if cancelada:
        flash(f"Se canceló la solicitud ID {cancelada['id']} de {cancelada['cliente']}.", "success")
    else:
        flash(f"La solicitud ID {id_solicitud} no está pendiente. Solo se pueden cancelar solicitudes de la cola.", "warning")
    return redirect(url_for("inicio"))


@app.post("/deshacer-varias")
def deshacer_varias():
    cantidad = request.form.get("cantidad", type=int)
    restauradas = logica.deshacer_varias(cantidad)

    if restauradas is None:
        flash("La cantidad debe ser un entero positivo.", "danger")
    elif restauradas == 0:
        flash("No hay atenciones en el historial para deshacer.", "warning")
    elif restauradas < cantidad:
        flash(f"Pediste deshacer {cantidad}, pero solo había {restauradas} disponibles. Se restauraron {restauradas}.", "info")
    else:
        flash(f"Se restauraron {restauradas} solicitudes.", "success")

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
