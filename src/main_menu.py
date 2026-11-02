import sys
import os
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repositories import room_repo, tenant_repo, employee_repo, contract_repo, notification_repo
from services import tenant_service, contract_service, auth_service

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "rental.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def reboot_db():
    print("\nПересоздание базы данных...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("База данных успешно сброшена к исходному состоянию.")
    except Exception as e:
        print(f"Ошибка при сбросе БД: {e}")

# --- ФУНКЦИИ МЕНЮ (АДМИНИСТРАТОР) ---
def rooms_menu():
    while True:
        print("\n--- ПОМЕЩЕНИЯ ---")
        print("1. Показать все")
        print("2. Добавить")
        print("3. Изменить статус")
        print("4. Удалить")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            for r in room_repo.get_all():
                print(f"ID: {r.room_id} | Номер: {r.number} | Тип: {r.type} | Площадь: {r.area} | Статус: {r.status}")
        elif choice == "2":
            try:
                number = input("Номер: ")
                rtype = input("Тип: ")
                area = float(input("Площадь: "))
                status = input("Статус (свободно/занято): ")
                room_repo.create(number, rtype, area, status)
                print("Помещение добавлено.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "3":
            try:
                room_id = int(input("ID помещения для изменения: "))
                room = room_repo.get_by_id(room_id)
                if not room:
                    print("Помещение не найдено.")
                    continue
                new_status = input(f"Новый статус (текущий: {room.status}): ")
                room_repo.update(room_id, room.number, room.type, room.area, new_status)
                print("Статус обновлен.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "4":
            try:
                room_id = int(input("ID помещения для удаления: "))
                room_repo.delete(room_id)
                print("Помещение удалено.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break

def tenants_menu():
    while True:
        print("\n--- АРЕНДАТОРЫ ---")
        print("1. Показать всех")
        print("2. Добавить")
        print("3. Удалить")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            for t in tenant_repo.get_all():
                print(f"ID: {t.tenant_id} | {t.last_name} {t.first_name} {t.middle_name or ''} | Тел: {t.phone} | Логин: {t.login}")
        elif choice == "2":
            try:
                last_name = input("Фамилия: ")
                first_name = input("Имя: ")
                middle_name = input("Отчество (Enter - пропустить): ")
                phone = input("Телефон: ")
                login = input("Логин: ")
                password = input("Пароль: ")
                if middle_name.strip() == "": middle_name = None
                tenant_service.create_tenant(last_name, first_name, phone, login, password, middle_name)
                print("Арендатор добавлен.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "3":
            try:
                tid = int(input("ID арендатора для удаления: "))
                tenant_repo.delete(tid)
                print("Арендатор удален.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break

def employees_menu():
    while True:
        print("\n--- СОТРУДНИКИ ---")
        print("1. Показать всех")
        print("2. Добавить")
        print("3. Удалить")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            for e in employee_repo.get_all():
                print(f"ID: {e.employee_id} | {e.last_name} {e.first_name} {e.middle_name or ''} | Должность: {e.position} | Логин: {e.login}")
        elif choice == "2":
            try:
                last_name = input("Фамилия: ")
                first_name = input("Имя: ")
                middle_name = input("Отчество (Enter - пропустить): ")
                position = input("Должность: ")
                login = input("Логин: ")
                password = input("Пароль: ")
                if middle_name.strip() == "": middle_name = None
                employee_repo.create(last_name, first_name, position, login, password, middle_name)
                print("Сотрудник добавлен.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "3":
            try:
                eid = int(input("ID сотрудника для удаления: "))
                employee_repo.delete(eid)
                print("Сотрудник удален.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break

def contracts_menu():
    while True:
        print("\n--- ДОГОВОРЫ ---")
        print("1. Показать все")
        print("2. Оформить новый")
        print("3. Расторгнуть (удалить)")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            for c in contract_repo.get_all():
                print(f"ID: {c.contract_id} | Room ID: {c.room_id} | Tenant ID: {c.tenant_id} | Сумма: {c.cost}")
        
        elif choice == "2":
            print("\n--- ДОСТУПНЫЕ ПОМЕЩЕНИЯ (СВОБОДНО) ---")
            free_rooms = [r for r in room_repo.get_all() if r.status == "свободно"]
            if not free_rooms:
                print("Нет свободных помещений!")
                continue
            for r in free_rooms:
                print(f"ID: {r.room_id} | Номер: {r.number} | Тип: {r.type}")
            
            print("\n--- АРЕНДАТОРЫ ---")
            for t in tenant_repo.get_all():
                print(f"ID: {t.tenant_id} | {t.last_name} {t.first_name}")
            
            print("\n--- СОТРУДНИКИ ---")
            for e in employee_repo.get_all():
                print(f"ID: {e.employee_id} | {e.last_name} {e.first_name}")

            try:
                room_id = int(input("\nID помещения: "))
                tenant_id = int(input("ID арендатора: "))
                employee_id = int(input("ID сотрудника: "))
                start_date = input("Дата начала (ГГГГ-ММ-ДД): ")
                end_date = input("Дата окончания (ГГГГ-ММ-ДД): ")
                cost = float(input("Стоимость: "))
                contract_service.create_contract(room_id, tenant_id, employee_id, start_date, end_date, cost)
                print("Договор успешно создан.")
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == "3":
            try:
                cid = int(input("ID договора для расторжения: "))
                contract = contract_repo.get_by_id(cid)
                if not contract:
                    print("Договор с таким ID не найден.")
                    continue
                contract_repo.delete(cid)
                room = room_repo.get_by_id(contract.room_id)
                if room:
                    room_repo.update(room.room_id, room.number, room.type, room.area, "свободно")
                print("Договор расторгнут, помещение освобождено.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break

def notifications_menu():
    while True:
        print("\n--- УВЕДОМЛЕНИЯ ---")
        print("1. Показать все")
        print("2. Добавить (вызвать техслужбу)")
        print("3. Удалить")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            for n in notification_repo.get_all():
                print(f"ID: {n.notification_id} | Room ID: {n.room_id} | Описание: {n.description}")
        
        elif choice == "2":
            print("\n--- СПИСОК ВСЕХ ПОМЕЩЕНИЙ ---")
            rooms = room_repo.get_all()
            for r in rooms:
                print(f"ID: {r.room_id} | Номер: {r.number} | Тип: {r.type} | Статус: {r.status}")
            
            print("\n--- СПИСОК ВСЕХ СОТРУДНИКОВ ---")
            employees = employee_repo.get_all()
            for e in employees:
                print(f"ID: {e.employee_id} | {e.last_name} {e.first_name} | {e.position}")

            try:
                room_id = int(input("\nВведите ID помещения: "))
                if not room_repo.get_by_id(room_id):
                    print("Ошибка: Помещения с таким ID не существует.")
                    continue
                employee_id = int(input("Введите ID сотрудника: "))
                if not employee_repo.get_by_id(employee_id):
                    print("Ошибка: Сотрудника с таким ID не существует.")
                    continue
                desc = input("Описание проблемы: ")
                notification_repo.create(room_id, employee_id, desc)
                print("Уведомление успешно создано.")
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == "3":
            try:
                nid = int(input("ID уведомления для удаления: "))
                notification_repo.delete(nid)
                print("Уведомление удалено.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break

# --- МЕНЮ ДЛЯ АРЕНДАТОРА ---
def tenant_dashboard(user):
    while True:
        print(f"\n=== ЛИЧНЫЙ КАБИНЕТ АРЕНДАТОРА: {user.last_name} {user.first_name} ===")
        print("1. Мои договоры")
        print("2. Подать заявку в техслужбу")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            print("\n--- МОИ ДОГОВОРЫ ---")
            all_contracts = contract_repo.get_all()
            my_contracts = [c for c in all_contracts if c.tenant_id == user.tenant_id]
            if not my_contracts:
                print("У вас пока нет договоров.")
            for c in my_contracts:
                room = room_repo.get_by_id(c.room_id)
                print(f"Договор ID: {c.contract_id} | Помещение: {room.number if room else 'Удалено'} | Сумма: {c.cost}")
        
        elif choice == "2":
            print("\n--- ЗАЯВКА В ТЕХСЛУЖБУ ---")
            print("Выберите помещение, по которому есть проблема:")
            my_contracts = [c for c in contract_repo.get_all() if c.tenant_id == user.tenant_id]
            if not my_contracts:
                print("У вас нет арендованных помещений.")
                continue
            
            for c in my_contracts:
                room = room_repo.get_by_id(c.room_id)
                if room:
                    print(f"ID: {room.room_id} | Номер: {room.number}")

            try:
                room_id = int(input("Введите ID помещения: "))
                desc = input("Описание проблемы: ")
                notification_repo.create(room_id, 1, f"От арендатора: {desc}")
                print("Заявка отправлена в техслужбу.")
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == "0":
            break

# --- АВТОРИЗАЦИЯ И ГЛАВНОЕ МЕНЮ ---
def login_screen():
    print("\n=== АВТОРИЗАЦИЯ ===")
    login = input("Логин: ")
    if login.strip() == "":
        return None
        
    password = input("Пароль: ")
    
    result = auth_service.authenticate(login, password)
    if not result:
        print("Неверный логин или пароль.")
        return None
    return result

def main():
    while True:
        print("\n=== СИСТЕМА УЧЁТА АРЕНДЫ ===")
        print("1. Авторизация")
        print("0. Выход")
        print("(Введите 'reboot' для сброса базы данных)")
        
        start_choice = input("Выберите действие: ")

        if start_choice == "0":
            print("Выход из программы.")
            break
        elif start_choice.lower() == "reboot":
            reboot_db()
            continue
        elif start_choice == "1":
            auth_result = login_screen()
            
            if auth_result is None:
                continue # Возврат на главный экран при ошибке/пустом вводе

            role = auth_result["role"]
            user = auth_result["user"]

            # --- МЕНЮ АДМИНИСТРАТОРА ---
            if role == "employee":
                print(f"\nДобро пожаловать, {user.position} {user.last_name}!")
                while True:
                    print("\n--- ГЛАВНОЕ МЕНЮ (АДМИНИСТРАТОР) ---")
                    print("1. Помещения")
                    print("2. Арендаторы")
                    print("3. Сотрудники")
                    print("4. Договоры")
                    print("5. Уведомления")
                    print("0. Выйти из аккаунта")
                    choice = input("Выберите раздел: ")

                    if choice == "1": rooms_menu()
                    elif choice == "2": tenants_menu()
                    elif choice == "3": employees_menu()
                    elif choice == "4": contracts_menu()
                    elif choice == "5": notifications_menu()
                    elif choice == "0":
                        print("Выход из аккаунта.")
                        break
                    else:
                        print("Неверный ввод.")

            # --- МЕНЮ АРЕНДАТОРА ---
            elif role == "tenant":
                print(f"\nДобро пожаловать, {user.last_name} {user.first_name}!")
                tenant_dashboard(user)
                
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()