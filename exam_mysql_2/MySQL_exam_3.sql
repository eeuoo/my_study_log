
drop trigger if exists insert_club ;



DELIMITER //

Create Trigger insert_club
  AFTER INSERT on Club FOR EACH ROW
  
BEGIN

insert into Clubmember(club, student)
select (select id from Club where name = NEW.name), id from Student
 where id not in (select student from Clubmember where level = 2 and club = (select id from Club where name = NEW.name) )
 order by rand() limit 50;

update Clubmember set level = 2 
where club = (select id from Club where name = NEW.name)
					order by rand() limit 1 ;

END //

DELIMITER ;


insert into Club(name) values('봉사활동부') ;

select * from Clubmember
where club = (select max(id) from Club);


