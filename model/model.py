from collections import defaultdict
from datetime import date

from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        self.dict_situazioni = {}
        self.inizializza_situa_localita()
        self._localita = self.dict_situazioni.keys()

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

    def min_umidita(self, umidita: dict):
        min = 9999999999
        citta = ''
        for localita in self._localita:
            if umidita[localita] < min:
                min = umidita[localita]
                citta = localita

        return min, citta

    def optimization_recursive(self, giorno, mese):
        if giorno == 0:
            umidita = {}
            for localita in self._localita:
                umidita[localita] = 0
                for situa in self.dict_situazioni[localita]:
                    if situa.data == date(2013, mese, giorno):
                        umidita[localita] = situa[localita].umidita
            return self.min_umidita(umidita)
        else:
            for localita in self._localita:
                return self.optimization_recursive(giorno-1, mese)

