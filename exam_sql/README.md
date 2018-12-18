
![1](https://user-images.githubusercontent.com/44750085/50141923-14710780-02ec-11e9-82bb-57af4e2f65ec.png)


* ### 학번, 학생명, 수강과목수, 전과목 평균 점수로 컬럼을 갖는 view 만들기
~~~mysql
drop view if exists all_of_student;

create view all_of_student as 
select stu.id as 'student_id', 
		  max(stu.name) as 'student_name', 
          count(*) as 'student_subjects',
          round((sum(midterm + finalterm)/ 2 )/ count(*), 1) as 'student_avg'

from Grade g inner join Enroll e on g.enroll = e.id
					  inner join Student stu on e.student = stu.id 

group by stu.id;


select * from all_of_student;
~~~

* ### 학번을 주면 해당 학생의 전과목 평균 점수를 반환하는 function 만들기
~~~mysql

drop function if exists f_student_avg ;

DELIMITER $$

CREATE Function f_student_avg(_stu_id int(11) ) 
RETURNS float

BEGIN

RETURN 
(select ((sum(midterm + finalterm)/ 2 )/ count(*)) as 'student_avg'

from Grade g inner join Enroll e on g.enroll = e.id
					  inner join Student stu on e.student = stu.id 
where stu.id = _stu_id
group by stu.id) ;

    
END $$

DELIMITER ;


-- ( ) 안에 학번을 넣어 검증해본다
select f_student_avg(113) ;
~~~


* ### Club Table에 클럽을 하나 추가하면 클럽 회원으로 임의의 한 학생을 회장으로 자동 등록되게 하는 Trigger 만들기
~~~mysql
drop trigger if exists insert_club ;



DELIMITER //

Create Trigger insert_club
  AFTER INSERT on Club FOR EACH ROW
  
BEGIN

-- 클럽에 임의의 회원 50명을 배정해준다
insert into Clubmember(club, student)
select (select id from Club where name = NEW.name), id from Student
 where id not in (select student from Clubmember where level = 2 and club = (select id from Club where name = NEW.name) )
 order by rand() limit 50;

-- 배정된 50명의 학생 중 임의의 한 학생을 회장으로 등록한다
update Clubmember set level = 2 
where club = (select id from Club where name = NEW.name)
					order by rand() limit 1 ;

END //

DELIMITER ;

-- 클럽 이름을 넣은 후,
insert into Club(name) values('봉사활동부') ;

-- 해당 클럽을 *로 읽어서 검증해본다
select * from Clubmember
where club = (select max(id) from Club);
~~~

* ### 지난 학기 데이터를 기준으로 인기 강좌 Top 3를 추천하는 procedure 작성하기 ( 가중치는 자유롭게 설정 )
~~~mysql
drop procedure if exists lecture_best3;


delimiter $$

create procedure lecture_best3()


BEGIN


drop view if exists lecture_base1;

create view lecture_base1 as
select  max(sub.name) as sub_name, 
		    count(*)  as student_cnt, 
            round(avg(g.avr), 2)as total_avg , 
            max(p.name) as prof_name, 
            max(p.likecnt) as prof_likecnt
from Grade g inner join Enroll e on g.enroll = e.id
					  inner join Subject sub on e.subject = sub.id
					  inner join Prof p on sub.prof = p.id
group by sub.id ;

drop view if exists lecture_base2;

create view lecture_base2 as
select ( student_cnt / (select sum(student_cnt) from lecture_base1) )* 100 as stu_cnt_100, 
           ( total_avg / (select sum(total_avg) from lecture_base1) ) * 100 as total_avg_100, 
           ( prof_likecnt / (select sum(prof_likecnt) from lecture_base1) ) * 100 as p_likecnt_100,
            sub_name,
            prof_name
from lecture_base1;


select ( ( stu_cnt_100 ) * 2 + (total_avg_100) * 3 + (p_likecnt_100) *5  ) as lecture_value,
			sub_name,
            prof_name
from lecture_base2
order by lecture_value desc limit 3;
 


end $$
delimiter ;

call lecture_best3();
~~~

* ### Oracle HR schema에서 Marketing 부서에 속한 직원의 last_name, salary, department_name 조회하기 ( 단, salary가 80번 부서의 평균보다 적게 받는 직원만)
~~~sql
select e.last_name, e.salary, d.department_name 
from employees e inner join departments d on e.department_id = d.department_id
where d.department_name = 'Marketing'
and e.salary < (select round(avg(salary), -1) from employees where department_id = 80);
~~~

* ### 과목별 Top 3 학생의 이름과 성적을 한 줄로 표현하는 리포트 출력하기
~~~mysql
alter table Grade add column avr float default 0 ;

update Grade set avr = (midterm + finalterm) / 2   ;

drop view if exists v_grade_enroll ;

CREATE VIEW v_grade_enroll AS
    SELECT 
        `g`.`id` AS `id`,
        `stu`.`name` AS `student_name`,
        `sub`.`name` AS `subject_name`,
        `g`.`midterm` AS `midterm`,
        `g`.`finalterm` AS `finalterm`,
        `g`.`avr` AS `avr`,
        `g`.`enroll` AS `enroll`,
        `e`.`subject` AS `subject`,
        `e`.`student` AS `student`
    FROM Grade g
       inner JOIN Enroll e ON g.enroll = e.id
       inner JOIN Student stu ON e.student = stu.id
	   inner JOIN Subject sub ON e.subject = sub.id ;
 

select subject_name, student_name, max(avr)
from v_grade_enroll 
group by subject_name, student_name
order by 1, 3 desc ;



drop procedure if exists sp_subject_top_3;


delimiter $$
create procedure sp_subject_top_3( )


BEGIN

	declare _isdone boolean default False;
    declare _sub_name varchar(31);
    declare `_stu_name` varchar(31);
    declare _score smallint;

	
	declare top_3 CURSOR FOR
		select subject_name, student_name, max(avr)
		from v_grade_enroll 
		group by subject_name, student_name 
		order by 1, 3 desc;
    
    declare continue handler 
        for not found set _isdone = True;
        
	drop table if exists t_g_top_3;
    
    create temporary table t_g_top_3 (
        `sub_name` varchar(31) default ' ' primary key,
        `1st_stu` varchar(31) default ' ',
        `1st_score` smallint default 0 ,
		`2nd_stu` varchar(31) default ' ',
        `2nd_score` smallint default 0 ,
        `3rd_stu` varchar(31) default ' ',
		`3rd_score` smallint default 0,
        `cnt` smallint default 0 
         );


	OPEN top_3  ;
        

	loop1 : LOOP
    
	Fetch top_3  into _sub_name,  _stu_name , _score  ;
    
        IF not exists (select * from t_g_top_3 where sub_name = `_sub_name`) THEN
            insert into t_g_top_3(`sub_name`, `1st_stu`, `1st_score`) value(_sub_name, _stu_name, _score );

       ELSEIF  exists (select * from t_g_top_3 where sub_name = `_sub_name` and cnt = 0) THEN
             update t_g_top_3 set `2nd_stu`= _stu_name, `2nd_score` = _score, cnt = cnt + 1
              where `sub_name` = _sub_name and cnt = 0  ;

		ELSE 
             update t_g_top_3 set `3rd_stu`= _stu_name, `3rd_score` = _score, cnt = cnt + 1
              where `sub_name` = _sub_name and cnt = 1;
             
        END IF;
        
    
		IF _isdone THEN
            LEAVE loop1;
        END IF;
       
    END LOOP loop1;
    
  
    
	CLOSE  top_3 ;
    
    select sub_name as '과목', 1st_stu as '1등' , 1st_score as '점수', 2nd_stu as '2등', 2nd_score as '점수',
    3rd_stu as '3등', 3rd_score as '점수'
    from t_g_top_3
    order by 1;


END  $$

delimiter ;

call  sp_subject_top_3() ;

~~~
