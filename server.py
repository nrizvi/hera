#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import cherrypy

config = {
    'global' : {
        'server.socket_host' : '127.0.0.1',
        'server.socket_port' : 8080
    }
}


class App:

    @cherrypy.expose
    def upload(self, ufile):
        # Either save the file to the directory where server.py is
        # or save the file to a given path:
        # upload_path = '/path/to/project/data/'
        upload_path = os.path.dirname(__file__)

        # Save the file to a predefined filename
        # or use the filename sent by the client:
        # upload_filename = ufile.filename
        upload_filename = 'image.jpg'

        upload_file = os.path.normpath(
            os.path.join(upload_path, upload_filename))
        size = 0
        with open(upload_file, 'wb') as out:
            while True:
                data = ufile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)
        out = '''
<html lang="en">
<head>
  <title>Test Page</title>
  <meta charset="utf-8"/>
  <link href="https://fonts.googleapis.com/css?family=Montserrat:900|Open+Sans" rel="stylesheet">
</head>
  <body id="body" style="background-color:#ff914d;">
    <div class="center" style="margin-top:20%;">
        <span style="text-align:center;"><h2 style="color:white;font-family: 'Open Sans', sans-serif;">You have an 80 percent chance of having arterial heart disease.</h2></span>
    </div>
  </body>
</html>
''' .format(ufile.filename, size, ufile.content_type, data)
        return out


if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config)