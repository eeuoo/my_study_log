
### Enroll 구성은 61번째 줄부터  ###


create table Club (
	id smallint unsigned not null auto_increment primary key,
    name varchar(31) not null,
    createdate timestamp not null default current_timestamp,
    leader int(11) unsigned, 
    constraint foreign key fk_leader_student(leader) references Student(id)
    on delete set null
    on update 
    );
    
insert into Club(name, leader) values('요트부', 100);  
insert into Club(name, leader) values('미술부', 200);  
insert into Club(name, leader) values('테니스부', 300);

select * from Club;

select c.* , s.name as 'student name' from Club c inner join Student s on c.leader = s.id ;  
      
      
      
      
create table Prof (
	  id smallint unsigned not null auto_increment primary key,
      name varchar(31) not null,
      likecnt int not null default 0,
      createdate timestamp not null default current_timestamp
       );

insert into Prof(name, likecnt) select name, ceil(rand() * 100) from Student order by rand() limit 100 ;

select * from Prof ;
    
    
    
    
 create table Subject (
	id int unsigned not null auto_increment primary key,
    createdate timestamp not null default current_timestamp,
    prof smallint unsigned, 
    constraint foreign key fk_prof(prof) references Prof(id)
    on delete set null
    );   
    
insert into Subject(prof, name) values( 66, '기초물리학') ; 
insert into Subject(prof, name) values( 12, '기초물리학') ; 
insert into Subject(prof, name) values( 44, '건축학 개론') ; 
insert into Subject(prof, name) values( 50, '소비자 심리') ; 
insert into Subject(prof, name) values( 1, '초급 영문법') ; 
insert into Subject(prof, name) values( 76, '초급 영문법') ; 

select s.* , p.name as 'prof name' from Subject s inner join Prof p on s.prof = p.id;  




    
 create table Enroll (
	id smallint unsigned not null auto_increment primary key,
    createdate timestamp not null default current_timestamp,
    subject int unsigned, 
    student int(11) unsigned
    );
    
alter table Enroll add constraint  fk_student foreign key ( student ) references Student(id) on delete cascade;
alter table Enroll add constraint  foreign key fk_subject(subject) references Subject(id) on delete cascade;


insert into Enroll(subject, student) select 1, id from Student order by rand();

update  Enroll  set subject =  (select id from Subject order by rand() limit 1) ;

-- unique index를 추가 후 실행
insert into Enroll(student, subject) select stu.id ,(select id from Subject order by rand() limit 1)
  from Student  stu order by rand() on duplicate key update student = student;

select * from Enroll order by student ;

select s.* , p.name as 'prof name' from Subject s inner join Prof p on s.prof = p.id;  



select e.subject, sub.name, e.student, stu.name
	from Enroll e inner join Subject sub on e.subject = sub.id
                         inner join Student stu on e.student = stu.id order by stu.name ;


-- 검증
select subject, count(*) from Enroll group by subject ;

select subject, student, count(*) from Enroll group by subject, student having count(*) > 1 ;



select * from Enroll ;


    desc Club;
    desc Prof;
    desc Subject;
    desc Enroll;
    desc Student;
    
    show create table Student;