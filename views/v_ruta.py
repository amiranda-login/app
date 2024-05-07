import flet as ft
from control.app_asgard import Asgard

def Ruta(page):
	view = ft.Column([
			ft.ResponsiveRow(vertical_alignment=ft.CrossAxisAlignment.CENTER,controls=[
			    ft.Column(col=2, controls=[
			    	ft.IconButton(
						icon=ft.icons.ARROW_DROP_DOWN,
						style=ft.ButtonStyle(
			                shape=ft.RoundedRectangleBorder(radius=0),
			                bgcolor=ft.colors.GREEN
			            ),
					)]),
			    ft.Column(col=8, controls=[ft.Text('NOMBRE CLIENTE')]),
			    ft.Column(col=2, controls=[
			    	ft.IconButton(
						icon=ft.icons.ARROW_DROP_UP,
						style=ft.ButtonStyle(
			                shape=ft.RoundedRectangleBorder(radius=0),
			                bgcolor=ft.colors.RED
			            ),
					)]),
			]),
		])

	return view