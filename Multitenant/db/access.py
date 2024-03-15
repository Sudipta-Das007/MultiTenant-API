from db.database import session
from db.models import UserRole, Role,RolePermission,Permission,LoginDetail
from sqlalchemy import select

from fastapi import HTTPException


def check_access(username):
    try:
        #get user details
        user_detail = (session.execute(select(LoginDetail,UserRole,Role).
                filter_by(user_name = username).
                join(UserRole, LoginDetail.user_id == UserRole.user_id).
                join(Role, UserRole.role_id==Role.role_id))
                .first())
        
        #get the role object from user_detail
        if not user_detail:
            raise HTTPException(status_code=400, detail="No Role Assigned")
        else:
            _,_,role = user_detail
            return(role)
        
    except HTTPException:
            raise
    
    except Exception as e:
        print(f"{e}")
    finally:
        session.close()
        
