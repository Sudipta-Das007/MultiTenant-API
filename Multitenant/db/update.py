from db.database import session
from db.models import TenantList,UserList,Role,Permission,Application,RoleTenant,UserRole,RolePermission,UserApplication,LoginDetail,ApplicationPermission
import re
from sqlalchemy import select

from fastapi import HTTPException

#Pattern allowing uppercase and lowercase letters, spaces, and hyphens ("-")
pattern = "^[a-zA-Z\\s-]*$"




#Function To Update Tenant
def update_specific_tenant(tenant_id,new_tenant_name,phone_number,owner,owner_contact,add_remove,current_tenant_name=None,floor_no=None,plot_no=None,plot_index=None):
    try:
        if(tenant_id == 0):
            if not current_tenant_name.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="Tenant name cannot be empty.")
                
        
            if not re.match(pattern, current_tenant_name):  # Check if the tenant name contains only letters and numbers
                raise HTTPException(status_code=400, detail="Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")
                

            #Check the Existence of the Tenant
            tenant_to_update=session.scalars(select(TenantList).filter_by(tenant_name = current_tenant_name)).first()

        else:
            tenant_to_update=session.scalars(select(TenantList).filter_by(tenant_id = tenant_id)).first()
        
        if tenant_to_update:
            i=0
            r=0
            if tenant_to_update.plot is not None:
                for plot in tenant_to_update.plot:
                    i=i+1
                r=1
            
            else:
                r=0


            if any(not field.strip() for field in [new_tenant_name, owner]):
                raise HTTPException(status_code=400, detail="Empty fields can't be stored in the database.")
                
            
            if any(not re.match(pattern, field) for field in [new_tenant_name, owner]):  # Check if the Owner name contains only letters and numbers
                raise HTTPException(status_code=400, detail="Tenant name and Owner name can only contain uppercase and lowercase letters, spaces, and hyphens.")
            
            existing_phone_number = session.scalars(select(TenantList).filter(TenantList.tenant_id!=tenant_to_update.tenant_id,
                                                                     TenantList.tenant_phone_number==int(phone_number)
                                                                     )).first()
            
            if (existing_phone_number):
                raise HTTPException(status_code=400, detail="Phone number already exists in the database.")
            
            if (len(str(phone_number)) != 10 and len(str(phone_number)) != 8):
                raise HTTPException(status_code=400, detail="Invalid Phone Number!!!")

            if (len(str(owner_contact)) != 10 and len(str(owner_contact)) != 8):
                raise HTTPException(status_code=400, detail="Invalid Phone Number!!!")
            
            
            tenant_to_update.tenant_name = new_tenant_name
            tenant_to_update.tenant_phone_number = int(phone_number)
            tenant_to_update.owner = owner
            tenant_to_update.owner_contact = int(owner_contact)

            if tenant_id == 0:#only user with owner role can change this
                if add_remove ==1:
                    plot_list =[]
                    if plot_no == None or floor_no == None:
                        raise HTTPException(status_code=400, detail="Provide the Values  of Floor No. & Plot No. ")
                    
                    # Create a dictionary with the plot details
                    plot_dict = {
                        "Floor": (floor_no),
                        "Plot No.": (plot_no)
                    }

                    all_tenant=session.scalars(select(TenantList)).all()

                    for tenant in all_tenant:
                        if tenant.plot is not None:
                            for plot in tenant.plot:
                                if plot_dict == plot:
                                    raise HTTPException(status_code=400, detail="Plot is Already Allocated!!!")

                    # Add the plot dictionary to the plot list
                    plot_list.append(plot_dict)

                    # Get the existing plot list from the tenant object and append the new plot list
                    new_plot_list= tenant_to_update.plot+plot_list

                    # Update the tenant object with the new plot list
                    tenant_to_update.plot = new_plot_list


                elif add_remove ==2 and r == 1:

                    if plot_index is None:
                        raise HTTPException(status_code=400, detail="Invalid Plot Index!!!")
                    
                    if plot_index <1 or plot_index > len(tenant_to_update.plot):
                        raise HTTPException(status_code=400, detail="Invalid Plot Index!!!")
                    new_plot_list = tenant_to_update.plot[:]
                    new_plot_list.pop(plot_index-1)
                    tenant_to_update.plot = new_plot_list

                

                elif add_remove == 3 and r == 1:

                    if plot_index is None:
                        raise HTTPException(status_code=400, detail="Invalid Plot Index!!!")
                    

                    if plot_index <1 or plot_index > len(tenant_to_update.plot):
                        raise HTTPException(status_code=400, detail="Invalid Plot Index!!!")
                    
                    new_plot_list = tenant_to_update.plot[:]
                    new_plot_list.pop(plot_index-1)
                    tenant_to_update.plot = new_plot_list

                    plot_list =[]

                    if plot_no == None or floor_no == None:
                        raise HTTPException(status_code=400, detail="Provide the Values  of Floor No. & Plot No. ")
                    
                    # Create a dictionary with the plot details
                    plot_dict = {
                        "Floor": (floor_no),
                        "Plot No.": (plot_no)
                    }
                    
                    all_tenant=session.scalars(select(TenantList)).all()

                    for tenant in all_tenant:
                        if tenant.plot is not None:
                            for plot in tenant.plot:
                                if plot_dict == plot:
                                    raise HTTPException(status_code=400, detail="Plot is Already Allocated!!!")


                    # Add the plot dictionary to the plot list
                    plot_list.append(plot_dict)

                    # Get the existing plot list from the tenant object and append the new plot list
                    new_plot_list= tenant_to_update.plot+plot_list

                    # Update the tenant object with the new plot list
                    tenant_to_update.plot = new_plot_list

                elif (add_remove == 2 or add_remove == 3) and r == 0:
                    raise HTTPException(status_code=400, detail="Cant remove or replace plots when No plots are Assigned")

                
            session.commit()
            return {
                'message': "Details Updated!!!"
            }

        else:
            raise HTTPException(status_code=404, detail=f"No tenant found. Please check and try again.")

    except HTTPException:
            raise
    
    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#Fuction To Update User
