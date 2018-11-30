# my_study_log


docker ubuntu container에 Oracle Express Edition 설치하기
-----------

docker  실행 후, docker search oracle 해서 나온 리스트 중 하나를 정합니다.

sath89/oracle-xe-11g를 선택해서 설치를 한다고 하면,

$> docker pull sath89/oracle-xe-11g 입력합니다.

이렇게 pull 받은 image(sath89/oracle-xe-11g)를 확인하고싶다면,

$> docker images 혹은 $> docker image ls 를 사용합니다.

Repository에서는 image를, Tag에서는 버전을 확인할 수 있습니다.

그리고 image를 구동하기 위해 oracle-xe-11g 기반의 컨테이너를 만들어줍니다.

$> docker run -d --name <컨테이너 이름> -p 8080:8080 -p 1521:1521 sath89/oracle-xe-11g 을 입력 후,

$> docker ps 로 실행중임을 확인합니다. 실행되고 있지 않은 컨테이너는 $> docker ps -a로 확인 가능합니다. 

만들어진 컨테이너는 $> docker start <컨테이너 이름> /  $> docker stop <컨테이너 이름> 으로 시작, 정지합니다.

컨테이너를 사용하고자 하다면,

$> docker exec -it <컨테이너 이름> bash / $> docker attach <컨테이너 이름> 을 입력해 사용합니다.



docker에 MYSQL 5.7 설치하기
-----------


docker  실행 후, docker search mysql  해서 나온 리스트 중 mysql 설치(pull) 합니다.

$> docker pull mysql:5.7 를 입력합니다. 

이렇게 pull 받은 image(mysql)를 확인하고싶다면, $> docker images 혹은 $> docker image ls 를 사용합니다.

Repository에서는 image인 mysql를, Tag에서는 버전 5.7을 확인할 수 있습니다.

그리고 image를 구동하기 위해 mysql 5.7 기반의 컨테이너를 만들어줍니다.

$> docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=<비밀번호> --name <컨테이너 이름> mysql:5.7

  MYSQL_ROOT_PASSWORD=<비밀번호> 를 넣으면 나중에 실행할 때, 비밀번호를 입력하게 만들 수 있습니다.
 
$> docker ps 로 실행중임을 확인합니다. 실행되고 있지 않은 컨테이너는 $> docker ps -a로 확인 가능합니다. 

만들어진 컨테이너는 $> docker start <컨테이너 이름> /  $> docker stop <컨테이너 이름> 으로 시작, 정지합니다.

컨테이너는 $> docker exec -it <컨테이너 이름> bash / $> docker attach <컨테이너 이름> 을 입력해 사용합니다.

컨테이너가 실행 아래와 같은 명령어를 입력한 뒤 사용합니다.

 #> mysql -u root -p
 
 
Oracle과 MYSQL에서 Database와 사용자(User) 생성하기
------------


1) 오라클 사용자(user) 생성과정


SQL Developer> 접속 > 다른 사용자 > 사용자 생성
 - 사용자, 룰, 권한, 할당량, SQL, 결과
 
SQL Developer > 접속 > 다른 사용자 > 사용자 편집 / 삭제

-------------

2) MYSQL 사용자(user) 생성과정

docker에서 생성하려면 mysql image의 컨테이너 안에서 #> mysql -u root -p로 접속합니다.

root인 상태에서 새로운 user를 추가하기 위해,
 
mysql> create user <user 이름>@'<host 이름>' identified by '<password>'; 를 입력합니다.
 
user가 생성되었다면 권한을 설정해줍니다.
 
모든 권한을 부여한다면, 

mysql> grant all privileges on *.* to '<user 이름>'@'<host 이름 >'; 
 
특정 DB의 권한만 부여한다면,

mysql> grant all privileges on <DB>.* to '<user 이름>'@'<host 이름>'';  

권한 설정을 마치면 mysql> flush privileges; 를 입력해 적용합니다.

생성된 user는 root에 접속했던 것과 마찬가지로, mysql -u <user 이름> -p로 접속하여 사용합니다.



Docker의 개념과 구성요소(image, container, docker-machine)에 대한 이해와 설치과정
------

