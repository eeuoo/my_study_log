
오라클 HR Schema와 수업 중 작성한 학적 DB를 통합할 경우의 데이터 표준 지침을 작성하기
-----------------------------------------------------------------------------------------------------------------------------
~~~
지침의 목적: mysql dooodb와 Oracle 데이터 통합
표준화 기준: 기존의 db (mysql)와 형식을 최대한 통일한다.

명칭
1) 모든 테이블명, (정식) 컬럼명은 영문으로 한다.
2) 테이블명은 단수형으로 한다.
3) 테이블의 첫글자는 대문자로 한다.
4) 테이블 이름에 이음동의어, 동음이의어는 허용하지 않는다.
5) 테이블명은 띄어쓰기를 하지 않는다. 언더바를 쓰는 대신 Pascal case로 한다.
6) 영문 약어명은 허용하지 않는다.
7) 컬럼명은 소문자로 한다.
8) 컬럼명에 띄어쓰기가 필요할 경우 언더바로 대체한다.
9) Primary key는 기존(HR스키마)의 것을 유지한다. 
10) Index의 이름은 '소문자 컬럼명_대문자 타입명'으로 한다.
11) Foreign key 이름은 'fk_참조할 테이블명'으로 한다.
12) Trigger 이름은 'tr_원 테이블명_업데이트 될 테이블명_컬럼명'으로 쓴다.
13) Charset/Collation은 utf8, utf8_unicode_ci로 통일한다.

데이터 타입
1) id의 타입은 int unsigned로 설정한다.
2) Oracle에서 varchar2는 MySQL에서 varchar로 변경한다.
3) Oracle에서 number는 MySQL에서 int unsigned로 변경한다.
4) Oracle의 number의 default는 0으로 설정한다.
5) Oracle의 varchar2의 default는 ‘’으로 설정한다.
6) Oracle의 chars는 MySQL에서 varchar로 변경한다.
7) Oracle의 date는 MySQL에서 date이며, YY/MM/DD 형식으로 입력한다.
8) null 값은 그대로 null로 설정한다.

~~~

오라클 HR Schema와 수업 중 작성한 학적 DB를 통합할 경우의 데이터 표준 지침을 작성하기
-----------------------------------------------------------------------

~~~

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


```
