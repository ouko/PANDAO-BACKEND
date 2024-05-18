from app import load_server
from fastapi import FastAPI
app = FastAPI()
load_server(app)
