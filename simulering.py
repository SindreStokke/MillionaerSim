import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import statistics
import time

class Spiller():
    def __init__(self, spiller_nr):
        self.nr = spiller_nr
        self.antall_runder = 1
        self.terningkast = 0
        self.flyttehistorikk = {
            "flytt": [0],
            "forrige_felt": [0],
            "ankommet_felt": [1],
            "terningkast": [0],
            "runde": [self.antall_runder],
            "antall_kast": [0],
            "vandret_avstand": [0]
            }
    
    def kast_terninger(self):
        """
        Returnerer summen av de to terningenes øyne
        """
        terning_1 = random.randrange(1,6+1)
        terning_2 = random.randrange(1,6+1)
        terningkast = terning_1+terning_2
        self.terningkast = terningkast
    
    def flytt(self, ankommet_felt, terningkast):
        self.flyttehistorikk["flytt"].append(self.flyttehistorikk["flytt"][-1]+1)
        self.flyttehistorikk["forrige_felt"].append(self.flyttehistorikk["ankommet_felt"][-1])
        self.flyttehistorikk["ankommet_felt"].append(ankommet_felt)
        self.flyttehistorikk["terningkast"].append(terningkast)
        self.flyttehistorikk["runde"].append(self.antall_runder)
        self.flyttehistorikk["vandret_avstand"].append(self.flyttehistorikk["vandret_avstand"][-1]+terningkast)
        
        if terningkast == 0:
            self.flyttehistorikk["antall_kast"].append(self.flyttehistorikk["antall_kast"][-1])
        else:
            self.flyttehistorikk["antall_kast"].append(self.flyttehistorikk["antall_kast"][-1]+1)

    def flytt_fra_terningkast(self, antall_felter):
        felt_b4_flytt = self.flyttehistorikk["ankommet_felt"][-1]
        feltplussterningkast = felt_b4_flytt + self.terningkast
        antall_felter = antall_felter
        
        if feltplussterningkast > antall_felter:
            nytt_felt = feltplussterningkast - antall_felter
            self.antall_runder += 1
        else:
            nytt_felt = feltplussterningkast
        
        self.flytt(nytt_felt, self.terningkast)
    
    def dobbelt_kast(self, antall_felter, sjansekort, spillere):
        if self.terningkast == 12:
            self.kast_terninger()
            self.flytt_fra_terningkast(antall_felter)
            self.fengsel()
            self.sjansekort(sjansekort)
        
    def fengsel(self):
        felt_b4_flytt = self.flyttehistorikk["ankommet_felt"][-1]
        
        if felt_b4_flytt == 31:
            self.flytt(11, 0)
    
    def sjansekort(self, sjansekort):
        felt_b4_flytt = self.flyttehistorikk["ankommet_felt"][-1]
        if felt_b4_flytt in [3, 8, 18, 23, 34, 37]:
            """
            Sjekker om man har ankommet et sjansekort og utfører isåfall sjansekortets funksjon.
            """
            trukket_sjansekort = sjansekort[0]
            
            if trukket_sjansekort == 19:
                nytt_felt = 31
            if trukket_sjansekort == 20:
                nytt_felt = 31
            if trukket_sjansekort == 21:
                nytt_felt = 1
                self.antall_runder += 1
            if trukket_sjansekort == 22:
                nytt_felt = 1
                self.antall_runder += 1
            if trukket_sjansekort == 23:
                nytt_felt = 25
            if trukket_sjansekort == 24:
                nytt_felt = 12
                self.antall_runder += 1
            if trukket_sjansekort == 25:
                nytt_felt = 40
            if trukket_sjansekort == 26:
                if felt_b4_flytt in [18, 23]:
                    nytt_felt = 29
                else:
                    if felt_b4_flytt in [34, 37]:
                        self.antall_runder += 1
                    nytt_felt = 13
            if trukket_sjansekort == 27:
                nytt_felt = 36
            
            if trukket_sjansekort in [19, 20, 21, 22, 23, 24, 25, 26, 27]:
                self.flytt(nytt_felt, 0)
            
            sjansekort.pop(0)
            sjansekort.append(trukket_sjansekort)


def spilloppsett():
    """
    Oppretter alt det nødvendige for spillet
    """
    antall_felter = 40
    antall_spillere = 4
    antall_sjansekort = 35
    
    sjansekort = [n for n in range(1,antall_sjansekort+1)] # Genererer sjansekort
    random.shuffle(sjansekort) # Stokker sjansekortene
    spillere = [Spiller(spiller_nr+1) for spiller_nr in range(antall_spillere)]
    
    return antall_felter, sjansekort, spillere


def spill_loop(antall_turer, antall_felter, sjansekort, spillere):
    t0 = time.time()
    for tur in range(antall_turer):
        for spiller in spillere:
            spiller.kast_terninger()
            spiller.flytt_fra_terningkast(antall_felter)
            spiller.fengsel()
            spiller.sjansekort(sjansekort)
            spiller.dobbelt_kast(antall_felter, sjansekort, spillere)
    t1 = time.time()
    return t1-t0


