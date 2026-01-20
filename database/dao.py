from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_albums_artist(num_albums):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT a.id, a.name, count(*) as num_alb
                FROM artist a, album alb
                WHERE a.id = alb.artist_id
                GROUP BY a.id, a.name
                having num_alb>%s
                """
        cursor.execute(query,(num_albums,))
        for row in cursor:
            result.append((row['id'], row['name'], row['num_alb']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessione(artisti):

        conn = DBConnect.get_connection()

        result = []
        artisti_id = tuple(a.id for a in artisti)
        cursor = conn.cursor(dictionary=True)
        query = f"""
                SELECT a1.artist_id as a1, a2.artist_id as a2 , COUNT(*) as peso
                FROM track t1, track t2, album a1, album a2
                WHERE a1.artist_id != a2.artist_id
                    AND a1.artist_id IN {artisti_id} AND a2.artist_id IN {artisti_id}
                    AND a1.id = t1.album_id 
                    AND a2.id = t2.album_id 
                    AND t1.genre_id = t2.genre_id 
                group by a1.artist_id, a2.artist_id
                """
        cursor.execute(query)
        for row in cursor:
        #    if row['a1'] in artisti_id and row['a2'] in artisti_id:
            result.append((row['a1'], row['a2'], row['peso']))
        cursor.close()
        conn.close()
        return result
