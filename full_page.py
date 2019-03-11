# Create a basic page to display content with cherrypy
 
import os.path
import cherrypy
from cherrypy.lib.static import serve_file
 
current_dir = os.path.dirname(os.path.abspath(__file__))
 
config = {'/' : {
 'tools.staticdir.on' : True,
 'tools.staticdir.dir' : current_dir+'/html/',
 'tools.staticdir.index' : 'index.html',
 }
}
cherrypy.config.update({'server.socket_port': 9090})
 
class Root:
 """ Base class to handle incoming requests. """
 def index(self,name):
   return serve_file(os.path.join(current_dir, name))
 index.exposed = True
 
cherrypy.quickstart(Root(), '/',config=config)