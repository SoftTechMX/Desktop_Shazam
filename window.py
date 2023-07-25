import urllib.request
import mutagen.id3
import glob  
import numpy as np
import os
import json
import asyncio
import tkinter as tk

from tkinter            import filedialog
from mutagen.mp3 		import MP3
from mutagen.easyid3 	import EasyID3 
from mutagen.id3 		import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
from shazamio 			import Shazam

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
def seleccionar_directorio():
    directorio = filedialog.askdirectory()
    if directorio:
        # Hacer algo con el directorio seleccionado
        print("Directorio seleccionado:", directorio)

def removeSpecialChars(texto):
	caracteres_especiales=['@','#','$','*','&',':','\n', '/', '\\','?','(',')','^','\"']
	for caracter in caracteres_especiales:
		if( caracter == '&'):
			texto = texto.replace(caracter,",")
		else:
			texto=texto.replace(caracter,"")
	return texto

def get_value_of(key, jsonObject, sanitize = True):
	for attribute, value in jsonObject.items():
		if( attribute == key):
			if( sanitize ):
				return removeSpecialChars( str.title(value) )
			else:
				return value
		
def getMetadata(key, jsonDocument):
	for jsonObject in jsonDocument:
		if( jsonObject["title"] == key):
			return jsonObject["text"]

async def detect():
	shazam = Shazam()
	directorio_de_musica = "C:\\Users\\bayro\\Music\\PENDIENTE"
	
	for nombre_del_archivo in os.listdir(directorio_de_musica):

		archivo   = os.path.join(directorio_de_musica, nombre_del_archivo)
		extension = os.path.splitext(nombre_del_archivo)[1]
		
		if( os.path.isfile(archivo) ):
			if( extension == ".mp3" ):
				print("Reading ... " + archivo)

				try:
					jsonSongData = await shazam.recognize_song(archivo)

					titulo_de_la_cancion  = get_value_of("title",    jsonSongData["track"])
					artista_de_la_cancion = get_value_of("subtitle", jsonSongData["track"])
					foto_del_album        = get_value_of("coverart", jsonSongData["track"]["images"], False)
					# sAlbum  = getValue("Album",     jsonSongData["track"]["sections"][0]["metadata"])
					# sYear   = getValue("Realeased", jsonSongData["track"]["sections"][0]["metadata"])
					comentario = "www.itm-developers.com"
					nuevo_nombre_del_archivo = artista_de_la_cancion +" - "+ titulo_de_la_cancion + ".mp3"

					mp3file = MP3(archivo, ID3=EasyID3)
					# mp3file['album']  = "album editado"
					mp3file['artist'] = artista_de_la_cancion
					# mp3file['year']   = 2000
					mp3file['title']  = titulo_de_la_cancion
					mp3file.save()

					urllib.request.urlretrieve(foto_del_album, os.path.join(directorio_de_musica, artista_de_la_cancion +" - "+ titulo_de_la_cancion + os.path.splitext(foto_del_album)[1]))

					os.rename(archivo, os.path.join(directorio_de_musica, nuevo_nombre_del_archivo))

				except KeyError:
					print("SHAZAM NO pudo reconocer el archivo: ", nombre_del_archivo)
				except ConnectionResetError:
					print("Ocurrio un Error de Conexion. Omitiendo Archivo: ", nombre_del_archivo)
					continue
				except FileExistsError:
					os.remove(archivo)
     
#VARIABLES GLOBALES
WIDTH = 500
HEIGHT = 200

ventana = tk.Tk()
ventana.geometry("%sx%s" % (WIDTH, HEIGHT) )


# Botón para abrir el selector de directorio
boton = tk.Button(ventana, text="Seleccionar Directorio", command=seleccionar_directorio)
boton.place(x=10,y=10,width=480, height=30)

# Botón para abrir el selector de directorio
boton = tk.Button(ventana, text="Ejecutar", command=detect)
boton.place(x=10,y=50,width=480, height=30)

center_window(ventana)
ventana.mainloop()