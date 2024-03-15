from db.update import update_specific_tenant, update_user, transfer_user, assign_revoke_role, add_remove_permission_from_role, assign_revoke_user_application, update_own_details, assign_revoke_role_tenant, update_application_permission
from fastapi import HTTPException, Query
from fastapi import APIRouter, Depends, status
from auth.oauth2 import oauth2_scheme, get_current_user
from schemas.input_schemas import UpdateTenantDetail, UpdateUserDetail, UpdateOwnDetail, UpdateUserTenant, UpdateUserRole, UpdateUserApplication, UpdateRolePermission, UpdateRoleTenant, UpdateApplicationPermission




router = APIRouter(prefix="/update", tags=["Update"])




'''
    functions for update file
'''
@router.get("")
async def update():
    return {
        "tenant" : "http://127.0.0.1:8000/update/tenant",
        "user_details" : "http://127.0.0.1:8000/update/user_details",
        "own_user_details" : "http://127.0.0.1:8000/update/own_user_details",
        "change_user_tenant" : "http://127.0.0.1:8000/update/change_user_tenant",
        "role_of_user": "http://127.0.0.1:8000/update/role_of_user", 
        "role_permission":"http://127.0.0.1:8000/update/role_permission",
        "user_application_access":"http://127.0.0.1:8000/update/user_application_access",
        "role_available_for_tenant": "http://127.0.0.1:8000/update/role_available_for_tenant",
        "application_permissions" : "http://127.0.0.1:8000/update/application_permissions"
    }




@router.put("/tenant")
async def update_tenant(tenant_details: UpdateTenantDetail,
                        current_user: dict = Depends(get_current_user)):
    
    required_permission = "Update Tenant"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']

    if tenant_id == 0 and not tenant_details.current_tenant_name:
        raise HTTPException(status_code=400, detail="Tenant name is required when tenant ID is 0.")
    
    if tenant_id != 0 and tenant_details.current_tenant_name:
        raise HTTPException(status_code=400, detail="No Permission to give tenant name")
    
    if tenant_id != 0 and tenant_details.assign_revoke and tenant_details.floor_no and tenant_details.plot_no and tenant_details.plot_index:
        raise HTTPException(status_code=400, detail="No Permission to Alter floor and plot")
    
    return {
        'response': update_specific_tenant(tenant_id,
                                           tenant_details.new_tenant_name,
                                           tenant_details.tenant_phone_number,
                                           tenant_details.owner,
                                           tenant_details.owner_phone_number,
                                           tenant_details.assign_revoke,
                                           tenant_details.current_tenant_name,
                                           tenant_details.floor_no,
                                           tenant_details.plot_no,
                                           tenant_details.plot_index),
        'user': current_user
    }




@router.patch("/user_details")
async def update_user_details(user_details: UpdateUserDetail,
                              current_user: dict = Depends(get_current_user)):
    
    required_permission = "Update User"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']
    
    return {
        'response': update_user(tenant_id,
                                user_details.current_user_name,
                                user_details.user_id,
                                user_details.new_user_name,
                                user_details.user_phone_number),
        'user': current_user
    }



@router.patch("/own_user_details")
async def update_own_user_details(own_detail:UpdateOwnDetail,
                                  current_user: dict = Depends(get_current_user)):
    
    required_permission = "Update Own User Details"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    login_user_name = current_user['login_username']
    
    return {
        'response': update_own_details(login_user_name,own_detail.new_user_name,own_detail.user_phone_number),
        'user': current_user
    }





@router.patch("/change_user_tenant")
async def update_change_user_tenant(user_details: UpdateUserTenant,
                                    current_user: dict = Depends(get_current_user)):
    
    required_permission = "Transfer User"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return {
        'response': transfer_user(user_details.user_name,user_details.user_id,user_details.new_tenant),
        'user': current_user
    }




@router.put("/role_of_user")
async def update_role_of_user(user_role:UpdateUserRole,
                              current_user: dict = Depends(get_current_user)):
    
    required_permission = "Assign/Revoke Role to Users"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']

    if user_role.assign_revoke == 2 and user_role.new_role_id:
        raise HTTPException(status_code=400, detail="Role ID not needed when revoking role from User")
    
    if user_role.assign_revoke !=2 and user_role.new_role_id is None:
        raise HTTPException(status_code=400, detail="Role ID is needed when assigning or replacing role from User")
    
    return {
        'response': assign_revoke_role(tenant_id,user_role.user_name,user_role.user_id,user_role.assign_revoke,user_role.new_role_id),
        'user': current_user
    }




@router.put("/role_permission")
async def update_role_permission(role_permission: UpdateRolePermission,
                                 current_user: dict = Depends(get_current_user)):
    
    required_permission = "Link/Unlink Role Permissions"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return {
        'response': add_remove_permission_from_role(role_permission.role_name,role_permission.assign_revoke,role_permission.permission_id),
        'user': current_user
    }




@router.put("/user_application_access")
async def update_user_application_access(user_application: UpdateUserApplication,
                                         current_user: dict = Depends(get_current_user)):
    
    required_permission = "Add Application Access For Users"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']

    if user_application.assign_revoke == 3 and user_application.replacing_application_id is None:
        raise HTTPException(status_code=400, detail="Replacing Application ID cannot be None")
    
    if user_application.assign_revoke != 3 and user_application.replacing_application_id is not None:
        raise HTTPException(status_code=400, detail="Replacing Application ID is not needed while assiging or removing Application Access")

    return {
        'response': assign_revoke_user_application(tenant_id,
                                                   user_application.user_name,
                                                   user_application.user_id,
                                                   user_application.assign_revoke,
                                                   user_application.application_id,
                                                   user_application.replacing_application_id),
        'user': current_user
    }





@router.put("/role_available_for_tenant")
async def update_role_available_for_tenant(role_tenant:UpdateRoleTenant,
                                           current_user: dict = Depends(get_current_user)):
    
    required_permission = "Update Roles Available For Assignment"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    if role_tenant.assign_revoke == 3 and role_tenant.replacing_role_id is None:
        raise HTTPException(status_code=400, detail="Replacing Role ID cannot be None")
    
    if role_tenant.assign_revoke != 3 and role_tenant.replacing_role_id is not None:
        raise HTTPException(status_code=400, detail="Replacing Role ID is not needed while assiging or removing Application Access")

    return {
        'response': assign_revoke_role_tenant(role_tenant.tenant_name,role_tenant.assign_revoke,role_tenant.role_id,role_tenant.replacing_role_id),
        'user': current_user
    }




@router.put("/application_permissions")
async def update_application_permissions(application_permission: UpdateApplicationPermission,
                                         current_user: dict = Depends(get_current_user)):

    required_permission = "Add User"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return {
        'response': update_application_permission(application_permission.application_name,
                                                  application_permission.assign_revoke,
                                                  application_permission.permission_id),
        'user': current_user
    }



