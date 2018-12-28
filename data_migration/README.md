* 데이터 변환설계서(이행계획서)에 의거하여 Oracle의 아래 4개 테이블들  
(EMPLOYEES, JOBS, JOB_HISTORY, DEPARTMENTS)을 MySQL로 이관하는 변환프로그램을 작성하시오.
```python
# python을 이용하여 데이터 이관.

import mysqldata2 as mu

oraconn = mu.get_oracle_conn()
myconn = mu.get_mysql_conn('dooodb')

with oraconn :

    cursor_j = oraconn.cursor()
    cursor_d = oraconn.cursor()    
    cursor_e = oraconn.cursor()    
    cursor_jh = oraconn.cursor()    

    oracle_j = ''' SELECT JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY FROM JOBS '''
    oracle_d = ''' SELECT DEPARTMENT_ID, DEPARTMENT_NAME, MANAGER_ID FROM DEPARTMENTS '''     
    oracle_e = ''' SELECT EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NUMBER, HIRE_DATE, JOB_ID,
                          NVL(SALARY, 0), NVL(COMMISSION_PCT, 0), MANAGER_ID, DEPARTMENT_ID
                     FROM EMPLOYEES'''
    oracle_jh = ''' SELECT EMPLOYEE_ID, START_DATE, END_DATE, JOB_ID, DEPARTMENT_ID FROM JOB_HISTORY '''  

    cursor_j.execute(oracle_j)
    cursor_d.execute(oracle_d)
    cursor_e.execute(oracle_e)
    cursor_jh.execute(oracle_jh)

    rows_j = cursor_j.fetchall()
    rows_d = cursor_d.fetchall()
    rows_e = cursor_e.fetchall()
    rows_jh = cursor_jh.fetchall()

''' 오라클 데이터 출력
for j in rows_j:
    print(j)

for d in rows_d:
    print(d)

for e in rows_e:
    print(e)

for jh in rows_jh:
    print(jh)
'''


with myconn :

    cur_j = myconn.cursor()
    cur_d = myconn.cursor()
    cur_e = myconn.cursor()
    cur_jh = myconn.cursor()

    sql_j = ''' create table Jobs (
                    id varchar(10) not null primary key default '',
                    job_title varchar(35) not null default '', 
                    min_salary int default 0,
                    max_salary int default 0
                )
            '''
    sql_d = ''' create table Departments (
                    id int unsigned primary key default 0,
                    department_name varchar(30) not null default '',
                    manager_id int unsigned default 0
                )
            '''
    sql_e = ''' create table Employees (
                    id int unsigned not null primary key default 0,
                    first_name varchar(20),
                    last_name varchar(25) not null,
                    email varchar(25) not null unique,
                    phone_number varchar(20),
                    hire_date date not null,
                    job_id varchar(10) not null,
                    salary int unsigned not null default 0,
                    commission_pct int unsigned not null default 0,
                    manager_id int unsigned default 0,
                    department_id int unsigned default 0
                )
            '''    
    sql_jh = ''' create table JobHistory (
                    employee_id int unsigned not null default 0,
                    start_date date not null,
                    end_date  date not null,
                    job_id varchar(10) not null default '',
                    department_id int unsigned not null default 0,
                    primary key (employee_id, start_date)
                )
             '''

# Jobs 데이터 이관
    cur_j.execute("drop table if exists Jobs")   
    cur_j.execute(sql_j)

    sql_insert_j = "insert into Jobs(id, job_title, min_salary, max_salary) values(%s, %s, %s, %s)"
    cur_j.executemany(sql_insert_j, rows_j)

# Departments 데이터 이관
    cur_d.execute("drop table if exists Departments")
    cur_d.execute(sql_d)

    sql_insert_d = "insert into Departments(id, department_name, manager_id) values(%s, %s, %s)"
    cur_d.executemany(sql_insert_d, rows_d)

# Employees 데이터 이관
    cur_e.execute("drop table if exists Employees")
    cur_e.execute(sql_e)

    sql_insert_e = '''insert into Employees(id, first_name, last_name, email, phone_number, 
                                            hire_date, job_id, salary, commission_pct, manager_id, department_id) 
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cur_e.executemany(sql_insert_e, rows_e)

# JobHistory 데이터 이관
    cur_jh.execute("drop table if exists JobHistory")
    cur_jh.execute(sql_jh)

    sql_insert_jh = '''insert into JobHistory(employee_id, start_date, end_date, job_id, department_id) 
                         values(%s, %s, %s, %s, %s)'''
    cur_jh.executemany(sql_insert_jh, rows_jh)

# 이관된 데이터 행 수 출력
    print( "Jobs rowcount :", cur_j.rowcount)
    print( "Departments rowcount :", cur_d.rowcount)    
    print( "Employees rowcount", cur_e.rowcount)
    print( "JobHistory rowcount", cur_jh.rowcount)
```
```mysql
-- mysql에서 외래키 생성.
alter table JobHistory add constraint  fk_job foreign key ( job_id ) references Jobs(id) on delete cascade;
alter table JobHistory add constraint  fk_departments foreign key ( department_id ) references Departments(id) on delete cascade;
alter table Departments add constraint  fk_employees foreign key ( manager_id ) references Employees(id) on delete cascade;
alter table Employees add constraint fk_employees_id foreign key ( manager_id ) references Employees(id) on delete cascade;
alter table Employees add constraint fk_department foreign key ( department_id ) references Departments(id) on delete cascade;
alter table Employees add constraint fk_jobs foreign key ( job_id ) references Jobs(id) on delete cascade;
alter table JobHistory add constraint  fk_employees_self foreign key ( employee_id ) references Employees(id) on delete cascade;
```
```mysql
# 외부 모듈
import pymysql
import cx_Oracle

def get_oracle_conn():
    return cx_Oracle.connect("hr", "hrpw", "localhost:1521/xe")

def get_mysql_conn(db):
    return pymysql.connect(
        host='localhost',
        user='dooo',
        password='dooo!',
        port=3306,
        db=db,
        charset='utf8')

def get_count(conn, tbl, where = ''):
    cur = conn.cursor()
    sql = "select count(*) frin " + tbl
    if where != '':
        sql = sql + " where " + where
    
    cur.execute(sql)
    return cur.fetchone()[0]

def trunc_table(conn, tbl):
    cur = conn.cursor()
    cur.execute('truncate table ' + tbl)
    return cur.rowcount

def get_count(conn, tbl, where = ''):
    cur = conn.cursor()
    sql = "select count(*) from " + tbl
    if where != '' :
        sql = sql + " where " + where        
    
    cur.execute(sql)
    return cur.fetchone()[0]

def get_all(conn, tbl, where = '', order = '') :
    cur = conn.cursor()
    sql = "select * from " + tbl
    if where != '' :
        sql = sql + " where " + where
    
    elif order != '' :
        sql = sql + " order by " + order
    
    cur.execute(sql)

    return cur.fetchall()


def get_inner_cnt(conn, tbl1, tbl2, on = '') :
    cur = conn.cursor()
    inner_cnt = "select count(*) from " + tbl1 + " inner join " + tbl2
    if on != '' :
        inner_cnt = inner_cnt + " on " + on

    cur.execute(inner_cnt)
    
    return cur.fetchone()[0]
```

