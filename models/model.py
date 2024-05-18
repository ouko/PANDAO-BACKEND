from sqlalchemy import create_engine, Column, Integer, String, ForeignKey , DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    name = Column(String)
    public_address = Column(String, primary_key=True)
    last_login = Column(DateTime)
    email = Column(String)


class BluePrint(Base):
    __tablename__='blueprints'
    slug = Column(String(100),primary_key=True)
    description = Column(String)
    terms = Column(String, primary_key=True)
    # avaliable_methods =   Column(UUID(as_uuid=True))
    price = Column(Integer)
    methods = relationship("Methods", backref="blueprint")

    
class Methods(Base):
    __tablename__ = 'method'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blueprint_slug = Column(String(100),ForeignKey('blueprints.slug'))
    name = Column(String(100))
    description = Column(String(100))
    args = relationship("MethodArgs", backref="method")

class MethodArgs(Base):
    __tablename__ = 'method_args'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    method_id = Column(UUID(as_uuid=True),ForeignKey('method.id'))
    name = Column(String(100))
    m_type = Column(String(100))
    description = Column(String(100))


    

engine = create_engine('postgresql://pandao_database_user:lhLX8ipBc7O7QKUu8z5HL31iHTJgavO8@dpg-cp12prvjbltc73e6l0tg-a.oregon-postgres.render.com/pandao_database')
Base.metadata.create_all(engine)
# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
dbsession = Session()

