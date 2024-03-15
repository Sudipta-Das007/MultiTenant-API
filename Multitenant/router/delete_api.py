from db.delete import delete_specific_user, delete_specific_tenant, delete_specific_role, delete_specific_permission, delete_specific_application
from fastapi import Query, HTTPException
from fastapi import APIRouter, Depends, status
from auth.oauth2 import oauth2_scheme, get_current_user
from schemas.input_schemas import DeleteTenant, DeleteUser, DeleteRole, DeletePermission, DeleteApplication
from enum import Enum


router = APIRouter(prefix="/delete", tags = ['Delete'])


'''
    functions for delete file
'''
@router.get("")
async def delete():
    return {
        "tenant" : "http://127.0.0.1:8000/delete/tenant",
        "user" : "http://127.0.0.1:8000/delete/user",
        "role": "http://127.0.0.1:8000/delete/role", 
        "permission":"http://127.0.0.1:8000/delete/permission",
        "application":"http://127.0.0.1:8000/delete/application"
    }



@router.delete("/tenant")
async def delete_tenant(tenant:DeleteTenant,
                        current_user: dict = Depends(get_current_user)):
    
    required_permission = "Delete Tenant"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return {
        'response': delete_specific_tenant(tenant.tenant_name,tenant.confirmation),
        'user': current_user
    }



@router.delete("/user")
async def delete_user(user:DeleteUser,
                      current_user: dict = Depends(get_current_user)):
    
    required_permission = "Delete User"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']

    return {
        'response': delete_specific_user(tenant_id,user.user_name,user.user_id,user.confirmation),
        'user': current_user
    }




@router.delete("/role")
async def delete_role(role:DeleteRole,
                      current_user: dict = Depends(get_current_user)):
    
    required_permission = "Delete Role"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return {
        'response': delete_specific_role(role.role_name,role.confirmation),
        'user': current_user
    }




@router.delete("/permission")
async def delete_permission(permission: DeletePermission,
                            current_user: dict = Depends(get_current_user)):
    
    required_permission = "Delete Permission"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return {
        'response': delete_specific_permission(permission.permission_name,permission.confirmation),
        'user': current_user
    }




@router.delete("/application")
async def delete_application(application: DeleteApplication,
                             current_user: dict = Depends(get_current_user)):
    
    required_permission = "Delete Application"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return {
        'response': delete_specific_application(application.application_name,application.confirmation),
        'user': current_user
    }




