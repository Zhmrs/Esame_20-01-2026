import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            numero_minimo_album=int(self._view.txtNumAlbumMin.value)
            if numero_minimo_album >0:

                self._model.load_artists_with_min_albums(numero_minimo_album)
            else:
                self._view.show_alert('Valore inferiore a 0!')
        except ValueError:
            self._view.show_alert('Valore inserito non valido!')

        self._model.build_graph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {self._model.numero_nodi()} nodi (artisti), {self._model.numero_archi()} archi"))

        self._view.update_page()

    def handle_connected_artists(self, e):
        self._view.ddArtist.disabled = False
        self._view.ddArtist.options.clear()

        for n in self._model._graph.nodes:
            self._view.ddArtist.options.append(ft.Text(n.name))



        self._view.update_page()