def update_user(tenant_id,user_name,uid,name,phone_number):
    try:
        user_ids = []

        if not user_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="User name cannot be empty.")
                
        
        if not re.match(pattern, user_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")
                
        
        if tenant_id == 0:
            #get user details
            user_to_update=session.scalars(select(UserList).filter_by(user_name = user_name)).all()
        
        else:
            #get user details
            user_to_update=session.scalars(select(UserList).filter(UserList.user_name == user_name, UserList.tenant == tenant_id)).all()

        #condition to check the existence of user
        if user_to_update:

            #Display User Details
            for user in user_to_update:
                user_ids.append(user.user_id)

            c=0
            if uid in user_ids:
                for user in user_to_update:
                    if(user.user_id == uid):
                        if any(not field.strip() for field in [name]):
                            raise HTTPException(status_code=400, detail="Empty fields can't be stored in the database.")
                             
                
                        if not re.match(pattern, name):  # Check if the tenant name contains only letters and numbers
                            raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")
                        

                        existing_phone_number = session.scalars(select(UserList).filter(UserList.user_id!=uid,
                                                                     UserList.user_phone_number==int(phone_number)
                                                                     )).first()
            
                        if (existing_phone_number):
                            raise HTTPException(status_code=400, detail="Phone number already exists in the database.")
                        
                        if (len(str(phone_number)) != 10 and len(str(phone_number)) != 8):
                            raise HTTPException(status_code=400, detail="Invalid Phone Number!!!")


                        #update the details of the specified user
                        user.user_name = name
                        user.user_phone_number = int(phone_number)
                        c=1
                        break

            session.commit()
            if(c==1):
                return {
                'message': "Details Updated!!!"
                }
            
            else:
                raise HTTPException(status_code=400, detail="Wrong ID!!!")

        else:
            raise HTTPException(status_code=400, detail=f"No user found with name {user_name}. Please check and try again.")


    except HTTPException:
            raise


    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")


    finally:
        #close the session
        session.close()




#Function to Update Own Details
def update_own_details(username,name,phone_number):
    try:
        details = session.execute(select(LoginDetail,UserList).filter_by(user_name = username).join(UserList,UserList.user_id == LoginDetail.user_id)).first()
        _, user = details

        if not name.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="User name cannot be empty.")

        
        if not re.match(pattern, name):  # Check if the tenant name contains only letters and numbers
                raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")

        
        existing_phone_number = session.scalars(select(UserList).filter(UserList.user_id!=user.user_id,
                                                               UserList.user_phone_number==int(phone_number)
                                                                )).first()
        if (existing_phone_number):
            raise HTTPException(status_code=400, detail="Phone number already exists in the database.")
        
        if (len(str(phone_number)) != 10 and len(str(phone_number)) != 8):
            raise HTTPException(status_code=400, detail="Invalid Phone Number!!!")

        user.user_name = name
        user.user_phone_number = phone_number
                            
        session.commit()
        return {
                'message': "Details Updated!!!"
                }

    except HTTPException:
            raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#Function To Transfer User From One Tenant to Another
