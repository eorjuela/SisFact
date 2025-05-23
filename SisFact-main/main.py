import shutil
import flet as ft
import pantalla_facturas as pf
import repath as rp
import os
import csv

class UI(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)

        if not os.path.exists('SisFact'):
            os.makedirs('SisFact')
        if not os.path.exists('SisFact/empresas_eliminadas'):
            os.makedirs('SisFact/empresas_eliminadas')
        if not os.path.isfile('SisFact/empresas.csv'):
            with open('SisFact/empresas.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Empresa", "NIT", "Correo", "Telefono", "Direccion"])

        # Campos para agregar empresa
        self.company_name_field = ft.TextField(hint_text="Nombre de la empresa", width=220)
        self.nit_field = ft.TextField(hint_text="NIT", width=220)
        self.email_field = ft.TextField(hint_text="Correo electrónico", width=220)
        self.phone_field = ft.TextField(hint_text="Teléfono", width=220)

        self.dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                width=320,
                height=320,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.company_name_field,
                        self.nit_field,
                        self.email_field,
                        self.phone_field,
                    ]
                ),
            ),
            actions=[
                ft.TextButton(text="Guardar", on_click=self.add_company),
                ft.TextButton(text="Cancelar", on_click=self.dialog_close)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.edit_company_fields = [
            ft.TextField(hint_text="Nombre de la empresa", width=220),
            ft.TextField(hint_text="NIT", width=220),
            ft.TextField(hint_text="Correo electrónico", width=220),
            ft.TextField(hint_text="Teléfono", width=220),
        ]
        self.edit_dialog_a = ft.AlertDialog(
            modal=True,
            visible=True,
            content=ft.Container(
                width=320,
                height=320,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=self.edit_company_fields
                ),
            ),
            actions=[
                ft.TextButton(text="Guardar", on_click=self.update_company),
                ft.TextButton(text="Cancelar", on_click=self.dialog_close)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.searh_field = ft.TextField(
            suffix_icon=ft.icons.SEARCH,
            label="Buscar por empresa",
            border=ft.InputBorder.UNDERLINE,
            border_color="black",
            label_style=ft.TextStyle(color="black"),
            on_change=self.searh_data,
        )
        self.dialogAlert = ft.AlertDialog(
            modal=True,
            visible=True,
            content=ft.Text("La empresa ya existe"),
            actions=[
                ft.TextButton(text="Aceptar", on_click=self.dialog_close)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.info_nombre = ft.Text("")
        self.info_nit = ft.Text("")
        self.info_correo = ft.Text("")
        self.info_telefono = ft.Text("")
        self.info_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text(
                    "Información de la Empresa",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#2d3a4a",
                    text_align=ft.TextAlign.CENTER
                )
            ),
            content=ft.Container(
                width=340,
                height=340,
                bgcolor="#f5f7fa",
                border_radius=20,
                padding=20,
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=18,
                    controls=[
                        ft.Icon(name=ft.icons.BUSINESS, size=48, color="#1976d2"),
                        ft.Divider(height=1, color="#e0e0e0"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Nombre:", size=14, color="#1976d2", weight=ft.FontWeight.BOLD),
                                self.info_nombre,
                            ]
                        ),
                        ft.Divider(height=1, color="#e0e0e0"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("NIT:", size=14, color="#1976d2", weight=ft.FontWeight.BOLD),
                                self.info_nit,
                            ]
                        ),
                        ft.Divider(height=1, color="#e0e0e0"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Correo:", size=14, color="#1976d2", weight=ft.FontWeight.BOLD),
                                self.info_correo,
                            ]
                        ),
                        ft.Divider(height=1, color="#e0e0e0"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Teléfono:", size=14, color="#1976d2", weight=ft.FontWeight.BOLD),
                                self.info_telefono,
                            ]
                        ),
                    ]
                ),
            ),
            actions=[
                ft.TextButton(
                    text="Cerrar",
                    style=ft.ButtonStyle(
                        bgcolor="#1976d2",
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(10, 5, 10, 5)
                    ),
                    on_click=lambda e: self.close_info_dialog()
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.lista_empresas = []
        self.direcciones = {}

        with open('SisFact/empresas.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) >= 5:
                    self.direcciones[row[0]] = {
                        "NIT": row[1],
                        "Correo": row[2],
                        "Telefono": row[3],
                        "Direccion": row[4]
                    }
                    self.lista_empresas.append(row[0])

        self.navigation_bar = ft.Container(
            col=1,
            expand=False,
            height=120,
            content=ft.Column(
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.NavigationBar(
                            bgcolor='black',
                            selected_index=0,
                            destinations=[
                                ft.NavigationDestination(icon_content=ft.TextButton(text="TAESMET S.A.S", icon=ft.icons.PERSON, style=ft.ButtonStyle(color='white', bgcolor='black'))),
                            ]
                        )
                    ),
                ]
            )
        )
        self.tablaDatos = ft.DataTable(
            data_row_max_height=50,
            width=800,
            bgcolor='white',
            border=ft.border.all(1, 'black'),
            border_radius=10,
            horizontal_lines=ft.border.BorderSide(1, 'black'),
            sort_ascending=True,
            expand=True,
            columns=[
                ft.DataColumn(
                    ft.Text("Empresa"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Editar"),
                    tooltip="Editar empresa",
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Borrar"),
                    tooltip="Eliminar empresa",
                ),
                ft.DataColumn(
                    ft.Text("Ver"),
                    tooltip="Ver facturas",
                ),
            ]
        )
        self.table = ft.Container(
            border_radius=10,
            padding=10,
            col=8,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                self.searh_field,
                            ]
                        )
                    ),
                    ft.Column(
                        expand=True,
                        scroll="auto",
                        controls=[
                            ft.ResponsiveRow([
                                self.tablaDatos
                            ]),
                        ]
                    ),
                ]
            )
        )

        self.buttom = ft.Container(
            expand=False,
            padding=10,
            col=1,
            content=ft.IconButton(
                icon=ft.icons.ADD,
                bgcolor="black",
                icon_color="white",
                on_click=self.open_dialog,
            )
        )

        self.container = ft.Column(
            controls=[self.navigation_bar, self.table, self.buttom],
        )
        if len(self.lista_empresas) > 0:
            for empresa in self.lista_empresas:
                self.cargar_tabla(empresa)
        self.page = page
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

    def go_home(self, e):
        self.page = e.page
        self.page.go("/")
    nombre = ""
    def go_facturas(self, event, company_name):
        global nombre
        self.page = event.page
        self.pantalla_facturas = pf.__view__(self.page, company_name, self.direcciones[company_name]["Direccion"])
        nombre = company_name
        self.page.go("/facturas")

    def route_change(self, route):
        self.page.views.clear()
        if self.page.route == "/facturas":
            self.page.views.clear()
            self.page.views.append(
                ft.View(
                    "/facturas",
                    [
                        ft.Stack(
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.START,
                                    controls=[
                                        ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_home)
                                    ],
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(value=nombre, size=35, weight=ft.FontWeight.BOLD)
                                    ],
                                ),
                            ],
                        ),
                        self.pantalla_facturas,
                    ],
                )
            )
        else:
            self.page.views.append(ft.View(self.page.route, self.page.controls))
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    def open_dialog(self, event):
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def edit_dialog(self, event, company_name):
        empresa_info = self.direcciones.get(company_name, {})
        self.edit_company_fields[0].value = company_name
        self.edit_company_fields[1].value = empresa_info.get("NIT", "")
        self.edit_company_fields[2].value = empresa_info.get("Correo", "")
        self.edit_company_fields[3].value = empresa_info.get("Telefono", "")
        self.old_company_name = company_name
        if self.edit_dialog_a not in self.page.overlay:
            self.page.overlay.append(self.edit_dialog_a)
        self.edit_dialog_a.open = True
        self.page.update()

    def show_company_info(self, company_name, nit, correo, telefono):
        self.info_nombre.value = company_name
        self.info_nit.value = nit
        self.info_correo.value = correo
        self.info_telefono.value = telefono
        if self.info_dialog not in self.page.overlay:
            self.page.overlay.append(self.info_dialog)
        self.info_dialog.open = True
        self.page.update()

    def dialog_close(self, event):
        self.dialog.open = False
        self.dialogAlert.open = False
        self.edit_dialog_a.open = False
        self.info_dialog.open = False
        self.page.update()
        # Opcional: limpiar overlays cerrados
        for dlg in [self.dialog, self.dialogAlert, self.edit_dialog_a, self.info_dialog]:
            if dlg in self.page.overlay and not dlg.open:
                self.page.overlay.remove(dlg)

    def add_company(self, event):
        name = self.company_name_field.value.strip()
        nit = self.nit_field.value.strip()
        correo = self.email_field.value.strip()
        telefono = self.phone_field.value.strip()

        if not name or not nit or not correo or not telefono:
            return

        if name in self.lista_empresas:
            self.dialog_close(event)
            self.page.dialog = self.dialogAlert
            self.dialogAlert.open = True
            self.page.update()
            return

        self.lista_empresas.append(name)
        folder_path = 'SisFact/' + name
        folder_pagadas = folder_path + '/pagadas'
        folder_no_pagadas = folder_path + '/no_pagadas'

        os.makedirs(folder_path)
        os.makedirs(folder_pagadas)
        os.makedirs(folder_no_pagadas)

        pagadas_file = os.path.join(folder_path, 'registro.csv')
        with open(pagadas_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["nombre_factura", "fecha_limite", "facturado"])

        self.direcciones[name] = {
            "NIT": nit,
            "Correo": correo,
            "Telefono": telefono,
            "Direccion": folder_path
        }
        with open('SisFact/empresas.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, nit, correo, telefono, folder_path])

        self.cargar_tabla(name)
        self.tablaDatos.update()
        self.dialog_close(event)
        self.company_name_field.value = ""
        self.nit_field.value = ""
        self.email_field.value = ""
        self.phone_field.value = ""

    def delete_company(self, event, company_name):
        self.lista_empresas.remove(company_name)
        shutil.move('SisFact/' + company_name, 'SisFact/empresas_eliminadas/' + company_name)
        self.tablaDatos.rows.clear()
        with open('SisFact/empresas.csv', 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        data = [row for row in data if row[0] != company_name]
        with open('SisFact/empresas.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        self.direcciones.pop(company_name, None)
        for empresa in self.lista_empresas:
            self.cargar_tabla(empresa)
        self.tablaDatos.update()

    def update_company(self, event):
        name = self.edit_company_fields[0].value.strip()
        nit = self.edit_company_fields[1].value.strip()
        correo = self.edit_company_fields[2].value.strip()
        telefono = self.edit_company_fields[3].value.strip()
        old_name = self.old_company_name

        if not name or not nit or not correo or not telefono:
            return

        if name != old_name and name in self.lista_empresas:
            self.dialog_close(event)
            self.page.dialog = self.dialogAlert
            self.dialogAlert.open = True
            self.page.update()
            return

        self.lista_empresas.remove(old_name)
        self.lista_empresas.append(name)
        old_folder = self.direcciones[old_name]["Direccion"]
        new_folder = 'SisFact/' + name
        os.rename(old_folder, new_folder)
        self.direcciones.pop(old_name)
        self.direcciones[name] = {
            "NIT": nit,
            "Correo": correo,
            "Telefono": telefono,
            "Direccion": new_folder
        }

        with open('SisFact/empresas.csv', 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        for row in data:
            if row[0] == old_name:
                row[0] = name
                row[1] = nit
                row[2] = correo
                row[3] = telefono
                row[4] = new_folder
                break
        with open('SisFact/empresas.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        self.tablaDatos.rows.clear()
        for empresa in self.lista_empresas:
            self.cargar_tabla(empresa)
        self.tablaDatos.update()
        self.dialog_close(event)

    def searh_data(self, e):
        if len(e.data) == 0:
            self.tablaDatos.rows.clear()
            for empresa in self.lista_empresas:
                self.cargar_tabla(empresa)
            self.tablaDatos.update()
        else:
            self.search = e.data.lower()
            self.tablaDatos.rows.clear()
            for empresa in self.lista_empresas:
                if self.search in empresa.lower():
                    self.cargar_tabla(empresa)
            self.tablaDatos.update()

    def cargar_tabla(self, company_name):
        empresa_info = self.direcciones.get(company_name, {})
        nit = empresa_info.get("NIT", "N/A")
        correo = empresa_info.get("Correo", "N/A")
        telefono = empresa_info.get("Telefono", "N/A")
        self.tablaDatos.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.TextButton(
                            text=company_name,
                            on_click=lambda e, n=company_name, ni=nit, co=correo, te=telefono: self.show_company_info(n, ni, co, te)
                        )
                    ),
                    ft.DataCell(ft.IconButton(icon=ft.icons.EDIT, on_click=lambda event, n=company_name: self.edit_dialog(event, n))),
                    ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda event, n=company_name: self.delete_company(event, n))),
                    ft.DataCell(ft.IconButton(icon=ft.icons.VISIBILITY, on_click=lambda event, n=company_name: self.go_facturas(event, n))),
                ]
            )
        )
        try:
            self.tablaDatos.update()
        except:
            pass

    def show_company_info(self, company_name, nit, correo, telefono):
        self.info_nombre.value = company_name
        self.info_nit.value = nit
        self.info_correo.value = correo
        self.info_telefono.value = telefono
        self.page.dialog = self.info_dialog
        self.info_dialog.open = True
        self.page.update()

    def close_info_dialog(self):
        self.info_dialog.open = False
        self.page.update()

    def build(self):
        return self.container

def main(page: ft.Page):
    page.window_min_height = 800
    page.window_min_width = 1400
    page.theme_mode = ft.ThemeMode.LIGHT
    file_picker = ft.FilePicker()
    page.controls.append(file_picker)
    page.title = "Taesmet S.A.S Facturas"
    page.add(UI(page))

ft.app(main)