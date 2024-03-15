from db.database import session
from db.models import TenantList,UserList,Role,Permission,Application,RoleTenant,UserRole,UserApplication,LoginDetail,RolePermission,ApplicationPermission
import re
from sqlalchemy import select

from fastapi import HTTPException

#Pattern allowing uppercase and lowercase letters, spaces, and hyphens ("-")
pattern = "^[a-zA-Z\s-]*$"



#Delete the Tenant
def delete_specific_tenant(tenant_name,confirmation):
    try:
        if not tenant_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Tenant name cannot be empty.")
   
        
        if not re.match(pattern, tenant_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")


        #Get Tenant Details
        tenant_details = (session.execute(select(TenantList,RoleTenant,UserList)
                          .filter_by(tenant_name = tenant_name)
                          .join(RoleTenant, RoleTenant.tenant_id == TenantList.tenant_id, isouter=True)
                          .join(UserList, UserList.tenant == TenantList.tenant_id, isouter= True))
                          .all())


        if not tenant_details:
            raise HTTPException(status_code=400, detail="No such Tenant exists in the Database.")


        else:
            #Print The Tenant Details
            tenant,_,_ = tenant_details[0]
            if confirmation.lower() == "yes":
                #Delete the Tenant
                session.delete(tenant)
                for tenant_row in tenant_details:
                    #Delete everything associated with the tenant
                    _,role,_ = tenant_row
                    if(role):
                        session.delete(role)
                delete_user_under_tenant(tenant.tenant_id)
                session.commit()
                return {
                    'message': "Tenant Deleted"
                }
    
            else:
                raise HTTPException(status_code=400, detail="Deletion canceled.")

        
    except HTTPException:
        raise

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        session.close()




#Delete the User under a tenant Only used for delete_tenant() funtion
def delete_user_under_tenant(tenant_id):
    try:
        #get the user details
        user_details = session.scalars(select(UserList).filter_by(tenant = tenant_id)).all()
        if not user_details:
            pass
    
        else:
            for user in user_details:

                #get the user connections
                get_user_connections = (session.execute(select(LoginDetail,UserRole,UserApplication)
                                        .filter_by(user_id = user.user_id)
                                        .join(UserApplication, UserApplication.user_id == LoginDetail.user_id,isouter= True)
                                        .join(UserRole,UserRole.user_id == LoginDetail.user_id, isouter= True))
                                        .all())
                
                #delete the user connections
                for connections in get_user_connections:
                    role,application,login = connections
                    if(role):
                        session.delete(role)
                    if(application):
                        session.delete(application)
                    if(login):
                        session.delete(login) 
                
                session.delete(user)

        session.commit()
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        session.close()




#Delete the User
def delete_specific_user(tenant_id,user_name,uid,confirmation):
    try:
        user_ids = []
        if not user_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="User name cannot be empty.")

        
        if not re.match(pattern, user_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")


        
        if(tenant_id == 0):
            #get the user details
            user_details = session.scalars(select(UserList).where(UserList.user_name == user_name)).all()
            
        
        else:
            #get the user details based on tenant_id and user_name
            user_details = session.scalars(select(UserList).where(UserList.user_name == user_name, UserList.tenant == tenant_id)).all()
        
        if not user_details:
            raise HTTPException(status_code=400, detail="No such User exists in the Database.")
    
        else:
            for user in user_details:
                user_ids.append(user.user_id)

            if uid in user_ids:
                for user in user_details:
                    if(user.user_id == uid):
                        a=1
                        if confirmation.lower() == "yes":
                            #get the user connections
                            session.delete(user)
                            get_user_roles = (session.scalars(select(UserRole)
                                                .filter_by(user_id = uid))
                                                .all())
                            get_user_applications = session.scalars(select(UserApplication).where(UserApplication.user_id == uid)).all()
                            get_user_login = session.scalars(select(LoginDetail).where(LoginDetail.user_id == uid)).first()
                            #delete the user connections
                            if  get_user_roles is not None and get_user_applications is not None and get_user_login is not None:
                                for connections in get_user_roles:
                                    session.delete(connections)

                                for connections in get_user_applications:
                                    session.delete(connections)
                                
                                session.delete(get_user_login)

                            
                            tenant = session.scalars(select(TenantList).where(TenantList.tenant_id == user.tenant)).first()
                            tenant.user_count = tenant.user_count-1
                            
                            session.commit()

                            return {
                                'message': "User Deleted"
                                }
                        else:
                            raise HTTPException(status_code=400, detail="Deletion canceled.")
                       
            else:
                raise HTTPException(status_code=400, detail="No user with that User ID")
        
        
    except HTTPException:
            raise
    
    except Exception:
        raise
    
    finally:
        session.close()




#Delete the Role from the System
def delete_specific_role(role_name,confirmation):
    try:
        if not role_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Role name cannot be empty.")

        
        if not re.match(pattern, role_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Role name can only contain uppercase and lowercase letters, spaces, and hyphens.")


        #Get the Role Details
        role_details = (session.execute(select(Role,RolePermission,UserRole,RoleTenant)
                        .filter_by(role = role_name)
                        .join(RolePermission,RolePermission.role_id == Role.role_id, isouter=True)
                        .join(UserRole,UserRole.role_id == Role.role_id, isouter=True)
                        .join(RoleTenant, RoleTenant.roles_available == Role.role_id, isouter=True))
                        .all())
        
        if not role_details:
            raise HTTPException(status_code=400, detail="No such Role exists in the Database.")
        
        else:
            #Print The role Details
            role,_,_,_ = role_details[0]
            if confirmation.lower() == "yes":
                session.delete(role)
                for connections in role_details:
                    #Delete the Connections
                    _,Permission,users,tenant = connections
                    if Permission:
                        session.delete(Permission)
                    if users:
                        session.delete(users)
                    if tenant:
                        session.delete(tenant)
                
                session.commit()
                return {
                        'message': "Role Deleted"
                        }
    
            else:
                raise HTTPException(status_code=400, detail="Deletion canceled.")

        

    except HTTPException:    
        raise


    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        session.close()




#Delete the Permission from the System
def delete_specific_permission(permission_name,confirmation):
    try:
        if not permission_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Permission name cannot be empty.")
        
        
        if not re.match(pattern, permission_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Permission name can only contain uppercase and lowercase letters, spaces, and hyphens.")
       

        #Get the Permission_Details
        permission_details = (session.execute(select(Permission,RolePermission,ApplicationPermission)
                              .filter_by(permission = permission_name)
                              .join(RolePermission, RolePermission.permission_id == Permission.permission_id, isouter=True)
                              .join(ApplicationPermission, ApplicationPermission.permission_id == Permission.permission_id, isouter=True))
                              .all())
        
        print(permission_details)
        
        if not permission_details:
            raise HTTPException(status_code=400, detail="No such Permission exists in the Database.")
        
        else:
            #Print The permission Details
            permission,_,_ = permission_details[0]
            if confirmation.lower() == "yes":
                session.delete(permission)
                for connections in permission_details:
                    #delete the Connections
                    _,role,application = connections
                    if role is not None:
                        session.delete(role)
                    if application is not None:
                        session.delete(application)

                session.commit()
                return {
                        'message': "Permission Deleted"
                        }
    
            else:
                raise HTTPException(status_code=400, detail="Deletion canceled.")

        
    
    except HTTPException:    
        raise

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        session.close()




#Delete the Application
def delete_specific_application(application_name,confirmation):
    try:
        if not application_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Application name cannot be empty.")

        
        if not re.match(pattern, application_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Application name can only contain uppercase and lowercase letters, spaces, and hyphens.")



        #get the Application Details
        application_details = (session.execute(select(Application, ApplicationPermission, UserApplication)
                               .filter_by(application_name = application_name)
                               .join(ApplicationPermission, ApplicationPermission.application_id == Application.application_id, isouter=True)
                               .join(UserApplication, UserApplication.application_id == Application.application_id, isouter=True))
                               .all())
        
        if not application_details:
            raise HTTPException(status_code=400, detail="No such Application exists in the Database.")
        
        else:
            application,_,_ = application_details[0]

            if confirmation.lower() == "yes":
                session.delete(application)
                #Delete the Application Connections 
                for connections in application_details:
                    _,Permission,user = connections
                    if Permission:
                        session.delete(Permission)
                    if user:
                        session.delete(user)
                session.commit()
                return {
                        'message': "Application Deleted"
                        }
    
            else:
                raise HTTPException(status_code=400, detail="Deletion canceled.")

        
    
    except HTTPException:    
        raise

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        session.close()




