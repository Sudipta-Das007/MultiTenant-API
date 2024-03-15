from db.models import TenantList,UserList,Role,Permission,Application,RoleTenant,UserRole,UserApplication,LoginDetail,RolePermission,ApplicationPermission

from sqlalchemy import select
from db.database import session


def get_user_access(username):
    user_detail = session.execute(select(LoginDetail, UserRole, RolePermission,Permission)
                                .filter_by(user_name = username)
                                .join(UserRole, UserRole.user_id == LoginDetail.user_id)
                                .join(RolePermission, RolePermission.role_id == UserRole.role_id)
                                .join(Permission, Permission.permission_id == RolePermission.permission_id)).all()
    permission_list =[]
    for _,_,_,permission in user_detail:
        permission_list.append(permission.permission)

    return  list(set(permission_list))
