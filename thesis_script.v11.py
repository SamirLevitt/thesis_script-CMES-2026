# thesis_script.v11
# algorithms compute innovative/borrowed features per 100 yr
# Samir Ismail-Levitt - MA Thesis University of Chicago CMES
# April 30th, 2026

import csv
import matplotlib.pyplot as plt
from scipy.stats import bootstrap, poisson, chi2
import numpy as np
from math import log


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
        global ws, cs, pa, oa
        ws, cs, pa, oa = [], [], [], []    # reset globals

        self.dict = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                language = row[0]
                feature = hash(row[1])
                neg_pos = row[2]
                source = row[3]
                category = row[4]
                if row[5] == 'UNK':
                    if language == 'WS':
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
                if language == 'WS':
                    ws.append((feature, neg_pos, source, category, t))
                elif language == 'CS':
                    cs.append((feature, neg_pos, source, category, t))
                elif language == 'PA':
                    pa.append((feature, neg_pos, source, category, t))
                elif language == 'OA':
                    oa.append((feature, neg_pos, source, category, t))
                else:
                    raise ValueError(f"Invalid language: {language}")

    def tally(self, language):
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
        return (
            neg, pos, inno, borrow, phono, morpho, synt, t
        )


class Regression(Inventory):
    def __init__(self, filename):
        super().__init__(filename)

        self.ws_tally = self.tally(ws)
        self.cs_tally = self.tally(cs)
        self.pa_tally = self.tally(pa)
        self.oa_tally = self.tally(oa)

        all_feats = ws + cs + pa + oa
        all_feats = sorted(all_feats, key=lambda x: x[4])

        # x-axis: termini post quem for all features
        self.t = [item[4] for item in all_feats]
        # y-axis: cumulative feature count
        self.y = list(range(len(self.t)))

        self.all_tally = self.tally(all_feats)

        self.inno = []
        self.borrow = []
        for i in all_feats:
            if i[2] == 'inno':
                self.inno.append(i[1])
            if i[2] == 'areal':
                self.borrow.append(i[1])

    # linear formula for innovativeness rate
    def innorate(self):
        ws_innorate = abs(self.ws_tally[2] / (t_west - t_proto))
        cs_innorate = abs(self.cs_tally[2] / (t_cs - t_west))
        pa_innorate = abs(self.pa_tally[2] / (t_arab - t_cs))
        oa_innorate = abs(self.oa_tally[2] / (t_old - t_arab))
        all_innorate = abs(self.all_tally[2] / (t_old - t_proto))
        return (ws_innorate, cs_innorate, pa_innorate, oa_innorate, all_innorate)

    # linear formula for borrowing rate
    def borrowrate(self):
        ws_borrowrate = abs(self.ws_tally[3] / (t_west - t_proto))
        cs_borrowrate = abs(self.cs_tally[3] / (t_cs - t_west))
        pa_borrowrate = abs(self.pa_tally[3] / (t_arab - t_cs))
        oa_borrowrate = abs(self.oa_tally[3] / (t_old - t_arab))
        return (ws_borrowrate, cs_borrowrate, pa_borrowrate, oa_borrowrate)

    def graph(self):
        self.i1, self.i2, self.i3, self.i4, self.i_all = self.innorate()

        # Innovations (red)
        y_2 = 0 + self.i1 * (t_west - t_proto)
        y_3 = y_2 + self.i2 * (t_cs - t_west)
        y_4 = y_3 + self.i3 * (t_arab - t_cs)
        y_5 = y_4 + self.i4 * (t_old - t_arab)
        y_all = 0 + self.i_all * (t_old - t_proto)

        plt.plot([t_proto, t_west], [0, y_2], color='red', label='Innovations per Century')
        plt.plot([t_west, t_cs], [y_2, y_3], color='red')
        plt.plot([t_cs, t_arab], [y_3, y_4], color='red')
        plt.plot([t_arab, t_old], [y_4, y_5], color='red')

        plt.plot([t_proto, t_old], [0, y_all], color='purple', ls='--')

        # write innovation rates above segments
        mid1_x = (t_proto + t_west) / 2
        mid1_y = (0 + y_2) / 2
        plt.text(mid1_x, mid1_y + 0.5 * max(1, y_2), f'{round(self.i1, 2)}',
                 color='red', ha='center', va='bottom')

        mid2_x = (t_west + t_cs) / 2
        mid2_y = (y_2 + y_3) / 2
        plt.text(mid2_x, mid2_y + 0.2 * max(1, mid2_y), f'{round(self.i2, 2)}',
                 color='red', ha='center', va='bottom')

        mid3_x = (t_cs + t_arab) / 2
        mid3_y = (y_3 + y_4) / 2
        plt.text(mid3_x, mid3_y + 0.05 * max(1, mid3_y), f'{round(self.i3, 2)}',
                 color='red', ha='center', va='bottom')

        mid4_x = (t_arab + t_old) / 2
        mid4_y = (y_4 + y_5) / 2
        plt.text(mid4_x, mid4_y + 0.05 * max(1, mid4_y), f'{round(self.i4, 2)}',
                 color='red', ha='center', va='bottom')

        mid5_x = (t_proto + t_old) / 2
        mid5_y = (y_all) / 2
        plt.text(mid5_x, mid5_y - 0.1 * max(1, mid5_y), f'{round(self.i_all, 2)}',
                 color='purple', ha='center', va='top')

        plt.xticks(
            [-30, -27.5, -22.5, -14.265, -1.155],
            ['', 'West Semitic', 'Central Semitic', 'Proto-Arabic', 'Old Arabic']
        )
        plt.tick_params(axis='x', rotation=45, length=0)
        plt.vlines(x=-30, ymin=0, ymax=len(self.y), colors='gray',
                   linestyles='dashed', alpha=0)
        plt.vlines(x=[-25, -20, -8.53, 6.22], ymin=0, ymax=len(self.y),
                   colors='gray', linestyles='dashed', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.2)
        plt.xlabel('Time in Centuries (BCE = negative, CE = positive)')
        plt.show()

    def bar(self):
        # x-axis labels
        x = ['West Semitic', 'Central Semitic', 'Proto-Arabic', 'Old Arabic']

        # unpack tallies: (neg, pos, inno, borrow, phono, morpho, synt, t_list)
        ws_neg, ws_pos, ws_inno, ws_borr, ws_ph, ws_mo, ws_sy, _ = self.ws_tally
        cs_neg, cs_pos, cs_inno, cs_borr, cs_ph, cs_mo, cs_sy, _ = self.cs_tally
        pa_neg, pa_pos, pa_inno, pa_borr, pa_ph, pa_mo, pa_sy, _ = self.pa_tally
        oa_neg, oa_pos, oa_inno, oa_borr, oa_ph, oa_mo, oa_sy, _ = self.oa_tally

        # lists of counts per language, by category
        y_phono  = [ws_ph, cs_ph, pa_ph, oa_ph]
        y_morpho = [ws_mo, cs_mo, pa_mo, oa_mo]
        y_synt   = [ws_sy, cs_sy, pa_sy, oa_sy]

        rates_dict = {
            'Phonological': np.array(y_phono),
            'Morphological': np.array(y_morpho),
            'Syntactic': np.array(y_synt),
        }

        bottom = np.zeros(len(x))

        for label, values in rates_dict.items():
            p = plt.bar(x, values, width=0.6, label=label, bottom=bottom)
            bottom += values
            plt.bar_label(p, label_type='center')

        plt.ylabel('Number of Features')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def histogram(self):
        self.i1, self.i2, self.i3, self.i4, self.i_all = self.innorate()

        centuries = list(range(int(t_proto), int(t_old)))
        innorates = []
        colors = []

        for c in centuries:
            if c < t_west:
                innorates.append(self.i1)
                colors.append('tab:pink')
            elif c < t_cs:
                innorates.append(self.i2)
                colors.append('tab:purple')
            elif c < t_arab:
                innorates.append(self.i3)
                colors.append('tab:blue')
            else:
                innorates.append(self.i4)
                colors.append('tab:cyan')

        plt.bar(centuries, innorates, width=1.0, align='edge', color=colors)

        plt.ylabel('Innovations/Century')
        plt.xlabel('Century')

        from matplotlib.patches import Patch
        legend_patches = [
            Patch(color='tab:pink', label='West Semitic'),
            Patch(color='tab:purple', label='Central Semitic'),
            Patch(color='tab:blue', label='Proto-Arabic'),
            Patch(color='tab:cyan', label='Old Arabic'),
        ]
        plt.legend(handles=legend_patches, title='Language')

        mid_WS = (t_proto + t_west) / 2
        mid_CS = (t_west + t_cs) / 2
        mid_PA = (t_cs + t_arab) / 2
        mid_OA = (t_arab + t_old) / 2

        offset = 0.001 * max(self.i1, self.i2, self.i3, self.i4, 1)

        plt.text(mid_WS, self.i1 + offset, f'{self.i1:.2f}',
                 ha='center', va='bottom', color='tab:gray')
        plt.text(mid_CS, self.i2 + offset, f'{self.i2:.2f}',
                 ha='center', va='bottom', color='tab:gray')
        plt.text(mid_PA, self.i3 + offset, f'{self.i3:.2f}',
                 ha='center', va='bottom', color='tab:gray')
        plt.text(mid_OA, self.i4 + offset, f'{self.i4:.2f}',
                 ha='center', va='bottom', color='tab:gray')

        plt.show()


