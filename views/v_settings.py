import flet as ft 
from control.app_asgard import Asgard

def Settings(page):
    api = Asgard(page,ft)

    setvalues = api.ejecutar('select value from parametros where id in("server")')

    def actualizar(e):
        if page.client_storage.get("actualizando"):
            api.alert('Sincronizando...','grey')
            return False
        page.client_storage.set("actualizando",1)
        api.run(api.load())

    def save_params(e):
        api.bloquear(acep_btn)
        ok_save = 1
        
        if api.validar(text_server,'Servidor Requerido','red'):
            api.desbloquear(acep_btn,'primary')
            return False

        api.crud("update parametros set value=? where id = ?",[(text_server.value,"server")])

        if api.curl() == -1 : 
            ok_save = 0
            text_server.focus()

        if ok_save:
            api.alert('Ajustes Guardados Correctamente','green')

        api.desbloquear(acep_btn,'primary')

    text_server = ft.TextField(
        width=page.width*0.6,
        value=setvalues[0][0],
    )

    acep_btn = ft.FilledButton(
        text="Guardar",
        on_click=save_params,
    )

    btn_sincro = ft.FilledButton(
                text="Cargar Datos del Servidor",
                on_click=actualizar,
                content=ft.ProgressRing(),
            )

    r1 = ft.Row(
        visible=False,
        controls=[
            btn_sincro
        ]
    )

    iduser = api.ejecutar('SELECT value from parametros where id in("iduser","idsucursal") order by id')

    if iduser[0][0] != 0:
        r1.visible = True

    view=ft.Column(
        width=page.width*0.8,
        controls=[
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                 ft.Text('SERVIDOR:',
                    weight=ft.FontWeight.BOLD,
                    ),
                 text_server
                ]
            ),
            r1,
            ft.Row(
                alignment = ft.MainAxisAlignment.END,
                controls=[
                 acep_btn,
                ]
            )
        ],
    )
    return view
