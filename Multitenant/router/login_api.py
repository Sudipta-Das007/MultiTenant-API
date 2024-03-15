from db.login import set_username_password,change_my_password, change_specific_user_password,delete_username_password,change_login_username,change_own_login_username
from fastapi import Query, HTTPException
from fastapi import APIRouter, Depends, status
from auth.oauth2 import oauth2_scheme, get_current_user
from schemas.input_schemas import SetupLogin, ChangeOwnUsername, ChangeUserUsername, ChangeOwnPassword, ChangeUserPassword, DeleteLoginDetails



router = APIRouter(prefix="/login", tags = ['Login'])



'''
    functions for login file
'''
@router.post("/setup_username_password")
async def setup_username_password(setup:SetupLogin,
                                  current_user: dict = Depends(get_current_user)):
    
    required_permission = "Set login details for users"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']
    
    return {
        'response': set_username_password(tenant_id, 
                                          setup.user_title, 
                                          setup.user_id, 
                                          setup.login_username, 
                                          setup.password),
        'user': current_user
    }




@router.patch("/change_own_login_user_name")
async def change_own_login_user_name(user_detail:ChangeOwnUsername,
                                     current_user: dict = Depends(get_current_user)):
    
    required_permission = "Change Own Username"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    login_username = current_user['login_username']

    return {
        'response': change_own_login_username(login_username,user_detail.password,user_detail.new_username),
        'user': current_user
    }




@router.patch("/change_login_user_name")
async def change_login_user_name(user_detail:ChangeUserUsername,
                                 current_user: dict = Depends(get_current_user)):
    
    required_permission = "Change user username"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']

    return {
        'response': change_login_username(tenant_id,user_detail.login_username,user_detail.new_username),
        'user': current_user
    }




@router.patch("/change_own_password")
async def change_own_password(password:ChangeOwnPassword,
                              current_user: dict = Depends(get_current_user)):

    required_permission = "Change Own Password"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    login_username = current_user['login_username']

    return {
        'response': change_my_password(login_username,password.current_password,password.new_password),
        'user': current_user
    }




@router.patch("/change_user_password")
async def change_user_password(password:ChangeUserPassword,
                               current_user: dict = Depends(get_current_user)):
    
    required_permission = "Change user password"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']

    return {
        'response': change_specific_user_password(tenant_id,password.login_username,password.new_password),
        'user': current_user
    }




@router.delete("/delete_login_details")
async def  delete_login_details(login_details: DeleteLoginDetails,
                                current_user: dict = Depends(get_current_user)):
    
    required_permission = "Delete login details"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']

    return {
        'response': delete_username_password(tenant_id,login_details.user_title,login_details.user_id,login_details.confirmation),
        'user': current_user
    }





