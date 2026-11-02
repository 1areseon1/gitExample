from repositories import contract_repo, room_repo, tenant_repo, employee_repo

def create_contract(room_id: int, tenant_id: int, employee_id: int, start_date: str, end_date: str, cost: float):

    room = room_repo.get_by_id(room_id)
    if not room:
        raise Exception("Помещение не найдено")
        
    tenant = tenant_repo.get_by_id(tenant_id)
    if not tenant:
        raise Exception("Арендатор не найден")
        
    employee = employee_repo.get_by_id(employee_id)
    if not employee:
        raise Exception("Сотрудник не найден")

    if room.status == "занято":
        raise Exception("Помещение занято, нельзя оформить договор")


    if cost <= 0:
        raise Exception("Стоимость должна быть больше нуля")

 
    contract_repo.create(room_id, tenant_id, employee_id, start_date, end_date, cost)
    

    room_repo.update(room.room_id, room.number, room.type, room.area, "занято")
    
    return True