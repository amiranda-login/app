import flet as ft


def NavBar(page,titulo):

    NavBar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK_ROUNDED,
                on_click=lambda _:page.go('/')),
            title=ft.Text(titulo),
            leading_width=40,
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

    return NavBar