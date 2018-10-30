library(ggplot2)


theme_set(theme_bw())
df <- read.csv('data/riskPerformance_dowJones_5years_2018-10-17.csv', 
               stringsAsFactors = FALSE)


# einzelne Betrachtung

d <- df[df$Timeperiod == 'YTD', ]
ggplot(d, aes(x = Volatility, y = Performance)) +
  geom_text(aes(label = Company), nudge_y = 0.01 * max(d$Performance)) +
  geom_point(aes(color = Industry))


d <- df[df$Timeperiod == 'year1', ]
ggplot(d, aes(x = Volatility, y = Performance)) +
  geom_text(aes(label = Company), nudge_y = 0.01 * max(d$Performance)) +
  geom_point(aes(color = Industry))


d <- df[df$Timeperiod == 'year2', ]
ggplot(d, aes(x = Volatility, y = Performance)) +
  geom_text(aes(label = Company), nudge_y = 0.01 * max(d$Performance)) +
  geom_point(aes(color = Industry))


d <- df[df$Timeperiod == 'year3', ]
ggplot(d, aes(x = Volatility, y = Performance)) +
  geom_text(aes(label = Company), nudge_y = 0.01 * max(d$Performance)) +
  geom_point(aes(color = Industry))


d <- df[df$Timeperiod == 'year4', ]
ggplot(d, aes(x = Volatility, y = Performance)) +
  geom_text(aes(label = Company), nudge_y = 0.01 * max(d$Performance)) +
  geom_point(aes(color = Industry))

d <- df[df$Timeperiod == 'year5', ]
ggplot(d, aes(x = Volatility, y = Performance)) +
  geom_text(aes(label = Company), nudge_y = 0.01 * max(d$Performance)) +
  geom_point(aes(color = Industry))
# im Bereich 1-3 Jahre haben Boeing, Microsoft, Apple durchweg
# überdurchschnittliche Performance und durchschnittliche Vola
# Amazon hat bei weitem die beste Performance aber auch die
# zweithöchste Vola


# die letzten 3 Jahre, Trends
d <- df[df$Timeperiod %in% c('YTD', 'year1', "year2", "year3"), ]
d2 <- df[df$Timeperiod == 'year3', ]
ggplot(d, aes(x = Volatility, y = Performance)) +
  geom_line(aes(group = Company, color = Industry)) +
  geom_point(aes(color = Industry)) +
  geom_text(aes(x = Volatility, y = Performance, label = Company), data = d2)
# die Kurven Boeing, United Health Group, Microsoft sind am steilsten
# also Perf stieg viel schneller als Vola
# sind nach 3 Jahren auch die besten Performer (nach Amazon)
# Amazons Kurve ist auch recht steil, aber eben auch hohe Vola


# Perf / Vola
# die letzten 3 Jahre
d <- df[df$Timeperiod %in% c('YTD', 'year1', "year2", "year3"), ]
d$PerfPerVola <- d$Performance / d$Volatility
# die schlechtesten raussortieren (overplotting)
companies = c()
for (tp in c('YTD', 'year1', "year2", "year3")) {
  thr <- quantile(d$PerfPerVola[d$Timeperiod == tp])[2]
  companies <- c(companies, d$Company[d$Timeperiod == tp & d$PerfPerVola < thr])  
}
d <- d[!d$Company %in% unique(companies), ]
ggplot(d, aes(y = PerfPerVola, x = reorder(Company, -PerfPerVola))) +
  geom_col(aes(fill = Industry)) +
  facet_wrap(~Timeperiod, scales = "free") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
# year 1, YTD sind Coca Cola, Verizon, Pfizer, Merck gut
# year2, 3 sinds Boeing, United Health, Amazon (aber recht ausgeglichen)
# die werte sind um 6-7 also 7 mal mehr performance als vola



# Amazon -> vllt wegen AWS? => Microsoft guter Kandidat
# Boeing hat einen Sprung bei 2 Jahren, ob das nochmal passiert?
# Pfizer, Merck, Verizon, wieso nicht... 
# Amazon steigt sicher nicht mehr weiter so steil, aber ich denke die werden trotzdem noch gut sein
# United Health... wieso nicht


# Präferenz

# Microsoft
# Amazon
# Boeing
# United Health

# Merck
# Verizon (eher für sicher)
# Pfizer (eher für sicher)





