![sql](https://user-images.githubusercontent.com/44750085/49565371-50aa7c80-f96a-11e8-8450-922e8d7eecee.png)

# MySQL 활용


## 여러 테이블(학생, 과목, 교수, 수강내역) 생성하는 DDL 

~~~
create table Student (
	id tinyint unsigned not null auto_increment,
	name varchar(32) not null ,
	addr varchar(30) not null ,
	birth varchar(8) not null,
	tel varchar(15) not null,
	email varchar(31) not null,
	regdt timestamp,
	primary key(id)  
    ) ;
~~~
~~~
 create table Subject (
	id int unsigned not null auto_increment primary key,
    createdate timestamp not null default current_timestamp,
    prof smallint unsigned, 
    constraint foreign key fk_prof(prof) references Prof(id)
    on delete set null
    );   
~~~
~~~
create table Prof (
	  id smallint unsigned not null auto_increment primary key,
      name varchar(31) not null,
      likecnt int not null default 0,
      createdate timestamp not null default current_timestamp
       );
   
 ~~~
 ~~~
create table Enroll (
	id smallint unsigned not null auto_increment primary key,
    createdate timestamp not null default current_timestamp,
    subject int unsigned, 
    student int(11) unsigned
    );

alter table Enroll add constraint  fk_student foreign key ( student ) references Student(id) on delete cascade;
alter table Enroll add constraint  foreign key fk_subject(subject) references Subject(id) on delete cascade;

 ~~~
 
검증하기

~~~
desc Student;
show create table Student;

desc Subject;
Show create table Subject;

desc Prof;
show create table Prof;

desc Enroll;
show create table Enroll;
show index from Enroll;
~~~

## 학생 테이블과 과목 테이블 활용하여 수강내역 테이블에 테스트용 데이터 넣는 DML 구성하기

학셍 테이블에 학생 1000명의 데이터가 들어있고, 과목 테이블에 수학, 영어, 국어, 역사, 체육, 가정, 기술, 화학, 사회의 10개 과목이 들어 있는 걸 전제로 수강내역 테이블을 구성한다면 다음과 같다.

~~~

create table Enroll (

    id smallint unsigned not null auto_increment primary key,
	
    createdate timestamp not null default current_timestamp,
    
    subject int unsigned, 
    
    student int(11) unsigned
    
    );
    
    
alter table Enroll add constraint  fk_student foreign key ( student ) references Student(id) on delete cascade;

alter table Enroll add constraint  foreign key fk_subject(subject) references Subject(id) on delete cascade;

START TRANSACTION;


insert into Enroll(subject, student) select 1, id from Student order by rand();


update  Enroll  set subject =  (select id from Subject order by rand() limit 1) ;


-- unique index를 추가 후 실행

insert into Enroll(student, subject) select stu.id ,(select id from Subject order by rand() limit 1)

  from Student  stu order by rand() on duplicate key update student = student;


select * from Enroll order by student ;

select s.* , p.name as 'prof name' from Subject s inner join Prof p on s.prof = p.id;  

select e.subject, sub.name, e.student, stu.name

from Enroll e inner join Subject sub on e.subject = sub.id  inner join Student stu on e.student = stu.id order by stu.name ;

-- 검증

select subject, count(*) from Enroll group by subject ;

select subject, student, count(*) from Enroll group by subject, student having count(*) > 1 ;

select * from Enroll ;

COMMIT ;
~~~

## 동아리별 회원 테이블을 만들고 회원 50명 임의 배정하기

~~~
create table Clubmember(
	id int unsigned not null auto_increment primary key,
    club smallint unsigned not null,
    student int(11) unsigned not null, 
    `level` tinyint not null default 0,
    CONSTRAINT `fk_club_club` FOREIGN KEY (`club`) REFERENCES `Club` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT `fk_student_student` FOREIGN KEY (`student`) REFERENCES `Student` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
    ); 
    
select * from Clubmember;    

show create table Clubmember; 
desc Clubmember;

START TRANSACTION;

alter table Club drop foreign key Club_ibfk_1 ;
alter table Club drop column leader, drop index fk_leader_student ;

desc Club;

insert into Clubmember(student, club)
  select id, (select id from Club order by rand() limit 1) cid from Student order by rand() limit 150;
 

select club, count(*) from Clubmember group by club ;
select club, student, count(*) from Clubmember group by club, student having count(*) > 1 ;

select club, student from Clubmember group by club, student order by 1, 2;

COMMIT:
~~~

## 학과 테이블 만들고 5개의 샘플 학과 데이터 등록 후, 학생 테이블에 학과 추가한 뒤 모든 학생에게 랜덤하게 배정해주기

~~~
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

START TRANSACTION;

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

-- 검증해보기
select id, s.dept from Student s where id = 과대표 id;
 
COMMIT;

~~~

## 강의실 테이블 만들고 샘플 강의실 데이터 10개 등록 후, 과목 테이블에 강의실을 추가하고 배정해주기

~~~
create table Classroom(
	id  smallint unsigned not null auto_increment primary key,
    name varchar(15) not null
    );
    
select * from Classroom;

show create table Classroom;

START TRANSACTION;

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

COMMIT;
~~~

## 데이터 활용하기

1) 수강하는 과목별 중간고사, 기말고사 성적을 저장하는 테이블(Grade) 생성.

