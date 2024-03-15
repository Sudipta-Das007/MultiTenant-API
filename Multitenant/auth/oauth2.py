from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from fastapi import HTTPException, status, Depends
from db.database import session
from sqlalchemy import select
from db.models import UserList,LoginDetail
from auth.access import get_user_access


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY ='eff916a12673ab71d26df3ae6ea4571de2af63fbe6ef97d0c931dc4861415655'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt





def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        if username  is None:
           raise credentials_exception
        

    except JWTError:
       raise credentials_exception

    function_access = get_user_access(username)
    
    get_user = session.execute(select(LoginDetail, UserList).filter_by(user_name = username).join(UserList, UserList.user_id == LoginDetail.user_id)).first()

    if get_user is None:
       raise credentials_exception
    
    user_dict = {}
    _,user = get_user
    user_dict = {
       'id': user.user_id,
       'username': user.user_name,
       'login_username': username,
       'tenant_id': user.tenant,
       'permissions' : function_access
    }
    return user_dict







