

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