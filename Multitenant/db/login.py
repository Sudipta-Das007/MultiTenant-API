from db.database import session
from db.models import UserList,LoginDetail, UserApplication
import re
from sqlalchemy import select
from fastapi import HTTPException

pattern = "^[a-zA-Z\s-]*$"



#Set Username Password for a User
def set_username_password(tenant_id, user_title, uid, login_username, password): 
    try:
        if not user_title.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="User name cannot be empty.")

        
        if not re.match(pattern, user_title):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")


        if(tenant_id == 0):
            user_data = session.scalars(select(UserList).filter_by(user_name = user_title)).all()

        else:
            user_data = session.scalars(select(UserList).filter(UserList.user_name == user_title, UserList.tenant == tenant_id)).all()
            
        if user_data:
            z=0
            for user in user_data:
                #print(user.user_id)
                if user.user_id == uid :
                    if not login_username.strip():  # Check if tenant_title is empty or contains only whitespace
                        raise HTTPException(status_code=400, detail="LogIn Username cannot be empty.")
                            
        
                    check_username = session.scalars(select(LoginDetail).filter_by(user_name = login_username)).first()
                    if check_username:
                            raise HTTPException(status_code=400, detail="Username Already Exists!!!")
                            
                    else:
                        new_user = LoginDetail(
                            user_id = uid,
                            user_name= login_username,
                            user_password = password
                            )
                        # Add the new tenant object to the session
                        session.add(new_user)
                            
                    # Commit the changes to the database
                    session.commit()
                    z=1
                    return {
                    'message': "Login Details Added Successfully"
                    }


            if z==0:
                raise HTTPException(status_code=400, detail="Wrong User ID!!!")
        else:
            raise HTTPException(status_code=400, detail="No User with the given username")
        
    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()





#Change Own login username
def change_own_login_username(user_name,password_input, new_login_username):
    try:
        password = session.scalars(select(LoginDetail).filter_by(user_name = user_name)).first()

        if password_input == password.user_password:
            user_details = session.scalars(select(LoginDetail).filter_by(user_name = user_name)).first()

            if not new_login_username.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="LogIn Username cannot be empty.")
                    

            check_username = session.scalars(select(LoginDetail).filter_by(user_name = new_login_username)).first()
            if check_username:
                    raise HTTPException(status_code=400, detail="Username Already Exists!!!")
                    
            else:
                user_details.user_name = new_login_username
                    
                # Commit the changes to the database
                session.commit()
                return {
                'message': "Username Changed Successfully"
                }
        else:
            raise HTTPException(status_code=400, detail="Wrong Password!!!")

            
    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()





#Change another user's password
def change_login_username(tenant_id,username,new_username):
    try:
        if not username.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="LogIn Username cannot be empty.")
            
        
        if(tenant_id == 0):
            login = session.execute(select(LoginDetail,UserList).filter(LoginDetail.user_name == username).join(UserList,UserList.user_id == LoginDetail.user_id)).first()
            if login is not None:
                _,user = login
                tenant_id = user.tenant

        else:
            login = session.execute(select(LoginDetail,UserList).filter(LoginDetail.user_name == username).join(UserList,UserList.user_id == LoginDetail.user_id)).first()
        
        
        if login is not None:
            password,user = login
            if password and user.tenant == tenant_id:
                if not new_username.strip():  # Check if tenant_title is empty or contains only whitespace
                    raise HTTPException(status_code=400, detail="Login Username cannot be empty.")
                
                password.user_name = new_username
                session.commit()
                return{
                        'message': "Login Username Updated!!!"
                    }
            else:
                raise HTTPException(status_code=400, detail="Username Doesnot Exist!!!")
        else:
            raise HTTPException(status_code=400, detail="Username Doesnot Exist!!!")
        
    except HTTPException:
        raise


    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()






#change the function name
#Change Own Password
def change_my_password(username,password_input,new_password):
    try:
        password = session.scalars(select(LoginDetail).filter_by(user_name = username)).first()
        if not password_input.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="Password cannot be empty.")
            
        if password_input == password.user_password:
            if not new_password.strip():  # Check if tenant_title is empty or contains only whitespace
                raise HTTPException(status_code=400, detail="Password cannot be empty.")
                
            password.user_password = new_password
            session.commit()
            return {
                    'message': "Password Updated!!!"
                    }

        else:
            raise HTTPException(status_code=400, detail="Wrong Password!!!")

    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()





#Change another user's password
def change_specific_user_password(tenant_id,username,new_password):
    try:
        if not username.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="LogIn Username cannot be empty.")
            
        
        if(tenant_id == 0):
            login = session.execute(select(LoginDetail,UserList).filter(LoginDetail.user_name == username).join(UserList,UserList.user_id == LoginDetail.user_id)).first()
            if login is not None:
                _,user = login
                tenant_id = user.tenant

        else:
            login = session.execute(select(LoginDetail,UserList).filter(LoginDetail.user_name == username).join(UserList,UserList.user_id == LoginDetail.user_id)).first()
        
        
        if login is not None:
            password,user = login
            if password and user.tenant == tenant_id:
                if not new_password.strip():  # Check if tenant_title is empty or contains only whitespace
                    raise HTTPException(status_code=400, detail="Password cannot be empty.")
                
                password.user_password = new_password
                session.commit()
                return{
                        'message': "Password Updated!!!"
                    }
            else:
                raise HTTPException(status_code=400, detail="Username Doesnot Exist!!!")
        else:
            raise HTTPException(status_code=400, detail="Username Doesnot Exist!!!")
        
    except HTTPException:
        raise


    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()





def delete_username_password(tenant_id,user_title,uid,confirmation):
    try:
        if not user_title.strip():  # Check if tenant_title is empty or contains only whitespace
            raise HTTPException(status_code=400, detail="User name cannot be empty.")

        
        if not re.match(pattern, user_title):  # Check if the tenant name contains only letters and numbers
            raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")


        if(tenant_id == 0):
            user_data = session.scalars(select(UserList).filter_by(user_name = user_title)).all()

        else:
            user_data = session.scalars(select(UserList).filter(UserList.user_name == user_title, UserList.tenant == tenant_id)).all()
            
        if user_data:
            z=0
            for user in user_data:
                #print(user.user_id)
                if user.user_id == uid :
                    login_detail=session.scalars(select(LoginDetail).filter(LoginDetail.user_id == uid)).first()
                    if login_detail:
                        if confirmation.lower() == "yes":
                            session.delete(login_detail)
                            # Commit the changes to the database
                            session.commit()
                            z=1
                            # Return a success message
                            return {
                                'message': "Login Details Deleted Successfully"
                                }
                        else:
                            raise HTTPException(status_code=400, detail="Deletion Cancelled!!!")
                    else:
                        raise HTTPException(status_code=404, detail="User has no Login Detail!!!")
            if z==0:
                raise HTTPException(status_code=400, detail="Wrong User ID!!!")
        else:
            raise HTTPException(status_code=404, detail="No User with the given username")
        
    except HTTPException:
        raise

    except Exception as e:
        # Print an error message if there's an exception
        print(f"Error: {e}")

    finally:
        #close the session
        session.close()






