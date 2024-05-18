from sqlalchemy.exc import IntegrityError
from models import dbsession as conn, User
from ....forms import UserLogin
from ....utils import ApiError



def user_login_req(req: UserLogin):
    # extract data frim form
    wallet_addr = req.public_address
    name = req.name
    dp = req.image_url
    # construct a new user class
    user = User(name=name, public_address=wallet_addr)
    conn.add(user)
    try:
        conn.commit()
    except IntegrityError:
        conn.rollback()
        return ApiError("wallet address already exits" , 401)

    response = conn.query(User).all()
    return response
    
                 