Docker는 하나의 서버(컨테이너)를 통해 제각각 다른 환경 속에서 같은 활용을 할 수 있게 만들어준다.
docker는 가상의 machine을 PC의 infra(H/W) 위 OS 위에 올린다. 하나의 machine이 올라가면 이를 물리적으로 여러 쪽 나눠서 사용하지 않고 가상으로, 논리적으로 나워서 사용한다. 작업에 필요한 것은 상황마다 다르며, 그에 맞춰 필요한 프로그램이나 파일을 받아 작업을 할 수 있는 환경을 구축해 놓는다. 이것이 하나의 서버, 컨테이너를 띄우는 과정이다. 본인이 필요한 모든 것이 갖춰져있는 컨테이너만 받는다면, 어떤 환경에서도 같은 활용을 할 수 있게 된다. 
컨테이너는 MYSQL이나 ubuntu, oracle 같은 image를 기반으로 돌아간다. 하나의 image라도 활용목적과 필요한 요소에 따라 여러 컨테이너를 구상, 생성한다.
Docker의 설치는 홈페이지에서 본인 PC의 OS에 맞춰 설치한다. 정상 설치가 되었다면 터미널에서 docker version 입력 후 버전 확인이 가능하다. docker가 정상 작동되면, 그 위에image를 pull 받고 컨테이너를 생성(run)하고 필요한 것들을 추가하며 사용하면 된다.


Linux(ubuntu) docker container 구동하기
------

1. Linux(Ubuntu) Docker Container를 구동하기 위한 절차

Docker에서 ubuntu를 기반으로 하는 컨테이너 하나를 띄웁니다.

$> docker container run ubuntu:latest 입력 후,
 
$> docker ps -a 로 컨테이너 생성이 잘 되었는지 확인합니다.

$> docker image ls를 통해 방금 생성한 컨테이너의 repository(image)가 ubuntu인지 확인합니다.


--------------------

2. 설치된 ubuntu 컨테이너에 Telnet daemon 구동하기

설치된 ubuntu 컨테이너에서 telnet이라는 23 포트를 사용하고자 한다면,

root인 상태에서 $> sudo apt-get install xinetd telnetd 를 다운받습니다.

다운이 끝나면 설정을 해주기 위해 vi를 여러 아래와 같이 입력합니다.

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

그 후엔 $> /etc/init.d/xinetd restart 를 한 뒤, 아래가 모두 [OK] 상태가 되면 성공입니다.

 * stopping internet superserver xinetd   [OK]

 * starting internet superserver xinetd   [OK]

exit로 모두 나간 후, docker commit <컨테이너 이름> <새 컨테이너 이름>으로 새로운  image를 하나 더 뜹니다.

새로운 image를 기반으로 23 포트를 연결해주는 새 컨테이너를 생성합니다.

$> docker run -itd -p 23:23 --name <새 컨테이너 이름> <새 image 이름> bash

이렇게 만들어진 컨테이너에 attach / exec 하고 xinetd를 재실행합니다.

모두  [OK] [OK]가 된다면 putty 실행 / 터미널에 telnet localhost 입력으로 접속 가능합니다.

----------


3. 한글 사용 설정

한글이 안 써진다면, root인 상태에서  $> locale  을 확인합니다.   

$> locale -a  로 적용 가능한 언어리스트에 한국어가 없다면,

$> apt-get install locales 를 입력해 다운받습니다.

다운이 완료되면,  $> localedef -f UTF-8 -i ko_KR ko_KR.UTF-8 ,

$> locale-gen ko_KR.UTF-8 을 입력해 한글을 다운받습니다.

그 뒤, $> locale -a 로 다시 적용 가능한 언어리스트에 한국어가 있는지 확인합니다.

#~/.profile에 
 
LC_ALL=ko_KR.UTF-8 bash

export LANGUAGE=ko

----------------


4. Git 사용 설정 

Git을 사용하려면 root가 아닌 사용하려는 user 상태에서 #> apt-get install git 로 설치합니다.

#> git config --global user.name <github-username> 

#> git config --global user.email <email>

위 두 명령어를 통해 user이름과 이메일을 설정합니다.

설정 상태는 #> git config  —list 로 확인 가능합니다.

Git clone 하고 싶은 폴더를 만들어  #> git clone <github-url> 를 입력합니다.

그 뒤로는 add, commit, push 를 이용해 git을 사용합니다.

