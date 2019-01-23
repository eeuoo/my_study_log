

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

