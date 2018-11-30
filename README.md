# my_study_log


문항 1.
-----------

docker  실행 후, docker search oracle 해서 나온 리스트 중 하나 선정.

$> docker pull sath89/oracle-xe-11g

$> docker images

$> docker run -d --name ora -p 8080:8080 -p 1521:1521 sath89/oracle-xe-11g

$> docker ps

$> docker exec -it oracle bas



문항 2.
-----------


docker  실행 후, docker search mysql  해서 나온 리스트 중 mysql 설치(pull).

$> docker pull mysql:5.7

$> docker images

$> docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=r! --name mysql5 mysql:5.7

$> docker ps

$> docker exec -it mysql5 bash

 #> mysql -u root -p


문항 3.
------------


1) 오라클 사용자(user) 생성과정


SQL Developer > 접속 > 다른 사용자 > 사용자 생성
 - 사용자, 룰, 권한, 할당량, SQL, 결과
 
SQL Developer > 접속 > 다른 사용자 > 사용자 편집 / 삭제

-------------

2) MYSQL 사용자(user) 생성과정


 #> mysql -u root -p
 
mysql> create user <user-name>@'<host>' identified by '<password>';
 
mysql> grant all privileges on *.* to '<user-name>'@'<host>';
 
mysql> grant all privileges on <DB>.* to '<user-name>'@'<host>'';  


문항 4.
------

Docker는 하나의 서버(컨테이너)를 통해 제각각 다른 환경 속에서 같은 활용을 할 수 있게 만들어준다.
docker는 가상의 machine을 PC의 infra(H/W) 위 OS 위에 올린다. 하나의 machine이 올라가면 이를 물리적으로 여러 쪽 나눠서 사용하지 않고 가상으로, 논리적으로 나워서 사용한다. 작업에 필요한 것은 상황마다 다르며, 그에 맞춰 필요한 프로그램이나 파일을 받아 작업을 할 수 있는 환경을 구축해 놓는다. 이것이 하나의 서버, 컨테이너를 띄우는 과정이다. 본인이 필요한 모든 것이 갖춰져있는 컨테이너만 받는다면, 어떤 환경에서도 같은 활용을 할 수 있게 된다. 
컨테이너는 MYSQL이나 ubuntu, oracle 같은 image를 기반으로 돌아간다. 하나의 image라도 활용목적과 필요한 요소에 따라 여러 컨테이너를 구상, 생성한다.
Docker의 설치는 홈페이지에서 본인 PC의 OS에 맞춰 설치한다. 정상 설치가 되었다면 터미널에서 docker version 입력 후 버전 확인이 가능하다. docker가 정상 작동되면, 그 위에image를 pull 받고 컨테이너를 생성(run)하고 필요한 것들을 추가하며 사용하면 된다.


문항 5.
------

1. Linux(Ubuntu) Docker Container를 구동하기 위한 절차

docker container run <docker-image-name> <command>
 
$> docker container run ubuntu:latest
 
$> docker ps -a

$> docker container ps -a

$> docker system df

$> docker image ls


--------------------

2. 설치된 ubuntu 컨테이너에 Telnet daemon 구동

$> sudo apt-get install xinetd telnetd

$> vi /etc/xinetd.d/telnet

 #!/bin/sh
 
service telnet

{
    disable = no
    flags = REUSE
    socket_type = stream
    wait = no
    user = root
    server = /usr/sbin/in.telnetd
    log_on_failure += USERID
}

$> /etc/init.d/xinetd restart

$> docker commit ub ub_telnet

$> docker run -itd -p 23:23 --name ubt ub_telnet bash

putty로 telnet 접속 / 터미널에 telnet localhost 입력

----------


3. 한글 사용 설정

$> locale     

$> locale -a  

$> apt-get install locales

$> cat /usr/share/i18n/SUPPORTED

$> localedef -f UTF-8 -i ko_KR ko_KR.UTF-8

$> locale-gen ko_KR.UTF-8

$> locale -a

#~/.profile에 추가
 
LC_ALL=ko_KR.UTF-8 bash
export LANGUAGE=ko

----------------


4. Git 사용 설정 

#> apt-get install git

#> git config --list

#> git config --global user.name <github-username>

#> git config --global user.email <email>

#> git config credential.helper store

#> git clone <github-url>