def transfer_user(user_name,uid,new_tenant):
    try:
        user_ids = []

        if not user_name.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="User name cannot be empty.")
                
        
        if not re.match(pattern, user_name):  # Check if the tenant name contains only letters and numbers
                raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")
                


        #fetch the user details
        user_to_update=(session.execute(select(UserList,TenantList)
                        .filter_by(user_name = user_name)
                        .join(TenantList, TenantList.tenant_id == UserList.tenant, isouter= True))
                        .all())

        #check the existence of user
        if user_to_update:
            for user,tenant in user_to_update:
                user_ids.append(user.user_id)
        
            c=0
            if uid in user_ids:
                for user,_ in user_to_update:
                    if(user.user_id == uid):
                        #update the tenant id of the user.
                        tenant_ids = session.scalars(select(TenantList.tenant_id)).all()
                        if new_tenant not in tenant_ids:
                            raise HTTPException(status_code=400, detail="Invalid Tenant ID!!!")
                        
                        user.tenant=new_tenant

                        user_role_delete = (session.scalars(select(UserRole).filter_by(user_id = uid)).first())
                        user_application_delete = session.scalars(select(UserApplication).filter_by(user_id = uid)).first()


                        if(user_role_delete is not None):
                            #delete all the roles associated with the user
                            session.delete(user_role_delete)
                        
                        if(user_application_delete is not None):
                            #delete all the applications associated with the user
                            session.delete(user_application_delete)
                        c=1
                        break
            
            session.commit()
            if(c==1):
                return {
                'message': "Details Updated!!!"
                }
            
            else:
                raise HTTPException(status_code=400, detail="Wrong ID!!!")
        
        else:
            raise HTTPException(status_code=400, detail=f"No user found with name {user_name}. Please check and try again.")

    except HTTPException:
            raise
    
    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")


    finally:
        #close the session
        session.close()




#Function To Assign/Revoke Role From User
def assign_revoke_role(tenant_id,user_name,uid,add_remove,new_role=None):
    try:
        user_ids = []

        if not user_name.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="User name cannot be empty.")
                
        
        if not re.match(pattern, user_name):  # Check if the tenant name contains only letters and numbers
                raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")
                
        

        if(tenant_id == 0):
            user_to_update=session.execute(select(UserList,UserRole,Role).filter_by(user_name = user_name).join(UserRole,UserRole.user_id == UserList.user_id, isouter=True).join(Role, Role.role_id == UserRole.role_id, isouter= True)).all()
            
            role_ids = session.scalars(select(Role.role_id)).all()



        else:
            user_to_update=session.execute(select(UserList,UserRole,Role).filter(UserList.user_name == user_name, UserList.tenant == tenant_id).join(UserRole,UserRole.user_id == UserList.user_id, isouter=True).join(Role, Role.role_id == UserRole.role_id, isouter= True)).all()

            role_ids = session.scalars(select(RoleTenant.roles_available).filter(RoleTenant.tenant_id == tenant_id)).all()

        
        if user_to_update:

            #Display User Details
            #for user,_,_ in user_to_update:#for loop in case of multiple users with same name
            for user,role_id,role in user_to_update:#for loop in case of multiple roles
                user_ids.append(user.user_id)
                #Display the Role Assigned to the User
                if(role_id is not None and role is not None):
                    r=1
                else:
                    r=0


            if uid in user_ids:
                for user,role_id,role in user_to_update:
                    if(user.user_id == uid):
                        if(role_id is not None and role is not None):
                            r=1
                        else:
                            r=0
                        #Add Role
                        if add_remove == 1 and r == 0:
                            if new_role in role_ids:
                                assigned_role = UserRole(
                                    user_id = user.user_id,
                                    role_id = new_role
                                    )
                                session.add(assigned_role)
                                session.commit()
                                return {
                                    'message': "Details Updated!!!"
                                    }

                            else:
                                raise HTTPException(status_code=400, detail="Wrong Role ID!!!")

                            
                        
                        #If User Already has a Role
                        elif add_remove == 1 and r != 0:
                            raise HTTPException(status_code=400, detail="Already has a role can't assign another one.")
                            


                        #Remove the role from the user
                        elif add_remove == 2 and r != 0:
                            session.delete(session.scalars(select(UserRole).filter_by(user_id = user.user_id)).first())
                            session.commit()
                            return {
                                'message': "Details Updated!!!"
                                }
                            


                        #When No Role is Assigned
                        elif (add_remove == 2 or add_remove == 3) and r == 0:
                            raise HTTPException(status_code=400, detail="Cant remove or replace roles when No Role Assigned")
                            


                        #Replace Role
                        elif add_remove == 3 and r != 0:
                            if new_role in role_ids:
                                role_id.role_id = new_role
                                session.commit()
                                return {
                                    'message': "Details Updated!!!"
                                    }

                            else:
                                raise HTTPException(status_code=400, detail="Wrong Role ID!!!")
             

        else:
            raise HTTPException(status_code=404, detail=f"No user found with name {user_name}. Please check and try again.")
    

    except HTTPException:
            raise
    
    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#Function To Add/Remove Permission To a Role
