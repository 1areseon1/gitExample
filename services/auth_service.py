from repositories import employee_repo, tenant_repo

def authenticate(login: str, password: str):
    
    employee = employee_repo.get_by_login(login)
    if employee and employee.password == password:
        return {"role": "employee", "user": employee}

    
    tenant = tenant_repo.get_by_login(login)
    if tenant and tenant.password == password:
        return {"role": "tenant", "user": tenant}

    
    return None