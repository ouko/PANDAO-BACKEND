from fastapi import FastAPI
from .logic import health as health_handler
from .logic.auth.users import user_login_req
from .logic.blueprint import get_blueprints, add_blueprint as add_blueprint_logic, get_blueprint_detail
from .forms import *
from .logic.community import get_community
from .logic.community.community import create_community


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
    @app.get('/blueprint', summary="Get all blueprints", description="use to get all blueprint")
    def get_blueprint_route():
      return get_blueprints()

    @app.get('/blueprint/{slug}', summary="get detail about a single blueprint", description="get detail about a single blueprint")
    def get_blueprint_route(slug : str):
      return get_blueprint_detail(slug)

    @app.post('/blueprint/{slug}', summary="add a blueprint ",description="add blue print by admin")
    def add_blueprint_route(req:BluePrintModel):
        add_blueprint_logic(req)

    @app.get('/community',summary="get communities of the platform ",description="get communities of platform")
    def get_community_route():
        return get_community()

    @app.post('/community',summary="create a community on platform ",description="create community on platform")
    def post_community_route(req:CommunityCreate):
        create_community(req)









       
       
