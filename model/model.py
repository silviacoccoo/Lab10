from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        self.G.clear() # Reset del grafo per una nuova analisi

        # AGGIUNTA NODI
        # I nodi sono tutti gli hub
        self._nodes=DAO.estrai_tutti_hub()
        self.G.add_nodes_from(self._nodes.keys()) # Aggiungo i nodi al grafo, i nodi sono le chiavi del dizionario restituito dalla funzione estrai_tutti_hub()

        # Verifica
        if not self._nodes:
            print('Nessun hub trovato')
            return

        # AGGIUNTA ARCHI
        tutte_tratte=DAO.estrai_spedizioni() # Restituisce una lista di tuple
        tratte_valide=[] # Archi validi

        for id_hub1, id_hub2, costo_medio in tutte_tratte:
            if costo_medio >= threshold: # Tratte con valore maggiore o uguale a quello inserito
                tratte_valide.append((id_hub1, id_hub2, {'weight': costo_medio}))
        self.G.add_edges_from(tratte_valide)

        self._edges=tratte_valide # Lo salviamo per l'output nel controller
        # TODO

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        return self.G.number_of_edges()
        # TODO

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return self.G.number_of_nodes()
        # TODO

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        return self.G.edges(data=True)
        # TODO

    def get_hub_name(self, hub_id):
        hub = self._nodes.get(hub_id)
        if hub:
            # Assumendo che l'oggetto Hub abbia un attributo 'nome'
            return hub.nome
        return f"ID Hub {hub_id}"  # Restituisce un fallback
