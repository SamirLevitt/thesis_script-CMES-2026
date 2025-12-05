# thesis_script.v4.py
# PROTO-ARABIC
# copy paste feature lists below
# remove any python non-compatible characters (e.g. IPA)


arab = """
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
arab_val1 = """
2
2
2
2
2
2
2
2
2
2
2
2
2
2
2
2
2
1
1
1
1
1
0
0
0
0
0
0
0
"""
arab_val2 ="""
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


arab_val3 ="""
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


arab_l = [l.strip() for l in arab.splitlines() if l.strip()] # feature list
arab_val1_l = [l.strip() for l in arab_val1.splitlines() if l.strip()] # weight list
arab_val2_l = [l.strip() for l in arab_val2.splitlines() if l.strip()] # category list
arab_val3_l = [l.strip() for l in arab_val3.splitlines() if l.strip()] # date list


arab_list = [[arab_l[i],arab_val2_l[i],arab_val3_l[i],arab_val1_l[i]] for i in range(len(arab_l))]


# summing weights
weight_arab = sum(map(int, arab_val1_l))
wp_arab = sum([int(arab_val1_l[i]) for i in range(len(arab_l)) if arab_val2_l[i]=="Phonetic"])
wm_arab = sum([int(arab_val1_l[i]) for i in range(len(arab_l)) if arab_val2_l[i]=="Morphological"])
ws_arab = sum([int(arab_val1_l[i]) for i in range(len(arab_l)) if arab_val2_l[i]=="Syntactic"])


#-------------------------------------------------------------------------------------------------------
# OLD ARABIC
# copy paste feature lists below
# remove any python non-compatible characters (e.g. IPA)


# feature list
old = """
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
# weight list
old_val1 = """
2
2
2
2
2
2
2
2
2
2
2
2
2
1
1
1
1
1
1
1
0
0
0
0
0
"""
# category list
old_val2 ="""
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
# timeframe list
old_val3 ="""
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


old_l = [l.strip() for l in old.splitlines() if l.strip()] # feature list
old_val1_l = [l.strip() for l in old_val1.splitlines() if l.strip()] # weight list
old_val2_l = [l.strip() for l in old_val2.splitlines() if l.strip()] # category list
old_val3_l = [l.strip() for l in old_val3.splitlines() if l.strip()] # date list


# list of Old Arabic features w/ weights, categories, dates
old_list = [[old_l[i],old_val2_l[i],old_val3_l[i],old_val1_l[i]] for i in range(len(old_l))]


# summing weights
weight_old = sum(map(int, old_val1_l))
wp_old = sum([int(old_val1_l[i]) for i in range(len(old_l)) if old_val2_l[i]=="Phonetic"])
wm_old = sum([int(old_val1_l[i]) for i in range(len(old_l)) if old_val2_l[i]=="Morphological"])
ws_old = sum([int(old_val1_l[i]) for i in range(len(old_l)) if old_val2_l[i]=="Syntactic"])


# terminus post quem (in centuries; BCE = negative, CE = positive)
t_proto = -30
t_west = -25
t_cs = -20
t_arab = -8.53
t_old = 6.22


# calculating avg. rates of innovativeness per century
mx_old = (((weight_old-weight_arab)/weight_arab)*100)/(t_old - t_arab) # total
try:
    mp_old = (((wp_old-wp_arab)/wp_arab)*100)/(t_old - t_arab) # phonological
except ZeroDivisionError as e:
    print("Ancestor Phon. Weight = 0", e)
try:
    mm_old = (((wm_old-wm_arab)/wm_arab*2)*100)/(t_old - t_arab) # morphological
except ZeroDivisionError as e:
    print("Ancestor Morph. Weight = 0", e)
try:
    ms_old = (((ws_old-ws_arab)/ws_arab)*100)/(t_old - t_arab) # syntactic
except ZeroDivisionError as e:
    ms_old = "null"
#--------------------------------------------------------------------------------
# PRINTING RESULTS
def tryround(value):
    try:
        return round(value,2)
    except TypeError as e:
        return "null"


from tabulate import tabulate

def roundyr(value):
    if value>= 0:
        return f"{tryround(abs(value)):g} CE"
    else:
        return f"{tryround(abs(value)):g} BCE"

data = [
    ["Termini post quem",roundyr(t_proto*100),roundyr(t_west*100),roundyr(t_cs*100),roundyr(t_arab*100),roundyr(t_old*100)],
    ["% Phono-Inno./100yr","wp_proto", "mp_west", "mp_cs", "mp_arab", (tryround(mp_old))],
    ["% Morph-Inno./100yr","wm_proto", "mm_west", "mm_cs", "mm_arab", (tryround(mm_old))],
    ["% Syntx-Inno./100yr","ws_proto", "ms_west", "ms_cs", "ms_arab", (tryround(ms_old))],
    ["% Total-Inno./100yr","total_proto", "(tryround(mx_west))", "(tryround(mx_cs))", "(tryround(mx_arab))", (tryround(mx_old))]
]


headers = ["","Proto-Semitic (Weights)", "West Semitic", "Central Semitic", "Proto-Arabic", "Old Arabic"]
print(tabulate(data, headers=headers, tablefmt="grid"))