class HypothesisTest(Regression):
    def __init__(self, filename):
        super().__init__(filename)
        self.i1, self.i2, self.i3, self.i4, all_innorate = self.innorate()

        # reuse existing tallies
        ws_inno = self.ws_tally[2]
        cs_inno = self.cs_tally[2]
        pa_inno = self.pa_tally[2]
        oa_inno = self.oa_tally[2]

        self.ws_inno = ws_inno
        self.cs_inno = cs_inno
        self.pa_inno = pa_inno
        self.oa_inno = oa_inno

        self.all_innorate = all_innorate
        self.reconstructed_t = t_arab - t_proto
        self.reconstructed_tally = self.ws_inno + self.cs_inno + self.pa_inno
        self.reconstructed_innorate = round(
            abs(self.reconstructed_tally / self.reconstructed_t), 2
        )

        print(
            f'\n'
            f"Pre-Historic Innovativeness: {self.reconstructed_innorate:.2f} (btw. c. 3000 BCE & c. 853 BCE)\n"
            f"Semi-Attested Innovativeness: {self.i4:.6f} (btw. c. 853 BCE & c. 622 CE)\n"
            f"Old Arabic has {self.reconstructed_innorate - self.i4:.6f} less avg. innovations/cen. than its ancestors.\n"
        )

    def data(self):
        eps = 1e-9
        i1 = self.i1 if self.i1 != 0 else eps
        i2 = self.i2 if self.i2 != 0 else eps
        i3 = self.i3 if self.i3 != 0 else eps
        i4 = self.i4 if self.i4 != 0 else eps

        hy_x = []
        y = 0

        for _ in range(self.ws_inno):
            x = t_proto + y / i1
            hy_x.append(x)
            y += 1
        y_ws_end = y

        for _ in range(self.cs_inno):
            x = t_west + (y - y_ws_end) / i2
            hy_x.append(x)
            y += 1
        y_cs_end = y

        for _ in range(self.pa_inno):
            x = t_cs + (y - y_cs_end) / i3
            hy_x.append(x)
            y += 1
        y_pa_end = y

        for _ in range(self.oa_inno):
            x = t_arab + (y - y_pa_end) / i4
            hy_x.append(x)
            y += 1

        self.hypothesis_data = hy_x

    def bootstrap(self):
        # Ensure hypothesis_data has been generated
        if not hasattr(self, "hypothesis_data"):
            self.data()

        data = (self.hypothesis_data,)
        rng = np.random.default_rng()
        bootstrap_ci = bootstrap(data, np.std, method='basic', rng=rng)
        print(bootstrap_ci.confidence_interval)

    def poisson(self):
        # Global innorate
        lambda_global = self.all_innorate

        # Language timelines (lengths in centuries)
        L_ws = t_west - t_proto
        L_cs = t_cs - t_west
        L_pa = t_arab - t_cs
        L_oa = t_old - t_arab

        # Null Hypothesis: calculated innorates
        mu_ws = abs(lambda_global * L_ws)
        mu_cs = abs(lambda_global * L_cs)
        mu_pa = abs(lambda_global * L_pa)
        mu_oa = abs(lambda_global * L_oa)

        # Two-sided Poisson p-values
        def two_sided_p(k, mu):
            cdf = poisson.cdf(k, mu)
            sf = poisson.sf(k - 1, mu)
            return min(1.0, 2 * min(cdf, sf))

        p_ws = two_sided_p(self.ws_inno, mu_ws)
        p_cs = two_sided_p(self.cs_inno, mu_cs)
        p_pa = two_sided_p(self.pa_inno, mu_pa)
        p_oa = two_sided_p(self.oa_inno, mu_oa)

        print(f'''-- p-values via Poisson Dist. (H0: single global rate) --
                West Semitic:     {p_ws}
                Central Semitic:  {p_cs}
                Proto-Arabic:     {p_pa}
                Old Arabic:       {p_oa}
                ''')

    def _log_poisson_no_const(self, k, mu):
        """
        Log-likelihood of Poisson(k | mu), dropping log(k!) which cancels in LR.
        """
        if mu <= 0:
            return float('-inf')
        return k * log(mu) - mu

    def _lr_two_rate_split(self, N_left, T_left, N_right, T_right):
        """
        Likelihood-ratio test for a split into left and right intervals.

        N_left, N_right: counts of innovations on each side
        T_left, T_right: durations (in centuries) of each side

        Returns (LR, p_value) for H0: single rate vs H1: two rates.
        """

        # Totals
        N_tot = N_left + N_right
        T_tot = T_left + T_right

        # If no innovations at all, LR is undefined / 0
        if N_tot == 0 or T_tot == 0:
            return 0.0, 1.0

        # H0: single rate
        lam0 = abs(N_tot / T_tot)
        muL0 = lam0 * abs(T_left)
        muR0 = lam0 * abs(T_right)

        logL0 = self._log_poisson_no_const(N_left, muL0) + \
                self._log_poisson_no_const(N_right, muR0)

        # H1: different rates left vs right
        lamL = abs(N_left / T_left) if T_left != 0 else 0.0
        lamR = abs(N_right / T_right) if T_right != 0 else 0.0

        # Protect against mu<=0
        muL1 = lamL * abs(T_left) if lamL > 0 and T_left != 0 else 1e-12
        muR1 = lamR * abs(T_right) if lamR > 0 and T_right != 0 else 1e-12

        logL1 = self._log_poisson_no_const(N_left, muL1) + \
                self._log_poisson_no_const(N_right, muR1)

        LR = 2.0 * (logL1 - logL0)
        if LR < 0:
            # LR should not be negative
            LR = 0.0

        p_value = chi2.sf(LR, df=1)
        return LR, p_value

    def lr_all_boundaries(self):
        """
        Likelihood-ratio tests for all internal boundaries:
          - t_west: WS vs (CS+PA+OA)
          - t_cs:   (WS+CS) vs (PA+OA)
          - t_arab: (WS+CS+PA) vs OA

        Returns a dict with LR and p-values for each boundary.
        """

        results = {}

        # Precompute counts from tallies
        ws_inno = self.ws_inno
        cs_inno = self.cs_inno
        pa_inno = self.pa_inno
        oa_inno = self.oa_inno

        # ---- Boundary at t_west: WS | (CS+PA+OA) ----
        N_left = ws_inno
        T_left = t_west - t_proto

        N_right = cs_inno + pa_inno + oa_inno
        T_right = (t_old - t_west)

        LR_west, p_west = self._lr_two_rate_split(N_left, T_left, N_right, T_right)
        results['t_west'] = {'LR': LR_west, 'p': p_west}

        # ---- Boundary at t_cs: (WS+CS) | (PA+OA) ----
        N_left = ws_inno + cs_inno
        T_left = (t_cs - t_proto)

        N_right = pa_inno + oa_inno
        T_right = (t_old - t_cs)

        LR_cs, p_cs = self._lr_two_rate_split(N_left, T_left, N_right, T_right)
        results['t_cs'] = {'LR': LR_cs, 'p': p_cs}

        # ---- Boundary at t_arab: (WS+CS+PA) | OA ----
        # Even though t_arab is fixed, this tells you whether OA has
        # a distinct rate compared to the pre-Arabic segments combined.
        N_left = ws_inno + cs_inno + pa_inno
        T_left = (t_arab - t_proto)

        N_right = oa_inno
        T_right = (t_old - t_arab)

        LR_arab, p_arab = self._lr_two_rate_split(N_left, T_left, N_right, T_right)
        results['t_arab'] = {'LR': LR_arab, 'p': p_arab}

        return results

    def sd_pvalue_for_interval(self, start, end, n_sim=10000, two_sided=True, rng=None):
        """
        Compute empirical SD (from synthetic innovation times) and its p-value
        under H0: times are i.i.d. Uniform(start, end), conditional on count.

        Returns (sd_empirical, p_value). If < 2 points, returns (sd_empirical, None).
        """
        if rng is None:
            rng = np.random.default_rng()

        # Make sure synthetic data are available
        if not hasattr(self, "hypothesis_data"):
            self.data()

        # Restrict synthetic times to [start, end)
        times = [x for x in self.hypothesis_data if start <= x < end]
        n_inno = len(times)

        if n_inno <= 1:
            # SD is undefined or trivial with <=1 point
            sd_emp = np.std(times, ddof=1) if n_inno == 1 else np.nan
            return sd_emp, None

        times = np.array(times, dtype=float)
        sd_emp = np.std(times, ddof=1)  # empirical SD in centuries

        # Parametric bootstrap under H0: Uniform(start, end)
        sds = np.empty(n_sim, dtype=float)
        for i in range(n_sim):
            sim_times = rng.uniform(start, end, size=n_inno)
            sds[i] = np.std(sim_times, ddof=1)

        if two_sided:
            p = 2 * min(
                np.mean(sds <= sd_emp),
                np.mean(sds >= sd_emp)
            )
            p = min(p, 1.0)
        else:
            # Example one-sided: P(SD <= sd_emp)
            p = np.mean(sds <= sd_emp)

        return sd_emp, p

    def sd_pvalues_all_termini(self, n_sim=10000):
        """
        Compute empirical SD and p-values for SD on each side of each internal terminus.
        Uses local segments as 'sides'.
        """
        results = {}

        # t_west: left WS [t_proto, t_west), right CS [t_west, t_cs)
        sd_L_west, p_L_west = self.sd_pvalue_for_interval(t_proto, t_west, n_sim=n_sim)
        sd_R_west, p_R_west = self.sd_pvalue_for_interval(t_west, t_cs, n_sim=n_sim)
        results['t_west'] = {'left': (sd_L_west, p_L_west),
                             'right': (sd_R_west, p_R_west)}

        # t_cs: left CS [t_west, t_cs), right PA [t_cs, t_arab)
        sd_L_cs, p_L_cs = self.sd_pvalue_for_interval(t_west, t_cs, n_sim=n_sim)
        sd_R_cs, p_R_cs = self.sd_pvalue_for_interval(t_cs, t_arab, n_sim=n_sim)
        results['t_cs'] = {'left': (sd_L_cs, p_L_cs),
                           'right': (sd_R_cs, p_R_cs)}

        # t_arab (fixed): left PA [t_cs, t_arab), right OA [t_arab, t_old)
        sd_L_arab, p_L_arab = self.sd_pvalue_for_interval(t_cs, t_arab, n_sim=n_sim)
        sd_R_arab, p_R_arab = self.sd_pvalue_for_interval(t_arab, t_old, n_sim=n_sim)
        results['t_arab'] = {'left': (sd_L_arab, p_L_arab),
                             'right': (sd_R_arab, p_R_arab)}

        return results


