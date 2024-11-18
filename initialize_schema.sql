USE student_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role ENUM('student', 'faculty', 'admin'),
    mobile VARCHAR(15) UNIQUE NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE
);

CREATE TABLE announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
show tables;

CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    filename VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
show tables;
INSERT INTO users (name, email, password, role, mobile, is_approved) 
VALUES ('Admin', 'admin@example.com', 'admin123', 'admin', '9806063850', TRUE);
UPDATE users
SET is_approved = True
WHERE mobile = '9770320930';
UPDATE users
SET is_approved = True
WHERE email = 'ajaysingha@something.com';
Select*from users;
USE student_management;
Select*from documents;
drop table announcements;
CREATE TABLE announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select*from announcements;