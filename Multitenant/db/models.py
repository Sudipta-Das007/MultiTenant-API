from db.database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date, Float, BigInteger, Boolean, JSON, Enum
from sqlalchemy.orm import relationship


class TenantList(Base):
    __tablename__ = 'tenant_list'
    tenant_id = Column(Integer, primary_key=True, index=True)
    tenant_name = Column(String)
    tenant_phone_number= Column(BigInteger)
    owner = Column(String)
    owner_contact = Column(BigInteger)
    plot = Column(JSON)
    user_count = Column(Integer)
    connect_user = relationship('UserList', back_populates= 'connect_tenant')
    connect_role_tenant = relationship('RoleTenant', back_populates='connect_tenant')

class UserList(Base):
    __tablename__ = 'user_list'
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    user_phone_number = Column(BigInteger)
    tenant = Column(Integer, ForeignKey('tenant_list.tenant_id'))
    connect_tenant = relationship('TenantList', back_populates= 'connect_user')
    connect_user_roles = relationship('UserRole', back_populates='connect_users')
    connect_user_application = relationship('UserApplication', back_populates='connect_users')
    connect_login_id = relationship('LoginDetail', back_populates='connect_user_id')
    #connect_login_name = relationship('LoginDetail', back_populates='connect_user_name')

class LoginDetail(Base):
    __tablename__ = "login_detail"
    serial=Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey('user_list.user_id'))
    user_name = Column(String, unique=True)
    user_password = Column(String)
    connect_user_id = relationship('UserList', back_populates='connect_login_id')

class Application(Base):
    __tablename__ = 'application'
    application_id = Column(Integer, primary_key=True, index=True)
    application_name = Column(String)
    connect_application_permissions = relationship('ApplicationPermission', back_populates='connect_applications')
    connect_user_application = relationship('UserApplication', back_populates='connect_applications')

class Role(Base):
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    description = Column(String)
    connect_role_permission = relationship('RolePermission', back_populates='connect_roles')
    connect_user_roles = relationship('UserRole', back_populates='connect_roles')
    connect_role_tenant = relationship('RoleTenant', back_populates='connect_roles')

class Permission(Base):
    __tablename__ = 'permission'
    permission_id = Column(Integer, primary_key=True, index=True)
    permission = Column(String)
    description = Column(String)
    connect_role_permission = relationship('RolePermission', back_populates='connect_permissions')
    connect_application_permissions = relationship('ApplicationPermission', back_populates='connect_permissions')

class RolePermission(Base):
    __tablename__ = 'role_permission'
    serial=Column(Integer,primary_key=True)
    role_id = Column(Integer,ForeignKey("role.role_id"))
    permission_id = Column(Integer,ForeignKey("permission.permission_id"))
    connect_roles = relationship('Role', back_populates='connect_role_permission')
    connect_permissions = relationship('Permission', back_populates='connect_role_permission')

class UserRole(Base):
    __tablename__ = 'user_role'
    serial = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey('user_list.user_id'))
    role_id = Column(Integer, ForeignKey('role.role_id'))
    connect_users = relationship('UserList',back_populates='connect_user_roles')
    connect_roles = relationship('Role', back_populates='connect_user_roles')

class ApplicationPermission(Base):
    __tablename__ = 'application_permission'
    serial = Column(Integer,primary_key=True)
    application_id = Column(Integer,ForeignKey("application.application_id"))
    permission_id = Column(Integer,ForeignKey("permission.permission_id"))
    connect_permissions = relationship('Permission', back_populates='connect_application_permissions')
    connect_applications = relationship('Application', back_populates='connect_application_permissions')

class UserApplication(Base):
    __tablename__ = "user_application"
    serial = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("user_list.user_id"))
    application_id = Column(Integer,ForeignKey("application.application_id"))
    connect_users = relationship('UserList',back_populates='connect_user_application')
    connect_applications = relationship('Application', back_populates='connect_user_application')

class RoleTenant(Base):
    __tablename__="role_tenant"
    serial = Column(Integer,primary_key=True)
    tenant_id = Column(Integer,ForeignKey("tenant_list.tenant_id"))
    roles_available = Column(Integer,ForeignKey("role.role_id"))
    connect_tenant = relationship('TenantList', back_populates= 'connect_role_tenant')
    connect_roles = relationship('Role', back_populates='connect_role_tenant')