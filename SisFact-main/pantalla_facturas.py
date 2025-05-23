
import flet as ft
import os
import datetime
from pathlib import Path
import shutil
import platform
import subprocess
import csv

def __view__(page, nombre_empresa, direccion_carpeta):

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        fecha.open = True
        page.update()

    def open_dlg_modal_2(e):
        page.dialog = dlg_modal_2
        dlg_modal_2.open = True
        fecha.open = True
        page.update()

    def open_dlg_fecha(e, files, direccion):
        page.dialog = dlg_fecha
        dlg_fecha.open = True
        fecha.open = True
        global archivos_a_cargar
        archivos_a_cargar = files
        global carpeta_destino
        carpeta_destino = direccion
        page.update()

    def close_dlg_fecha(e):
        fecha.value = ""
        dlg_fecha.open = False
        page.update()

    numero_factura = ft.TextField(label="No. de Factura")
    fecha_vencimiento = ft.DatePicker(on_change=lambda e: actualizar_fecha_vencimiento(e))
    fecha_emision = ft.DatePicker(on_change=lambda e: actualizar_fecha_emision(e))
    forma_pago = ft.TextField(label="Forma de Pago")
    fecha = ft.DatePicker()
    fecha_emision_text = ft.Text(value="", size=14)
    fecha_vencimiento_text = ft.Text(value="", size=14)
    evidencia_soporte = ft.TextField(label="Evidencia de soporte")

    items = []

    def agregar_item(e):
        if item_descripcion.value and item_cantidad.value:
            items.append({"descripcion": item_descripcion.value, "cantidad": item_cantidad.value})
            item_descripcion.value = ""
            item_cantidad.value = ""
            actualizar_lista_items()
            page.update()

    def eliminar_item(index):
        items.pop(index)
        actualizar_lista_items()
        page.update()

    def actualizar_lista_items():
        lista_items.controls.clear()
        for i, item in enumerate(items):
            lista_items.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(f"{item['cantidad']} x {item['descripcion']}"),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=i: eliminar_item(idx))
                    ]
                )
            )
        page.update()

    item_descripcion = ft.TextField(label="Descripción del Ítem")
    item_cantidad = ft.TextField(label="Cantidad", width=100)
    lista_items = ft.Column()

    fecha_emision_button = ft.ElevatedButton(
    text="Seleccionar Fecha de Emisión",
    icon=ft.icons.CALENDAR_MONTH,
    on_click=lambda _: fecha_emision.pick_date(),
)

    fecha_vencimiento_button = ft.ElevatedButton(
    text="Seleccionar Fecha de Vencimiento",
    icon=ft.icons.CALENDAR_MONTH,
    on_click=lambda _: fecha_vencimiento.pick_date(),
)
    
    def actualizar_fecha_emision(e):
        fecha_emision_text.value = f"Seleccionada: {fecha_emision.value}"
        page.update()

    def actualizar_fecha_vencimiento(e):
        fecha_vencimiento_text.value = f"Seleccionada: {fecha_vencimiento.value}"
        page.update()

    def close_dlg(e):
        numero_factura.value = ""
        fecha_emision.value = ""
        fecha_vencimiento.value = ""
        forma_pago.value = ""
        valor_factura.value = ""
        evidencia_soporte.value = ""
        items.clear()
        actualizar_lista_items()
        dlg_modal.open = False
        page.update()

    def close_dlg_2(e):
        numero_factura.value = ""
        fecha_emision.value = ""
        fecha_vencimiento.value = ""
        forma_pago.value = ""
        valor_factura.value = ""
        evidencia_soporte.value = ""
        items.clear()
        actualizar_lista_items()
        dlg_modal_2.open = False
        page.update()

    valor_factura = ft.TextField(label="Valor por Pagar")

    def agregar_archivo_no_pagadas(e):
        if numero_factura.value != "":
            ruta_archivo = os.path.join(direccion_carpeta + "/no_pagadas/" + numero_factura.value + ".txt")
            with open(ruta_archivo, "w") as archivo:
                archivo.write(f"Número de Factura: {numero_factura.value}\n")
                archivo.write(f"Fecha de Emisión: {fecha_emision.value}\n")
                archivo.write(f"Fecha de Vencimiento: {fecha_vencimiento.value}\n")
                archivo.write(f"Forma de Pago: {forma_pago.value}\n")
                archivo.write("Ítems:\n")
                for item in items:
                    archivo.write(f"  - {item['cantidad']} x {item['descripcion']}\n")
                archivo.write(f"Valor por Pagar: {valor_factura.value}\n")
                archivo.write(f"Evidencia de soporte: {evidencia_soporte.value}\n")  # Guardar evidencia
            with open(os.path.join(direccion_carpeta, "registro.csv"), mode="a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([numero_factura.value + ".txt", fecha_vencimiento.value, "False"])
            cargar_tabla_1(numero_factura.value + ".txt", fecha_vencimiento.value)
            close_dlg(e)

    def agregar_archivo_pagadas(e):
        if numero_factura.value:
            ruta_archivo = os.path.join(direccion_carpeta + "/pagadas/" + numero_factura.value + ".txt")
            with open(ruta_archivo, "w") as archivo:
                archivo.write(f"Número de Factura: {numero_factura.value}\n")
                archivo.write(f"Fecha de Emisión: {fecha_emision.value}\n")
                archivo.write(f"Fecha de Vencimiento: {fecha_vencimiento.value}\n")
                archivo.write(f"Forma de Pago: {forma_pago.value}\n")
                archivo.write("Ítems:\n")
                for item in items:
                    archivo.write(f"  - {item['cantidad']} x {item['descripcion']}\n")
                archivo.write(f"Valor por Pagar: {valor_factura.value}\n")
                archivo.write(f"Evidencia de soporte: {evidencia_soporte.value}\n")  # Guardar evidencia
            with open(os.path.join(direccion_carpeta, "registro.csv"), mode="a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([numero_factura.value + ".txt", fecha_vencimiento.value, "True"])
            cargar_tabla_2(numero_factura.value + ".txt", fecha_vencimiento.value)
            close_dlg_2(e)

    def agregar_archivos_cargados(e):
        global archivos_a_cargar
        global carpeta_destino
        if carpeta_destino == "/no_pagadas":
            facturado = "False"
        else:
            facturado = "True"
        if fecha_vencimiento.value != "":
            for file in archivos_a_cargar:
                nombre_archivo = Path(file.path).stem
                extension= Path(file.path).suffix
                ruta_archivo = os.path.join(direccion_carpeta + carpeta_destino + "/" + nombre_archivo + extension)
                shutil.move(file.path, ruta_archivo)
                with open(os.path.join(direccion_carpeta, "registro" + ".csv"), mode="a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([nombre_archivo+extension, fecha_vencimiento.value, facturado])
            cargar_tablas()
            page.update()
        close_dlg_fecha(e)

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Crear Factura No Pagada"),
        actions=[
            numero_factura,
            ft.Row([fecha_emision_button, fecha_emision_text]),
            ft.Row([fecha_vencimiento_button, fecha_vencimiento_text]),
            forma_pago,
            ft.Row(controls=[item_cantidad, item_descripcion, ft.ElevatedButton("Agregar Ítem", on_click=agregar_item)]),
            lista_items,
            valor_factura,
            evidencia_soporte,  # Mostrar campo en el formulario
            ft.ElevatedButton("Agregar", on_click=agregar_archivo_no_pagadas),
            ft.ElevatedButton("Cancelar", on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_modal_2 = ft.AlertDialog(
        modal=True,
        title=ft.Text("Crear Factura Pagada"),
        actions=[
            numero_factura,
            ft.Row([fecha_emision_button, fecha_emision_text]),
            ft.Row([fecha_vencimiento_button, fecha_vencimiento_text]),
            forma_pago,
            ft.Row(controls=[item_cantidad, item_descripcion, ft.ElevatedButton("Agregar Ítem", on_click=agregar_item)]),
            lista_items,
            valor_factura,
            evidencia_soporte,  # Mostrar campo en el formulario
            ft.ElevatedButton("Agregar", on_click=agregar_archivo_pagadas),
            ft.ElevatedButton("Cancelar", on_click=close_dlg_2)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    ) 

    page.overlay.append(fecha_emision)
    page.overlay.append(fecha_vencimiento)

    dlg_fecha = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cargar Archivos"),
        actions=[
            fecha_vencimiento,
            ft.ElevatedButton("Agregar", on_click=lambda event: (agregar_archivos_cargados(event))),
            ft.ElevatedButton("Cancelar", on_click=close_dlg_fecha)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    search_field = ft.TextField(label="Buscar por numero de factura", on_change=lambda e: filtrar_tablas())
    date_field_text = ft.Text("Filtrar por fecha: ")

    def on_date_change(e):
        if date_filter.value:
            date_button.text = date_filter.value
        else:
            date_button.text = "Pick date"
        filtrar_tablas()
        page.update()

    date_filter = ft.DatePicker(on_change=on_date_change)
    page.overlay.append(date_filter)

    date_button = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: date_filter.pick_date(),
    )

    def clear_date_filter(e):
        date_filter.value = None
        date_button.text = "Pick date"
        filtrar_tablas()
        page.update()

    clear_date_button = ft.ElevatedButton(
        "Clear date",
        icon=ft.icons.CLEAR,
        on_click=clear_date_filter,
    )

    def filtrar_tablas():
        search_query = search_field.value.lower()
        selected_date = date_filter.value
        tabla1.rows.clear()
        tabla2.rows.clear()
        
        with open(Path(direccion_carpeta) / "registro.csv", mode="r") as archivo:
            reader = csv.reader(archivo)
            for fila in reader:
                if fila[0] != "nombre_factura":
                    facturado = fila[2] == 'True'
                    nombre_factura = fila[0]
                    fecha_factura = fila[1]
    
                    # Validar formato de fecha
                    try:
                        datetime.datetime.strptime(fecha_factura, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        print(f"Fecha inválida encontrada: {fecha_factura}")
                        continue
    
                    # Filtrar por nombre
                    if search_query and search_query not in nombre_factura.lower():
                        continue
                    
                    # Filtrar por fecha
                    if selected_date and selected_date != datetime.datetime.strptime(fecha_factura, "%Y-%m-%d %H:%M:%S"):
                        continue
    
                    if not facturado:
                        cargar_tabla_1(nombre_factura, fecha_factura)
                    else:
                        cargar_tabla_2(nombre_factura, fecha_factura)
        
        page.update()

    global selected_rows
    selected_rows = []

    def get_index(e):
        global selected_rows
        row = e.control
        name = row.cells[0].content.text

        if row.selected:
            row.selected = False
            row.style = None
            selected_rows = [r for r in selected_rows if r[0] != name]
        else:
            row.selected = True
            row.style = ft.TextStyle(bgcolor="yellow")
            selected_rows.append([name, row])

        page.update()

    tabla1 = ft.DataTable(
        border=ft.border.all(1, 'black'),
        border_radius=10,
        horizontal_lines=ft.border.BorderSide(1, 'black'),
        show_checkbox_column=True,
        sort_ascending=True,
        expand=False,
        data_row_max_height=float("inf"),
        width= 450,
        columns=[
            ft.DataColumn(
                ft.Text("Factura"),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
            ft.DataColumn(
                ft.Text("Fecha de vencimiento"),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
        ]
    )

    def abrir_archivo(nombre, tipo):
        if tipo == "no_pagadas":
            file_path = Path(direccion_carpeta) / "no_pagadas" / nombre
        else:
            file_path = Path(direccion_carpeta) / "pagadas" / nombre

        if os.path.exists(file_path):
            try:
                if platform.system() == 'Windows':
                    os.startfile(file_path)  # Para Windows
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', file_path])
                else:  # Linux
                    subprocess.run(['xdg-open', file_path])
            except Exception as e:
                print(f"No se pudo abrir el archivo: {e}")
        else:
            print(f"El archivo {file_path} no existe.")

    def calcular_dias_restantes(fecha_mod):
        if isinstance(fecha_mod, str):
            fecha_obj = datetime.datetime.strptime(fecha_mod, "%Y-%m-%d %H:%M:%S")
        else:
            fecha_obj = fecha_mod
        fecha_actual = datetime.datetime.now()
        diferencia = fecha_obj - fecha_actual
        return abs(diferencia.days)

    def determinar_color_fila(dias_restantes):
        if dias_restantes >= 180:
            return "red"
        elif dias_restantes >= 30:
            return "yellow"
        elif dias_restantes >= 7:
            return "#ff9800"
        elif dias_restantes >= 1:
            return "#4fc3f7"
        else:
            return "#4fc3f7"

    def cargar_tabla_1(nombre, fecha_mod):
        dias_restantes = calcular_dias_restantes(fecha_mod)
        color_fila = determinar_color_fila(dias_restantes)

        tabla1.rows.append(
            ft.DataRow(
                on_select_changed=get_index,
                cells=[
                    ft.DataCell(ft.TextButton(
                        text=nombre, 
                        on_click=lambda e: abrir_archivo(nombre, "no_pagadas"),
                    )),
                    ft.DataCell(ft.Text(fecha_mod,))  # Permitir que el texto se ajuste
                ],
                color=color_fila,
            )
        )
        try:
            tabla1.update()
        except Exception as e:
            print(f"Error al actualizar las tablas: {e}")

    tabla2 = ft.DataTable(
        border=ft.border.all(1, 'black'),
        border_radius=10,
        horizontal_lines=ft.border.BorderSide(1, 'black'),
        show_checkbox_column=True,
        sort_ascending=True,
        expand=False,
        data_row_max_height=float("inf"),
        width= 450,
        columns=[
            ft.DataColumn(
                ft.Text("Factura"),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
            ft.DataColumn(
                ft.Text("Fecha de vencimiento"),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
        ]
    )

    def cargar_tabla_2(nombre, fecha_mod):
        tabla2.rows.append(
            ft.DataRow(
                on_select_changed=get_index,
                cells=[
                    ft.DataCell(ft.TextButton(
                        text=nombre, 
                        on_click=lambda e: abrir_archivo(nombre, "pagadas"),
                    )),
                    ft.DataCell(ft.Text(fecha_mod))  # Permitir que el texto se ajuste
                ],
            ),
        )
        try:
            tabla2.update()
        except Exception as e:
            print(f"Error 2 al actualizar las tablas: {e}")

    titulo_tabla_1 = ft.Text(value="No Pagadas", size=30, weight=ft.FontWeight.BOLD, color="#1976d2")
    titulo_tabla_2 = ft.Text(value="Pagadas", size=30, weight=ft.FontWeight.BOLD, color="#388e3c")

    with open(Path(direccion_carpeta) / "registro.csv", mode="r") as archivo:
        reader = csv.reader(archivo)
        for fila in reader:
            if fila[0] != "nombre_factura":
                facturado = fila[2] == 'True'  # Convertir cadena a booleano
                if not facturado:
                    cargar_tabla_1(fila[0], fila[1])
                else:
                    cargar_tabla_2(fila[0], fila[1])

    def mover_archivo(nombre_archivo, origen, destino):
        origen_archivo = Path(origen) / nombre_archivo
        destino_archivo = Path(destino) / nombre_archivo
        shutil.move(origen_archivo, destino_archivo)

    def mover_factura(nombre_factura, direccion):
        updated_rows = []
        with open(Path(direccion_carpeta) / "registro.csv", mode='r') as file:
            reader = csv.reader(file)
            for fila in reader:
                if fila[0] == nombre_factura:
                    fila[2] = 'False' if direccion == 'izquierda' else 'True'
                updated_rows.append(fila)

        with open(Path(direccion_carpeta) / "registro.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        origen = direccion_carpeta + '/pagadas' if direccion == 'izquierda' else direccion_carpeta + '/no_pagadas'
        destino = direccion_carpeta + '/no_pagadas' if direccion == 'izquierda' else direccion_carpeta + '/pagadas'
        mover_archivo(nombre_factura, origen, destino)

    def mover_facturas_seleccionadas(direccion):
        global selected_rows
        for row in selected_rows:
            nombre_factura = row[0]
            mover_factura(nombre_factura, direccion)
        cargar_tablas()
        selected_rows = []

    def eliminar_facturas_seleccionadas(e):
        global selected_rows
        for row in selected_rows:
            nombre_factura = row[0]
            ruta_archivo_no_pagadas = Path(direccion_carpeta) / "no_pagadas" / nombre_factura
            ruta_archivo_pagadas = Path(direccion_carpeta) / "pagadas" / nombre_factura
            if ruta_archivo_no_pagadas.exists():
                os.remove(ruta_archivo_no_pagadas)
            if ruta_archivo_pagadas.exists():
                os.remove(ruta_archivo_pagadas)
            eliminar_registro_csv(nombre_factura)
        cargar_tablas()
        selected_rows = []
    
    def eliminar_registro_csv(nombre_archivo):
        registros = []
        archivo_registro = os.path.join(direccion_carpeta, "registro.csv")
        
        # Leer todos los registros del CSV
        with open(archivo_registro, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != nombre_archivo:
                    registros.append(row)
        
        # Sobrescribir el CSV sin el registro eliminado
        with open(archivo_registro, mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(registros)
        cargar_tablas()
        page.update()

    def cargar_tablas():
        global selected_rows
        selected_rows = []
        tabla1.rows.clear()
        tabla2.rows.clear()
        with open(Path(direccion_carpeta) / "registro.csv", mode="r") as archivo:
            reader = csv.reader(archivo)
            for fila in reader:
                if fila[0] != "nombre_factura":
                    facturado = fila[2] == 'True'  # Convertir cadena a booleano
                    if not facturado:
                        cargar_tabla_1(fila[0], fila[1])
                    else:
                        cargar_tabla_2(fila[0], fila[1])
        page.update()

    def on_dialog_result(e):
        open_dlg_fecha(e, e.files, direccion1)

    filepicker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(filepicker)
    page.update()

    def files_p(direccion):
        global direccion1
        direccion1 = direccion
        filepicker.pick_files(allow_multiple=True)

    boton_izquierda = ft.ElevatedButton(
        text="←",
        icon=ft.icons.ARROW_LEFT,
        style=ft.ButtonStyle(
            bgcolor="#1976d2",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(10, 10, 10, 10)
        ),
        on_click=lambda event: mover_facturas_seleccionadas('izquierda')
    )
    boton_derecha = ft.ElevatedButton(
        text="→",
        icon=ft.icons.ARROW_RIGHT,
        style=ft.ButtonStyle(
            bgcolor="#388e3c",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(10, 10, 10, 10)
        ),
        on_click=lambda event: mover_facturas_seleccionadas('derecha')
    )
    boton_eliminar = ft.ElevatedButton(
        text="Eliminar Seleccionadas",
        icon=ft.icons.DELETE,
        style=ft.ButtonStyle(
            bgcolor="#d32f2f",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(10, 10, 10, 10)
        ),
        on_click=eliminar_facturas_seleccionadas
    )
    boton_agregar_tabla_1 = ft.FilledButton(
        text="Nueva factura no pagada",
        icon=ft.icons.ADD,
        style=ft.ButtonStyle(
            bgcolor="#1976d2",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(10, 10, 10, 10)
        ),
        on_click=open_dlg_modal
    )
    boton_agregar_tabla_2 = ft.FilledButton(
        text="Nueva factura pagada",
        icon=ft.icons.ADD,
        style=ft.ButtonStyle(
            bgcolor="#388e3c",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(10, 10, 10, 10)
        ),
        on_click=open_dlg_modal_2
    )

    # Crear botones cargar archivos
    #boton_agregar_archivos1 = ft.ElevatedButton(text="Cargar archivos", on_click=lambda event: files_p("/no_pagadas"))
    #boton_agregar_archivos2 = ft.ElevatedButton(text="Cargar archivos", on_click=lambda event: files_p("/pagadas"))

    fila_tabla_1 = ft.Column(
        controls=[tabla1],
        scroll=ft.ScrollMode.ALWAYS,
        height=350,
    )

    fila_tabla_2 = ft.Column(
        controls=[tabla2],
        scroll=ft.ScrollMode.ALWAYS,
        height=350,
    )

    # Crear filas para las tablas y botones (sin los de cargar archivos)
    fila_boton_tabla_1 = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[titulo_tabla_1, fila_tabla_1, boton_agregar_tabla_1])
    fila_boton_tabla_2 = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[titulo_tabla_2, fila_tabla_2, boton_agregar_tabla_2])

    # Modificar la fila para incluir los botones
    fila = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=100,
        width='90%',
        height='auto',
        controls=[
            fila_boton_tabla_1,
            ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[boton_izquierda, boton_derecha, boton_eliminar]),
            fila_boton_tabla_2
        ],
    )

    legend = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,  # Centrar horizontalmente
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,  # Más espacio entre los elementos
        controls=[
            ft.Container(width=18, height=18, bgcolor="red", border_radius=4),
            ft.Text("6 meses o más", size=13, color="#2d3a4a"),
            ft.Container(width=18, height=18, bgcolor="yellow", border_radius=4),
            ft.Text("Menos de 6 meses", size=13, color="#2d3a4a"),
            ft.Container(width=18, height=18, bgcolor="#ff9800", border_radius=4),  # Naranja
            ft.Text("Menos de un mes", size=13, color="#2d3a4a"),
            ft.Container(width=18, height=18, bgcolor="#4fc3f7", border_radius=4),  # Azul cielo
            ft.Text("Menos de una semana", size=13, color="#2d3a4a")
        ]
    )
    
    respuesta = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[search_field, date_field_text, date_button, clear_date_button]
                ),
                bgcolor="#e3eafc",  # Color suave de fondo
                border_radius=10,
                padding=10,
            ),
            fila,
            ft.Container(legend, margin=ft.margin.only(top=15)),  # Separación extra arriba del legend
        ],
        alignment=ft.alignment.center
    )

    page.update()

    return respuesta
