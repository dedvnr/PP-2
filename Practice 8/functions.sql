-- 1. Поиск по шаблону (имя, фамилия или телефон)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(search_term TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.first_name, c.last_name, c.phone_number 
    FROM contacts c
    WHERE c.first_name ILIKE '%' || search_term || '%'
       OR c.last_name ILIKE '%' || search_term || '%'
       OR c.phone_number ILIKE '%' || search_term || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Пагинация (выдача по страницам)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.first_name, c.last_name, c.phone_number 
    FROM contacts c
    ORDER BY c.id 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;