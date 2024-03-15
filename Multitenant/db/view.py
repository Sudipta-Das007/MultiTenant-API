from db.database import session
from db.models import TenantList,UserList,Role,Permission,Application,RoleTenant,UserRole,UserApplication,LoginDetail,RolePermission,ApplicationPermission
from sqlalchemy import select
import re
from fastapi import HTTPException
from collections import OrderedDict


#Pattern allowing uppercase and lowercase letters, spaces, and hyphens ("-")
pattern = "^[a-zA-Z\s-]*$"


#view details of All Tenants
def view_tenant_details():
    try:
        i=0
        #get all tenant data
        tenant_details = session.scalars(select(TenantList).order_by(TenantList.tenant_id)).all()
        if not tenant_details:
            raise HTTPException(status_code=400, detail="No Tenant is present in our records.")
        
        else:
            tenant_dict = {}
            tenant_list=[]
            for tenant in tenant_details:
                i=i+1
                tenant_list.append(tenant.__dict__)
                for item in tenant_list:
                    if '_sa_instance_state' in item:
                        del item['_sa_instance_state']
            tenant_dict['all tenants'] = tenant_list
            return tenant_dict

    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#View All Users of all tenants
def view_all_users():
    try:
        i=0
        #get User Data
        user_dict = {}
        user_data = session.execute(select(UserList,TenantList).join(TenantList,TenantList.tenant_id == UserList.tenant, isouter=True)).all()
        if not user_data:
            raise HTTPException(status_code=400, detail="No User is present in our records.")
        
        else:
            for user,tenant in user_data:
                if tenant:
                    tenant_details = {
                        'tenant_id': tenant.tenant_id,
                        'tenant_name': tenant.tenant_name,
                        'tenant_phone_number': tenant.tenant_phone_number,
                    }
                else:
                    tenant_details = None
                user_details = {key: value for key, value in user.__dict__.items() if key != 'tenant' and '_sa_instance_state' not in key}
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




#View All Role present in the System
def view_all_roles():
    try:
        i=0
        #Get all the Role
        all_roles = (session.scalars(select(Role)
                     .order_by(Role.role_id))
                     .all())
        
        if not all_roles:
            raise HTTPException(status_code=400, detail="No Role is present in our records.")

        
        else:
            roles_dict = {}
            #Get the Associated Permission
            role_data = (session.execute(select(RolePermission,Permission).order_by(RolePermission.permission_id)
                     .join(Permission, Permission.permission_id == RolePermission.permission_id))
                     .all())
            
            for role in all_roles: 
                permissions_list = []
                for permission_id,permission in role_data:
                    if role.role_id==permission_id.role_id:
                        permissions = {key: value for key, value in permission.__dict__.items() if '_sa_instance_state' not in key}
                        permissions_list.append(permissions)

                if len(permissions_list)==0:
                    permissions_list.append("No Permission Associated.")
                
                i=i+1
                roles = {key: value for key, value in role.__dict__.items() if '_sa_instance_state' not in key}
                
                roles_dict[i] = {
                    'role details': roles,
                    'permissions associated' : permissions_list
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





#View All Permission in the System
def view_all_permissions():
    try:
        i=0
        permissions_dict = {}
        #Get Permission Data
        permission_data = session.scalars(select(Permission).order_by(Permission.permission_id)).all()
        if not permission_data:
            raise HTTPException(status_code=400, detail="No Permission is present in our records.\n")
        
        else:
            for permission in permission_data:
                i=i+1
                permissions = {key: value for key, value in permission.__dict__.items() if '_sa_instance_state' not in key}
                permissions_dict[i] = OrderedDict(permissions)

            return permissions_dict
    
    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()





#View All the Application in the system
def view_all_applications():
    try:
        i=0
        applications_dict = OrderedDict()
        #Get Application Details
        application_data = session.scalars(select(Application).order_by(Application.application_id)).all()
        if not application_data:
            raise HTTPException(status_code=400, detail="No Application is present in our records.")
        
        else:
            for application in application_data: 
                applications = {key: value for key, value in application.__dict__.items() if '_sa_instance_state' not in key}
                i=i+1
                applications_dict[i] = applications

            return applications_dict
    

    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#View All users under a Tenant
def view_all_users_under_tenant(tenant_id,tenant_name = None):
    try:
        if(tenant_id == 0):
            if not tenant_name.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="Tenant name cannot be empty.")
        
            if not re.match(pattern, tenant_name):  # Check if the tenant name contains only letters and numbers
                raise HTTPException(status_code=400, detail="Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")

            #get User Data
            user_data = session.execute(select(TenantList,UserList).filter_by(tenant_name = tenant_name).join(UserList,UserList.tenant == TenantList.tenant_id, isouter=True)).all()

        else:
            user_data = session.execute(select(TenantList,UserList).filter_by(tenant_id = tenant_id).join(UserList,UserList.tenant == TenantList.tenant_id, isouter=True)).all()

        
        if not user_data:
            raise HTTPException(status_code=404, detail="No such Tenant is present in our records.\n")
        
        else:
            tenant,users = user_data[0]
            tenant_details = {
                        'tenant_id': tenant.tenant_id,
                        'tenant_name': tenant.tenant_name,
                        'tenant_phone_number': tenant.tenant_phone_number,
                    }
            user_list = []
            user_dict = OrderedDict()
            if users:
                for _,user in user_data:
                    user_details = OrderedDict({key: value for key, value in user.__dict__.items() if key != 'tenant' and '_sa_instance_state' not in key})
                    user_list.append(user_details)
            else:
                user_list.append("No Users Present")

            user_dict = {
                'tenant details' :  tenant_details,
                'user details' :  user_list
            }
            return  user_dict
        
    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#View All the Role That the Tenant Can Assign its Users
