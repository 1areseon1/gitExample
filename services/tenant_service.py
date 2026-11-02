from repositories import tenant_repo

def create_tenant(last_name: str, first_name: str, phone: str, middle_name: str | None = None):
    if not last_name.strip():
        raise Exception("Фамилия не может быть пустой")
    
    if not first_name.strip():
        raise Exception("Имя не может быть пустым")
    
    if not phone.strip():
        raise Exception("Телефон не может быть пустым")

    tenants = tenant_repo.get_all()
    for t in tenants:
        if (t.last_name.lower() == last_name.lower() and
            t.first_name.lower() == first_name.lower() and
            (t.middle_name or "").lower() == (middle_name or "").lower()):
            raise Exception("Арендатор с такими ФИО уже существует")

    # Исправлено: передаем middle_name на 3-е место, phone на 4-е (как в репозитории)
    tenant_repo.create(last_name, first_name, middle_name, phone)
    return True