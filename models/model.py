from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, PrimaryKeyConstraint
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
    communities = relationship("Community", backref="owner")

class BluePrint(Base):
    __tablename__ = 'blueprints'
    slug = Column(String(100), primary_key=True)
    description = Column(String)
    terms = relationship("Terms", backref="blueprint")
    price = Column(Integer)
    methods = relationship("Methods", backref="blueprint")
    package_addr = Column(String, nullable=False)
    deploy_manifests = relationship("DeployManifest", backref="blueprint")

class Terms(Base):
    __tablename__ = 'terms'
    blueprint_slug = Column(String(100), ForeignKey('blueprints.slug'), primary_key=True)
    key = Column(String(100), primary_key=True)
    description = Column(String)

class Methods(Base):
    __tablename__ = 'methods'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blueprint_slug = Column(String(100), ForeignKey('blueprints.slug'))
    name = Column(String(100))
    description = Column(String(100))
    args = relationship("MethodArgs", backref="method")
    is_function = Column(Boolean)

class MethodArgs(Base):
    __tablename__ = 'method_args'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    method_id = Column(UUID(as_uuid=True), ForeignKey('methods.id'))
    name = Column(String(100))
    m_type = Column(String(100))
    description = Column(String(100))

class DeployManifest(Base):
    __tablename__ = 'deploymanifest'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest = Column(String, nullable=False)
    blueprint_slug = Column(String(2048), ForeignKey('blueprints.slug'), nullable=False)

class Community(Base):
    __tablename__ = 'community'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(128))
    component_address = Column(String(2048))
    description = Column(String)
    owner_address = Column(String(2048), ForeignKey('users.public_address'))

class Participants(Base):
    __tablename__ = 'participants'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    community_id = Column(UUID(as_uuid=True),ForeignKey('community.id'))
    user_addr = Column(String, ForeignKey('users.public_address'))


engine = create_engine('postgresql://pandao_database_user:lhLX8ipBc7O7QKUu8z5HL31iHTJgavO8@dpg-cp12prvjbltc73e6l0tg-a.oregon-postgres.render.com/pandao_database')
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
dbsession = Session()