* Grade 테이블 생성
```
START TRANSACTION;

create table Grade(  
    id int unsigned not null auto_increment primary key,
    midterm smallint unsigned not null default 0,
    finalterm smallint unsigned not null default 0,
    enroll smallint unsigned not null
);

COMMIT;
```
```
다른 설정 값
Grade테이블 편집 -> Indexes 탭 -> 컬럼 enroll에 인덱스 생성
Grade테이블 편집 -> 컬럼 enroll에 UQ값을 줌
```

2) 수강테이블 기준으로 샘플 데이터를 중간(midterm), 기말(finalterm), 성적(100점 만점)으로 구성하기

```
START TRANSACTION;
insert into Grade(enroll) (select id from Enroll order by id);
 
update Grade set midterm = (floor(rand() * 101));
update Grade set finalterm = (floor(rand() * 101));
COMMIT;
```
```
# 데이터 검증
select * from Grade;
```

3) 과목별 수강생을 과목/성적 순으로 아래와 같은 형식으로 출력하는 SQL을 작성하시오.

```
select sub.name as '과목명', stu.name as '학생명', g.midterm as '중간', g.finalterm as '기말',
          midterm + g.finalterm as '총점',  round((g.midterm + g.finalterm) / 2 , 1) as '평균',
          case when round((g.midterm + g.finalterm) / 2 , 1) >= 90 then 'A' 
               when round((g.midterm + g.finalterm) / 2 , 1) >= 80 then 'B' 
               when round((g.midterm + g.finalterm) / 2 , 1) >= 70 then 'C' 
               when round((g.midterm + g.finalterm) / 2 , 1) >= 60 then 'D' 
               when round((g.midterm + g.finalterm) / 2 , 1) >= 50 then 'E' 
           else 'F' end as '학점' 
from Grade g inner join (Enroll e inner join Student stu on e.student = stu.id
                        inner join Subject sub on e.subject = sub.id) on g.enroll = e.id
order by 1, 5 desc;
```

4) 과목별 통계 리포트를 과목순으로 하여 아래와 같이 출력하는 SQL을 작성하시오.

```
# T1 테이블 생성.(문제3을 그대로 가져오는 테이블을 생성)
START TRANSACTION;
create table T1(
    id smallint unsigned not null auto_increment primary key,
    subject_t varchar(31) not null,
    student_t varchar(31) not null,
    midterm_t smallint unsigned not null,
    finalterm_t smallint unsigned not null,
    sum_t smallint unsigned not null,
    avg_t smallint unsigned not null,
    level_t varchar(10) not null
);
COMMIT;
```
```# 값을 넣어줌
START TRANSACTION;
insert into T1(subject_t , student_t, midterm_t, finalterm_t, sum_t , avg_t, level_t ) select sub.name as '과목', stu.name as '학생명', 
            g.midterm as '중간고사', g.finalterm as '기말고사',
            midterm + g.finalterm as '총점',  round((g.midterm + g.finalterm) / 2 , 1) as '평균',
            case when round((g.midterm + g.finalterm) / 2 , 1) >= 90 then 'A' 
                 when round((g.midterm + g.finalterm) / 2 , 1) >= 80 then 'B' 
                 when round((g.midterm + g.finalterm) / 2 , 1) >= 70 then 'C' 
                 when round((g.midterm + g.finalterm) / 2 , 1) >= 60 then 'D' 
                 when round((g.midterm + g.finalterm) / 2 , 1) >= 50 then 'E' 
         else 'F' end as '학점' 
from Grade g inner join (Enroll e inner join Student stu on e.student = stu.id
         inner join Subject sub on e.subject = sub.id) on g.enroll = e.id
order by 1, 6 desc;
COMMIT;
```
```
select t.subject_t as '과목', round(avg(t.avg_t), 1) as '평균', count(t.student_t) as '학생 수',  
      (select student_t from T1 where subject_t = t.subject_t and sum_t = max(t.sum_t) limit 1) as '최고득점자',
      max(t.sum_t) as '최고점수'
from T1 t
group by t.subject_t
order by 1;

```
5) 학생별 통계 리포트를 성적순으로 하여 아래와 같이 출력하는 SQL을 작성

```
select student_t as '학생명', count(subject_t) as '과목수', sum(sum_t) as '총점', round(sum(avg_t)/count(subject_t), 1) as '평균', 
       case when round(sum(avg_t)/count(subject_t), 1) >= 90 then 'A' 
            when round(sum(avg_t)/count(subject_t), 1) >= 80 then 'B' 
            when round(sum(avg_t)/count(subject_t), 1) >= 70 then 'C' 
            when round(sum(avg_t)/count(subject_t), 1) >= 60 then 'D' 
            when round(sum(avg_t)/count(subject_t), 1) >= 50 then 'E' 
            else 'F' end as '평점' 
from T1
group by 1
order by 3  desc;

```


