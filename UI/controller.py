import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.clear_lst()
        mese = self._mese
        self._view.lst_result.controls.append(ft.Text(f"Umidità media nel mese selzionato:"))
        self._view.update_page()
        for situa_key in self._model.dict_situazioni.keys():
            self._view.lst_result.controls.append(
                ft.Text(f"{situa_key}: {self._model.umidita_media_citta(situa_key, mese)}"))
            self._view.update_page()
        self._view.clear_dd()


    def handle_sequenza(self, e):
        self._view.clear_lst()

        self._model.cerca_percorso_ottimo(self._mese)
        #print(self._model.possibili_percorsi)
        for soluzione in self._model.soluzioni:
            self._view.lst_result.controls.append(ft.Text(f"La sequenza ha costo totale: {soluzione[-1].costo}"))
            self._view.update_page()
            for tappa in soluzione:
                self._view.lst_result.controls.append(ft.Text(f"{tappa}"))
                self._view.update_page()

        self._view.clear_dd()


    def read_mese(self, e):
        self._mese = int(e.control.value)