* 데이터 검증 설계서에 의거하여  Oracle의 아래 4개 테이블들  
(EMPLOYEES, JOBS, JOB_HISTORY, DEPARTMENTS)을 MySQL로 이관한 데이터를 검증하는 프로그램을 작성하시오.
```python
import mysqldata2 as mu

oraconn = mu.get_oracle_conn()
myconn = mu.get_mysql_conn('dooodb')



with oraconn :
    ora_cnt_j = mu.get_count(oraconn, 'Jobs')
    ora_cnt_d = mu.get_count(oraconn, 'Departments')
    ora_cnt_e = mu.get_count(oraconn, 'Employees')
    ora_cnt_jh = mu.get_count(oraconn, 'JOB_HISTORY')

with myconn:
    dooo_cnt_j = mu.get_count(myconn, 'Jobs')
    dooo_cnt_d = mu.get_count(myconn, 'Departments')
    dooo_cnt_e = mu.get_count(myconn, 'Employees')    
    dooo_cnt_jh = mu.get_count(myconn, 'JobHistory')    

# Jobs의 카운트
print("[Jobs table count]\noradb =", ora_cnt_j, ", dooodb =", dooo_cnt_j) 

if ora_cnt_j == dooo_cnt_j:
    print("OK")

else:
    print("[Jobs] Not Valid Count!! oradb =", ora_cnt_j, ", dooodb =", dooo_cnt_j)

# Departments의 카운트

print("\n[Departments table count]\noradb =", ora_cnt_d, ", dooodb =", dooo_cnt_d) 

if ora_cnt_d == dooo_cnt_d:
    print("OK")

else:
    print("[Departments] Not Valid Count!! oradb =", ora_cnt_d, ", dooodb =", dooo_cnt_d)

# Employees의 카운트

print("\n[Employees table count]\noradb =", ora_cnt_e, ", dooodb =", dooo_cnt_e) 

if ora_cnt_e == dooo_cnt_e:
    print("OK")

else:
    print("[Employees] Not Valid Count!! oradb =", ora_cnt_e, ", dooodb =", dooo_cnt_e)

# JobHistory의 카운트

print("\n[JobHistory table count]\noradb =", ora_cnt_jh, ", dooodb =", dooo_cnt_jh) 

if ora_cnt_jh == dooo_cnt_jh:
    print("OK")

else:
    print("[JobHistory] Not Valid Count!! oradb =", ora_cnt_jh, ", dooodb =", dooo_cnt_jh)
```
```mysql
import mysqldata2 as mu

oraconn = mu.get_oracle_conn()
myconn = mu.get_mysql_conn('dooodb')

# read from source db
with oraconn:
    emp_dpt_inner_cnt = mu.get_inner_cnt(oraconn, 'Employees e', 'Departments d', 'e.department_id = d.department_id')
    emp_job_inner_cnt = mu.get_inner_cnt(oraconn, 'Employees e', 'Jobs j', 'e.job_id = j.job_id')
    ora_emp_mng_inner_cnt = mu.get_inner_cnt(oraconn, 'Employees e', 'Employees ep', 'e.employee_id = ep.manager_id')
    ora_dpt_mng_inner_cnt = mu.get_inner_cnt(oraconn, 'Departments d', 'Employees e', 'd.manager_id = e.employee_id')
    ora_jh_emp_inner_cnt = mu.get_inner_cnt(oraconn, 'Job_history jh', 'Employees e', 'jh.employee_id = e.employee_id')
    ora_jh_dpt_inner_cnt = mu.get_inner_cnt(oraconn, 'Job_history jh', 'Departments d', 'jh.department_id = d.department_id')
    ora_jh_job_inner_cnt = mu.get_inner_cnt(oraconn, 'Job_history jh', 'jobs j', 'jh.job_id = j.job_id')


with myconn:
    my_emp_dpt_inner_cnt = mu.get_inner_cnt(myconn, 'Employees e', 'Departments d', 'e.department_id = d.id')
    my_job_inner_cnt = mu.get_inner_cnt(myconn, 'Employees e', 'Jobs j', 'e.job_id = j.id')
    my_emp_mng_inner_cnt = mu.get_inner_cnt(myconn, 'Employees e', 'Employees ep', 'e.id = ep.manager_id')
    my_dpt_mng_inner_cnt = mu.get_inner_cnt(myconn, 'Departments d', 'Employees e', 'd.manager_id = e.id')
    my_jh_emp_inner_cnt = mu.get_inner_cnt(myconn, 'JobHistory jh', 'Employees e', 'jh.employee_id = e.id')
    my_jh_dpt_inner_cnt = mu.get_inner_cnt(myconn, 'JobHistory jh', 'Departments d', 'jh.department_id = d.id')
    my_jh_job_inner_cnt = mu.get_inner_cnt(myconn, 'JobHistory jh', 'Jobs j', 'jh.job_id = j.id')

def samecount(oracnt, mycnt):
    if oracnt == mycnt :
        print('일치 ora = ' , oracnt, 'my =', mycnt )
    else :    
        print('불일치 ora = ' , oracnt, 'my =', mycnt )

samecount( emp_dpt_inner_cnt, my_emp_dpt_inner_cnt )   
samecount(emp_job_inner_cnt, my_job_inner_cnt )       
samecount(ora_emp_mng_inner_cnt, my_emp_mng_inner_cnt )
samecount(ora_dpt_mng_inner_cnt,  my_dpt_mng_inner_cnt )
samecount(ora_jh_emp_inner_cnt,  my_jh_emp_inner_cnt )
samecount(ora_jh_dpt_inner_cnt,  my_jh_dpt_inner_cnt  )
samecount(ora_jh_job_inner_cnt,  my_jh_job_inner_cnt  )
```
```mysql
import mysqldata2 as mu

oraconn = mu.get_oracle_conn()
myconn = mu.get_mysql_conn('dooodb')
table = 'JOBS'
cols = "JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY"
rand_row_count = 0


with oraconn:
	ora_cnt = mu.get_count(oraconn, table)

	cur = oraconn.cursor()
	sql = "SELECT * FROM (SELECT " + cols + " FROM " + table + " ORDER BY DBMS_RANDOM.RANDOM) WHERE rownum <= 10"
	cur.execute(sql)
	ora_list = cur.fetchall()
	rand_row_count = cur.rowcount
	



with myconn :

    my_cnt = mu.get_count(myconn , "Jobs")

    print("이관된 oracle 레코드수", ora_cnt, ", 이관된 mysql 레코드 수 =", my_cnt)
    if ora_cnt != my_cnt:
        print("레코드 수가 일치하지 않습니다! oracle=", ora_cnt, ", mysql =", my_cnt)
        exit()

    else:
        print("레코드 수가 일치합니다.")
        cur = myconn.cursor()

        sql = '''select id, job_title, min_salary, max_salary
                   from Jobs
                  where id = %s
                    and job_title = %s
                    and min_salary = ifnull(%s, 0)
                    and max_salary = ifnull(%s, 0)
                  '''
        cur.executemany(sql, ora_list)
        curcnt = cur.rowcount
	
	
        if rand_row_count == curcnt:
            print("데이터 샘플이 일치합니다", "샘플 레코드 개수는", rand_row_count)

        else:
            print("실패. oracle에서 읽힌 레코드와 mysql에서 읽힌 레코드의 개수는 각각 다음과 같습니다",
                  rand_row_count, curcnt)
```
```mysql
import mysqldata2 as mu

oraconn = mu.get_oracle_conn()
myconn = mu.get_mysql_conn('dooodb')
table = 'JOB_HISTORY'
cols = "EMPLOYEE_ID, START_DATE, END_DATE, JOB_ID, DEPARTMENT_ID"
rand_row_count = 0


with oraconn :
	ora_cnt = mu.get_count(oraconn, table)

	cur = oraconn.cursor()
	sql = "SELECT * FROM (SELECT " + cols + " FROM " + table + " ORDER BY DBMS_RANDOM.RANDOM) WHERE rownum <= 10"
	cur.execute(sql)
	ora_list = cur.fetchall()
	rand_row_count = cur.rowcount
	
	



with myconn :

    my_cnt = mu.get_count(myconn , "JobHistory")

    print("이관된 oracle 레코드수", ora_cnt, ", 이관된 mysql 레코드 수 =", my_cnt)
    if ora_cnt != my_cnt:
        print("레코드 수가 일치하지 않습니다! oracle=", ora_cnt, ", mysql =", my_cnt)
        exit()

    else:
        print("레코드 수가 일치합니다.")
        cur = myconn.cursor()

        sql = '''select employee_id, start_date, end_date, job_id, department_id
                   from JobHistory
                  where employee_id = %s
                    and start_date = %s
                    and end_date = %s
                    and job_id = %s
					and department_id = %s
                  '''
        cur.executemany(sql, ora_list)
        curcnt = cur.rowcount
	
	
        if rand_row_count == curcnt:
            print("데이터 샘플이 일치합니다", "샘플 레코드 개수는", rand_row_count)

        else:
            print("실패. oracle에서 읽힌 레코드와 mysql에서 읽힌 레코드의 개수는 각각 다음과 같습니다",
                  rand_row_count, curcnt)
```
