# thesis_script.v2.py
## DATA INCOMPLETE - THIS IS A TEST

# PROTO SEMITIC
# copy paste feature lists below
# remove any python non-compatible characters (e.g. IPA)

# phonological
list_p_proto = """
a

"""
# morphological
list_m_proto = """
b

"""
# syntactic
list_s_proto = """
c

"""
# list of Proto-Semitic phonological, morphological, syntactic features
p_proto = [l.strip() for l in list_p_proto.splitlines() if l.strip()]
m_proto = [l.strip() for l in list_m_proto.splitlines() if l.strip()]
s_proto = [l.strip() for l in list_s_proto.splitlines() if l.strip()]

# multiplicities of feature lists
wp_proto = len(p_proto)
wm_proto = len(m_proto)
ws_proto = len(s_proto)

# summing total weight of Proto-Semitic in the century it split
wc_proto = wp_proto*1, wm_proto*2, ws_proto*1
total_proto = sum(wc_proto)

x_proto = 0

print("Proto-Semitic")
print("     Phonological Weight     ",wp_proto*1)
print("     Morphological Weight    ",wm_proto*2)
print("     Semantic Weight         ",ws_proto*1)
print("     Total Weight            ",total_proto)

#--------------------------------------------------------------------------------

# CENTRAL SEMITIC
# copy paste feature lists below
# remove any python non-compatible characters (e.g. IPA)

# phonological
list_p_cs = """
a

"""
# morphological
list_m_cs = """
b

"""
# syntactic
list_s_cs = """
c

"""
# list of Proto_Arabic phonological, morphological, syntactic features
p_cs = [l.strip() for l in list_p_cs.splitlines() if l.strip()]
m_cs = [l.strip() for l in list_m_cs.splitlines() if l.strip()]
s_cs = [l.strip() for l in list_s_cs.splitlines() if l.strip()]

# multiplicities of feature lists
wp_cs = len(p_cs)
wm_cs = len(m_cs)
ws_cs = len(s_cs)

# summing total weight of Central Semitic in the century it split
wc_cs = wp_cs*1, wm_cs*2, ws_cs*1
total_cs = sum(wc_cs)

# calculating rate of change per century
x_cs = 6 # century in which Central Semitic split
t_cs = x_cs-x_proto # centuries between Proto-Semitic split and Central Semitic split 
mx_cs = (((total_cs-total_proto)/total_proto)*100)/t_cs # avg. rate of change per century


print("Central Semitic")
print("     Phonological Weight     ",wp_cs*1)
print("     Morphological Weight    ",wm_cs*2)
print("     Semantic Weight         ",ws_cs*1)
print("     Total Weight            ", total_cs)
print("Rate of Change per century   ",(round(mx_cs,2)),"%")

#--------------------------------------------------------------------------------

# PROTO-ARABIC
# # copy paste feature lists below
# remove any python non-compatible characters (e.g. IPA)
# phonological
list_p_arab = """
s1 s3 merger
"""
# morphological
list_m_arab = """
"Imperfect *yaqtulu
G-stem prefix a- w/ theme u/i
u~i passive perfect vowel harmony
mimation -> nunation
-at levelling replacing -t
3fp perf. *-a -> -na
mafūl G-stem passive participle
fam -> fi prep. grammaticalized
anaphoric 3p pronouns -> dalika dems.
Nunation on nominal heads of indefinite asyndetic relative clauses
complex/assymetrical negation
pre-verbal tense/aspect qad, sawfa, etc
'anna complementizer
ind. obj. pron. base *(iy)yā
a-marked subj. prefix (yaf'ala)
atawa -> hat quasi-supplative imper.
prepositions 'ind 'an 'lada
vocative -*mma eg Allahumma"
"""
# syntactic
list_s_arab = """


"""
# list of Proto_Arabic phonological, morphological, syntactic features
p_arab = [l.strip() for l in list_p_arab.splitlines() if l.strip()]
m_arab = [l.strip() for l in list_m_arab.splitlines() if l.strip()]
s_arab = [l.strip() for l in list_s_arab.splitlines() if l.strip()]

# multiplicities of feature lists
wp_arab = len(p_arab)
wm_arab = len(m_arab)
ws_arab = len(s_arab)

# summing total weight of Proto-Arabic in the century it split
wc_arab = wp_arab*1, wm_arab*2, ws_arab*1
total_arab = sum(wc_arab)


# calculating rate of change per century
x_arab = 9 # century in which Proto-Arabic split
t_arab = x_arab-x_cs # centuries between Ccentral Semitic split and Proto-Arabic split 
mx_arab = (((total_arab-total_cs)/total_cs)*100)/t_arab # avg. rate of change per century


print("Proto-Arabic")
print("     Phonological Weight     ",wp_arab*1)
print("     Morphological Weight    ",wm_arab*2)
print("     Semantic Weight         ",ws_arab*1)
print("     Total Weight            ", total_arab)
print("Rate of Change per century   ",(round(mx_arab,2)),"%")