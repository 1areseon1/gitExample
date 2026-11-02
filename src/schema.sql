
DROP TABLE IF EXISTS Notification;
DROP TABLE IF EXISTS Contract;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Tenant;
DROP TABLE IF EXISTS Room;

CREATE TABLE Room (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    type TEXT NOT NULL,
    area REAL NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE Tenant (
    tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    phone TEXT NOT NULL
);

CREATE TABLE Employee (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    position TEXT NOT NULL
);

CREATE TABLE Contract (
    contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    tenant_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    cost REAL NOT NULL,
    FOREIGN KEY (room_id) REFERENCES Room(room_id),
    FOREIGN KEY (tenant_id) REFERENCES Tenant(tenant_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

CREATE TABLE Notification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES Room(room_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);



-- Помещения (Room)
INSERT INTO Room (number, type, area, status) VALUES 
('101', 'Офис', 45.5, 'свободно'),
('102', 'Склад', 120.0, 'занято'),
('201', 'Магазин', 80.0, 'свободно');

-- Арендаторы (Tenant)
INSERT INTO Tenant (last_name, first_name, middle_name, phone) VALUES 
('Иванов', 'Иван', 'Иванович', '+7-900-111-22-33'),
('Петрова', 'Анна', 'Сергеевна', '+7-900-444-55-66');

-- Сотрудники (Employee)
INSERT INTO Employee (last_name, first_name, middle_name, position) VALUES 
('Сидоров', 'Петр', 'Алексеевич', 'Администратор');

-- Договоры (Contract)
INSERT INTO Contract (room_id, tenant_id, employee_id, start_date, end_date, cost) VALUES 
(2, 1, 1, '2026-10-01', '2026-12-31', 50000.00);

-- Уведомления (Notification)
INSERT INTO Notification (room_id, employee_id, description) VALUES 
(2, 1, 'Протечка крыши');