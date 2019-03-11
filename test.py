import cherrypy

config = {
    'global' : {
        'server.socket_host' : '127.0.0.1',
        'server.socket_port' : 8080
    }
}

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return """<html lang="en">
            <head>
            <title>Test Page</title>
            <meta charset="utf-8"/>
            <link href="https://fonts.googleapis.com/css?family=Montserrat:900|Open+Sans" rel="stylesheet">
            <style>
                #body{
                    background-color: #ff914d;
                }

                #pageName{
                    color: white;
                    font-weight: bold;
                    text-align: center;
                    font-size: 3em;
                    margin-top: 15%;
                    font-family: 'Montserrat', sans-serif;
                }

                #tagline{
                    color: white;
                    text-align: center;
                    font-family: 'Open Sans', sans-serif;
                }

                .center{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-left: 55px;
                    margin-right: 55px;
                }

                button{
                    background-color: white;
                    color: black;
                    border: none;
                    height: 30px;
                    margin-top: 30px;
                    width: 150px;
                    font-family: 'Open Sans', sans-serif;
                    border-radius: 10px;
                }

                .left{
                    margin-right: 30px;
                }

                .right{
                    margin-right: 30px;
                }
            </style>
            </head>
            <body id="body">
                <h2 id="pageName">H E R A</h2>
                <p id="tagline">Using deep learning to address gender inequality in healthcare.</p>
                <div class="center">
                <span class="left"><button>Choose Photo</button></span>
                <span class="right"></span><button>Upload Photo</button></span>
                </div>
            </body>
            </html>
        """

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())