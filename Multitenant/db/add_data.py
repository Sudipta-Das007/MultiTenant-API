from db.database import session
from db.models import TenantList,UsersList,Role,Permission,Application,RoleTenant,UserRole,UserApplication,LoginDetail,RolePermission,ApplicationPermission
from sqlalchemy import select


def add_permissions():
    permissions_dict = {

    'Update Own User Details': 'Update own user details',
    'View own tenant details': 'View details of own tenant',
    'View All users under a tenant': 'View details of all users under a tenant',
    'Change Own Password': 'Change own password',
    }

    permission_ids = []
    role_id = 3

    # Query the database for permission IDs
    for permission_name in permissions_dict.keys():
        permission = session.scalars(select(Permission).filter_by(permission=permission_name)).first()
        if permission:
            permission_ids.append(permission.permission_id)

    for permission_id in permission_ids:
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        session.add(role_permission)
    '''for name, description in permissions_dict.items():
        permission = Permissions(permission=name, description=description)
        session.add(permission)'''

    # Commit the changes
    session.commit()

    # Close the session
    session.close()

