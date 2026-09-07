# =============================================================
# Analyse de données — Cours 1 : premiers pas en Python
# =============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

#   numpy      -> calcul numérique et vectoriel
#   pandas     -> tableaux de données et séries temporelles
#   matplotlib -> graphiques
#   statsmodels-> économétrie (MCO, tests, séries temporelles)

# -------------------------------------------------------------
# 1. Génération d'une variable pseudo-aléatoire de 40 points
# -------------------------------------------------------------

rng = np.random.default_rng(1)
x = rng.standard_normal(10)

print(x)


x = "hello world"
x = 1
x = 1.0
x = [1,2,3,4]

print(x)

# -------------------------------------------------------------
# 2. Accéder aux éléments
# -------------------------------------------------------------

print(x[0])      # 1er élément
print(x[1])      # 2e élément
print(len(x))    # nombre d'éléments

print(x[-1])     # dernier élément
print(x[:5])     # les 5 premiers
print(x[-3:])    # les 3 derniers


# -------------------------------------------------------------
# 3. Un échantillon plus grand
# -------------------------------------------------------------

x = rng.standard_normal(1000)


# -------------------------------------------------------------
# 4. Une boucle : y[i] = 2 * x[i]
# -------------------------------------------------------------

y = x.copy()                 # copie explicite

for i in range(len(x)):
    print(i)
    y[i] = 2 * x[i]

# la vectorisation est beaucoup plus rapide :
y = 2 * x

import time

t0 = time.perf_counter()
y_boucle = x.copy()
for i in range(len(x)):
    y_boucle[i] = 2 * x[i]
t_boucle = time.perf_counter() - t0

t0 = time.perf_counter()
y_vect = 2 * x
t_vect = time.perf_counter() - t0

print(f"boucle    : {t_boucle * 1000:.3f} ms")
print(f"vectorisé : {t_vect * 1000:.3f} ms")
print(f"facteur   : {t_boucle / t_vect:.0f}x")
print("résultats identiques :", np.allclose(y_boucle, y_vect))


# -------------------------------------------------------------
# 5. Une somme cumulée : y[i] = y[i-1] + x[i]
# -------------------------------------------------------------

y = x.copy()
for i in range(1, len(x)):
    y[i] = y[i - 1] + x[i]

# Version vectorisée
y = np.cumsum(x)

print("les deux versions coïncident :", np.allclose(y, np.cumsum(x)))


# -------------------------------------------------------------
# 6. Création d'une série temporelle
# -------------------------------------------------------------

dates = pd.period_range(start="2000Q1", periods=len(y), freq="Q")
z = pd.Series(y, index=dates)

print(z.head())
print(z.describe())


z.plot(figsize=(10, 4), title="Marche aléatoire, données trimestrielles")
plt.xlabel("Date")
plt.ylabel("Niveau")
plt.tight_layout()
plt.show()

print(z["2005":"2007"].head())
print(z.resample("Y").mean().head())


# -------------------------------------------------------------
# 7. Conditions
# -------------------------------------------------------------

i = 2

if x[i] > 0:
    msg = f"{i} => {x[i]} positif"
    print(msg)
else:
    msg = f"{i} => {x[i]} negatif"
    print(msg)
    print("not ok")

# -------------------------------------------------------------
# 8. Boucle + condition
# -------------------------------------------------------------

for i in range(20):
    signe = "positif" if x[i] > 0 else "negatif"
    print(f"{i} => {x[i]:.4f} {signe}")

positifs = x > 0
print("nombre de valeurs positives :", positifs.sum())
print("proportion :", positifs.mean())

# np.where est l'équivalent vectorisé du if/else
signes = np.where(x > 0, "positif", "negatif")
print(signes[:10])

 
# =============================================================
# 9. Lecture d'un fichier CSV
# =============================================================
 
FICHIER = "apple.csv"

apple = pd.read_csv("cours_1/data/apple.csv", parse_dates=["date"], index_col="date")
 
print(apple.head())
print(apple.shape)
print(apple.dtypes)
print(apple.describe())
print("valeurs manquantes :", apple.isna().sum().sum())
print("période :", apple.index.min().date(), "->", apple.index.max().date())
 
fig, ax1 = plt.subplots(figsize=(10, 4.5))
 
ax1.plot(apple.index, apple["adj_close"], linewidth=1.5)
ax1.set_title("Apple — cours ajusté", loc="left", fontsize=11)
ax1.set_xlabel("Date")
ax1.set_ylabel("Cours ($)")
 
fig.tight_layout()
plt.show()