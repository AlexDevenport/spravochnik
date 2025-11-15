--   BUILDINGS
INSERT INTO buildings (id, address, latitude, longitude) VALUES
(1, 'Проспект Победы 15', 55.12345, 61.23456),
(2, 'Ленина 10', 55.20000, 61.30000),
(3, 'Молодёжная 8', 55.15000, 61.21000);

-- Синхронизация последовательности
SELECT setval(pg_get_serial_sequence('buildings', 'id'), (SELECT MAX(id) FROM buildings));


--   ACTIVITIES (дерево категорий)
INSERT INTO activities (id, name, parent_id) VALUES
(1, 'Товары', NULL),
(2, 'Продукты питания', 1),
(3, 'Мясная продукция', 2),
(4, 'Овощи и фрукты', 2),
(5, 'Услуги', NULL),
(6, 'Строительные услуги', 5),
(7, 'Мастерские', 5),
(8, 'Ремонт техники', 7),
(9, 'Пошив одежды', 7),
(10, 'Инструменты', 6);

-- синхронизация sequence
SELECT setval(pg_get_serial_sequence('activities', 'id'), (SELECT MAX(id) FROM activities));

--   ORGANIZATIONS
INSERT INTO organizations (id, name, building_id) VALUES
(1, 'Молочный Двор', 1),
(2, 'Ремонт-Техно', 2),
(3, 'ФруктыЛэнд', 1),
(4, 'СтройМастер', 3);

SELECT setval(pg_get_serial_sequence('organizations', 'id'), (SELECT MAX(id) FROM organizations));

--   ORGANIZATION PHONES
INSERT INTO organization_phones (id, number, organization_id) VALUES
(1, '88005553535', 1),
(2, '79001234567', 1),
(3, '79000001122', 2),
(4, '78005550101', 3),
(5, '75550000001', 4);

SELECT setval(pg_get_serial_sequence('organization_phones', 'id'), (SELECT MAX(id) FROM organization_phones));

--   ORGANIZATION_ACTIVITIES (таблица связи многие-ко-многим)
CREATE TABLE IF NOT EXISTS organization_activities (
    organization_id INTEGER REFERENCES organizations(id),
    activity_id INTEGER REFERENCES activities(id),
    PRIMARY KEY (organization_id, activity_id)
);

-- Молочный двор → Продукты питания
INSERT INTO organization_activities (organization_id, activity_id) VALUES (1, 2);

-- Ремонт-Техно → Ремонт техники
INSERT INTO organization_activities (organization_id, activity_id) VALUES (2, 8);

-- ФруктыЛэнд → Овощи и фрукты
INSERT INTO organization_activities (organization_id, activity_id) VALUES (3, 4);

-- СтройМастер → Строительные услуги + Инструменты
INSERT INTO organization_activities (organization_id, activity_id) VALUES (4, 6);
INSERT INTO organization_activities (organization_id, activity_id) VALUES (4, 10);