from uuid import UUID

from pydantic import BaseModel, Field
from typing_extensions import Optional,List


class UserLogin(BaseModel):
    public_address : str =  Field( ... , description ="user wallet public address")
    name : str = Field ( ... ,description = "user name, taken out from wallet")
    image_url : str = Field ( ... , description =" user image url, taken from wallet")
# Pydantic models

class MethodArgsModel(BaseModel):
    id: Optional[UUID]
    method_id: Optional[UUID]
    name: Optional[str]
    m_type: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True

class MethodsModel(BaseModel):
    id: Optional[UUID]
    name: Optional[str]
    description: Optional[str]
    args: Optional[List[MethodArgsModel]]
    is_function: Optional[bool]

    class Config:
        orm_mode = True
        from_attributes = True

class TermsModel(BaseModel):
    key: str
    description: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True

class BluePrintModel(BaseModel):
    slug: str
    description: Optional[str]
    terms: Optional[List[TermsModel]]
    price: Optional[int]
    methods: Optional[List[MethodsModel]]
    package_addr: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True


class CommunityCreate(BaseModel):
    name: Optional[str] = Field(None, max_length=128)
    component_address: Optional[str] = Field(None, max_length=2048)
    description: Optional[str]
    owner_address: str = Field(..., max_length=2048)


