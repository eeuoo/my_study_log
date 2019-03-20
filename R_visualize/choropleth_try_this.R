# 1. 다음과 같이 미국의 범죄율을 한번에 작도하시오.

head(USArrests)

chodata = rownames_to_column(USArrests, var = 'state')
chodata$state = tolower(chodata$state)
head(chodata)

usmap = map_data('state')
head(usmap)

ggChoropleth(data=chodata, 
             aes(map_id=state),
             map = usmap,
             title = '..',
             reverse = F,
             interactive = T)


# 2. 미국 범죄율의 Rape부분을 단계 구분도로 작성하시오. (단, 툴팁은 그림과 같이 표현하고,  클릭시 해당 state의 wikipedia 페이지를 보이도록 HTML로 저장하시오) http://en.wikipedia.org/wiki/wisconsin

tooltips = paste0(
  sprintf("<p><strong>%s</strong></p>", as.character(chodata$state)),
  '<table>',
  '  <tr>',
  sprintf('<td>%.0f / %.0f 만</td> ', chodata$Rape, chodata$UrbanPop * 10),
  '  </tr>',
  '</table>')

onclick = sprintf('window.open("http://en.wikipedia.org/wiki/%s")', as.character(chodata$state))

ggplot(chodata, aes(map_id = state)) + 
  geom_map_interactive(aes(fill = Rape,
                           tooltip = tooltips,
                           onclick = onclick),
                       map = usmap) + 
  expand_limits(x = usmap$long, y = usmap$lat) +
  labs(title="USA Rape", fill = 'Rape') + 
  scale_fill_gradient2('Rape', low='red', mid = 'green', high = 'blue') -> usa_rape

ggiraph(code = print(usa_rape))
girafe(ggobj = usa_rape)


# 3. 우리나라 시도별 결핵환자수(kormaps::tbc)를 단계 구분도로 작성하시오. (단, 환자수는 2006년부터 2015년 통합, NA인 지역은 0으로 표시할 것)

tbc = kormaps2014::tbc

# 결측 처리
table(is.na(tbc))
tbc[is.na(tbc)] = 0   
str(tbc)

tooltips2 = paste0(
  sprintf("<p><strong>%s</strong></p>", as.character(tbc2$name)),
  '<table>',
  '  <tr>',
  sprintf('<td>결핵환자수 : %.0f 만</td>', tbc2$sum_newpts),
  '  </tr>',
  '</table>')

tbc$year =  as.character(tbc$year)

tbc2 = tbc %>% filter( year >= '2006' & year <= '2015' ) %>% group_by(name, code) %>% summarise(sum_newpts = sum(NewPts))
head(tbc2)

tbc_map = ggplot(tbc2, aes(data = sum_newpts, map_id = code)) +
  geom_map_interactive( aes(fill = sum_newpts,
                            tooltip = tooltips2), map = kormap1, color = 'gray', size = 0.3) + 
  expand_limits(x = kormap1$long, y = kormap1$lat) +
  scale_fill_gradient2('인구', low='green', mid = 'lightyellow', high = 'red') +
  xlab('경도') + ylab('위도') + 
  labs(title="시도별 결핵환자수")

ggiraph(code = print(tbc_map))
girafe(ggobj = tbc_map)

tbc2$name

