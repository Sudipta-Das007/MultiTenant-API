from db.database import session # Import the session object from the database module
from db.models import TenantList,UserList,Role,Permission,Application,RoleTenant # Import the class from the models module
import re
from sqlalchemy import func,select
from fastapi import HTTPException


#Pattern allowing uppercase and lowercase letters, spaces, and hyphens ("-")
pattern = "^[a-zA-Z\s-]*$"


#Function to add Tenant
def add_new_tenant(tenant_title, tenant_phone_number, owner, owner_phone_number,floor_no, plot_no):
    """
    Function to add a new tenant to the database.
    """
    try:
        if not tenant_title.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Tenant name cannot be empty.")
        
        if not re.match(pattern, tenant_title):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")
        

        # Check if the tenant already exists in the database
        existing_tenant = session.scalars(select(TenantList).filter(func.lower(TenantList.tenant_name) == tenant_title.lower())).first()

        plot_list=[]
        if existing_tenant:
            raise HTTPException(status_code=400, detail="Tenant Already Exists!!!")
        
        else:
            # If the tenant doesn't exist, get user input for other tenant details
            existing_phone_number = session.scalars(select(TenantList).filter_by(tenant_phone_number=int(tenant_phone_number))).first()
            if (existing_phone_number):
                raise HTTPException(status_code=400, detail="Phone number already exists in the database.")


            if (len(str(tenant_phone_number)) != 10 and len(str(tenant_phone_number)) != 8):
                raise HTTPException(status_code=400, detail="Invalid Phone Number!!!")

            if (len(str(owner_phone_number)) != 10 and len(str(owner_phone_number)) != 8):
                raise HTTPException(status_code=400, detail="Invalid Phone Number!!!")

            if any(not field.strip() for field in [tenant_title, owner]):
                raise HTTPException(status_code=400, detail="Empty fields can't be stored in the database.")
            
            if not re.match(pattern, owner):  # Check if the Owner name contains only letters and numbers
                raise HTTPException(status_code=400, detail="Owner name can only contain uppercase and lowercase letters, spaces, and hyphens.")


            # Create a dictionary with the plot details
            plot_dict = {
                "Floor":int(floor_no),
                "Plot No.": int(plot_no)
            }

            all_tenant=session.scalars(select(TenantList)).all()

            for tenant in all_tenant:
                if tenant.plot is not None:
                    for plot in tenant.plot:
                        if plot_dict == plot:
                            raise HTTPException(status_code=400, detail="Plot is Already Allocated!!!")


            # Add the plot dictionary to the plot list
            plot_list.append(plot_dict)
            #print(plot_list)

            # Create a new tenant object with the user inputs
            new_tenant = TenantList(
                tenant_name = tenant_title,
                tenant_phone_number=int(tenant_phone_number),
                owner = owner,
                owner_contact = int(owner_phone_number),
                plot = plot_list
            )

            # Add the new tenant object to the session
            session.add(new_tenant)

        # Commit the changes to the database
        session.commit()

        tenant_added = session.scalars(select(TenantList).filter_by(tenant_name=tenant_title)).first()
        return {"message":"Tenant Successfully Added", 
                "tenant added":tenant_added.__dict__}
    

    except HTTPException:
        raise
    
    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#Function to add User
def add_new_user(tenant_id,user_title,user_phone_number,tenant_title=None):
    """
    Function to add a new user to the database.
    """
    try:
        if not user_title.strip(): 
            raise HTTPException(status_code=400, detail="Empty fields can't be stored in the database.")

        
        if not re.match(pattern, user_title):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")

        

        existing_phone_number = session.scalars(select(UserList).filter_by(user_phone_number=int(user_phone_number))).first()
        if (existing_phone_number):
            raise HTTPException(status_code=400, detail="Phone number already exists in the database.")
        
        if (len(str(user_phone_number)) != 10 and len(str(user_phone_number)) != 8):
                raise HTTPException(status_code=400, detail="Invalid Phone Number!!!")

        if(tenant_id == 0):
            if not tenant_title.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="Tenant name cannot be empty.")

            if not re.match(pattern, tenant_title):  # Check if the tenant name contains only letters and numbers
                raise HTTPException(status_code=400, detail="Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")

            tenant_id = session.scalars(select(TenantList).filter_by(tenant_name = tenant_title)).first()
        else:
            tenant_id = session.scalars(select(TenantList).filter(TenantList.tenant_id == tenant_id)).first()
            
        if tenant_id:

            new_user = UserList(
                user_name = user_title,
                user_phone_number = int(user_phone_number),
                tenant = tenant_id.tenant_id
                )
            
            if tenant_id.user_count is not None:
                tenant_id.user_count = tenant_id.user_count + 1
            elif tenant_id.user_count is None:
                tenant_id.user_count = 1

            # Add the new tenant object to the session
            session.add(new_user)

            # Commit the changes to the database
            session.commit()

            user_added = session.scalars(select(UserList).filter_by(user_phone_number=user_phone_number)).first()
            return {"message":"User Successfully Added", 
                    "tenant added":user_added.__dict__}

        else:
            raise HTTPException(status_code=400, detail="No tenant Found")



    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#Function to add Role
