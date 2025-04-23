CREATE OR REPLACE FUNCTION search_pattern(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook.id, phonebook.name, phonebook.phone
    FROM phonebook
    WHERE phonebook.name ILIKE '%' || pattern || '%'
       OR phonebook.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

SELECT * FROM search_pattern('Aliya');

CREATE OR REPLACE PROCEDURE insert_or_update_user(username TEXT, userphone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = username) THEN
        UPDATE phonebook SET phone = userphone WHERE name = username;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (username, userphone);
    END IF;
END;
$$;

CALL insert_or_update_user('Aliya', '87001234567');

CREATE OR REPLACE PROCEDURE bulk_insert_users(names TEXT[], phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 1;
BEGIN
    WHILE i <= array_length(names, 1) LOOP
        IF phones[i] ~ '^\d{10,15}$' THEN
            INSERT INTO phonebook(name, phone) VALUES (names[i], phones[i]);
        ELSE
            RAISE NOTICE 'Қате телефон: % (% қолданушы)', phones[i], names[i];
        END IF;
        i := i + 1;
    END LOOP;
END;
$$;


CALL bulk_insert_users(
    ARRAY['Aliya', 'Dana', 'Serik'],
    ARRAY['87001112233', '87056788787', '1234567890']
);


CREATE OR REPLACE FUNCTION get_paginated_users(lim INT, offs INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook.id, phonebook.name, phonebook.phone
    FROM phonebook
    ORDER BY phonebook.id
    LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_paginated_users(5, 0);


CREATE OR REPLACE PROCEDURE delete_by_value(val TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook WHERE name = val OR phone = val;
END;
$$;



CALL delete_by_value('Aliya');




















