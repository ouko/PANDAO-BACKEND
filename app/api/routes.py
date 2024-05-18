from fastapi import FastAPI
from .logic import health as health_handler
from .logic.auth.users import user_login_req
from .logic.blueprint import get_blueprint
from .forms import * 


def load_server(app):

    # defines routes

    @app.get('/')
    def health_check():
      return health_handler()

    @app.get('/health-check')
    def health_check():
      return health_handler()
    
    # api for user to register
    @app.post('/login')
    def register(req:UserLogin):
       return user_login_req(req)

    # define routes for blueprints
    @app.post('/blueprint', summary="Get all blueprints", description="use to get all blueprint")
    def get_blueprint_route():
      return get_blueprint()

       
       
       
