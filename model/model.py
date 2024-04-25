import copy
from collections import defaultdict
from datetime import date

from database.meteo_dao import MeteoDao
from model.tappa import Tappa


class Model:
    def __init__(self):
        self.dict_situazioni = {}
        self.inizializza_situa_localita()
        self._localita = self.dict_situazioni.keys()

        self.possibili_percorsi = []
        self.soluzioni = []

    def inizializza_situa_localita(self):
        situazioni = MeteoDao.get_all_situazioni()
        for situa in situazioni:
            if self.dict_situazioni.get(situa.localita) is None:
                self.dict_situazioni[situa.localita] = []
            self.dict_situazioni[situa.localita].append(situa)

    def umidita_media_citta(self, localita: str, mese: date.month):
        umidita_tot = 0
        num_situa = 0
        for situa in self.dict_situazioni[localita]:
            if situa.data.month == mese:
                umidita_tot += situa.umidita
                num_situa += 1
            elif mese == 0:
                umidita_tot += situa.umidita
                num_situa += 1

        return umidita_tot / num_situa

    # funzioni per ricorsione:
    def min_percorso(self):
        minimo = 1e16
        soluzioni = []
        for percorso in self.possibili_percorsi:
            if percorso[-1].costo < minimo:
                soluzioni = [percorso]
                minimo = percorso[-1].costo
            elif percorso[-1].costo == minimo:
                soluzioni.append(percorso)

        return soluzioni

    def get_situa(self, localita, mese, giorno):
        for situa in self.dict_situazioni[localita]:
            if situa.data.month == mese and situa.data.day == giorno:
                return situa

    def calcola_costo(self, percorso_parziale):
        costo_tot = 0
        giorni_in_cui_cambia = []

        # costo variabile
        for tappa_old in percorso_parziale:
            i = percorso_parziale.index(tappa_old)
            tappa_precedente = percorso_parziale[i - 1]
            if tappa_old.localita != tappa_precedente.localita:
                giorni_in_cui_cambia.append(i)
            costo_tot += tappa_old.umidita

        # costo fisso
        for giorno in giorni_in_cui_cambia:
            if giorno == 0:
                pass
            elif giorno == len(percorso_parziale):
                costo_tot += 100
            elif giorno == len(percorso_parziale) - 1:
                costo_tot += 200
            else:
                costo_tot += 200

        return costo_tot

    def filtro_vincoli(self, percorso_parziale):
        # più di 6 giorni nella stessa città anche non consecutivi
        giorni_fermo = 0
        for localita in self._localita:
            for tappa in percorso_parziale:
                if tappa.localita == localita:
                    giorni_fermo += 1
            if giorni_fermo > 6:
                return False
            else:
                giorni_fermo = 0

        # deve stare almeno 3 giorni di seguito in una città
        i = 0
        cambiata = True
        while i < len(percorso_parziale) - 1:
            if i == 0 or percorso_parziale[i].localita != percorso_parziale[i - 1].localita:
                cambiata = True
            if cambiata:
                if i == len(percorso_parziale) - 2:
                    break
                elif (percorso_parziale[i].localita != percorso_parziale[i + 1].localita or
                        percorso_parziale[i].localita != percorso_parziale[i + 2].localita):
                    return False
                else:
                    cambiata = False
                    i += 3
            else:
                i += 1

        return True

    # ALGORITMO:
    def cerca_percorso_ottimo(self, mese):
        self.optimization_recursive([], 15, mese)
        self.soluzioni = self.min_percorso()

    def optimization_recursive(self, percorso_parziale, giorni, mese):
        if percorso_parziale == []:
            self.soluzioni = []
            self.possibili_percorsi = []

        if len(percorso_parziale) == giorni:
            self.possibili_percorsi.append(copy.deepcopy(percorso_parziale))
            #print(percorso_parziale)
        else:
            for localita in self._localita:
                situa = self.get_situa(localita, mese, len(percorso_parziale) + 1)
                if situa is None:
                    pass
                else:
                    tappa = Tappa(situa.localita, situa.data, situa.umidita, 0)
                    percorso_parziale.append(tappa)
                    tappa.costo = self.calcola_costo(percorso_parziale)
                    if self.filtro_vincoli(percorso_parziale):
                        # print(percorso_parziale)
                        self.optimization_recursive(percorso_parziale, giorni, mese)
                    percorso_parziale.pop()

'''[Tappa(localita='Milano', data=datetime.date(2013, 2, 1), umidita=100, costo=100)
    , Tappa(localita='Milano', data=datetime.date(2013, 2, 2), umidita=99, costo=199)
    , Tappa(localita='Milano', data=datetime.date(2013, 2, 3), umidita=58, costo=257)
    , Tappa(localita='Torino', data=datetime.date(2013, 2, 4), umidita=44, costo=701)
    , Tappa(localita='Torino', data=datetime.date(2013, 2, 5), umidita=70, costo=771)
    , Tappa(localita='Torino', data=datetime.date(2013, 2, 6), umidita=42, costo=813)
    , Tappa(localita='Torino', data=datetime.date(2013, 2, 7), umidita=54, costo=867)
    , Tappa(localita='Torino', data=datetime.date(2013, 2, 8), umidita=35, costo=902)
    , Tappa(localita='Torino', data=datetime.date(2013, 2, 9), umidita=34, costo=936)
    , Tappa(localita='Genova', data=datetime.date(2013, 2, 10), umidita=32, costo=1168)
    , Tappa(localita='Genova', data=datetime.date(2013, 2, 11), umidita=77, costo=1245)
    , Tappa(localita='Genova', data=datetime.date(2013, 2, 12), umidita=64, costo=1309)
    , Tappa(localita='Genova', data=datetime.date(2013, 2, 13), umidita=50, costo=1359)
    , Tappa(localita='Genova', data=datetime.date(2013, 2, 14), umidita=44, costo=1403)
    , Tappa(localita='Genova', data=datetime.date(2013, 2, 15), umidita=58, costo=1461)]'''