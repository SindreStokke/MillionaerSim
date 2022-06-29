import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import statistics
import time

class Spiller():
    def __init__(self, spiller_nr):
        self.nr = spiller_nr
        self.felt = 1
        self.forrige_felt = 0
        self.antall_kast = 0
        self.antall_runder = 0
        self.terningkast = 0
        self.vandrede_felter = 0
        self.historikk = {"antall_kast": [self.antall_kast],
                          "felter": [self.felt],
                          "vandret": [self.vandrede_felter],
                          "terningkast": [0]}
        global feltenes_besok
        global antall_felter
        global data
        global sjansekort
        
        feltenes_besok["vanlige"][self.felt-1] += 1
    
    def kast_terninger(self):
        """
        Returnerer summen av de to terningenes øyne
        """
        terning_1 = random.randrange(1,6)
        terning_2 = random.randrange(1,6)
        terningkast = terning_1+terning_2
        self.terningkast = terningkast
        #print("Spiller "+str(self.nr)+" kastet "+str(self.terningkast))
        return terningkast


    def flytt(self):
        gammelt_felt = self.felt
        terningkast = self.terningkast
        feltplussterningkast = self.felt + terningkast
        
        if feltplussterningkast > antall_felter:
            nytt_felt = feltplussterningkast - antall_felter
            self.antall_runder += 1
        else:
            nytt_felt = feltplussterningkast
        
        self.antall_kast += 1
        self.vandrede_felter += terningkast
        self.forrige_felt = self.felt
        self.felt = nytt_felt
        if self.forrige_felt == 21:
            feltenes_besok["trafikklys"][self.felt-1] += 1
        else:
            feltenes_besok["vanlige"][self.felt-1] += 1
        
        self.historikk["antall_kast"].append(self.antall_kast)
        self.historikk["felter"].append(self.felt)
        self.historikk["vandret"].append(self.vandrede_felter)
        self.historikk["terningkast"].append(terningkast)
        #print("Spiller "+str(self.nr)+" flyttet fra felt "+str(gammelt_felt)+ " til felt "+str(self.felt))
        
    def fengsel(self):
        if self.felt == 31:
            self.forrige_felt = self.felt
            self.felt = 11
            feltenes_besok["vanlige"][self.felt-1] += 1
            self.antall_runder += 1
            #print("Spiller "+str(self.nr)+" havnet i fengsel og flyttet derfor til "+str(self.felt))
    
    def sjansekort(self):
        if self.felt in [3, 8, 18, 23, 34, 37]:
            """
            Sjansekortene
            """
            trukket_sjansekort = sjansekort[0]
            
            if trukket_sjansekort == 19:
                self.forrige_felt = self.felt
                self.felt = 31
            if trukket_sjansekort == 20:
                self.forrige_felt = self.felt
                self.felt = 31
            if trukket_sjansekort == 21:
                self.forrige_felt = self.felt
                self.felt = 1
                self.antall_runder += 1
            if trukket_sjansekort == 22:
                self.forrige_felt = self.felt
                self.felt = 1
                self.antall_runder += 1
            if trukket_sjansekort == 23:
                self.forrige_felt = self.felt
                self.felt = 25
            if trukket_sjansekort == 24:
                self.forrige_felt = self.felt
                self.felt = 12
                self.antall_runder += 1
            if trukket_sjansekort == 25:
                self.forrige_felt = self.felt
                self.felt = 40
            if trukket_sjansekort == 26:
                if self.felt in [18, 23]:
                    self.forrige_felt = self.felt
                    self.felt = 29
                else:
                    if self.felt in [34, 37]:
                        self.antall_runder += 1
                    self.forrige_felt = self.felt
                    self.felt = 13
            if trukket_sjansekort == 27:
                self.forrige_felt = self.felt
                self.felt = 36
            
            if trukket_sjansekort in [19, 20, 21, 22, 23, 24, 25, 26, 27]:
                feltenes_besok["vanlige"][self.felt-1] += 1
                #print("Spiller "+str(self.nr)+" havnet på sjansekortet "+ str(trukket_sjansekort) +" og flyttet derfra til "+str(self.felt))
            else:
                #print("Spiller "+str(self.nr)+" havnet på sjansekortet "+ str(trukket_sjansekort) +" og flyttet ikke videre")
                pass
            sjansekort.pop(0)
            sjansekort.append(trukket_sjansekort)


def generer_spillere(antall_spillere):
    # Genererer tilfeldige spillere
    spillere = [Spiller(spiller_nr+1) for spiller_nr in range(antall_spillere)]
    return spillere


def stats(feltenes_besok, spillere):
    # Stats: andeler
    besoksandel = []
    antall_vanlige_gatebesok = sum(feltenes_besok["vanlige"])
    antall_gatebesok_etter_trafikklys = sum(feltenes_besok["trafikklys"])
    totalt_antall_gatebesok = sum(feltenes_besok["vanlige"])+sum(feltenes_besok["trafikklys"])
    for n in feltenes_besok["vanlige"]:
        besoksandel.append(n/totalt_antall_gatebesok)
    
    gj_besoksandel = sum(besoksandel)/len(besoksandel)
    median_besoksandel = statistics.median(besoksandel)
    
    besoksandel_ift_gj = besoksandel/gj_besoksandel-1
    besoksandel_ift_median = besoksandel/median_besoksandel-1
    
    # Stats per runde
    rundesum = 0
    for spiller in spillere:
        rundesum += spiller.antall_runder
    runder_per_spiller = rundesum/len(spillere)
    
    besok_per_runde_per_spiller = feltenes_besok["vanlige"]/rundesum
    
    stats = {"totalt_antall_gatebesok": totalt_antall_gatebesok,
             "besoksandel": besoksandel,
             "gj_besoksandel": gj_besoksandel,
             "median_besoksandel": median_besoksandel,
             "besoksandel_ift_gj": besoksandel_ift_gj,
             "besoksandel_ift_median": besoksandel_ift_median,
             "runder_per_spiller": runder_per_spiller,
             "besok_per_runde_per_spiller": besok_per_runde_per_spiller}
    
    return stats


if __name__ == "__main__":
    feltenes_besok = {"vanlige": np.zeros(40),
                      "trafikklys": np.zeros(40)}
    antall_felter = 40
    sjansekort = [n for n in range(1,36)]
    random.shuffle(sjansekort) # Stokker sjansekortene
    
    # Genererer og utplasser spillere
    spillere = generer_spillere(4)
    
    # Starter grafikk
    
    
    # Gjennomfører turene
    t0 = time.time()
    turer = int((5.6)*10**6)
    for tur in range(turer):
        for spiller in spillere:
            spiller.kast_terninger()
            spiller.flytt()
            spiller.fengsel()
            spiller.sjansekort()
    t1 = time.time()
    
    stats = stats(feltenes_besok, spillere)
    
    # Printing
    print("Turer: " + str(turer))
    print("Runder: " + str(stats["runder_per_spiller"]))
    print("Kast per runde: " + str(turer/stats["runder_per_spiller"]))
    print("Tid brukt: " + str(round(t1 - t0, 2)) + " sekunder")
    
    # Lagrer resultatene til DataFrame
    df = pd.DataFrame(columns=["Rundenr"])
