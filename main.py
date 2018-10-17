import pandas as pd
from altair import Chart
import matplotlib as plt
import seaborn as sns
from ggplot import *
from matplotlib.pyplot import savefig

df = pd.read_pickle('data/riskPerformance_dowJones_5years_2018-10-17.pkl')

df.columns


d = df.loc[df['Timeperiod'] == 'YTD']
base = Chart(d).encode(
    x='Volatility',
    y='Performance',
    color='Industry'
)

p = ggplot(aes(x='Volatility', y='Performance', color='Industry'), data=d) +\
    geom_text(aes(label='Company')) +\
    geom_point() +\
    theme_bw()
p.save('asd.png')
ggsave('asd.png')

full = base.mark_circle() + base.mark_text(dx=15).encode(text='Company')
savefig('foo.png')
full.save('asd.png')

# TODO gescheite plotting lib raussuchen

import altair
