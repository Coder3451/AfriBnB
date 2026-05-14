-- prepares a MySQL server for AfriBnB testing
CREATE DATABASE IF NOT EXISTS afribnb_test_db;
CREATE USER IF NOT EXISTS 'afribnb_test'@'localhost' IDENTIFIED BY 'AfriBnB_Test_2024!';
GRANT ALL PRIVILEGES ON afribnb_test_db.* TO 'afribnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'afribnb_test'@'localhost';
FLUSH PRIVILEGES;
