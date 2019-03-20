library('ggplot2')
library('dplyr')
theme_set(theme_gray(base_family="AppleGothic"))
par(family = "AppleGothic")
head(data)

save(data, file = 'data/data.rda')

# 1. mpg데이터에서 연도별 배기량에 따른 통합연비를 꺾은선으로 그리시오. (단, 2008년은 굵은 선으로 표현하시오)

d2 = mpg %>% group_by(year, displ) %>% 
  summarise(cty = mean(cty), hwy = mean(hwy))

levels(factor(d2$year)) 

ggplot() +
  geom_line(data=d2 %>% filter(year == 2008), aes(displ, cty, color = '2008 cty'), size = 1) +
  geom_line(data=d2 %>% filter(year == 2008), aes(displ, hwy, color = '2008 hwy'), size = 1) +
  geom_line(data=d2 %>% filter(year == 1999), aes(displ, cty, color = '1999 cty')) +
  geom_line(data=d2 %>% filter(year == 1999), aes(displ, hwy, color = '1999 hwy')) +
  xlab('배기량') +
  labs(colour = "")+
  xlim(1, 7) +
  scale_y_continuous("연비", limits = c(5, 50)) +
  labs(title = '연도별 통합 연비', subtitle = '(굵은 선은 2008년)')




# 2. data(성적.csv) 데이터에서 국어 성적이 80점 이상인 학생들의 수를 성비가 보이도록 학급별로 막대그래프를 그리시오.

ggplot(data %>% filter( kor >= 80) , aes(cls)) +
  geom_bar(aes(fill=gen), width = 0.5) +
  scale_fill_discrete(name = "성별") +      
  labs(x = '학급', y = '학생수', title = '국어 우수 학생', subtitle = '(80점 이상)')



# 3. 국어 성적이 95점 이상인 학생들의 점수별 밀도그래프를 그리시오.
ggplot(data %>% filter( kor >= 95 ), aes(kor)) +
  geom_density(aes(fill=factor(cls)),size = 0.2, alpha = 0.5) +
  labs(x = '성적', y = '밀도', title = '반별 국어 우수 학생', subtitle = '(국어 점수 A+ 이상)', fill = '학급')



# 4. midwest데이터에서 전체인구와 아시아계 인구의 관계를 알아보기 위한 그래프를 그리시오. (단, 전체인구는 50만명 이하, 아시아계인구는 1만명 이하만 표시되게)

ggplot(data=midwest, aes(x=total, y=asian)) + 
  geom_point() +
  geom_smooth() +
  scale_x_continuous("전체 인구", limits = c(0, 500000 )) +
  scale_y_continuous("아시아계 인구", limits = c(0, 10000)) +
  labs(title = '전체 인구과 아시아계 인구의 관계')
  


