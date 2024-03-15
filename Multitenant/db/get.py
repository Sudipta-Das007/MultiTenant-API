from db.database import session
from db.models import UserList, LoginDetail, RolePermission, Permission, TenantList,ApplicationPermission
from sqlalchemy import select



#Retrive Permission associated with the user
def get_roles_permissions(access,application_id):
    try:
        permissions_role=[]
        permissions_application=[]
        #get the permissions of the role
        permissions_role_obj = (session.execute(select(RolePermission, Permission)
                                .filter_by(role_id = access.role_id)
                                .join(Permission, Permission.permission_id == RolePermission.permission_id))
                                .all())

        #get the permissions of the application
        permissions_application_obj = (session.execute(select(ApplicationPermission,Permission)
                                       .filter_by(application_id = application_id)
                                       .join(Permission, Permission.permission_id == ApplicationPermission.permission_id))
                                       .all())
        
        #get the permissions and store them in a list
        for _,role_permission in permissions_role_obj:
            permissions_role.append(role_permission.permission)

        
        for _,application_permission in permissions_application_obj:
            permissions_application.append(application_permission.permission)

        # Find the common permissions
        common_permissions = list(set(permissions_role).intersection(permissions_application))

        #return the permissions list
        return common_permissions
    
    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()


#get the Tenant Details of the User
def get_tenant(username,access):
    try:
        #get the tenant details of the user
        if  access.role != 'Owner':
            tenant = session.execute(select(LoginDetail,UserList,TenantList).filter_by(user_name=username).join(UserList, UserList.user_id == LoginDetail.user_id).join(TenantList,TenantList.tenant_id == UserList.tenant)).all()

            #store the tenant details object in a variable
            _,_,tenant_name = tenant[0]

            #return the tenant name to the main function
            return (tenant_name.tenant_id)
        
        
        else:
            return None
    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()

