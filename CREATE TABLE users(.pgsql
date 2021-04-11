CREATE TABLE users(
    id_user serial PRIMARY KEY,
    username varchar not null,
    email varchar not null,
    password varchar not null    
);

select * from users
CREATE TABLE books(
    id_book serial PRIMARY KEY,
    isbn varchar not null,
    title varchar not null,
    author varchar not null,
    year varchar not null
);
select * from users where username = 'anneke';
SELECT id FROM users WHERE username = 'anneke';
SELECT * FROM users WHERE username = 'anneke' OR email = 'anneke@gmail.com'
CREATE TABLE review(
    id_book INTEGER not null,
    user_id INTEGER null,
    rating INTEGER not null,
    post varchar not null
);
select id_book  from books where isbn='1442468351'
SELECT * FROM reviews WHERE isbn=:isbn AND user_id=:user_id
INSERT INTO review(isbn, user_id, rating, post) VALUES(1234, 8, 4, 'Good book!')

CREATE TABLE rev(
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users,
    revi varchar not null
);

INSERT INTO rev VALUES (69,1,'prueba')

SELECT id_book FROM books where isbn='1442468351'