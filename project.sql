CREATE TABLE Customer (
    email VARCHAR(80),
    customerFName VARCHAR(50) NOT NULL REFERENCES PersonName(fname) ,
    customerLName VARCHAR(50)  NOT NULL REFERENCES PersonName(lname),
    id INT AUTO_INCREMENT,
    passwd VARCHAR(50),
    PRIMARY KEY(id)
);
CREATE TABLE Librarian (
    id INT AUTO_INCREMENT,
    passwd VARCHAR(50),
    librarianFName VARCHAR(50) NOT NULL REFERENCES PersonName(fname) ,
    librarianLName VARCHAR(50) NOT NULL REFERENCES PersonName(lname) ,
    Salary INT ,
    Hours_Worked INT,
    Libarian_Email VARCHAR(100),
    PRIMARY KEY(id)
);
CREATE TABLE PersonName (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL
);
CREATE TABLE Event (
    event_id INT AUTO_INCREMENT,
    participant_id INT,
    start_dt_time VARCHAR(150),
    PRIMARY KEY(event_id)
);
CREATE TABLE Item (
    id INT AUTO_INCREMENT,
    genre VARCHAR(80),
    itemName VARCHAR(80),
    rating INT check (rating >= 0 and rating <= 100),
    Item_Aval BOOL,
    holder_id INT REFERENCES Customer(id),
    PRIMARY KEY(id)
);
CREATE TABLE Book (
    authorFName VARCHAR(50) NOT NULL REFERENCES PersonName(fname) ,
    authorLName VARCHAR(50) NOT NULL REFERENCES PersonName(lname) ,
    isbn VARCHAR(50),
    publisher VARCHAR(50),
    publishDate TIMESTAMP
);
CREATE TABLE Magazine (
    publisher VARCHAR(50),
    publishDate TIMESTAMP
);
CREATE TABLE Album (
    releaseDate TIMESTAMP,
    songNum INT,
    artistFName VARCHAR(50) NOT NULL REFERENCES PersonName(fname) ,
    artistLName VARCHAR(50) NOT NULL REFERENCES PersonName(lname) ,
    albumLength VARCHAR(50)
);
CREATE TABLE Movie (
    directorFName VARCHAR(50) NOT NULL REFERENCES PersonName(fname) ,
    directorLName VARCHAR(50) NOT NULL REFERENCES PersonName(lname) ,
    releaseDate TIMESTAMP,
    movLength VARCHAR(80)
);

INSERT INTO Item VALUES (151541, '', 'Test', 75, 1, 0);
INSERT INTO Item VALUES (654565, '', 'Leo--Test', 13, 1, 0);
INSERT INTO Item VALUES (754454, '', 'Andrew--Test', 20, 1, 0);

INSERT INTO Librarian VALUES (534685,'bruh','Leo','Flaker',75000,40,"lflaker@gmail.com");
