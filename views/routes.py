from control.app_bar import NavBar

from views.v_login import Login
from views.v_main import Main
from views.v_settings import Settings
from views.v_facturacion import Facturacion
from views.v_ruta import Ruta
  
class Router():
  def __init__(self):
        self.routes = {}
        self.page = ''

  def route_change(self,route):
    _page = route.route.split("?")[0].replace('.','') 

    if _page != '/login':
      titulo = self.routes[_page]['title']
      self.page.appbar = NavBar(self.page,titulo)
    else:
      self.page.appbar = ''
    
    self.contenedor.gradient = None
    self.contenedor.content = self.routes[_page]['fn'](self.page)
    self.contenedor.update()

router = Router()

router.routes = {
  "/": {
    "fn": Main,
  },
  "/login":{
    "fn": Login,
  },
  "/settings": {
    "fn":Settings,
    "title":'Ajustes',
  },
  "/facturacion":{
    "fn":Facturacion,
    "title":'Facturación',
  },
  "/rutas":{
    "fn":Ruta,
    "title":'Ruta',
  }
}