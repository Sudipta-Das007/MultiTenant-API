from pydantic import BaseModel
from typing import Optional
from enum import Enum



class AddTenantDetail(BaseModel):
    tenant_title: str
    tenant_phone_number: int
    owner: str
    owner_phone_number: int
    floor_no: int
    plot_no: int



class AddUserDetail(BaseModel):
    user_title: str
    user_phone_number: int
    tenant_title: Optional[str] = None



class AddRoleDetail(BaseModel):
    new_role_name: str
    new_role_description: str



class AddPermissionDetail(BaseModel):
    new_permission_name: str
    new_permission_description: str



class AddApplicationDetail(BaseModel):
    new_application_name: str



class UpdateTenantDetail(BaseModel):
    current_tenant_name: Optional[str] = None
    new_tenant_name: str
    tenant_phone_number: int
    owner: str
    owner_phone_number: int
    assign_revoke: Optional[int] = None
    floor_no: Optional[int] = None
    plot_no: Optional[int] = None
    plot_index: Optional[int] = None



class UpdateUserDetail(BaseModel):
    current_user_name: str
    user_id: int
    new_user_name: str
    user_phone_number: int



class UpdateOwnDetail(BaseModel):
    new_user_name: str
    user_phone_number: int



class UpdateUserTenant(BaseModel):
    user_name: str
    user_id: int
    new_tenant: int



class UpdateUserRole(BaseModel):
    user_name: str
    user_id: int
    assign_revoke: int
    new_role_id: Optional[int] = None



class UpdateRolePermission(BaseModel):
    role_name: str
    assign_revoke: int
    permission_id: int



class UpdateUserApplication(BaseModel):
    user_name: str
    user_id: int
    assign_revoke: int
    application_id: int
    replacing_application_id: Optional[int] = None


class UpdateRoleTenant(BaseModel):
    tenant_name: str
    assign_revoke: int
    role_id: int
    replacing_role_id: Optional[int] = None


class UpdateApplicationPermission(BaseModel):
    application_name: str
    assign_revoke: int
    permission_id: int



class Confirmation(str,Enum):
    YES="yes"
    NO="no"



class DeleteTenant(BaseModel):
    tenant_name: str
    confirmation: Confirmation



class DeleteUser(BaseModel):
    user_name: str
    user_id: int
    confirmation: Confirmation



class DeleteRole(BaseModel):
    role_name: str
    confirmation: Confirmation



class DeletePermission(BaseModel):
    permission_name: str
    confirmation: Confirmation



class DeleteApplication(BaseModel):
    application_name: str
    confirmation: Confirmation



class SetupLogin(BaseModel):
    user_title: str
    user_id: int
    login_username: str
    password: str


class ChangeOwnUsername(BaseModel):
    password: str
    new_username: str


class ChangeUserUsername(BaseModel):
    login_username: str
    new_username: str


class ChangeOwnPassword(BaseModel):
    current_password: str
    new_password: str



class ChangeUserPassword(BaseModel):
    login_username: str
    new_password: str



class DeleteLoginDetails(BaseModel):
    user_title: str
    user_id: int
    confirmation: Confirmation


