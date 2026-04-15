# thesis_script.v7
# algorithms compute innovative/borrowed features per 100 yr
# Samir Ismail-Levitt - MA Thesis University of Chicago CMES
# work in progress - est. project end date c. April 2026

import csv
from collections import Counter
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import linregress
import numpy as np

ps = []
ws = []
cs = []
pa = []
oa = []

# termini post quem (in centuries; BCE = negative, CE = positive)
t_proto = -30
t_west = -25
t_cs = -20
t_arab = -8.53
t_old = 6.22

class Inventory(object):
    def __init__(self, filename):
        self.dict = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader,None) # skip header
            for row in reader:
                language = row[0]
                feature = hash(row[1])
                neg_pos = row[2]
                source = row[3]
                category = row[4]
                if row[5] == 'UNK':
                    if language == 'PS':
                        t = t_proto
                    elif language == 'WS':
                        t = t_west
                    elif language == 'CS':
                        t = t_cs
                    elif language == 'PA':
                        t = t_arab
                    elif language == 'OA':
                        t = t_old
                    else:
                        raise ValueError(f"Invalid language: {language}")
                else:
                    t = float(row[5])
                self.dict.append((language, feature, neg_pos, source, category))
                if language == 'PS':
                    ps.append((feature, neg_pos, source, category, t))
                elif language == 'WS':
                    ws.append((feature, neg_pos, source, category, t))
                elif language == 'CS':
                    cs.append((feature, neg_pos, source, category, t))
                elif language == 'PA':
                    pa.append((feature, neg_pos, source, category, t))
                elif language == 'OA':
                    oa.append((feature, neg_pos, source, category, t))
                else:
                    raise ValueError(f"Invalid language: {language}")

    def tally(self,language):
        neg = 0
        pos = 0
        inno = 0
        borrow = 0
        phono = 0
        morpho = 0
        synt = 0
        t = []

        for i in language:
            if i[1] == 'neg':
                neg += 1
            elif i[1] == 'pos':
                pos += 1
            if i[2] == 'inno':
                inno += 1
            elif i[2] == 'areal':
                borrow += 1
            if i[3] == 'phono':
                phono += 1
            elif i[3] == 'morpho':
                morpho += 1
            elif i[3] == 'synt':
                synt += 1
            if i[4] is not None:
                t.append(i[4])
        return(
            neg, pos, inno, borrow, phono, morpho, synt, t
        )

class Regression(Inventory):
    def __init__(self, filename):
        super().__init__(filename)
        
        self.ps_tally = self.tally(ps)
        self.ws_tally = self.tally(ws)
        self.cs_tally = self.tally(cs)
        self.pa_tally = self.tally(pa)
        self.oa_tally = self.tally(oa)

        all = ps + ws + cs + pa + oa
        
        self.t = [item[4] for item in all] # x-axis: termini post quem for all features in dataset
        self.y = [i for i in range(len(self.t))] # y-axis: cumulative feature count
        
        self.inno = []
        self.borrow = []
        len_inno = 0
        len_borrow = 0
        for i in all:
            if i[2] == 'inno':
                len_inno += 1
            if i[2] == 'areal':
                len_borrow += 1
            self.inno.append(len_inno)
            self.borrow.append(len_borrow)

    def graph(self):
        plt.plot(self.t, self.y, label='Novel Features', zorder=10)
        plt.plot(self.t, self.inno, label='Innovations', zorder=5)
        plt.plot(self.t, self.borrow, label='Borrowings', zorder=1)
        plt.xticks([-30, -27.5, -22.5, -14.265, -1.155], ['', 'West Semitic', 'Central Semitic', 'Proto-Arabic', 'Old Arabic'])
        plt.tick_params(axis='x', rotation=45, length=0)
        plt.vlines(x=[-30, -25, -20, -8.53, 6.22], ymin=0, ymax=len(self.y), colors='gray', linestyles='dashed', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.2)
        plt.xlabel('Time in Centuries (BCE = negative, CE = positive)')
        plt.show()

    # linear formula for innovativeness rate
    def innorate(self):
        ws_innorate = round(abs(self.ws_tally[2]/(t_west-t_proto)), 2)
        cs_innorate = round(abs(self.cs_tally[2]/(t_cs-t_west)), 2)
        pa_innorate = round(abs(self.pa_tally[2]/(t_proto-t_cs)), 2)
        oa_innorate = round(abs(self.oa_tally[2]/(t_old-t_proto)), 2)
        return(ws_innorate, cs_innorate, pa_innorate, oa_innorate)

    # linear formula for borrowing rate
    def borrowrate(self):
        ws_borrowrate = round(abs(self.ws_tally[3]/(t_west-t_proto)), 2)
        cs_borrowrate = round(abs(self.cs_tally[3]/(t_cs-t_west)), 2)
        pa_borrowrate = round(abs(self.pa_tally[3]/(t_proto-t_cs)), 2)
        oa_borrowrate = round(abs(self.oa_tally[3]/(t_old-t_proto)), 2)
        return(ws_borrowrate, cs_borrowrate, pa_borrowrate, oa_borrowrate)
    
    def bar(self):
        x = ['West Semitic', 'Central Semitic', 'Proto-Arabic', 'Old Arabic']
        y0 = list(self.innorate())
        y1 = list(self.borrowrate())
        rates = {
            'Innovations': np.array(y0),
            'Borrowings': np.array(y1),
            }
        
        bottom = np.zeros(4)

        for rate, rates in rates.items():
            p = plt.bar(x, rates, width=0.6, label=rate, bottom=bottom)
            bottom += rates
            plt.bar_label(p, label_type='center')

        plt.ylabel('Features per Century')
        plt.legend()
        plt.show()

    def compare(self):
        innovativeness = linregress(self.t, self.inno) # of entire dataset
        borrowness = linregress(self.t, self.borrow) # of entire dataset

        innorates = list(self.innorate())
        highest = max(innorates)
        lowest = min(innorates)
        if highest == self.ws_innorate:
            print('West Semitic has the highest innovativeness rate.')
            print(f'{highest} is the highest innovativeness rate, and {lowest} is the lowest.')
        borrowrates = list(self.borrowrate())


file = r"c:\Users\samrl\OneDrive\Desktop\thesis\innovations_data.csv"
run = Regression(file)
run.graph()
run.bar()
run.compare()