create table Dept (
	id int unsigned not null auto_increment primary key,
    `name` varchar(15) not null,
    prof smallint(5) unsigned,
    student int(11) unsigned,
    constraint fk_prof_dept foreign key (prof) references Prof(id) on delete set null,
    constraint fk_student_dept foreign key (student) references Student(id) on delete set null
    );
    
show create table Dept;
show index from Dept;

select * from Dept;

insert into Dept(name, prof, student) select '국문학과', id , (select id from Student order by rand() limit 1) sid from Prof order by rand() limit 1;
insert into Dept(name, prof, student) select '경제학과', id , (select id from Student order by rand() limit 1) sid from Prof order by rand() limit 1 
on duplicate key update student = student and prof = prof;
insert into Dept(name, prof, student) select '건축학과', id , (select id from Student order by rand() limit 1) sid from Prof order by rand() limit 1 
on duplicate key update student = student and prof = prof;
insert into Dept(name, prof, student) select '신문방송과', id , (select id from Student order by rand() limit 1) sid from Prof order by rand() limit 1 
on duplicate key update student = student and prof = prof;
insert into Dept(name, prof, student) select '무용학과', id , (select id from Student order by rand() limit 1) sid from Prof order by rand() limit 1 
on duplicate key update student = student and prof = prof;

alter table Student add column dept int unsigned not null;

update Student set dept = 1 ;

alter table Student add constraint  fk_dept_dept foreign key ( dept ) references Dept(id) ;

select * from Student;

update Student set dept =  (select id from Dept order by rand() limit 1) ; 

select dept, count(*) from Student group by dept ;
select dept, id, count(*) from Student group by dept, id having count(*) > 1;

update Student s inner join Dept d on d.student = s.id
 set s.dept = d.id where d.student = s.id;


 select id, s.dept from Student s where id = 979;
 
 