file = r"c:\Users\samrl\OneDrive\Desktop\thesis\innovations_data.csv"
run = HypothesisTest(file)

#run.graph()
#run.bar()
#run.histogram()

#run.bootstrap()
run.poisson()

lr_results = run.lr_all_boundaries()

print("\nLikelihood-ratio tests for innovation rate breaks at internal boundaries")
for boundary, vals in lr_results.items():
    label = {
        't_west': 'West Semitic boundary (t_west)',
        't_cs':   'Central Semitic boundary (t_cs)',
        't_arab': 'Proto-Arabic boundary (t_arab)'
    }.get(boundary, boundary)

    LR = vals['LR']
    p  = vals['p']
    print(f"{label}: LR = {LR:.4f}, p = {p:.4f}")

sd_results = run.sd_pvalues_all_termini(n_sim=100000)

def print_sd_results(sd_results):
    print("\nStandard deviation of synthetic innovation times by terminus and side")
    print("  (SD in centuries; p = two-sided p-value vs Uniform null)\n")

    labels = {
        't_west': 'West Semitic boundary (t_west)',
        't_cs': 'Central Semitic boundary (t_cs)',
        't_arab': 'Proto-Arabic boundary (t_arab)',
    }

    for key, sides in sd_results.items():
        print(f"{labels.get(key, key)}:")
        for side in ['left', 'right']:
            sd, p = sides[side]
            side_label = "Left side " if side == 'left' else "Right side"
            if p is None:
                print(f"  {side_label}: SD = {sd:.3f} (p = n/a; insufficient data)")
            else:
                print(f"  {side_label}: SD = {sd:.3f} centuries, p = {p:.3f}")
        print()  # blank line between termini

print_sd_results(sd_results)