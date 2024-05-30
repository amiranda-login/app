import flet as ft
from control.app_asgard import Asgard

def NavBar(page,titulo):
    api = Asgard(page,ft)
    info = api.ejecutar('select id,value from parametros where id in("sucname","uname") order by id')

    def getBtn(icon,text,tgo):
        return ft.MenuItemButton(
            content=ft.Text(text),
            leading=ft.Icon(icon),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                #bgcolor={
                #"":'cyan',
                #},
                padding=0,
            ),
            on_click=tgo,
            width=page.width*0.7,
        )

    def ajustes(e):
        hide_drawer('/settings')

    def facturar(e):
        hide_drawer('/facturacion')

    def logout(e):
        api.crud("update parametros set value=? where id = ?",[(0,"iduser")])
        page.client_storage.set("user",0)
        hide_drawer('/login')

    def show_drawer(e):
        page.drawer = menu
        menu.open = True
        page.update()

    def hide_drawer(pg):
        page.drawer.open = False
        page.update()
        page.go(pg)

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
                    ]),
                
            ],
        )
        NavBar.leading = ft.IconButton(
                    icon=ft.icons.MENU_ROUNDED,
                    icon_size=20,
                    on_click=show_drawer
                )

    return NavBar