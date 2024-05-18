from pydantic import BaseModel, Field
class UserLogin(BaseModel):
    public_address : str =  Field( ... , description ="user wallet public address")
    name : str = Field ( ... ,description = "user name, taken out from wallet")
    image_url : str = Field ( ... , description =" user image url, taken from wallet")