def view_all_roles_under_tenant(tenant_id, tenant_name = None):
    try:
        roles=[]
        details_dict = {}
        if(tenant_id == 0):
            if not tenant_name.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="Tenant name cannot be empty.")
                return
        
            if not re.match(pattern, tenant_name):  # Check if the tenant name contains only letters and numbers
                raise HTTPException(status_code=400, detail="Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")
                return

            #get the Tenant Details
            tenant_data = (session.execute(select(TenantList,RoleTenant,Role)
                        .filter_by(tenant_name = tenant_name)
                        .join(RoleTenant,RoleTenant.tenant_id == TenantList.tenant_id, isouter=True)
                        .join(Role, Role.role_id == RoleTenant.roles_available,isouter = True)
                        .order_by(Role.role_id))
                        .all())
        
        else:
            #get the Tenant Details
            tenant_data = (session.execute(select(TenantList,RoleTenant,Role)
                        .filter_by(tenant_id = tenant_id)
                        .join(RoleTenant,RoleTenant.tenant_id == TenantList.tenant_id, isouter=True)
                        .join(Role, Role.role_id == RoleTenant.roles_available,isouter = True)
                        .order_by(Role.role_id))
                        .all())
            


        if tenant_data:
            tenant,role,role_id = tenant_data[0]
            if (role is not None) and (role_id is not None):
                for _,_,role in tenant_data:
                    roles.append({key: value for key, value in role.__dict__.items() if '_sa_instance_state' not in key})
            else:
                roles.append("No Roles Associated")

            tenant_details = {
                        'tenant_id': tenant.tenant_id,
                        'tenant_name': tenant.tenant_name,
                        'tenant_phone_number': tenant.tenant_phone_number,
                    }
            
            details_dict = {
                'tenant details' :  tenant_details,
                'roles associated' :   roles
            }

            return details_dict
            
        
        else:
            raise HTTPException(status_code=400, detail="No such Tenant is present in our records.\n")
    
    except HTTPException:
        raise
            
    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#View All the Application Permission
def view_all_application_permissions(application_name):
    try:
        permissions = []
        details_dict = {}

        #Get Application Data
        application_data = (session.execute(select(Application,ApplicationPermission,Permission)
                     .filter_by(application_name = application_name)
                     .join(ApplicationPermission,ApplicationPermission.application_id == Application.application_id, isouter=True)
                     .join(Permission,Permission.permission_id == ApplicationPermission.permission_id, isouter=True))
                     .all())
        
        if not application_data:
            raise HTTPException(status_code=400, detail="No such application is present in our records.")
        
        else:
            application,permissions_id,_ = application_data[0]
            if permissions_id is not None:
                for _,_,permission in application_data:
                    permissions.append({key: value for key, value in permission.__dict__.items() if '_sa_instance_state' not in key})
            
            if len(permissions) == 0:
                permissions.append("No Permissions Assigned")

            details_dict = {
                'application details' : {key: value for key, value in application.__dict__.items() if '_sa_instance_state' not in key},
                'permissions assigned' :  permissions
            }
            return details_dict

    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




def view_own_user_details(username):
    try:
        details = session.execute(select(LoginDetail,UserList).filter_by(user_name = username).join(UserList,UserList.user_id == LoginDetail.user_id)).first()
        _, user = details
        details_dict = {key: value for key, value in user.__dict__.items() if '_sa_instance_state' not in key}
        return  details_dict

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()