def add_new_role(new_role_name,new_role_description):
    """
    Function to add a new role to the database.
    """
    try:
        if not new_role_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Role name cannot be empty.")

        
        if not re.match(pattern, new_role_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Role name can only contain uppercase and lowercase letters, spaces, and hyphens.")


        #Check the existence of the new Role
        check_role = session.scalars(select(Role).filter(func.lower(Role.role) == new_role_name.lower())).first()

        if(check_role):
            raise HTTPException(status_code=400, detail="Role already Exists")

        else:
            if not new_role_description.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="Role Description cannot be empty.")

            new_role = Role(
                role=new_role_name,
                description = new_role_description
            )

            # Add the new role object to the session
            session.add(new_role)

            #Commit changes to the database
            session.commit()
            role_added = session.scalars(select(Role).filter_by(role=new_role_name)).first()
            return {"message":"Role Successfully Added", 
                    "tenant added":role_added.__dict__}
        
    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()



#Function to add Permission
def add_new_permission(new_permission_name,new_permission_description):
    """
    Function to add a new permission to the database.
    """
    try:
        
        if not new_permission_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Permission name cannot be empty.")

        
        if not re.match(pattern, new_permission_name):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Permission name can only contain uppercase and lowercase letters, spaces, and hyphens.")


        #Check the existence of the new Permission
        check_permission = session.scalars(select(Permission).filter(func.lower(Permission.permission) == new_permission_name.lower())).first()

        if(check_permission):
            raise HTTPException(status_code=400, detail="Permission already Exists")

        else:
            if not new_permission_description.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="Permission description cannot be empty.")
            new_permission = Permission(
                permission=new_permission_name,
                description = new_permission_description
            )

            # Add the new permission object to the session
            session.add(new_permission)

            #Commit changes to the database
            session.commit()
            
            permission_added = session.scalars(select(Permission).filter_by(permission=new_permission_name)).first()
            return {"message":"Permission Successfully Added", 
                    "tenant added":permission_added.__dict__}
        

    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()




#Function to add Application
def add_new_application(new_application_name):
    """
    Function to add a new application to the database.
    """
    try:
        if not new_application_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Application name cannot be empty.")

        if not re.match(pattern, new_application_name):  # Check if the permission name contains only letters and numbers
            raise HTTPException(status_code=400, detail="Application name can only contain uppercase and lowercase letters, spaces, and hyphens.")


        #Check the existence of the new application
        check_application = session.scalars(select(Application).filter(func.lower(Application.application_name) == new_application_name.lower())).first()

        if(check_application):
            raise HTTPException(status_code=400, detail="Application already Exists")

        else:
            #Create an object of Application
            new_application = Application(
                application_name = new_application_name,
            )

            # Add the new application object to the session
            session.add(new_application)

            #Commit changes to the database
            session.commit()

            application_added = session.scalars(select(Application).filter_by(application_name=new_application_name)).first()
            return {"message":"Application Successfully Added", 
                    "tenant added":application_added.__dict__}
        

    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()



#The next function is not Needed
#Function to add role available for a Tenant 
def add_role_available_for_tenant():
    """
    Function to add Role available for the Tenant to Assign.
    """
    try:
        #Get user input for the Tenant Name
        tenant_name = input("Enter the Tenant Name: ")

        if not tenant_name.strip():  # Check if tenant_title is empty or contains only whitespace
            raise ValueError("Tenant name cannot be empty.")

        
        if not re.match(pattern, tenant_name):  # Check if the tenant name contains only letters and numbers
            raise ValueError("Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")


        #Check the existence of Tenant
        check_tenant = session.scalars(select(TenantList).filter(func.lower(TenantList.tenant_name) == tenant_name.lower())).first()

        if check_tenant:
            #while loop for binding multiple Role to Tenant
            while(True):
                #Get user input for the Role Name
                role_name = input("Enter the role Name: ")

                if not role_name.strip():  # Check if tenant_title is empty or contains only whitespace
                    raise ValueError("Role name cannot be empty.")

        
                if not re.match(pattern, role_name):  # Check if the tenant name contains only letters and numbers
                    raise ValueError("Role name can only contain uppercase and lowercase letters, spaces, and hyphens.")


                #Check for existence of Role
                check_role = session.scalars(select(Role).filter_by(role = role_name)).first()
                if check_role:
                    check_role_tenant = session.scalars(select(RoleTenant).filter(RoleTenant.roles_available == check_role.role_id,
                                                                         RoleTenant.tenant_id == check_tenant.tenant_id)).first()

                    if check_role_tenant:
                        raise ValueError("Role already Assigned")
                    
                    else:

                        #Create an object of RoleTenant
                        new_RoleTenant = RoleTenant(
                            tenant_id = check_tenant.tenant_id,
                            roles_available = check_role.role_id
                        )

                        #Add the object to the table
                        session.add(new_RoleTenant)


                else:
                    raise ValueError("Role does not Exist!!!")
                

                #Check if user want to add more
                flag = input("Add more Role:(Yes/No) \n")
                if flag != "Yes":
                    break
                
            session.commit()
            print("Role Added!!!")

        else:
            raise ValueError("Tenant does not Exist!!!")

    except ValueError:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()

