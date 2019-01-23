create table Classroom(
	id  smallint unsigned not null auto_increment primary key,
    name varchar(15) not null
    );
    
select * from Classroom;

show create table Classroom;

insert Classroom(name) values('101');
insert Classroom(name) values('102');
insert Classroom(name) values('103');
insert Classroom(name) values('104');
insert Classroom(name) values('201');
insert Classroom(name) values('202');
insert Classroom(name) values('203');
insert Classroom(name) values('301');
insert Classroom(name) values('302');
insert Classroom(name) values('303');

select * from Classroom;

alter table Subject drop column classroom;
alter table Subject add column classroom smallint unsigned not null;

select * from Subject; 

update Subject set classroom = (select id from Classroom order by rand() limit 1) ;
on duplicate key update classroom = classroom;

alter table Subject add constraint foreign key fk_classroom_subject (classroom) references Classroom(id) on delete set null;

select classroom, count(*) from Subject group by classroom; 

