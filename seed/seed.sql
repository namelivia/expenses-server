--Insert test categories
INSERT INTO categories (id, name) VALUES (1, 'Test Category 1');
INSERT INTO categories (id, name) VALUES (2, 'Test Category 2');

--Insert test user data
INSERT INTO user_data (id, user_id, "group") VALUES (1, 'localhost/testuser', 'Test group');
INSERT INTO user_data (id, user_id, "group") VALUES (2, 'localhost/testuser2', 'Test group');

--Insert some test expenses
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (1, 'Test expense 1', 120, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (2, 'Test expense 2', 240, 2, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser2', 'Test user 2');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (3, 'Test expense 3', 40, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (4, 'Test expense 1', 120, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (5, 'Test expense 2', 240, 2, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser2', 'Test user 2');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (6, 'Test expense 3', 40, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (7, 'Test expense 1', 120, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (8, 'Test expense 2', 240, 2, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser2', 'Test user 2');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (9, 'Test expense 3', 40, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (10, 'Test expense 1', 120, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (11, 'Test expense 2', 240, 2, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser2', 'Test user 2');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (12, 'Test expense 3', 40, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (13, 'Test expense 1', 120, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (14, 'Test expense 2', 240, 2, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser2', 'Test user 2');
INSERT INTO expenses (id, name, value, category_id, "group", date, user_id, user_name) VALUES (15, 'Test expense 3', 40, 1, 'Test group', '2020-11-07 20:19:30.000000', 'localhost/testuser', 'Test user');
