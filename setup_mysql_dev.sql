-- prepares a MySQL server for AfriBnB project
CREATE DATABASE IF NOT EXISTS afribnb_dev_db;
CREATE USER IF NOT EXISTS 'afribnb_dev'@'localhost' IDENTIFIED BY 'AfriBnB_Dev_2024!';
GRANT ALL PRIVILEGES ON afribnb_dev_db.* TO 'afribnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'afribnb_dev'@'localhost';
FLUSH PRIVILEGES;
