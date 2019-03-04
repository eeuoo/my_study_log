library(ggplot2)
mpg = as.data.frame(ggplot2::mpg)
str(mpg)
summary(mpg)


#1 mpg 데이터에서 통합 연비(도시와 고속도로)가 높은 순으로 출력하시오.
mpg[order((mpg[,8]+mpg[,9])*-1),]


#2 mpg 데이터에서 생산연도별 연료 종류에 따른 통합연비를 연도순으로 출력하시오.
aggregate(data=mpg, (cty+hwy)~(fl+year), mean)
