library(ggplot2)
mpg = as.data.frame(ggplot2::mpg)
str(mpg)
summary(mpg)

  
#1 mpg 데이터에서 통합 연비(도시와 고속도로)가 높은 순으로 출력하시오.
mpg[order((mpg[,8]+mpg[,9])*-1),]


#2 mpg 데이터에서 생산연도별 연료 종류에 따른 통합연비를 연도순으로 출력하시오.
mpg
aggregate(data=mpg, cbind(cty,hwy)~(fl+year), sum)


#3 midwest 데이터를 data.frame으로 불러온 후, 전체인구와 아시아계인구 데이터의 특징을 설명하시오. (state별 비교 설명)
midwest = as.data.frame(ggplot2::midwest)

midwest
library('psych')

#midwest는 크게 state로 분류되고, 각 state는 다시 county로 세분화된다. state는 IL, IN, MI, OH, WI 총 5개이다. 
# 총 인구수, 인종별 인구수와 그 비율, 빈곤률, 교육 수준 등을 나타내고 있다. 
# state의 평균 인구는 8,401,788명, 아시아계 인구 평균은 114,534.6명이다. 
# 전체 인구와 아시아계 인구가 가장 많은 state는 IL로, IL의 전체 인구는 11,430,602명, 아시아계 인구는 285,311명이다. 
# 최소 전체 인구를 가진 state는 4,891,769명의 WI이며, 최소 아시아계 인구를 가진 state는 37,617명의 IN이다.
# state의 전체 인구를 보면 평균값인 8,401,788 중간에 분포하기 보다는 최솟값과 최댓값 양 쪽으로 나뉘어 몰려있는 형태이다. 
# 아시아계 인구는 평균값인 114,534.6을 중심으로 왼쪽, 즉 평균보다 더 작은 값들이 많이 분포되어 있다.  

describe(midwest$total)
summary(midwest$total)

describe(midwest$asian)
summary(midwest$asian)

aggregate(data=midwest, cbind(total,asian)~state, sum)


#4 poptotal 변수(컬럼)를 total로, popasian 변수를 asian으로 변수명을 변경하는 코드를 작성하시오.
colnames(midwest)[c(5,10)] = c("total","asian")


#5 전체 아시아계 인구수와, asian 변수를 이용해 `전체 아시아계 인구 대비 아시아계 인구 백분율` 파생변수(asianpct)를 추가하고, 히스토그램을 그리시오.
midwest$asianpct = (midwest$asian/sum(midwest$asian))*100
hist(midwest$asianpct)

#6 도시(state)기준으로 아시아계 인구가 어떻게 분포하는지 설명하시오.
midwest[,c('state','total','asian')]
total_asian = aggregate(data=midwest, cbind(total,asian)~state, sum)
total_asian['asianpct'] = (total_asian['asian']/total_asian['total'])*100
hist(total_asian$asianpct)
#아시아계 인구는 평균 1.24798%로 분포되어 있고, 최소는 IN의 0.6784979%, 최대는 IL의 2.496028%이다.


#7 아시아계 인구 백분율(asianpct)의 전체 평균을 구하고, 평균을 초과하면 "lg", 그 외는 "sm"을 부여하는 파생변수(asianrate)를 추가하는 코드를 작성하시오.
mean(midwest$asianpct)
midwest$asianrate = ifelse(midwest$asianpct > mean(midwest$asianpct), 'lg', 'sm')

#8 "lg"와 "sm"에 해당하는 지역이 얼마나 되는지 빈도 막대그래프(qplot)을 그려보시오.
qplot(midwest$asianrate)
