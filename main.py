import pandas as pd
from altair import Chart
import matplotlib as plt
import seaborn as sns
from ggplot import *
from matplotlib.pyplot import savefig

# wie generalisiere ich monatl. Volas und Perfs?
# ==============================================
# hist daily adj closing nach Monat of interest filtern
# need mind. 3 Werte damit ich var berechnen kann (-> 2 returns -> vola)
# daily log returns daraus berechnen
# daily log returns summieren für monatl log return
# aus daily log returns daily vola berechnen
# mit extrapol={'monthly': 252/12} extrapolieren auf monatl.

# Auf stock liegen nun alles high level aktionen
# - daten laden
# -features extrahieren
# - features speichern

# TODO prozedur, die durch den stock geht und alles schreibt

# TODO company liste
# zumindest mit ticker symbolen und nem namen
# cool wären auch noch labels wie industry und isin

# TODO in schritt 2
# vermutlich liste per hand pflegen für boerse namen
# vllt lohnt es sich ein programmm zu schreiben, was die schätzen kann
