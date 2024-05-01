import flet as ft
from control.app_asgard import Asgard

def Main(page):
    api = Asgard(page,ft)
    info = api.ejecutar('select id,value from parametros where id in("sucname","uname") order by id')

    def logout(e):
        api.crud("update parametros set value=? where id = ?",[(0,"iduser")])
        page.client_storage.set("user",0)
        page.go('../')

    def getBtn(icon,text,tgo):
        return ft.ElevatedButton(
            bgcolor = ft.colors.WHITE,
            width = page.width*0.40,
            height = page.height*0.25,
            content=ft.Column(
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(icon,size=90),
                        ft.Text(text)
                    ]
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
            ),
            on_click=tgo,
        )

    page.controls[0].gradient = ft.LinearGradient(
        begin=ft.alignment.top_center,
        end=ft.alignment.bottom_center,
       colors=[ft.colors.BLUE, ft.colors.GREY],
    )

    btn_facturacion = getBtn(ft.icons.CARD_TRAVEL_OUTLINED,'Facturación',lambda _:page.go('/facturacion'))

    view = ft.Column([
        ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            controls=[
             ft.Text(info[0][1],
                weight=ft.FontWeight.BOLD,
                color='#e2e2e2',
             ),
            ]
        ),
        ft.Row(
            alignment = ft.MainAxisAlignment.START,
            controls=[
             ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, color=ft.colors.WHITE),
             ft.Text(info[1][1],
                color=ft.colors.WHITE,
             ),
            ],
        ),
        ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            controls = [
                btn_facturacion,
                getBtn(ft.icons.LOGOUT_SHARP,'Cerrar Sesión',logout),
            ]
        ),
        ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            controls = [
                getBtn(ft.icons.SETTINGS,'Ajustes',lambda _:page.go('/settings')),
            ]
        )
    ])

    return view