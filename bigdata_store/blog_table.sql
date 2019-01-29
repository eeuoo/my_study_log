create table Blogger (
	id varchar(127) not null  primary key,
    blogger_name varchar(127),
    link varchar(511)
	);
    

create table BlogPost (
	id varchar(127) not null,
    title varchar(511),
    addr varchar(511),
    post_date varchar(31)
);

ALTER TABLE BlogPost ADD FOREIGN KEY (id) REFERENCES Blogger(id);

select * from Blogger;

select * from BlogPost;