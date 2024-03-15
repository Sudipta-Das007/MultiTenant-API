from db.add import add_new_tenant, add_new_user, add_new_role, add_new_permission, add_new_application
from fastapi import HTTPException, Query
from fastapi import APIRouter, Depends, status
from auth.oauth2 import oauth2_scheme, get_current_user
from fastapi.responses import PlainTextResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional
from schemas.input_schemas import AddTenantDetail,AddUserDetail,AddRoleDetail,AddPermissionDetail,AddApplicationDetail

router = APIRouter(prefix="/add", tags= ["Add"])





#For practising the custom responses
'''
products = ['watch', 'camera', 'phone']

@router.get('/{id}', responses={
  200: {
    "content": {
      "text/html": {
        "example": "<div>Product</div>"
      }
    },
    "description": "Returns the HTML for an object"
  },
  404: {
    "content": {
      "text/plain": {
        "example": "Product not available"
      }
    },
    "description": "A cleartext error message"
  }
})
def get_product(id: int):
  if id > len(products):
    out = "Product not available"
    return PlainTextResponse(status_code=404, content=out, media_type="text/plain")
  else:
    product = products[id]
    out = f"""
    <head>
      <style>
      .product {{
        width: 500px;
        height: 30px;
        border: 2px inset green;
        background-color: lightblue;
        text-align: center;
      }}
      </style>
    </head>
    <div class="product">{product}</div>
    """
    return HTMLResponse(content=out, media_type="text/html")
'''




'''
    functions for add file
'''
@router.get("")
async def add():
    return {
        "tenant" : "http://127.0.0.1:8000/add/tenant",
        "user" : "http://127.0.0.1:8000/add/user",
        "role": "http://127.0.0.1:8000/add/role", 
        "permission":"http://127.0.0.1:8000/add/permission",
        "application":"http://127.0.0.1:8000/add/application"
    }



@router.post("/tenant")
async def add_tenant(tenant: AddTenantDetail,current_user: dict = Depends(get_current_user)):
    required_permission = "Add Tenant"

    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return {
    'response': add_new_tenant(tenant.tenant_title, tenant.tenant_phone_number, tenant.owner, tenant.owner_phone_number,tenant.floor_no, tenant.plot_no),
    'user': current_user
    }




@router.post("/user")
async def add_user(user:AddUserDetail,current_user: dict = Depends(get_current_user)):
    
    required_permission = "Add User"

    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']
    
    if tenant_id == 0 and not user.tenant_title:
        raise HTTPException(status_code=400, detail="Tenant name is required when tenant ID is 0.")
    
    if tenant_id != 0 and user.tenant_title:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No Permission to give tenant name")
    
    return {
    'response': add_new_user(tenant_id,user.user_title,user.user_phone_number,user.tenant_title),
    'user': current_user
    }



@router.post("/role")
async def add_role(role:AddRoleDetail,
                    current_user: dict = Depends(get_current_user)):
    
    required_permission = "Add Role"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    return {
        'response': add_new_role(role.new_role_name,role.new_role_description),
        'user': current_user
    }




@router.post("/permission")
async def add_permission(permission: AddPermissionDetail,
                            current_user: dict = Depends(get_current_user)):
    
    required_permission = "Add Permission"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    return {
        'response': add_new_permission(permission.new_permission_name,permission.new_permission_description),
        'user': current_user
    }



@router.post("/application")
async def add_application(application:AddApplicationDetail,current_user: dict = Depends(get_current_user)):
    
    required_permission = "Add Application"

    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    return {
        'response': add_new_application(application.new_application_name),
        'user': current_user
    }