def add_remove_permission_from_role(role_name,add_remove,pid):
    try:
        assigned_permission = []
        r=0

        if not role_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Role name cannot be empty.")
            return 
        
        if not re.match(pattern, role_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Role name can only contain uppercase and lowercase letters, spaces, and hyphens.")
            return


        role_to_update=(session.execute(select(Role,RolePermission,Permission)
                        .filter_by(role = role_name)
                        .join(RolePermission,RolePermission.role_id == Role.role_id,isouter = True)
                        .join(Permission,Permission.permission_id == RolePermission.permission_id, isouter =True))
                        .all())
        
        if role_to_update:
            role,_,_ = role_to_update[0]
            #For printing the role when role has multiple permissions
            for _,permission_id,permission in role_to_update:
                if(permission_id is not None and permission is not None):
                    assigned_permission.append(permission_id.permission_id)
                    r=1

                else:
                    r=0

            permission_ids = session.scalars(select(Permission.permission_id)).all()
            

            

            #Add Permission
            if add_remove == 1:
                c=True
                if pid in permission_ids:
                    #Check if Permission is already assigned
                    for _,permission_id,_ in role_to_update:
                        if(permission_id is not None and pid == permission_id.permission_id):
                            raise HTTPException(status_code=400, detail='This Permission is already assigned')
                    #IF Permission not assigned assign it
                    if c:
                        assigned_role = RolePermission(
                            role_id = role.role_id,
                            permission_id = pid
                            )
                        session.add(assigned_role)
                        session.commit()
                        return {
                            'message': "Details Updated!!!"
                            }
                
                else:
                    raise HTTPException(status_code=400, detail="Wrong Permission ID!!!")
            
            #Remove Permission
            elif add_remove == 2 and r!=0:
                if pid in permission_ids:
                    if pid in assigned_permission:
                        for _,permission_id,_ in role_to_update:
                            if(pid == permission_id.permission_id == pid):
                                session.delete(session.scalars(select(RolePermission).filter_by(permission_id = pid)).first())
                                session.commit()
                                return {
                                    'message': "Details Updated!!!"
                                    }
                               
                    
                    else:
                        raise HTTPException(status_code=400, detail="The Permission is not Assigned")
                
                else:
                    raise HTTPException(status_code=400, detail="Wrong Permission ID!!!")
            
            elif (add_remove == 2) and r == 0:
                raise HTTPException(status_code=400, detail="Cant remove permissions when No permissions are Assigned")


            


        else:
            raise HTTPException(status_code=404, detail=f"No role found with name {role_name}. Please check and try again.")

    except HTTPException:
            raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()



#Beutify It
#Function To Add/Remove User Access to Application
def assign_revoke_user_application(tenant_id,user_name,uid,add_remove,app_id,replacing_app_id=None):
    try:
        user_ids = []
        application_ids = []
        app=[]
        if not user_name.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="User name cannot be empty.")
                
        
        if not re.match(pattern, user_name):  # Check if the tenant name contains only letters and numbers
                raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")
               


        if tenant_id == 0:
            #Get User Details
            user_to_update=(session.execute(select(UserList,UserApplication,Application)
                            .filter_by(user_name = user_name)
                            .join(UserApplication,UserApplication.user_id == UserList.user_id, isouter=True)
                            .join(Application, Application.application_id == UserApplication.application_id, isouter= True))
                            .all())
            
        
        else:
            #Get User Details
            user_to_update=(session.execute(select(UserList,UserApplication,Application)
                            .filter(UserList.user_name == user_name, UserList.tenant == tenant_id)
                            .join(UserApplication,UserApplication.user_id == UserList.user_id, isouter=True)
                            .join(Application, Application.application_id == UserApplication.application_id, isouter= True))
                            .all())
            
        

        if user_to_update:

            #For printing the application when user has multiple applications
            for user, user_application, application in user_to_update:
                user_ids.append(user.user_id)
                
                

           
            if uid in user_ids:
                
                application_ids = session.scalars(select(Application.application_id)).all()
                

                for user,application_id,_ in user_to_update:
                    if user.user_id == uid and application_id is not None:
                        app.append(application_id.application_id)



                for user,application_id,_ in user_to_update:
                    if(user.user_id == uid):
                        #Add application Access
                        if add_remove == 1:
                            if app_id in application_ids:
                                #check if access to application is already assigned
                                if application_id not in app:
                                    assigned_application = UserApplication(
                                        user_id = user.user_id,
                                        application_id = app_id
                                    )
                                    session.add(assigned_application)
                                    session.commit()
                                    return {
                                        'message': "Details Updated!!!"
                                        }
                                else:
                                    raise HTTPException(status_code=400, detail="Already has The Application Access!!!")
                                break
                            else:
                                raise HTTPException(status_code=400, detail="Wrong Application ID!!!")
                                
                        

                        #Remove the application from the user
                        elif add_remove == 2 and len(app) != 0:
                            
                            if app_id in app:
                                session.delete(session.scalars(select(UserApplication).filter(UserApplication.application_id == app_id,
                                                                                     UserApplication.user_id == uid)).first())
                                session.commit()
                                return {
                                    'message': "Details Updated!!!"
                                    }

                            else:
                                raise HTTPException(status_code=400, detail="Wrong Application ID!!!")
                                
                        

                        elif (user.user_id == uid) and len(app) == 0 and  (add_remove == 2 or add_remove ==3):
                            raise HTTPException(status_code=400, detail="Cant remove or replace applications when No applications Assigned")
                            
                        
                        #Replace the Application Access
                        elif add_remove == 3 and len(app) != 0:
                            if app_id in app:
                                for user,application_id,_ in user_to_update:
                                    if(user.user_id == uid and application_id.application_id == app_id):
                                        
                                        if replacing_app_id in application_ids:
                                            if replacing_app_id not in app:
                                                application_id.application_id = int(replacing_app_id)
                                                session.commit()
                                                return {
                                                    'message': "Details Updated!!!"
                                                    }
                                            else:
                                                raise HTTPException(status_code=400, detail="Already has The Application Access!!!")
                                            break
                                        else:
                                            raise HTTPException(status_code=400, detail="Wrong Application ID!!!")
                                            
                            else:
                                raise HTTPException(status_code=400, detail="Wrong Application ID!!!")
                        
                        

        else:
            raise HTTPException(status_code=400, detail=f"No user found with name {user_name}. Please check and try again.")


    except HTTPException:
            raise

    
    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")


    finally:
        #close the session
        session.close()




