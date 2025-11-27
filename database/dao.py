from database.DB_connect import DBConnect
from model.hub import Hub

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def estrai_tutti_hub():
        cnx=DBConnect.get_connection()
        risultato={}

        if cnx is None:
            print('❌ Errore nella connessione al database')
            return None

        cursor=cnx.cursor(dictionary=True)
        query='SELCT * FROM hub'
        cursor.execute(query)
        for row in cursor:
            # Per ogni riga del cursore creo un oggetto hub e lo aggiungo al risultato
            hub=Hub(
                id=row['id'],
                codice=row['codice'],
                nome=row['nome'],
                citta=row['citta'],
                stato=row['stato'],
                latitudine=row['latitudine'],
                longitudine=row['longitude']
            )
            risultato[hub.id]=hub
            # Il dizionario ha come chiave l'id e come valore l'oggetto hub
        cursor.close()
        cnx.close()
        return risultato

    @staticmethod
    def estrai_spedizioni():
        conn=DBConnect.get_connection() # Creo la connessione
        risultato=[]

        if conn is None:
            print('❌ Errore nella connessione al database')
            return None # Se c'è un errore nella connessione il metodo non deve restituire niente

        cursor=conn.cursor(dictionary=True)
        # Per ogni riga prendo gli hub della spedizione
        query="""
            SELECT
                LEAST(s.id_hub_origine, s.id_hub_destinazione) AS hub1,
                GREATEST(s.id_hub_origine, s.id_hub_destinazione) AS hub2,
                SUM(s.valore_merce) / COUNT(*) AS guadagno_medio
            FROM spedizione s
            GROUP BY hub1, hub2
            HAVING hub1 <> hub2
        """
        cursor.execute(query)

        for row in cursor:
            risultato.append((row['hub1'], row['hub2'], row['guadagno_medio']))

        cursor.close()
        conn.close()

        return risultato

    # TODO
