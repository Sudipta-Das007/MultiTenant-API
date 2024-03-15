import pytest
from unittest.mock import patch
from db.login import set_username_password,delete_username_password
from db.read import view_all_users, view_all_applications, view_all_permissions, view_all_roles, view_tenant_details, view_all_application_permissions, view_all_users_under_tenant, view_all_roles_under_tenant, view_own_user_details
from db.database import session
from db.models import TenantList
from sqlalchemy import select


def test_view_tenant_details(capsys):

    view_tenant_details()

    captured = capsys.readouterr()

    tenant_data = session.scalars(select(TenantList).filter_by(tenant_name = "Test Tenant")).first()

    assert "Tenant ID 3   Tenant: Test Tenant  Phone Number: 8410257963" in captured.out
    assert "Owner Name: New Test Owner Owner Contact: 8410257024" in captured.out
    assert f"Total users of this Tenant: {tenant_data.user_count}" in captured.out
    assert "Plots Rented: " in captured.out
    assert "{'Floor': 2, 'Plot No.': 3}" in captured.out




def test_view_all_users(capsys):

    view_all_users()

    captured = capsys.readouterr()

    assert "User ID 5   User: Test Dummy Owner  Phone Number: 9876543210" in captured.out
    assert "Tenant ID: 3 Tenant Name: Test Tenant" in captured.out





def test_view_all_roles(capsys):

    view_all_roles()
    captured = capsys.readouterr()
    assert "Role ID 8   Role: No Deleting  Role Description: Testing" in captured.out





def test_view_all_permissions(capsys):

    view_all_permissions()
    captured = capsys.readouterr()
    assert "Permission ID 2   Permission: No Deleting  Permission Description: Testing EveryThing" in captured.out





def test_view_all_applications(capsys):

    view_all_applications()
    captured = capsys.readouterr()
    assert "Application ID 7   Application Name: Test Beta" in captured.out





def test_all_users_under_tenant(capsys):
    #case owner
    with patch('builtins.input', return_value = "Test Tenant"):
        view_all_users_under_tenant(0)

    captured = capsys.readouterr()

    assert "TENANT DETAILS:" in captured.out
    assert "Tenant ID: 3 Tenant Name: Test Tenant" in captured.out
    assert "User DETAILS:" in captured.out
    assert "User ID 5   User: Test Dummy Owner  Phone Number: 9876543210" in captured.out

    #Empty Tenant
    with patch('builtins.input', return_value = ""):
        view_all_users_under_tenant(0)

    captured = capsys.readouterr()

    assert "Tenant name cannot be empty." in captured.out

    #Special Charater Input
    with patch('builtins.input', return_value = "Test Ten@nt"):
        view_all_users_under_tenant(0)

    captured = capsys.readouterr()

    assert "Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens." in captured.out

    #case tenant
    view_all_users_under_tenant(3)

    captured = capsys.readouterr()

    assert "TENANT DETAILS:" in captured.out
    assert "Tenant ID: 3 Tenant Name: Test Tenant" in captured.out
    assert "User DETAILS:" in captured.out
    assert "User ID 5   User: Test Dummy Owner  Phone Number: 9876543210" in captured.out

    #case nonexistant tenant
    view_all_users_under_tenant(-1)

    captured = capsys.readouterr()

    assert "No such Tenant is present in our records." in captured.out
    




def test_all_roles_under_tenant(capsys):
    #case owner
    with patch('builtins.input', return_value = "Testing-Tenant"):
        assert view_all_roles_under_tenant(0) == None

    
    captured = capsys.readouterr()

    assert "TENANT DETAILS:" in captured.out
    assert "Tenant ID: 68 Tenant Name: Testing-Tenant" in captured.out
    assert "No Roles Associated" in captured.out


    #Empty Tenant
    with patch('builtins.input', return_value = ""):
        view_all_users_under_tenant(0)

    captured = capsys.readouterr()

    assert "Tenant name cannot be empty." in captured.out

    #Special Charater Input
    with patch('builtins.input', return_value = "Test Ten@nt"):
        view_all_users_under_tenant(0)

    captured = capsys.readouterr()

    assert "Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens." in captured.out



    #case tenant
    view_all_roles_under_tenant(3)

    captured = capsys.readouterr()
    assert "TENANT DETAILS:" in captured.out
    assert "Tenant ID: 3 Tenant Name: Test Tenant" in captured.out
    assert "Roles Associated:" in captured.out
    assert "Role ID 8   Role: No Deleting  Role Description: Testing" in captured.out
    assert "Role ID 25   Role: Admin  Role Description: Testing" in captured.out


    #case nonexistant tenant
    view_all_roles_under_tenant(55)

    captured = capsys.readouterr()

    assert "No such Tenant is present in our records." in captured.out





def test_view_all_application_permissions(capsys):

    with patch('builtins.input', return_value="Test Beta"):
        view_all_application_permissions()

    captured = capsys.readouterr()

    assert "Application DETAILS:" in captured.out
    assert "Application ID: 7 application Name: Test Beta" in captured.out


    #Empty Tenant
    with patch('builtins.input', return_value = ""):
        view_all_application_permissions()

    captured = capsys.readouterr()

    assert "Application name cannot be empty." in captured.out

    #Special Charater Input
    with patch('builtins.input', return_value = "Test Ten@nt"):
        view_all_application_permissions()

    captured = capsys.readouterr()

    assert "Application name can only contain uppercase and lowercase letters, spaces, and hyphens." in captured.out




#Setup for testing view own details
@pytest.fixture(scope="class")
def setup_login_database():
    #setup process
    input_values = ["Test Dummy Owner",5,"TDO","789"]
    tenant_id = 0

    with patch('builtins.input', side_effect = input_values):
        set_username_password(tenant_id)

    yield

    #teardownprocess
    input_values = ["Test Dummy Owner",5,"yes"]
    
    with patch('builtins.input', side_effect = input_values):
        delete_username_password(tenant_id)

def test_view_own_details(setup_login_database,capsys):

    view_own_user_details("TDO")

    captured = capsys.readouterr()

    assert "User ID: 5" in captured.out
    assert "User Name: Test Dummy Owner" in captured.out
    assert "User Phone Number: 9876543210" in captured.out


