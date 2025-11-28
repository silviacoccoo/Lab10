import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        testo_soglia = self._view.guadagno_medio_minimo.value

        try:
            soglia = float(testo_soglia)
            if soglia < 0:
                raise ValueError("La soglia non può essere negativa.")
        except ValueError:
            # L'applicazione mostra un alert in caso di valore non valido
            self._view.show_alert("Errore: la soglia deve essere un valore numerico positivo.")
            return

        self._model.costruisci_grafo(soglia)

        # Recupero dei dati richiesti
        num_nodi = self._model.get_num_nodes()
        num_archi = self._model.get_num_edges()
        tutte_le_tratte = self._model.get_all_edges()  # (u, v, {'weight': peso})

        # Pulizia della lista di visualizzazione
        self._view.lista_visualizzazione.controls.clear()

        # Mostra il numero totale dei nodi del grafo
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"⭐ Numero di Hub presenti (Nodi): {num_nodi}", weight=ft.FontWeight.BOLD)
        )
        # Mostra il numero degli archi
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"🔗 Numero di Tratte valide (Archi, soglia: {soglia:.2f} €): {num_archi}",
                    weight=ft.FontWeight.BOLD)
        )

        # Se non ci sono archi, non stampiamo l'elenco
        if num_archi > 0:
            self._view.lista_visualizzazione.controls.append(
                ft.Text("--- Elenco Tratte Valide (Hub - Hub | Guadagno Medio) ---", size=16,
                        weight=ft.FontWeight.W_600)
            )

            # Elenco di tutte le tratte, ciascuna accompagnata dal rispettivo valore
            for hub_id1, hub_id2, data in tutte_le_tratte:
                peso = data['weight']  # Accesso al peso

                # Usiamo la funzione helper per rendere leggibili i nomi degli Hub
                nome1 = self._model._nodes[hub_id1].nome
                nome2 = self._model._nodes[hub_id2].nome

                self._view.lista_visualizzazione.controls.append(
                    ft.Text(f"   - {nome1} <-> {nome2} | {peso:.2f} €")
                )

        self._view.update()
        # TODO

