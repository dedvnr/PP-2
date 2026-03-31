-- 1. Добавление или обновление (Upsert)
CREATE OR REPLACE PROCEDURE upsert_contact(p_first TEXT, p_last TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE first_name = p_first AND last_name = p_last) THEN
        UPDATE contacts SET phone_number = p_phone 
        WHERE first_name = p_first AND last_name = p_last;
    ELSE
        INSERT INTO contacts(first_name, last_name, phone_number) 
        VALUES(p_first, p_last, p_phone);
    END IF;
END;
$$;

-- 2. Удаление контакта
CREATE OR REPLACE PROCEDURE delete_contact(p_identifier TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE first_name = p_identifier 
       OR last_name = p_identifier 
       OR phone_number = p_identifier;
END;
$$;

-- 3. Массовая вставка с проверкой номера (только цифры 10-15 знаков)
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(names_first TEXT[], names_last TEXT[], phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_upper(names_first, 1) LOOP
        IF phones[i] ~ '^[0-9]{10,15}$' THEN
            INSERT INTO contacts (first_name, last_name, phone_number)
            VALUES (names_first[i], names_last[i], phones[i]);
        ELSE
            RAISE NOTICE 'Некорректный номер для %: %', names_first[i], phones[i];
        END IF;
    END LOOP;
END;
$$;