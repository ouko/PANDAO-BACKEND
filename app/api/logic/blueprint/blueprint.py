from sqlalchemy.exc import IntegrityError
from models import dbsession as conn, BluePrint
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError



def get_blueprint():
    try:
        blueprint = conn.query(BluePrint).all()
        if blueprint is None:
            return {}
        return blueprint
    except SQLAlchemyError as e:
        # Log the error e
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


