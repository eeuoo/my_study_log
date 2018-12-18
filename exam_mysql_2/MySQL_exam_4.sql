
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


