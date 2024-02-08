CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publish_date DATE NOT NULL
);

CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    rent_allowed BOOLEAN NOT NULL
);

CREATE TABLE student_rented_books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    book_id INT NOT NULL,
    rent_date DATE NOT NULL,
    required_return_date DATE NOT NULL,
    actual_return_date DATE,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (book_id) REFERENCES books (id)
);
