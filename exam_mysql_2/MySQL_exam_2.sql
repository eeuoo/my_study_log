
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



select f_student_avg(113) ;