from db.database import session
from db.models import TenantList,UserList,Role,Permission,Application,RoleTenant,UserRole,UserApplication,LoginDetail,RolePermission,ApplicationPermission
from sqlalchemy import select
import re
from fastapi import HTTPException
from collections import OrderedDict

pattern = "^[a-zA-Z\s-]*$"


#Search A Particular Tenant
def search_specific_tenant(tenant_name):
    try:
        #Get that Tenant Details
        tenant_data = session.scalars(select(TenantList).filter_by(tenant_name = tenant_name)).first()
        if not tenant_data:
            raise HTTPException(status_code=400, detail="No such Tenant is present in our records.")
        
        else:
            details_dict = {}
            details_dict = {key: value for key, value in tenant_data.__dict__.items() if '_sa_instance_state' not in key}
            return details_dict

    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()



#Search A Particular User
def search_specific_user(tenant_id, user_name):
    try:
        if(tenant_id == 0):
            #get the User Data
            user_data = session.execute(select(UserList,TenantList).filter_by(user_name=user_name).order_by(UserList.user_id).join(TenantList,TenantList.tenant_id == UserList.tenant, isouter=True)).all()
        
        else:
            user_data = session.execute(select(UserList,TenantList).filter(UserList.user_name == user_name, UserList.tenant == tenant_id).order_by(UserList.user_id).join(TenantList,TenantList.tenant_id == UserList.tenant, isouter=True)).all()


        if not user_data:
            raise HTTPException(status_code=400, detail="No User is present in our records.")
        
        else:
            user_dict = OrderedDict()
            i=0
            for user,tenant in user_data:
                if tenant:
                    tenant_details = {
                        'tenant_id': tenant.tenant_id,
                        'tenant_name': tenant.tenant_name,
                        'tenant_phone_number': tenant.tenant_phone_number,
                    }
                else:
                    tenant_details = None
                user_details = OrderedDict({key: value for key, value in user.__dict__.items() if key != 'tenant' and '_sa_instance_state' not in key})
                i=i+1
                user_dict[i] = {
                    'user_details': user_details,
                    'tenant_details': tenant_details
                }
            return user_dict
            
    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()



#Search A Particular Role
def search_specific_role(role_name):
    try:
        #Get the Role Details
        roles = (session.scalars(select(Role)
                     .filter_by(role = role_name))
                     .first())
        
        if not roles:
            raise HTTPException(status_code=400, detail="No Role is present in our records.")

        
        else:
            roles_dict = {}
            #Get the Associated Permission
            role_data = (session.execute(select(RolePermission,Permission).order_by(RolePermission.permission_id)
                     .join(Permission, Permission.permission_id == RolePermission.permission_id))
                     .all())
        
            permissions = []
            for permission_id,permission in role_data:
                if roles.role_id==permission_id.role_id:
                    permissions.append({key: value for key, value in permission.__dict__.items() if '_sa_instance_state' not in key})

            if len(permissions)==0:
                permissions.append("No Permission Associated.")
            
            roles_dict = {
                'role details': {key: value for key, value in roles.__dict__.items() if '_sa_instance_state' not in key},
                'permissions associated' : permissions
                }
            return roles_dict
        
    except HTTPException:
        raise
    
    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()



#Search A Particular Permission
def search_specific_permission(permission_name):
    try:  
        #get the permission details
        permission_data = session.scalars(select(Permission).filter_by(permission = permission_name)).first()
        if not permission_data:
            raise HTTPException(status_code=400, detail="No Permission is present in our records.")
        
        else:
            details_dict = {}
            details_dict = {key: value for key, value in permission_data.__dict__.items() if '_sa_instance_state' not in key}
            return details_dict

    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()


