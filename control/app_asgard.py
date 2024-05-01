import sqlite3 as db
import requests
import json
import asyncio

class Asgard():
    """docstring for ASGARD"""
    def __init__(self,page,ft):
        self.db_name = 'apsy.db'
        self.page = page
        self.ft = ft
    
    def ejecutar(self,sql):
        con = db.connect(self.db_name)
        cur = con.cursor()

        try:
            res = cur.execute(sql)
            salida = res.fetchall();
        except db.Error as err:
            print(err)
            salida = False
        con.close()

        return salida

    def crud(self,sql,data):
        con = db.connect(self.db_name)
        cur = con.cursor()
        try:
            res = cur.executemany(sql,data)
            con.commit()
            salida = res.fetchall()
        except db.Error as err:
            print(err)
            salida = False

        con.close()
        
        return salida;

    def inicializar(self):
        print("INICIALIZANDO BASE DE DATOS...")
        self.ejecutar("CREATE TABLE IF NOT EXISTS parametros(id,value)")
    
        params = [
            ("iduser",0),
            ("idsucursal",0),
            ("server","https://fe.logintechcr.com"),
            ("uname",""),
            ("unick",""),
            ("umail",""),
            ("sucname",""),
            ("terminal",""),
            ("memory",""),
            ("tipousuario",""),
            ("tiposucursal","")
        ]
        self.crud("INSERT INTO parametros VALUES(?,?)",params)

        self.ejecutar("CREATE TABLE IF NOT EXISTS consecutivos(idsucursal,consecutivo,consecutivo6,consecutivo7,ec3,ec7,devoluciones)")

        self.ejecutar("CREATE TABLE IF NOT EXISTS clientes(id integer primary key autoincrement,nombre varchar(150),cedula varchar(20),plazo int,credito decimal(20,2),idServer int,idsucursal int)")
        self.ejecutar("CREATE table if not exists correos(id integer primary key autoincrement,correo varchar(64),idtabla int, idfila int)")

        self.ejecutar("CREATE TABLE IF NOT EXISTS productos(id integer primary key autoincrement,nombre varchar(150),codigo varchar(64),iva decimal(3,1),cabys varchar(20),venta decimal(23,5),costo decimal(23,5),timv int,ivi bool,idserver int,idsucursal int)")
        self.ejecutar("CREATE TABLE IF NOT EXISTS inventario(id integer primary key autoincrement, idproducto int,cantidad decimal(12,2),idinventario int)")
        self.ejecutar("CREATE TABLE IF NOT EXISTS last_price(id integer primary key autoincrement,idproducto int,precio decimal(23,5),idcliente int, fecha varchar(20))")

        self.ejecutar("CREATE TABLE IF NOT EXISTS servicios(id integer primary key autoincrement,nombre varchar(150),codigo varchar(64),iva decimal(3,1),cabys varchar(20),venta decimal(23,5),ivi bool,timv int,idserver int,idsucursal int)")

        self.ejecutar("CREATE TABLE IF NOT EXISTS facturas(id integer primary key autoincrement,fecha varchar(20),idcliente int,idtipo int,idtipoventa int,idtipopago int,gravado decimal(23,5),excento decimal(23,5),exonerado decimal(23,5),iva decimal(23,5),descuento decimal(23,5),oc varchar(64),idmoneda int,divisa decimal(5,2),feestado int, idserver int,idsucursal int,idusuario int)")
        self.ejecutar("CREATE TABLE IF NOT EXISTS cuentas(id integer primary key autoincrement,idtipo int,idfactura int, valor decimal(23,5), saldo decimal(23,5),idserver int,idsucursal int,idusuario int)")

        self.ejecutar("CREATE table if not exists rutas(id integer primary key autoincrement,idcarga int,fcarga varchar(20),iddescarga,fdescarga varchar(20))")
        self.ejecutar("CREATE table if not exists ruta_clientes(idruta int,idcliente int,inicio varchar(10),fin varchar(10))")

    def curl(self,args={},tipo=1):
        #http: direccion del api
        #aegs: arguementos a pasar al API formato {arg1=val1,...,argn=valn}
        #tipo: 1 post, 2 get

        server = self.ejecutar('select value from parametros where id = "server"')[0][0]

        http = server+'/api'
        #headers = {'Content-Type': 'application/json','charset':'utf-8'}
        try:
            if tipo == 1:
                result = requests.post(http,json =  args,timeout = 3)
            else:
                result = requests.get(http,json = args,timeout = 3)
        except requests.exceptions.RequestException as e:
            print(e)
            self.alert("Error Conectando al Servidor: "+server,'red')

            return -1

        rs = json.loads(result.content)
        return rs

    def validar(self,vinput,msj,color):
        if vinput.value == '' :
            self.alert(msj,color)
            vinput.focus()
            return True
        else:
            return False

    def alert(self,msj,color):
        self.page.snack_bar = self.ft.SnackBar(
            self.ft.Text(msj),
            bgcolor=color,elevation=9999)
        self.page.snack_bar.open = True
        self.page.update()

    def bloquear(self,elem):
        elem.disabled = True
        elem.bgcolor = 'grey'
        self.page.update()

    def desbloquear(self,elem,color):
        elem.disabled = False
        elem.bgcolor = color
        self.page.update()

    def jsonParse(self,text):
        return json.loads(text)

    def getRs(self,rs,multiple):
        if(multiple):
            rs = json.loads(rs)
        else:
            rs = json.loads(rs)[0]
        return rs

    def salidModal(self,modal):
        modal.open = False
        self.page.update()

    async def loadProductos(self):
        terminal = self.ejecutar('select value,case id when "iduser" then 1 when "idsucursal" then 2 else 3 end as orden from parametros where id in("iduser","idsucursal","terminal") union select ifnull(max(id),0),100 from productos where idsucursal = '+self.page.client_storage.get('idsucursal')+' order by orden;')
        lista = self.curl({'cmd':6,'tipo':1,'terminal':terminal[2][0],'iduser':terminal[0][0],'idsucursal':terminal[1][0],'lastid':terminal[3][0]},0)

        if lista['success'] == 0:
            self.alert(rs['msj'],'red')
        else:

            rs = self.getRs(lista['rs'],1)
            if len(rs):
                lista_prod = []
                for product in rs:
                    lista_prod.append( (
                        product['nombre'],
                        product['codigo'],
                        product['iva'],
                        product['cabys'],
                        product['venta'],
                        product['costo'],
                        product['timv'],
                        product['ivi'],
                        product['id'],
                        self.page.client_storage.get('idsucursal'),
                        ) )
                if len(lista_prod):
                    self.crud("INSERT INTO productos(nombre,codigo,iva,cabys,venta,costo,timv,ivi,idserver,idsucursal) VALUES(?,?,?,?,?,?,?,?,?,?)",lista_prod)
            
            add_inv = []
            act_inv = []
            if 'inventarios' in lista:
                rs = self.getRs(lista['inventarios'],1)
     
                for stock in rs:
                    stock['idproducto'] = self.ejecutar('select id from productos where idserver = '+stock['idproducto']+';')[0][0]

                    if stock['accion'] == '1':
                        add_inv.append((
                            stock['idproducto'],
                            stock['cantidad'],
                            stock['idinventario'],
                            ))
                    else:
                        act_inv.append((
                            stock['cantidad'],
                            stock['idproducto'],
                            stock['idinventario'],
                            ))

            if 'inventario' in lista:
                rs = self.getRs(lista['inventario'],1)
                
                for stock in rs:
                    stock['idproducto'] = self.ejecutar('select id from productos where idserver = '+stock['idproducto']+';')[0][0]

                    if stock['accion'] == '1':
                        add_inv.append((
                            stock['idproducto'],
                            stock['cantidad'],
                            stock['idinventario'],
                            ))
                    else:
                        act_inv.append((
                            stock['cantidad'],
                            stock['idproducto'],
                            stock['idinventario'],
                            ))

            if len(add_inv):
                self.crud("INSERT INTO inventario(idproducto,cantidad,idinventario) VALUES(?,?,?)",add_inv)
            if len(act_inv):
                self.crud("UPDATE inventario set cantidad=? where idproducto = ? and idinventario=?",act_inv)

        self.alert('Carga de Productos Completa','green')

    async def loadClientes(self):
        terminal = self.ejecutar('select value,case id when "iduser" then 1 when "idsucursal" then 2 else 3 end as orden from parametros where id in("iduser","idsucursal","terminal") union select ifnull(max(id),0),100 from clientes where idsucursal = '+self.page.client_storage.get('idsucursal')+' order by orden;')

        lista = self.curl({'cmd':6,'tipo':2,'terminal':0,'iduser':0,'idsucursal':terminal[1][0],'lastid':terminal[3][0]},0)

        if lista['success'] == 0:
            self.alert(rs['msj'],'red')
        else:
            rs = self.getRs(lista['rs'],1)
            lista_clie = []
            for cliente in rs:
                lista_clie.append( (
                    cliente['nombre'],
                    cliente['cedula'],
                    cliente['plazo'],
                    cliente['credito'],
                    cliente['idServer'],
                    self.page.client_storage.get('idsucursal'),
                    ) )
            if len(lista_clie):
                self.crud("INSERT INTO clientes(nombre,cedula,plazo,credito,idServer,idsucursal) VALUES(?,?,?,?,?,?)",lista_clie)

            rs = self.getRs(lista['correos'],1)
            lista_corr = []
            for correo in rs:
                correo['idfila'] = self.ejecutar('select id from clientes where idserver = '+stock['idfila']+';')[0][0]

                if correo['accion'] == '1':
                    add_crr.append((
                        correo['correo'],
                        2,
                        correo['idfila'],
                        ))
                else:
                    act_crr.append((
                        correo['correo'],
                        correo['idfila'],
                        ))
                if len(add_crr):
                    self.crud("INSERT INTO correos(correo,idtabla,idfila) VALUES(?,?,?)",add_crr)
                if len(act_crr):
                    self.crud("UPDATE correos set correo=? where idfila = ? and idtabla=2",act_crr)

        self.alert('Carga de Clientes Completa','green')

    async def loadRutas(self):
        terminal = self.ejecutar('select value,case id when "iduser" then 1 when "idsucursal" then 2 else 3 end as orden from parametros where id in("iduser","idsucursal","terminal") order by orden;')

        lista = self.curl({'cmd':6,'tipo':5,'terminal':terminal[2][0],'iduser':terminal[0][0],'idsucursal':terminal[1][0],'lastid':0},0)

        if lista['success'] == 0:
            self.alert(rs['msj'],'red')
        else:
            rs = self.getRs(lista['rs'],1)

    async def load(self):
        await self.loadProductos()
        await self.loadClientes()
        tipo_sucursal = self.ejecutar('select value from parametros where id = "tiposucursal"')[0][0][0]
        if(tipo_sucursal == 1):
            await self.loadRutas()

        self.alert('Actualización Completa','green')

    def run(self,fn):
        asyncio.run(fn)