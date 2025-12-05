# thesis_script.v6.py
# algorithms compute innovative/borrowed features per 100 yr
# MA Thesis University of Chicago CMES
# work in progress - est. project end date c. April 2026

from collections import Counter

# PROTO-ARABIC
# feature list
feat_arab = """
Imperfect *yaqtulu
G-stem prefix a- w/ theme u/i
u~i passive perfect vowel harmony
-at levelling replacing -t
3fp perf. *-a -> -na
mafūl G-stem passive participle
fam -> fi prep. grammaticalized
anaphoric 3p pronouns -> dalika dems.
Nunation on nominal heads of indefinite asyndetic relative clauses
complex/assymetrical negation
pre-verbal tense/aspect qad, sawfa, etc
anna complementizer
ind. obj. pron. base *(iy)yā
a-marked subj. prefix (yaf'ala)
atawa -> hat quasi-supplative imper.
prepositions 'ind 'an 'lada
vocative -*mma eg Allahumma"
mimation -> nunation
s1 s3 merger
loss of 'anaku
? loss of qataal"
Loss of fem. -t
"Definite article
Triphthong reduction
Pharyngealization of emphatics
*p > f
Broken plurals
L-stem
Conjugation suffix leveling t > k"
"""

# timeframe of features
time_arab = """
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
2000-1000 BCE
UNK
UNK
UNK
UNK
UNK
UNK
"""

# genetic ~ areal qualification of features
model_arab = """
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Areal
Areal
Areal
Areal
Areal
Areal
Areal
"""

# category of features
cat_arab = """
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Phonetic
Phonetic
Morphological
Morphological
Morphological
Morphological
Phonetic
Phonetic
Phonetic
Morphological
Morphological
Morphological
"""

# OLD ARABIC
## feature list
feat_old = """
perfective use of active participle
fem -at -> -ah
-a precative mood inflection
-n possibly energic
h- proclitic demonstrative
/ḏā/ ms dem.
ly plural dem.
alla- based relative pronouns
rel. pronoun ms ḏ/ḏVV
rel.p. agreement in definiteness hḏ /haḏḏVV
rel.p. fs ḏt */ḏāʔ(a)t
rel.p. plural dw */ḏū/
rel.p. fs lt /allatī/
Partial loss of case
adnonimal demonstrative syntax
loss of nunation
aspirated p
al coda assimilation to coronals
nominal infinitive
asyndetic clauses?
definite article
triphthongs
s2 voiceless lateral fricative
glottalized emphatics
t- onset fs dem.
"""

# timeframe of features
time_old = """
UNK
300 CE (4th cen.)
UNK
UNK
UNK
568 CE
UNK
UNK
UNK
UNK
UNK
UNK
UNK
550 CE (6th cen.)
267 CE
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
UNK
"""

# genetic ~ areal qualification of features
model_old = """
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Genetic
Areal
Retention
Retention
Retention
Retention
"""

# category of features
cat_old = """
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Morphological
Syntactic
Phonetic
Phonetic
Phonetic
Syntactic
Syntactic
Morphological
Phonetic
Phonetic
Phonetic
Morphological
"""

#-----

# dictionaries
d_arab = {}
d_old = {}

# strings to lists
def string2list(string):
    return [l.strip() for l in string.splitlines() if l.strip()]

# zipping lists (values)
def ziplist(time,model,cat):
    return [list(v) for v in list(zip(time,model,cat))]

# populating dict w/ zipped lists
def populate(keys,dictionary,values):
    for i in range(1,len(keys)):
        dictionary[f"Feat. {i}"] = values[i]

populate(string2list(feat_arab),d_arab,ziplist(string2list(time_arab),string2list(model_arab),string2list(cat_arab)))
populate(string2list(feat_old),d_old,ziplist(string2list(time_old),string2list(model_old),string2list(cat_old)))

# termini post quem (in centuries; BCE = negative, CE = positive)
t_proto = -30
t_west = -25
t_cs = -20
t_arab = -8.53
t_old = 6.22

# tallying features by genetic/areal, category (WIP)
def gen(model):
    return Counter(model)["Genetic"]
def areal(model):
    return Counter(model)["Areal"]

# linear formula for innovativeness rate
def innorate(model,t1,t0):
    return abs(gen(string2list(model))/(t1-t0))

# linear formula for borrowing rate
def borrowrate(model,t1,t0):
    return abs(areal(string2list(model))/(t1-t0))

#--------------------------------------------------------------------------------
# PRINTING RESULTS
from tabulate import tabulate

def tryround(value):
    try:
        return round(value,3)
    except TypeError as e:
        return "null"

def roundyr(value):
    if value>= 0:
        return f"{tryround(abs(value)):g} CE"
    else:
        return f"{tryround(abs(value)):g} BCE"

data = [
    ["Termini post quem",roundyr(t_proto*100),roundyr(t_west*100),roundyr(t_cs*100),roundyr(t_arab*100),roundyr(t_old*100)],
    ["Innovativeness", "WIP","WIP","WIP",f"{tryround(innorate(model_arab,t_arab,t_cs))} features/century",f"{tryround(innorate(model_old,t_old,t_arab))} features/century"],
    ["Borrowing Rate", "WIP","WIP","WIP",f"{tryround(borrowrate(model_arab,t_arab,t_cs))} features/century",f"{tryround(borrowrate(model_old,t_old,t_arab))} features/century"],
]

headers = ["","Proto-Semitic","West Semitic","Central Semitic","Proto-Arabic","Old Arabic"]
print(tabulate(data, headers=headers, tablefmt="grid"))

#--------------------------------------------------------------------------------
# VISUALIZING DATA
import numpy as np

def poissondist():
    np.random.poisson()
    pass

# to do:
# innovativeness/borrowing rate by category
# poisson distribution
# visualize data