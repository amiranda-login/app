import flet as ft
from control.app_asgard import Asgard

def NavBar(page,titulo):
    api = Asgard(page,ft)
    info = api.ejecutar('select id,value from parametros where id in("sucname","uname") order by id')

    def getBtn(icon,text,tgo):
        return ft.TextButton(
            text,
            icon=icon,
            icon_color="green400",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=tgo,
        )

    def ajustes(e):
        hide_drawer()
        page.go('/settings')

    def facturar(e):
        hide_drawer()
        page.go('/facturacion')

    def logout(e):
        api.crud("update parametros set value=? where id = ?",[(0,"iduser")])
        page.client_storage.set("user",0)
        hide_drawer()
        page.go('/login')

    def show_drawer(e):
        menu.open = True
        page.drawer.update()

    def hide_drawer():
        menu.open = False
        page.update()

    NavBar = ft.AppBar(
            title=ft.Text(titulo),
            leading_width=40,
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

    if page.client_storage.get("user") == 0:
        NavBar.leading = ft.IconButton(
                    icon=ft.icons.ARROW_BACK_ROUNDED,
                    icon_size=20,
                    on_click=lambda _:page.go('/login')
                )
        page.drawer = ''
    else:
        facturacion = getBtn(ft.icons.CARD_TRAVEL_OUTLINED,'facturación',facturar)

        menu = ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                ft.Row(
                    alignment = ft.MainAxisAlignment.CENTER,
                    controls=[
                     ft.Text(info[0][1],
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE,
                     ),
                    ]
                ),
                ft.Row(
                    alignment = ft.MainAxisAlignment.START,
                    controls=[
                     ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, color=ft.colors.BLACK),
                     ft.Text(info[1][1],
                        color=ft.colors.BLACK,
                     ),
                    ],
                ),
                ft.Divider(thickness=2),
                ft.Column(controls=[
                    facturacion,
                    getBtn(ft.icons.SETTINGS,'Ajustes',ajustes),
                    getBtn(ft.icons.LOGOUT_SHARP,'Cerrar Sesión',logout),
                    ])
                
            ],
        )
        page.drawer = menu
        NavBar.leading = ''

    return NavBar