#Function To Add/Remove Role To Tenant that it can assign its Users 
def assign_revoke_role_tenant(tenant_name,add_remove,rid,replacing_role=None):
    try:
        r=0
        role_list=[]
        if not tenant_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Tenant name cannot be empty.")
            
        
        if not re.match(pattern, tenant_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")
            

        #Get tenanat Details
        tenant_to_update=(session.execute(select(TenantList,RoleTenant,Role)
                        .filter_by(tenant_name = tenant_name)
                        .join(RoleTenant,RoleTenant.tenant_id == TenantList.tenant_id, isouter=True)
                        .join(Role, Role.role_id == RoleTenant.roles_available, isouter= True))
                        .all())
        
        #Checking If The Tenant Exists Or Not
        if tenant_to_update:
            tenant,_,_ = tenant_to_update[0]
            
            #For printing the role when Tenant has multiple roles
            for tenant,role_id,role in tenant_to_update:
                if(role_id is not None and role is not None):
                    role_list.append(role_id.roles_available)
                    r=1

                else:
                    r=0

            uid=tenant.tenant_id

            role_ids = session.scalars(select(Role.role_id)).all()



            #This Loop has no function, remove it
            for tenant,_,_ in tenant_to_update:
                if(tenant.tenant_id == uid):
                    #Add Role
                    if add_remove == 1:
                        if rid in role_ids:
                            if rid not in role_list:
                                assigned_role = RoleTenant(
                                    tenant_id = tenant.tenant_id,
                                    roles_available = rid
                                )
                                session.add(assigned_role)
                                session.commit()
                                return {
                                    'message': "Details Updated!!!"
                                    }
                            else:
                                raise HTTPException(status_code=400, detail="Already has The role Access!!!")
                            break

                        else:
                            raise HTTPException(status_code=400, detail="Wrong Role ID!!!")
                            
                    

                    #Remove the role from the user
                    elif add_remove == 2 and r != 0:
                        if rid in role_list:
                            for _,role_id,_ in tenant_to_update:
                                if role_id.roles_available == rid:
                                    session.delete(session.scalars(select(RoleTenant).filter(RoleTenant.roles_available == rid,
                                                                                    RoleTenant.tenant_id ==uid)).first())
                                    session.commit()
                                    return {
                                        'message': "Details Updated!!!"
                                        }
                                    
                        else:
                            raise HTTPException(status_code=400, detail="Wrong Role ID!!!")
                            
                    
                    elif (add_remove == 2 or add_remove == 3) and r == 0:
                        raise HTTPException(status_code=400, detail="Cant remove or replace roles when No roles Assigned")

                    #Replace The Role
                    elif add_remove == 3 and r != 0:
                        if rid in role_list:
                            for tenant,role_id,_ in tenant_to_update:
                                if role_id.roles_available == rid:
                                    if replacing_role in role_ids:
                                        if replacing_role not in role_list:
                                            role_id.roles_available = replacing_role
                                            session.commit()
                                            return {
                                                'message': "Details Updated!!!"
                                                }
                                        else:
                                            raise HTTPException(status_code=400, detail="Already has The role Access!!!")
                                        break
                                    else:
                                        raise HTTPException(status_code=400, detail="Wrong Role ID!!!")
                                        
                        else:
                            raise HTTPException(status_code=400, detail="Wrong Role ID!!!")
                        
        else:
            raise HTTPException(status_code=400, detail=f"No Tenant found with name {tenant_name}. Please check and try again.")



    except HTTPException:
            raise


    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")


    finally:
        #close the session
        session.close()




#Function to Update Application Permission
def update_application_permission(application_name,add_remove,pid):
    try:
        permission_assigned = []

        if not application_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Application name cannot be empty.")
            return
        
        if not re.match(pattern, application_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Application name can only contain uppercase and lowercase letters, spaces, and hyphens.")
            return


        application_to_update=(session.execute(select(Application,ApplicationPermission, Permission)
                        .filter_by(application_name = application_name)
                        .join(ApplicationPermission, ApplicationPermission.application_id == Application.application_id, isouter=True)
                        .join(Permission, Permission.permission_id == ApplicationPermission.permission_id,isouter=True))
                        .all())
        
        if application_to_update:
            #Display User Details
            application,_,_ = application_to_update[0]
            for _,_,permission in application_to_update:#for loop in case of multiple permissions
                #Display the Permission Assigned to the Appliation
                if(permission is not None):
                    r=1
                    permission_assigned.append(permission.permission_id)
                else:
                    r=0


            permission_ids = session.scalars(select(Permission.permission_id)).all()



            #Add Permission
            if add_remove == 1:
                #Check if Permission is already assigned
                if pid in permission_ids:
                    if pid not in permission_assigned:
                        assigned_permission = ApplicationPermission(
                            application_id = application.application_id,
                            permission_id = pid
                            )
                        session.add(assigned_permission)
                        session.commit()
                        return {
                            'message': "Details Updated!!!"
                            }
                    
                    else:
                        raise HTTPException(status_code=400, detail='This Permission is already assigned')
                
                else:
                    raise HTTPException(status_code=400, detail="Wrong Permission ID!!!")

            #Remove Permission
            elif add_remove == 2 and r !=0:
                if pid in permission_assigned:
                    for _,permission_id,_ in application_to_update:
                        if(pid == permission_id.permission_id):
                            session.delete(session.scalars(select(ApplicationPermission).filter(ApplicationPermission.permission_id == pid,
                                                                                       ApplicationPermission.application_id == application.application_id)).first())
                            session.commit()
                            return {
                                'message': "Details Updated!!!"
                                }
                            break
                else:
                    raise HTTPException(status_code=400, detail="Wrong Permission ID!!!")

            
            elif (add_remove == 2) and r == 0:
                raise HTTPException(status_code=400, detail="Cant remove permissions when No permissions are Assigned")


        else:
            raise HTTPException(status_code=400, detail=f"No application found with name {application_name}. Please check and try again.")
    

    except HTTPException:
            raise


    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")


    finally:
        #close the session
        session.close()
    



