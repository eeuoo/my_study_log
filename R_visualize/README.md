### 1. R의 시각화 Package 중 대표적인 그래프 함수(5개이상)에 대한 용도와 작도법.

<br>

1) 산점도 (scatter)   
2개의 변수 간 관계를 알아보기 위해 두 변수의 값을 점으로 표현한 그래프이다.    
두 측정치 사이의 기본적인 관계를 나타내며, 가장 정확하고 빠르게 인식할 수 있다.
~~~r
# 작도법
geom_point(mapping = NULL, data = NULL, stat = "identity",
  position = "identity", ..., na.rm = FALSE, show.legend = NA,
  inherit.aes = TRUE)
  
# 예시
ggplot(data=smdt) +
   geom_point(aes(x=stuno, y=Korean), color='blue', size = 5)
~~~
<br>

2) 꺾은선 그래프 (line)   
두 변수의 값을 점으로 표시하고 선분으로 이어 그린 형태의 그래프이다.   
보통 시계열 데이터를 표현할 때 사용한다. 연속적인 변화의 모양을 나타내는데 편리하다.
~~~r
# 작도법
geom_line(mapping = NULL, data = NULL, stat = "identity",
  position = "identity", na.rm = FALSE, show.legend = NA,
  inherit.aes = TRUE, ...)

# 예시
ggplot(d2, aes(x=displ)) + 
  geom_line(aes(y=m1, color='cty')) + 
  geom_line(aes(y=m2, color='hwy'), size=1) +
  scale_colour_manual("", breaks = c("cty", "hwy"),
                          values = c("red", "blue")) +
  xlab("x축") +
  xlim(1, 8) +
  scale_y_continuous("y축", limits = c(5, 45)) +
  labs(title = '타이틀', subtitle = '서브 타이틀') 
~~~
<br>

3) Histogram   
자료를 일정 계급(범위)로 나누고, 각 계급의 수량을 나타낸 그래프이다.   
막대그래프로 표현하기 때문에 크기를 비교하기 용이하다.   
~~~r
# 작도법
geom_histogram(mapping = NULL, data = NULL, stat = "bin",
  position = "stack", ..., binwidth = NULL, bins = NULL,
  na.rm = FALSE, show.legend = NA, inherit.aes = TRUE)

# 예시
ggplot(mpg, aes(displ)) +
  geom_histogram(aes(fill=class), 
                 binwidth = .3,     # 또는  bins = 5
                 col='black',       # line color
                 size=.1) +         # line size
  labs(title = 'Title', subtitle = 'Sub Title')

~~~
<br>

4) 막대 그래프 (bar)    
여러 항목의 수를 막대로 나타낸 그래프이다. 항목 간 수량의 많고 적음을 비교하기 쉽다.
~~~r
# 작도법
geom_bar(mapping = NULL, data = NULL, stat = "count",
  position = "stack", ..., width = NULL, binwidth = NULL,
  na.rm = FALSE, show.legend = NA, inherit.aes = TRUE)

# 예시
ggplot(mpg, aes(manufacturer)) +
  geom_bar(aes(fill=class),
           width = 0.5) +
  theme(axis.text.x = element_text(angle=45, vjust=0.6)) +   # 글씨의 기울기와 하단 맞춤(띄우기)
  scale_fill_discrete(name = "class") +      # legend
  labs(title = 'Title', subtitle = 'Sub Title')
~~~
<br>

5) 분포, 밀도 그래프 (density)   
데이터를 일정 범위로 나누고, 어떤 구간에 더 많이 분포/밀집되어 있는지 그린 그래프이다.   
단일 그래프도 있지만 복수로 분포도를 그려 상호 관계를 파악할 수 있다.
~~~r
# 작도법
geom_density(mapping = NULL, data = NULL, stat = "density",
  position = "identity", ..., na.rm = FALSE, show.legend = NA,
  inherit.aes = TRUE)

# 예시
ggplot(mpg, aes(cty)) +
  geom_density(aes(fill=factor(cyl)), alpha=0.8) +
  labs(title="밀도그래프", subtitle = "실린더수에 따른 시내연비의 밀도그래프",
       caption="Source: ggplot2::mpg",
       x = "도시 연비",
       fill = "실린더수")
~~~

### 2. data(성적.csv) 데이터에서 수학 성적이 90점 이상인 학생들에 대한 그래프 작도.
1) 성비가 표현된 학급별 학생수 막대그래프.
~~~r
~~~

2) 학급별 밀도그래프.
~~~r
~~~

### 3. 시각화 포트폴리오 1
~~~r
~~~

### 4. 시각화 포트폴리오 2
~~~r
~~~

