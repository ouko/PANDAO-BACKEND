import uuid

from sqlalchemy.exc import IntegrityError

from app.api.forms import BluePrintModel, TermsModel, MethodArgsModel, MethodsModel
from models import dbsession as conn, BluePrint, Terms, Methods, MethodArgs
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError



def add_blueprint(blueprint_input:BluePrintModel):
    try:
        # Create a new BluePrint instance using the validated data
        new_blueprint = BluePrint(
            slug=blueprint_input.slug,
            description=blueprint_input.description,
            price=blueprint_input.price,
            package_addr=blueprint_input.package_addr
        )

        # Add terms if provided
        if blueprint_input.terms:
            for term in blueprint_input.terms:
                new_term = Terms(
                    blueprint_slug=blueprint_input.slug,
                    key=term.key,
                    description=term.description
                )
                new_blueprint.terms.append(new_term)

        # Add methods if provided
        m_args = []
        if blueprint_input.methods:

            for method in blueprint_input.methods:
                new_method_id = method.id or uuid.uuid4(),
                new_method = Methods(
                    id=new_method_id,
                    blueprint_slug=blueprint_input.slug,
                    name=method.name,
                    description=method.description,
                    is_function=method.is_function
                )

                # Add method arguments if provided
                if method.args:
                    for arg in method.args:
                        new_arg = MethodArgs(
                            id=arg.id or uuid.uuid4(),
                            method_id=new_method_id,
                            name=arg.name,
                            m_type=arg.m_type,
                            description=arg.description
                        )

                        m_args.append(new_arg)

                new_blueprint.methods.append(new_method)

        # Add the new blueprint to the conn and commit
        conn.add(new_blueprint)
        conn.commit()

    except SQLAlchemyError as e:
        # Log the error e
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")





def get_blueprints():
    try:
        blueprint = conn.query(BluePrint).all()
        if blueprint is None:
            return {}
        return blueprint
    except SQLAlchemyError as e:
        # Log the error e
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Function to get a blueprint by slug
def get_blueprint_detail(slug: str):
    try:
        # Query the blueprint by slug
        blueprint = conn.query(BluePrint).filter(BluePrint.slug == slug).first()

        if not blueprint:
            return None

        # Convert SQLAlchemy object to Pydantic model
        blueprint_output = BluePrintModel.from_orm(blueprint)

        # Manually load terms and methods to ensure nested data is included
        terms = conn.query(Terms).filter(Terms.blueprint_slug == slug).all()
        methods = conn.query(Methods).filter(Methods.blueprint_slug == slug).all()

        terms_models = [TermsModel.from_orm(term) for term in terms]
        methods_models = []

        for method in methods:
            args = conn.query(MethodArgs).filter(MethodArgs.method_id == method.id).all()
            args_models = [MethodArgsModel.from_orm(arg) for arg in args]
            method_model = MethodsModel.from_orm(method)
            method_model.args = args_models
            methods_models.append(method_model)

        blueprint_output.terms = terms_models
        blueprint_output.methods = methods_models

        return blueprint_output
    except SQLAlchemyError as e:
        # Log the error e
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
