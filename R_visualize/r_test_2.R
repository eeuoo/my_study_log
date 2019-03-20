# 2. data(성적.csv) 데이터에서 수학 성적이 90점 이상인 학생들에 대한 그래프 작도.

load('data/data.rda')

# 1) 성비가 표현된 학급별 학생수 막대그래프.
ggplot(data %>% filter(math >= 90), aes(cls)) +
  geom_bar(aes(fill=gen), width = 0.5) +
  scale_fill_discrete(name = "성별") +      
  labs(x = '학급', y = '학생수', title = '학급별 학생수', subtitle = '(수학 성적 90점 이상)')

# 2) 학급별 밀도그래프.
ggplot(data %>% filter( math >= 90), aes(math)) +
  geom_density(aes(fill=factor(cls)),size = 0.2, alpha = 0.5) +
  labs(x = '성적', y = '밀도', title = '반별 수학 우수 학생', subtitle = '(수학 점수 90 이상)', fill = '학급')



