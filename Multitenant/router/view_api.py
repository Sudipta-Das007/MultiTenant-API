import re
import json
from db.view import view_tenant_details, view_all_users, view_all_roles, view_all_permissions, view_all_applications, view_all_users_under_tenant, view_all_roles_under_tenant, view_all_application_permissions,view_own_user_details
from fastapi import HTTPException, Query, Depends
from fastapi import APIRouter, status
from fastapi.responses import Response
from auth.oauth2 import oauth2_scheme, get_current_user
import redis


pattern = "^[a-zA-Z\s-]*$"


r = redis.Redis(host='localhost', port=6379)


router = APIRouter(prefix="/view",tags = ['View'])


TTL = 120

'''
    functions for view file
'''
@router.get("")
async def view():
    return {
        "tenants" : "http://127.0.0.1:8000/view/tenants",
        "users" : "http://127.0.0.1:8000/view/users",
        "roles": "http://127.0.0.1:8000/view/roles", 
        "permissions":"http://127.0.0.1:8000/view/permissions",
        "applications":"http://127.0.0.1:8000/view/applications",
        "users_under_tenant" : "http://127.0.0.1:8000/view/users_under_tenant",
        "roles_under_tenant" : "http://127.0.0.1:8000/view/roles_under_tenant",
        "application_permissions" : "http://127.0.0.1:8000/view/application_permissions",
        "own_details" : "http://127.0.0.1:8000/view/own_details"
    }


@router.get("/tenants")
async def view_tenant(current_user: dict = Depends(get_current_user)):
    required_permission = "View All tenants"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    required_permission = required_permission.replace(" ","").lower()

    
    cache_key = required_permission
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = view_tenant_details()
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,TTL)

        return {
        'response': data,
        'cache':'false',
        'user': current_user
        }
    
    else:
        return {
        'response': json.loads(cached_data),
        'key':cache_key,
        'cache':'true',
        'user': current_user
        }

    


@router.get("/users")
async def view_users(current_user: dict = Depends(get_current_user)):
    required_permission = "View All Users"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")


    required_permission = required_permission.replace(" ","").lower()

    cache_key = required_permission
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = view_all_users()
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,TTL)

        return {
        'response': data,
        'cache':'false',
        'user': current_user
        }
    
    else:
        return {
        'response': json.loads(cached_data),
        'key':cache_key,
        'cache':'true',
        'user': current_user
        }



@router.get("/roles")
async def view_roles(current_user: dict = Depends(get_current_user)):
    required_permission = "View All Role Detials"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    

    required_permission = required_permission.replace(" ","").lower()

    
    cache_key = required_permission
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = view_all_roles()
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,TTL)

        return {
        'response': data,
        'cache':'false',
        'user': current_user
        }
    
    else:
        return {
        'response': json.loads(cached_data),
        'key':cache_key,
        'cache':'true',
        'user': current_user
        }



@router.get("/permissions")
async def view_permissions(current_user: dict = Depends(get_current_user)):
    required_permission = "View All Permissions"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")


    required_permission = required_permission.replace(" ","").lower()

    
    cache_key = required_permission
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = view_all_permissions()
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,TTL)

        return {
        'response': data,
        'cache':'false',
        'user': current_user
        }
    
    else:
        return {
        'response': json.loads(cached_data),
        'key':cache_key,
        'cache':'true',
        'user': current_user
        }



@router.get("/applications")
async def view_applications(current_user: dict = Depends(get_current_user)):
    required_permission = "View Application Details"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    required_permission = required_permission.replace(" ","").lower()

    
    cache_key = required_permission
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = view_all_applications()
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,TTL)

        return {
        'response': data,
        'cache':'false',
        'user': current_user
        }
    
    else:
        return {
        'response': json.loads(cached_data),
        'key':cache_key,
        'cache':'true',
        'user': current_user
        }



@router.get("/users_under_tenant")
async def view_users_under_tenant(current_user: dict = Depends(get_current_user), tenant_name: str = Query(None, description="Tenant Name")):
    required_permission = "View All users present under a tenant"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']

    if tenant_id == 0 and not tenant_name:
        raise HTTPException(status_code=400, detail="Tenant name is required when tenant ID is 0.")
    
    if tenant_id != 0 and tenant_name:
        raise HTTPException(status_code=401, detail="No Permission to give tenant name")
    

    required_permission = required_permission.replace(" ","").lower()
    tenant_key = tenant_name.replace(" ","").lower()

    
    cache_key = required_permission+tenant_key
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = view_all_users_under_tenant(tenant_id, tenant_name)
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,TTL)

        return {
        'response': data,
        'cache':'false',
        'user': current_user
        }
    
    else:
        return {
        'response': json.loads(cached_data),
        'key':cache_key,
        'cache':'true',
        'user': current_user
        }



@router.get("/roles_under_tenant")
async def view_roles_under_tenant(current_user: dict = Depends(get_current_user),tenant_name: str = Query(None, description="Tenant Name")):
    required_permission = "View All roles available for a Tenant"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    tenant_id = current_user['tenant_id']

    if tenant_id == 0 and not tenant_name:
        raise HTTPException(status_code=400, detail="Tenant name is required when tenant ID is 0.")
    
    if tenant_id != 0 and tenant_name:
        raise HTTPException(status_code=400, detail="No Permission to give tenant name")

    required_permission = required_permission.replace(" ","").lower()
    tenant_key = tenant_name.replace(" ","").lower()

    
    cache_key = required_permission+tenant_key
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = view_all_roles_under_tenant(tenant_id, tenant_name)
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,TTL)

        return {
        'response': data,
        'cache':'false',
        'user': current_user
        }
    
    else:
        return {
        'response': json.loads(cached_data),
        'key':cache_key,
        'cache':'true',
        'user': current_user
        }




@router.get("/application_permissions")
async def view_application_permissions(current_user: dict = Depends(get_current_user),application_name: str = Query(..., description= "Application Name")):
    required_permission = "View All Permissions applicable for an Application"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    if not application_name.strip():
        raise HTTPException(status_code=400, detail="Application name cannot be empty.")
        
    if not re.match(pattern, application_name):
        raise HTTPException(status_code=400, detail="Application name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    

    required_permission = required_permission.replace(" ","").lower()
    application_key = application_name.replace(" ","").lower()

    
    cache_key = required_permission+application_key
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = view_all_application_permissions(application_name)
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,TTL)

        return {
        'response': data,
        'cache':'false',
        'user': current_user
        }
    
    else:
        return {
        'response': json.loads(cached_data),
        'key':cache_key,
        'cache':'true',
        'user': current_user
        }

    

@router.get("/own_details")
async def view_own_details(current_user: dict = Depends(get_current_user)):
    required_permission = "View Own Details"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    
    cache_key = current_user['login_username']
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = view_own_user_details(current_user['login_username'])
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,TTL)

        return {
        'response': data,
        'cache':'false',
        'user': current_user
        }
    
    else:
        return {
        'response': json.loads(cached_data),
        'key':cache_key,
        'cache':'true',
        'user': current_user
        }







