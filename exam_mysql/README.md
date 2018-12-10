![sql](https://user-images.githubusercontent.com/44750085/49565371-50aa7c80-f96a-11e8-8450-922e8d7eecee.png)

# MySQL 활용

의미 있는 데이터 만들기 

~~~

create table Enroll (

    id smallint unsigned not null auto_increment primary key,
	
    createdate timestamp not null default current_timestamp,
    
    subject int unsigned, 
    
    student int(11) unsigned
    
    );
    
~~~
~~~
    
alter table Enroll add constraint  fk_student foreign key ( student ) references Student(id) on delete cascade;

alter table Enroll add constraint  foreign key fk_subject(subject) references Subject(id) on delete cascade;

~~~
~~~

insert into Enroll(subject, student) select 1, id from Student order by rand();


update  Enroll  set subject =  (select id from Subject order by rand() limit 1) ;

~~~

-- unique index를 추가 후 실행
~~~

insert into Enroll(student, subject) select stu.id ,(select id from Subject order by rand() limit 1)

  from Student  stu order by rand() on duplicate key update student = student;

~~~
~~~
select * from Enroll order by student ;

~~~
~~~
select s.* , p.name as 'prof name' from Subject s inner join Prof p on s.prof = p.id;  

~~~
~~~

select e.subject, sub.name, e.student, stu.name

from Enroll e inner join Subject sub on e.subject = sub.id  inner join Student stu on e.student = stu.id order by stu.name ;

~~~
-- 검증
~~~
select subject, count(*) from Enroll group by subject ;

select subject, student, count(*) from Enroll group by subject, student having count(*) > 1 ;
~~~

~~~
select * from Enroll ;
~~~
