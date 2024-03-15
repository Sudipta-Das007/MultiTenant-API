from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from db.login import set_username_password,change_my_password, change_specific_user_password,delete_username_password,change_login_username,change_own_login_username
from db.database import session
from db.models import UserList,LoginDetail, UserApplication
from sqlalchemy import select
from auth import oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends()):
    user_details = session.scalars(select(LoginDetail).filter_by(user_name = request.username)).first()
    if not user_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials")
    
    if not user_details.user_password == request.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Password")

    access_token = oauth2.create_access_token(data={'sub': user_details.user_name})
    

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }





