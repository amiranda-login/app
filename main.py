import flet as ft
from views.routes import router
from control.app_asgard import Asgard

def main(page: ft.Page):
    db = Asgard(page,ft)

    def check():
        iduser = db.ejecutar('SELECT value from parametros where id in("iduser","idsucursal") order by id')
        inicial = 'login'

        if iduser == False:
            db.inicializar()
            page.client_storage.set("user", 0)
            page.client_storage.set("actualizando",1)
        else:
            page.client_storage.set("sucursal", iduser[0][0])
            page.client_storage.set("user", iduser[1][0])
            page.client_storage.set("actualizando",0)

            if page.client_storage.get("user") == 0:
                inicial = 'login'
            else:
                inicial = db.loadMain()

        return inicial

    page.title = "APSY APP"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    #page.splash = ft.ProgressBar()

    contenedor = ft.Container(height=page.height);

    page.add(contenedor)

    page.on_route_change = router.route_change
    router.page = page
    router.contenedor = contenedor
    init = check()
    page.go('/'+init)

ft.app(target=main, assets_dir="assets")