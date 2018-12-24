
drop table if exists Departments;

create table Departments(
     id int unsigned not null primary key default 0,
     department_name varchar(30) not null default ' ',
     manager_id int default 0,
     location_id int default 0
);


drop table if exists Jobs;

create table Jobs(
      id varchar(10) not null primary key default ' ',
      job_title varchar(35) not null default ' ',
      min_salary int default 0,
      max_salary int default 0
);


drop table if exists Employees;

create table Employees (
      id int unsigned not null primary key default 0,
     first_name varchar(20)  default ' ',
      last_name varchar(25) not null default ' ',
      email varchar(25) not null default ' ',
      phone_number varchar(20) default ' ',
      hire_date date not null,
      salary int unsigned not null default 0,
      commission_pct int unsigned not null default 0,
      manager_id int unsigned not null default 0,
      job_id varchar(10) not null default ' ',
      department_id int unsigned not null default 0 ,
     constraint foreign key fk_jobs(job_id) references Jobs(id),
     constraint foreign key fk_departments(department_id) references Departments(id)
);

alter table Employees  add constraint  fk_employees_manager foreign key ( manager_id ) references Employees(id) on delete cascade;


drop table if exists JobHistory;

create table JobHistory(
      employee_id int unsigned not null default 0,
      start_date date not null,
      end_date  date not null,
      job_id varchar(10) not null default ' ',
      department_id int unsigned not null default 0,
      constraint foreign key fk_employees(employee_id) references Employees(id),
     constraint foreign key fk_jobs(job_id) references Jobs(id),
     constraint foreign key fk_departments(department_id) references Departments(id),
      primary key (employee_id, start_date)
);