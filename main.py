import pandas as pd
from altair import Chart
import matplotlib as plt
import seaborn as sns
from ggplot import *
from matplotlib.pyplot import savefig


#TODO Prozedur für Features basierend auf hist daten
# - historische daten für nicht mehr als 1 aktie im RAM
# - nur einmal hist daten pro Aktie downloaden
# - monatliche Volas und Perfs berechnen
# - soweit zurück in Vergangenheit, wie es Daten zulassen
# - maximal 10 Jahre (bei 30 aktien also 2 matrizen mit max 3600 rows)

# TODO wie generalisiere ich monatl. Volas und Perfs?
# hist daily adj closing nach Monat of interest filtern
# need mind. 3 Werte damit ich var berechnen kann (-> 2 returns -> vola)
# daily log returns daraus berechnen
# daily log returns summieren für monatl log return
# aus daily log returns daily vola berechnen
# mit extrapol={'monthly': 252/12} extrapolieren auf monatl.

# TODO Methode, die mir Daten zu einem speziellen Monat, sortiert liefert

# TODO Vola und Perf berechnung auf diesen Daten
# (was für exceptions können kommen? soll robust sein)


# TODO Methode, die das monat für monat berechnet (in verg. gehend) bis daten "leer"
# TODO schreib methode: in RAM? oder lieber direkt schreiben? (vllt sicherer)
# TODO mögliche exceptions finden und sinnvoll behandeln


# TODO

# TODO company liste
# zumindest mit ticker symbolen und nem namen
# cool wären auch noch labels wie industry und isin

# TODO in schritt 2
# vermutlich liste per hand pflegen für boerse namen
# vllt lohnt es sich ein programmm zu schreiben, was die schätzen kann
