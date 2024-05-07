import flet as ft
from control.app_asgard import Asgard

def Login(page):
    api = Asgard(page,ft) 

    def login(e):
        
        api.bloquear(btn_login)

        if api.validar(text_user,"Usuario Requerido","red") :
            api.desbloquear(btn_login,'primary')
            return False

        if api.validar(text_psw,"Contraseña Requerida","red") :
            api.desbloquear(btn_login,'primary')
            return False

        rs = api.curl({'cmd':3,'usr':text_user.value,'psw':text_psw.value})
        
        api.desbloquear(btn_login,'primary')

        if rs == -1:
            return False

        if rs['success'] == 0:
            api.alert(rs['msj'],'red')
        else:
            rs = api.getRs(rs['rs'],0)
            datos = [
                (rs['veid'],"idsucursal"),
                (rs['vid'],"iduser"),
                (rs['venom'],"sucname"),
                (rs['vcorreo'],"umail"),
                (rs['vnom'],"uname"),
                (rs['vusr'],"unick"),
                (rs['vterminal'],"terminal"),
                (rs['vmemory'],"memory"),
                (rs['vtu'],"tipousuario"),
                (rs['vtipoapp'],"tiposucursal"),
                (rs['vsimplificado'],"simplificado")
            ]
            api.crud('update parametros set value=? where id = ?',datos)
            page.client_storage.set("user",rs['vid'])
            page.client_storage.set("idsucursal",rs['veid'])

            exists = api.ejecutar('select count(*) from consecutivos where idsucursal = '+rs['veid'])[0][0]

            if exists == 0:
                api.crud("INSERT INTO consecutivos VALUES(?,?,?,?,?,?,?)",[(rs['veid'],0,0,0,0,0,0)])
            #carga async de datos
            api.run(api.load())

            page.go('/'+api.loadMain())

    def recover(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def send_mail():
        print(1)

    text_user = ft.TextField(
        label="Usuario",
        width=page.width*0.95,
        icon=ft.icons.ACCOUNT_CIRCLE,
        autofocus=True,
        on_submit=login,
    )

    text_psw = ft.TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True,
        width=page.width*0.95,
        icon=ft.icons.KEY,
        on_submit=login,
    )

    btn_login = ft.FilledButton(
        width=page.width*0.85,
        text="Ingresar",
        on_click = login
     )

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Recuperar Contraseña"),
        content=ft.Text("Enviar código de recuperación al correo "),
        actions=[
            ft.TextButton("Enviar", on_click=send_mail),
        ],
    )

    view=ft.Column(
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
                ft.Image(
                    src=f"assets/icon/login.png",
                    width=page.width*0.85,
                    height=page.height*0.35,
                    #fit=ft.ImageFit.CONTAIN,
                )
            ]),
            text_user,
            text_psw,
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                 btn_login,
                ]
            ),
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                 ft.FilledButton(
                    width=page.width*0.85,
                    text="Registrarse",
                 ),
                ]
            ),
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                 ft.Text('Recuperar Contraseña',
                    style=ft.TextStyle(
                        decoration=ft.TextDecoration.UNDERLINE,
                        decoration_style=ft.TextDecorationStyle.DASHED),
                        spans=[ft.TextSpan(
                                on_click = recover,
                            )
                        ]),
                 ft.IconButton(
                    icon=ft.icons.SETTINGS,
                    icon_color="grey",
                    icon_size=20,
                    tooltip="Ajustes",
                    on_click=lambda _:page.go('/settings'),
                    ),
                ]
            ),
            
        ],
    )

    return view
