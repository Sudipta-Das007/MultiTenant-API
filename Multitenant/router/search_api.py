import re
from db.search import search_specific_tenant,search_specific_user, search_specific_role, search_specific_permission
from fastapi import HTTPException, Query
from fastapi import APIRouter, Depends, status
from auth.oauth2 import oauth2_scheme, get_current_user
import redis
import json


pattern = "^[a-zA-Z\s-]*$"


router = APIRouter(prefix="/search",tags = ['Search'])


r = redis.Redis(host='localhost', port=6379)


'''
    functions for search file
'''
@router.get("")
async def search():
    return {
        "tenant" : "http://127.0.0.1:8000/search/tenant",
        "user" : "http://127.0.0.1:8000/search/user",
        "role": "http://127.0.0.1:8000/search/role", 
        "permission":"http://127.0.0.1:8000/search/permission",
    }



@router.get("/tenant")
async def search_tenant(current_user: dict = Depends(get_current_user),tenant_name: str = Query(..., description= "Tenant Name")):
    required_permission = "Search tenant"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    if not tenant_name.strip():
        raise HTTPException(status_code=400, detail="Tenant name cannot be empty.")
        
    if not re.match(pattern, tenant_name):
        raise HTTPException(status_code=400, detail="Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")

    ttl = 60
    cache_key = required_permission.replace(" ","").lower()+tenant_name.replace(" ","").lower()
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = search_specific_tenant(tenant_name)
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,ttl)

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



@router.get("/user")
async def search_user(current_user: dict = Depends(get_current_user),user_name: str = Query(..., description= "User Name")):
    required_permission = "Search Users"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    tenant_id = current_user['tenant_id']
    
    if not user_name.strip():
        raise HTTPException(status_code=400, detail="User name cannot be empty.")
        
    if not re.match(pattern, user_name):
        raise HTTPException(status_code=400, detail="User name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    
    ttl = 60
    cache_key = required_permission.replace(" ","").lower()+user_name.replace(" ","").lower()
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = search_specific_user(tenant_id,user_name)
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,ttl)

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



@router.get("/role")
async def search_role(current_user: dict = Depends(get_current_user),role_name: str = Query(..., description= "Role Name")):
    required_permission = "Search Role"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    if not role_name.strip():
        raise HTTPException(status_code=400, detail="Role name cannot be empty.")
        
    if not re.match(pattern, role_name):
        raise HTTPException(status_code=400, detail="Role name can only contain uppercase and lowercase letters, spaces, and hyphens.")

    ttl = 60
    cache_key = required_permission.replace(" ","").lower()+role_name.replace(" ","").lower()
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = search_specific_role(role_name)
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,ttl)

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


    
    

'''
#Done Using Path Parameters
@router.get("/role/{role_name}")
async def search_role(role_name):
    if not role_name.strip():
        raise HTTPException(status_code=400, detail="Role name cannot be empty.")
        
    if not re.match(pattern, role_name):
        raise HTTPException(status_code=400, detail="Role name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    
    return search_specific_role(role_name)'''
    




@router.get("/permission")
async def search_permission(current_user: dict = Depends(get_current_user),permission_name: str = Query(..., description= "Permission Name")):
    required_permission = "Search Permissions"
    
    if required_permission not in current_user['permissions']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    if not permission_name.strip():
        raise HTTPException(status_code=400, detail="Permission name cannot be empty.")
        
    if not re.match(pattern, permission_name):
        raise HTTPException(status_code=400, detail="Permission name can only contain uppercase and lowercase letters, spaces, and hyphens.")

    ttl = 60
    cache_key = required_permission.replace(" ","").lower()+permission_name.replace(" ","").lower()
    cached_data = r.get(cache_key)

    if cached_data is None:
        data = search_specific_permission(permission_name)
        r.set(cache_key,json.dumps(data)) #set cache
        r.expire(cache_key,ttl)

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


'''
#Done Using Path Parameters
@router.get("/permission/{permission_name}")
async def search_permission(permission_name):
    if not permission_name.strip():
        raise HTTPException(status_code=400, detail="Permission name cannot be empty.")
        
    if not re.match(pattern, permission_name):
        raise HTTPException(status_code=400, detail="Permission name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    
    return search_specific_permission(permission_name)
    
'''






