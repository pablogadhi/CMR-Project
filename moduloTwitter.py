# -*- coding: cp1252 -*-
import json
from pymongo import MongoClient
from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
import credenciales


#connect
#connection = Connection()
#db = connection.tweets
#----------------------- Clase para clientes de tweets ------------------------
class TwitterClient():
    def __init__(self, usuarioTw=None):
        self.auth = auTwitter().autenticar()
        self.clienteTw = API(self.auth)
        self.usuarioTw = usuarioTw
        

    def get_tweets_usuario(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.clienteTw.user_timeline, id = self.usuarioTw).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_amigos(self, num_friends):
        amigos = []
        for friend in Cursos(self.clienteTw.friends, id=self.usuarioTw).items(num_friends):
            amigos.append(friend)
        return amigos
        

#----------------------- Clase para autenticarse con twitter ----------------
class auTwitter():
    def autenticar(self):
        auth = OAuthHandler(credenciales.CONSUMER_KEY, credenciales.CONSUMER_SECRET)
        auth.set_access_token(credenciales.ACCESS_TOKEN, credenciales.ACCESS_TOKEN_SECRET)
        return auth


#----------------------- Clase dedicada al streaming y procesamiento de tweets ----------------

class TwitterStreamer():
    def __init__(self):
        self.autenticacion = auTwitter()
        
    def stream_tweets(self, jsonTweets, hash_tag_list):
        #Esta clase maneja la autentificación y la conexión con twitter API
        listener = TWListener(jsonTweets)
        auth = self.autenticacion.autenticar()
        stream = Stream(auth,listener)
        stream.filter(track=hash_tag_list)

#----------------------- Clase listener para tweets ----------------
class TWListener(StreamListener):

    def __init__(self, jsonTweets):
        self.jsonTweets = jsonTweets
        
    def on_data(self,data):
        try:
            #print(data)
            with open(self.jsonTweets, "a") as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("error en datos: %s" % str(e))
        return True

    #Metodo al que hacemos override de clase StreamListener que maneja errores
    def on_error(self,status):
        #Retornar cuando twitter lanza error de acceso incorrecto
        if status == 420:
            return False 
        print(status)
"""
--------------------------------------------- AQUI FUNCIONA NITIDO------------------------------------------------
if __name__ == "__main__":
    clienteDB = MongoClient()
    db = clienteDB.tweets
    coleccion = db.tweetsUsuario
    #hash_tag_list = ["bases de datos", "por el 100"]
    twitter_client = TwitterClient()
    tw = []
    tw = twitter_client.get_tweets_usuario(3)
    cont = 0
    try:
        for t in tw:
            cont = cont + 1
            vamosVer = {'_id': cont,'texto':t.text,'id':t.id, 'created_at':t.created_at,'screen_name':t.author.screen_name,'author_id':t.author.id}
            print(vamosVer)
            coleccion.insert_one(vamosVer)
    except Exception as e:
        print(e)
"""
        
    
