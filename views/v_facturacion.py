import flet as ft
from control.app_asgard import Asgard

def Facturacion(page):
	api = Asgard(page,ft)
	totalizar = [];

	def creditoOn(e):
		if int(e.control.value) == 2:
			plazo.visible=True
			plazo.focus()
		else:
			plazo.visible=False
		page.update()

	def addLine(e):
		page.dialog = modal_addline
		modal_addline.open = True
		page.update()
		add_codigo.focus()

	def agregarLinea(e):
		lineas = len(totalizar)

		if lineas == 0:
			lista_productos.controls = []

		totalizar.append(lineas)
		totalizar[lineas] = []	
		totalizar[lineas].append({'punitario':add_precio.value,'cantidad':add_cantidad.value})

		lineas += 1;

		total = float(add_cantidad.value)*float(add_precio.value)

		newline = ft.Row([
		 		ft.Container(
		 			width=page.width*0.5,
		 			content=ft.Text(add_descp.value,weight=ft.FontWeight.BOLD)
		 			),
		 		ft.Container(
		 			padding = ft.padding.only(right=20),
		 			width=page.width*0.5,
		 			content=ft.Row(alignment=ft.MainAxisAlignment.END,controls=[
		 					ft.IconButton(
								icon=ft.icons.EDIT_ROUNDED,
								icon_color="blue400",
								icon_size=20,
								tooltip="Editar Línea",
							),

							ft.IconButton(
								icon=ft.icons.DELETE_ROUNDED,
								icon_color="red400",
								icon_size=20,
								tooltip="Eliminar Línea",
							),
		 					])
		 			),
		 		])
		lista_productos.controls.append(newline)

		newline = ft.Row([
		 		ft.Container(
		 			width=page.width*0.3,
		 			content=ft.TextField(label='Precio Unitario',value=add_precio.value,read_only=True,border=ft.InputBorder.UNDERLINE)
		 			),
		 		ft.Container(
		 			width=page.width*0.3,
		 			content=ft.TextField(label='Cantidad',value=add_cantidad.value)
		 			),
		 		ft.Container(
		 			width=page.width*0.3,
		 			content=ft.TextField(label='Total',value=total,read_only=True,border=ft.InputBorder.UNDERLINE)
		 			),
		 	])

		lista_productos.controls.append(newline)

		totLineas.value = lineas
		totFactura.value = '{:,.2f}'.format(float(totFactura.value.replace(',',''))+total)

		api.salidModal(modal_addline)

	def mostarCorreos(e):
		correos = api.ejecutar('select * from correos where idfila = '+page.client_storage.get("fact_user")+' and idtabla = 2')
		print(correos)

	def delCorreo(e):
		correos.controls.remove(e.control)
		correos.update()

	def cargarCorreo(e):
		if not text_correo.value == '':
			correos.controls.append(
				ft.Chip(
			        label=ft.Text(text_correo.value),
			        bgcolor=ft.colors.GREEN_200,
			        on_delete=delCorreo
			    )
			)
			correos.update()

			text_correo.value = ''
			text_correo.focus()
		

	def shcred(e):
		col_cred.visible = e.control.value
		_plazo.value = 0
		_lim_cred = 0
		page.update()

	def cargarCliente(e):
		text_cliente.value = e.control.leading.value
		page.client_storage.set("fact_user",e.control.leading.data['idcliente'])
		lista_clientes.controls = [];
		getFactTitulo(1,1)
		autocomplete.height = 100
		autocomplete.update()

	def mostrarLista(e):
		value = str(e.control.value)
		page.client_storage.set("fact_user",0)
		getFactTitulo(7,1)
		resultado = []
		lista_clientes.controls = [];

		if not value == '':
			rs = api.ejecutar("select id,nombre,cedula from clientes where nombre||cedula like '%"+value+"%' limit 10")
			for cliente in rs:
				lista_clientes.controls.append(
					ft.ListTile(leading=ft.Text(f'{cliente[1]}, {cliente[2]}',size=12,expand=1,data={'idcliente':cliente[0]}),content_padding=ft.padding.all(0),on_click=cargarCliente),
				)

			rs = len(rs)
		else:
			rs = 0;

		autocomplete.height = 100+(rs*30)
		autocomplete.update()

	def getSic(e):
		api.bloquear(btn_search)

		rs = api.curl({'cmd':5,'ced':text_cedula.value.replace('-','')})
		rs = api.getRs(rs['rs'])

		if rs['succed'] == 0:
			api.alert(rs['error'],'red')
			text_cedula.focus()
		else:
			span_nombre.value = rs['nom']
			page.client_storage.set('new_client',{'tipo':rs['tip']})
			page.update()

		api.desbloquear(btn_search,'white')
		text_correo.focus()
	
	def guardarCliente(e):
		if len(correos.controls) == 1:
			api.alert('Correo Requerido','red')
			text_correo.focus()
			return False

		exists = api.ejecutar("SELECT id from clientes where cedula = '"+str(text_cedula.value)+"'")

		if len(exists):
			api.alert('Cédula Existente','red')
			text_cedula.focus()
			return False

		api.crud('INSERT into clientes values(?,?,?,?,?,?)',[(None,span_nombre.value,str(text_cedula.value),_plazo.value,float(_lim_cred.value),0)])

		new = api.ejecutar('select id from clientes where cedula = "'+str(text_cedula.value)+'"')

		api.crud('INSERT into correos values(?,?,?,?)',[(None,str(correo.value),2,new[0][0])])

		api.alert('Cliente Guardado Correctamente','green')
		modal_cliente.open = False
		page.update()

	def agregarCliente(e):
		_credito.value = False
		col_cred.visible = False
		correos.controls = []
		correos.controls.append(text_correo)
		page.dialog = modal_cliente
		modal_cliente.open = True
		page.update()
		text_cedula.focus()

	def salidModal(e):
		modal_cliente.open = False
		page.update()

	def getFactTitulo(param,upt):
		page.client_storage.set('param',param)

		if param == 1:
			tipoFactura.value = 'Factura N°'
			param = ''
		elif param == 7:
			tipoFactura.value = 'Tiquete N°'
			param = 6;
		
		consecutivo.value = str(api.ejecutar('Select consecutivo'+str(param)+'+1 from consecutivos where idsucursal = '+str(page.client_storage.get('sucursal')))[0][0]).zfill(10)

		if upt:
			tipoFactura.update()
			consecutivo.update()


	text_cliente = ft.TextField(
		label="Nombre o Cédula del Cliente",
		width=page.width*0.7,
		autofocus=True,
		on_change=mostrarLista
	)

	lista_clientes = ft.ListView(expand=1, spacing=0,horizontal=False,item_extent=30, padding=0,divider_thickness=5,controls=[])

	autocomplete = ft.Container(
		width=page.width*0.7,
		height=95,
		padding=ft.padding.only(top=15,right=9,bottom=15,left=3),
		clip_behavior=ft.ClipBehavior.HARD_EDGE,
		animate=ft.animation.Animation(400,'decelerate'),
		content=ft.Column(
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			alignment=ft.MainAxisAlignment.START,
			spacing=0,
			controls=[
				ft.Row(
					alignment = ft.MainAxisAlignment.CENTER,
					vertical_alignment = ft.CrossAxisAlignment.CENTER,
					controls=[
						text_cliente
					]
				),
				lista_clientes,
			]
		)
	)

	t_rgroup = ft.RadioGroup(content=ft.Row([
		ft.Radio(value=1,label='Contado'),
		ft.Radio(value=2,label='Crédito')
		]),on_change=creditoOn
	)

	plazo = ft.TextField(label="Plazo",value=0,border=ft.InputBorder.UNDERLINE,visible=False)

	tipo_factura = ft.Row(
					alignment=ft.MainAxisAlignment.CENTER,
					controls=[
						t_rgroup,
						plazo
					]
				)

	totLineas = ft.Text(len(totalizar));
	totFactura = ft.Text('0.00')

	lista_productos = ft.Column(scroll=ft.ScrollMode.AUTO,controls=[
		ft.Row(alignment=ft.MainAxisAlignment.CENTER,
			controls=[
				ft.Text('No Hay Líneas Ingresadas')
			])
	])

	text_cedula = ft.TextField(label='Ingrese el Número de Cédula',on_submit=getSic,width=page.width*0.8)
	text_correo = ft.TextField(label='Correo',border=ft.InputBorder.UNDERLINE,on_submit=cargarCorreo)
	span_nombre = ft.Text('----',)
	_credito = ft.Switch(label="Crédito", value=False,on_change=shcred)
	_plazo = ft.TextField(label='Plazo en Días',border=ft.InputBorder.UNDERLINE,value=0)
	_lim_cred = ft.TextField(label='Max. Crédito',border=ft.InputBorder.UNDERLINE,value=0)
	col_cred = ft.Row([
			_plazo,
			_lim_cred,
		])

	tipoFactura = ft.Text(' N°')
	consecutivo = ft.Text('0'.zfill(10),color=ft.colors.RED)

	btn_search = ft.IconButton(
					ft.icons.SEARCH_ROUNDED,
					on_click=getSic
				)

	correos = ft.Row(
		controls=[
			text_correo,
		]
	)

	modal_cliente = ft.AlertDialog(
		bgcolor = ft.colors.WHITE,
		modal=True,
		title=ft.Text('Ingresar Cliente',weight=ft.FontWeight.BOLD),
		content=ft.Column(width=page.width,controls=[
			ft.Row(
				alignment=ft.MainAxisAlignment.CENTER,
				controls=[
					text_cedula,
					btn_search,
				]
			),
			ft.Row(
				controls=[
					ft.Text('Razón Social:'),
					span_nombre,
				]
			),
			correos,
			ft.Row(
				[
					_credito,
				]
			),
			col_cred,
		 ]),
		actions=[
			ft.TextButton("Aceptar", on_click=guardarCliente),
			ft.TextButton("Salir", on_click=salidModal),
		],
		actions_alignment=ft.MainAxisAlignment.END,
	)
	add_codigo=ft.TextField(label='Código',border=ft.InputBorder.UNDERLINE,value="05")	
	add_descp=ft.TextField(label='Descripcion',border=ft.InputBorder.UNDERLINE,value="PRUEBA")
	add_precio=ft.TextField(label='Precio',border=ft.InputBorder.UNDERLINE,value=1000)
	add_unidad=ft.Dropdown(
		label='Unidad',
		width=100,
		value=1,
		options=[
			ft.dropdown.Option(text="Kilos",key=1),
			ft.dropdown.Option(text="Gramos",key=2)
		],
	)
	add_cantidad=ft.TextField(label='Cantidad',border=ft.InputBorder.UNDERLINE,value=1)

	modal_addline = ft.AlertDialog(
		bgcolor = ft.colors.WHITE,
		modal=True,
		title=ft.Text('Ingresar Linea',weight=ft.FontWeight.BOLD),
		content=ft.Column(scroll=ft.ScrollMode.AUTO,width=page.width,controls=[
				add_codigo,
				add_descp,
				add_precio,
				add_unidad,
				add_cantidad
		]),
		actions=[
				ft.TextButton("Agregar", on_click=agregarLinea),
				ft.TextButton("Salir", on_click=lambda _:api.salidModal(modal_addline)),
		],
		actions_alignment=ft.MainAxisAlignment.CENTER,
	)

	getFactTitulo(7,0)
	t_rgroup.value = 1
	page.client_storage.set("fact_user",0)

	view = ft.Column(scroll=ft.ScrollMode.AUTO,controls=[
		ft.Row(
			controls=[
				tipoFactura,
				consecutivo,
				ft.IconButton(
					icon=ft.icons.SETTINGS,
					icon_color="grey",
					icon_size=20,
					tooltip="Ajustes Facturación",
				),
			]
		),
		ft.Row(
			alignment=ft.MainAxisAlignment.CENTER,
			spacing=0,
			controls=[
			autocomplete,
			ft.IconButton(
				ft.icons.ADD_SHARP,
				on_click=agregarCliente
			),
			ft.IconButton(
				ft.icons.MAIL_SHARP,
				visible=True,
				on_click=mostarCorreos
			)
		]),
		tipo_factura,	
		ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
			ft.FilledButton("Agregar Línea", icon="add",style=ft.ButtonStyle(bgcolor='orange'),on_click=addLine),
			ft.FilledButton(text='Procesar Factura',icon=ft.icons.SEND_ROUNDED)
			]),
		ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
			ft.Text('Cantidad de Lineas: '),
			totLineas,
			ft.Text('Total Factura: ',weight=ft.FontWeight.BOLD),
			totFactura,
			]),
		lista_productos,
		
	])

	return view;