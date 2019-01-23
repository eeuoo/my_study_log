
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

create table Club (
	id smallint unsigned not null auto_increment primary key,
    name varchar(31) not null,
    createdate timestamp not null default current_timestamp,
    leader int(11) unsigned, 
    constraint foreign key fk_leader_student(leader) references Student(id)
    on delete set null
    );
    
select id, c.leader from Club c;

insert into Clubmember(club, student, level) select id, c.leader, 2 from Club c;

alter table Club drop foreign key Club_ibfk_1 ;
alter table Club drop column leader, drop index fk_leader_student ;

desc Club;

truncate Clubmember;

insert into Clubmember(student, club)
 select id, (select id from Club order by rand() limit 1) cid from Student order by rand() limit 150;
 

select club, count(*) from Clubmember group by club ;
select club, student, count(*) from Clubmember group by club, student having count(*) > 1 ;

select club, student from Clubmember group by club, student order by 1, 2;