def lagre_spillerdata_til_df(spillere):
    # Merger spillerdataene til en dictionary
    spillerdata = {
        "spiller": [],
        "flytt": [],
        "forrige_felt": [],
        "ankommet_felt": [],
        "terningkast": [],
        "runde": [],
        "antall_kast": [],
        "vandret_avstand": []
        }
    for spiller in spillere:
        for flytt in spiller.flyttehistorikk["flytt"]:
            spillerdata["spiller"].append(spiller.nr)
            spillerdata["flytt"].append(spiller.flyttehistorikk["flytt"][flytt])
            spillerdata["forrige_felt"].append(spiller.flyttehistorikk["forrige_felt"][flytt])
            spillerdata["ankommet_felt"].append(spiller.flyttehistorikk["ankommet_felt"][flytt])
            spillerdata["terningkast"].append(spiller.flyttehistorikk["terningkast"][flytt])
            spillerdata["runde"].append(spiller.flyttehistorikk["runde"][flytt])
            spillerdata["antall_kast"].append(spiller.flyttehistorikk["antall_kast"][flytt])
            spillerdata["vandret_avstand"].append(spiller.flyttehistorikk["vandret_avstand"][flytt])
    
    # Lagrer spillerdataene til DataFrame
    df = pd.DataFrame(spillerdata)
    
    return df


def statistikk(antall_felter, df, spillere):
    # Teller opp antall terningkast
    statistikk_terningkast = []
    for terningkast in [n for n in range(0,13)]:
        statistikk_terningkast.append(df[ (df["terningkast"] == terningkast)].shape[0])
    
    # Statistikk for spillerne
    statistikk_spillere = {
        "antall_runder": []
        }
    statistikk_spillere["antall_runder"] = [spiller.antall_runder for spiller in spillere]
    
    # Statistikk for feltene
    statistikk_felter = {
        "felter": [n for n in range(1, antall_felter+1)],
        "b_totalt": np.zeros(antall_felter), # antall besøk totalt
        "b_fra_trafikklys": np.zeros(antall_felter), # antall besøk fra trafikklys
        "b_fra_sjansekort": np.zeros(antall_felter), # antall besøk fra sjansekort
        "b_betalingspliktige": np.zeros(antall_felter), # antall betalingspliktige besøk
        "bpr_totalt": [], # antall besøk totalt per runde
        "bpr_betalingspliktige": [], # antall betalingspliktige besøk per runde
        "bpr_besøk_fra_sjansekort": [] # antall besøk fra sjansekort per runde
        }
    
    for felt in range(1,antall_felter+1):
        statistikk_felter["b_totalt"][felt-1] =\
            df[ df["ankommet_felt"] == felt ].shape[0]
        statistikk_felter["b_fra_trafikklys"][felt-1] =\
            df[ (df["ankommet_felt"] == felt) & (df["forrige_felt"] == 21) ].shape[0]
        statistikk_felter["b_fra_sjansekort"][felt-1] =\
            df[ (df["ankommet_felt"] == felt) &\
               (df["forrige_felt"].isin([19, 20, 21, 22, 23, 24, 25, 26, 27])) &\
                   (df["terningkast"] == 0) ].shape[0]
    
    statistikk_felter["b_betalingspliktige"] =\
        statistikk_felter["b_totalt"] - statistikk_felter["b_fra_trafikklys"]
    
    statistikk_felter["bpr_totalt"] =\
        statistikk_felter["b_totalt"] / sum(statistikk_spillere["antall_runder"])
    
    statistikk_felter["bpr_betalingspliktige"] =\
        statistikk_felter["b_betalingspliktige"] / sum(statistikk_spillere["antall_runder"])
    
    statistikk_felter["bpr_besøk_fra_sjansekort"] =\
        statistikk_felter["b_fra_sjansekort"] / sum(statistikk_spillere["antall_runder"])
    
    return statistikk_spillere, statistikk_felter, statistikk_terningkast


if __name__ == "__main__":
    # Setter opp spillet
    antall_felter, sjansekort, spillere = spilloppsett()
    
    # Gjennomfører turene
    antall_turer = int((5.6)*10**4)
    tidsbruk = spill_loop(antall_turer, antall_felter, sjansekort, spillere)
    
    # Statistikk
    df = lagre_spillerdata_til_df(spillere)
    statistikk_spillere, statistikk_felter, statistikk_terningkast = statistikk(antall_felter, df, spillere)
    
    # Printing
    print("Turer: " + str(antall_turer))
    #print("Runder: " + str(statistikk["runder_per_spiller"]))
    #print("Kast per runde: " + str(antall_turer/statistikk["runder_per_spiller"]))
    print("Tid brukt: " + str(round(tidsbruk, 2)) + " sekunder")
    
