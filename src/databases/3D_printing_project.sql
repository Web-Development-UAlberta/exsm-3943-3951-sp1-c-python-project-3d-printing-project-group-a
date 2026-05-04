-- 3D Printing Project Database

-- Create and Use the Database
CREATE DATABASE IF NOT EXISTS 3D_printing_project;
USE 3D_printing_project;

-- Create Tables
-- User Table
CREATE TABLE Users(
    user_id INT AUTO_INCREMENT PRIMARY Key,
    username VARCHAR(200) NOT NULL UNIQUE,   
    full_name VARCHAR(200),
    email VARCHAR(250) UNIQUE,
    phone_number CHAR(15) NOT NULL UNIQUE,
    city VARCHAR(100) NOT NULL,
    street_address VARCHAR(250) NOT NULL,
    province CHAR(2) NOT NULL, 
    postal_code CHAR(10),
    is_admin BOOLEAN DEFAULT FALSE
);

-- Filament Table
CREATE TABLE Filament(
    filament_id INT AUTO_INCREMENT PRIMARY KEY,
    material_name VARCHAR(100) NOT NULL,
    color_hex VARCHAR(250),
    quantity_in_stock FLOAT,
    manufacturer VARCHAR(100),
    more_wear_and_tear DECIMAL(5,2),
    finish_filament VARCHAR(100),
    filament_price FLOAT NOT NULL
);

-- Printer_Type Table
CREATE TABLE Printer_Type(
    printer_type_id INT AUTO_INCREMENT PRIMARY KEY,
    printer_name VARCHAR(100),
    max_size FLOAT NOT NULL
);

-- Printer Table
CREATE TABLE Printer(
printer_id INT AUTO_INCREMENT PRIMARY KEY,
filament_id INT,
printer_type_id INT,

FOREIGN KEY (filament_id) REFERENCES Filament(filament_id),
FOREIGN KEY (printer_type_id) REFERENCES Printer_Type(printer_type_id)
);

-- Tag Table
CREATE TABLE Tag(
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(100) NOT NULL UNIQUE
);

-- Model Table
CREATE TABLE Model(
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_length FLOAT,
    model_width FLOAT,
    model_height FLOAT,
    model_description TEXT,
    model_file VARCHAR(500),
    tag_id INT,
    printer_id INT,

    FOREIGN KEY (tag_id) REFERENCES Tag(tag_id),
    FOREIGN KEY (printer_id) REFERENCES Printer(printer_id)
);

-- Model_Filament Table
CREATE TABLE Model_Filament(
    model_id INT,
    filament_id INT,
    PRIMARY KEY (model_id, filament_id),

    FOREIGN Key (model_id) REFERENCES Model(model_id),
    FOREIGN KEY (filament_id) REFERENCES Filament(filament_id)
);

-- Order_Header Table
CREATE TABLE Order_Header(
    order_header_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    shipping_price FLOAT NOT NULL,
    extra_fee FLOAT,
    total_price FLOAT NOT NULL,
    order_tracking_number VARCHAR(200) UNIQUE,
    order_status ENUM('Pending', 'Printing', 'Shipped', 'Completed') NOT NULL,
    stripe_payment_id VARCHAR(500),
    payment_date DATE,
    payment_status ENUM('Pending', 'Succeeded', 'Failed'),
    user_id INT,

    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Order_Detail Table
CREATE TABLE Order_Detail(
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_quantity INT,
    infill_percent DECIMAL(5,2),
    scale FLOAT,
    unit_price FLOAT,
    model_id INT,
    order_header_id INT,
    filament_id INT,

    FOREIGN KEY (model_id) REFERENCES Model(model_id),
    FOREIGN KEY (order_header_id) REFERENCES Order_Header(order_header_id),
    FOREIGN KEY (filament_id) REFERENCES Filament(filament_id)
);

-- Data Insertions
-- Users table
START TRANSACTION;
INSERT INTO Users(
    username, full_name, 
    phone_number, city, 
    street_address, province, 
    postal_code, is_admin)
VALUES('admin','Bo Cen', '000-111-2222', 'Edmonton', '123 Main St', 'AB', 'T6G 2G5', TRUE);
COMMIT;

-- Filament Table
START TRANSACTION;
INSERT INTO Filament(material_name, color_hex, quantity_in_stock, 
manufacturer, more_wear_and_tear, finish_filament, filament_price)
VALUES('PLA', '#FFFFFF', 100, 'm3D', 10.00, 'Satin', 18.00);
COMMIT;

-- Printer Type Table
START TRANSACTION;
INSERT INTO Printer_Type(printer_name, max_size)
VALUES('Prusa MK4', 500.00);
COMMIT;

-- Printer Table
START TRANSACTION;
INSERT INTO Printer(printer_type_id, filament_id)
VALUES(1, 1);
COMMIT;

-- Tag Table
START TRANSACTION;
INSERT INTO Tag(tag_name)
VALUES('Gaming');
COMMIT;

-- Model Table
START TRANSACTION;
INSERT INTO Model(model_name, model_length, 
model_width, model_height, 
model_description, 
tag_id, printer_id)
VALUES('Iron Man', 10, 10, 10, 'Iron Man Model', 1, 1);
COMMIT;