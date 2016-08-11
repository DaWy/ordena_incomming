#!/usr/bin/python
# -*- encoding: utf-8 -*-
#Autor: David Martin
#Descripcio: Script per ordenar l'Incomming del Multimedia

#TODO: Comprobar la resolució del video abans de convertirlo per tal que els videos que no son apaisats o amb menys resolució es converteixin malament

def cmd_dir_browser(basedir):
	import os

	full_path = ""
	last_dir = False
	cur_dir = basedir

	while not last_dir:
		dir_list = os.listdir(cur_dir)
		counter = 0
		for element in dir_list:
			print element
			if os.path.isdir(element):
				print str(counter)+') '+element
				counter = counter + 1
		if counter is 0:
			last_dir = True
			return full_path
		selection = raw_input('Selecciona el directori: ')
		next_path = dir_list[selection]
		cur_dir = os.path.join(cur_dir, next_path)

	return full_path


def convert(imgurl):
	import PIL
	from PIL import Image
	import os

	directori = os.path.dirname(imgurl)
	arxiu = os.path.basename(imgurl)

	#Mida base. Mes gran = Mes pixels = Mes definició
	basewidth = 1600

	img = Image.open(imgurl)
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img.save(os.path.join(directori,arxiu))

def check_video_track(track):
	"""
	Comproba si el video track cumpleix els requeriments per ser transformat
	@track: Track del video
	"""
	#Video mes gran de 20MB
	try:
		#assert(track.stream_size / 1024 / 1024 >= 20)
		#Resolucio grossa
		#if is_video_vertical(track):
		#	assert(track.width > 720)
		#	assert(track.height > 1280)
		#else:
		#	assert(track.width > 1280)
		#	assert(track.height > 720)
		#Bitrate elevat
		assert(track.bit_rate / 1800 > 2000)
	except:
		pass
		return False
	return  True

def is_video_vertical(track):
	"""
	Comproba si el video esta grabat de manera vertical
	@track: Track del video
	"""
	if track.height > track.width:
		return True
	return False


def main():
	import os
	import shutil
	import re
	import sys
	from subprocess import call
	import md5
	import argparse
	from pymediainfo import MediaInfo

	reload(sys)  
	sys.setdefaultencoding('utf8')

	print sys.getdefaultencoding()



	argparser = argparse.ArgumentParser(description="Manage gallery incoming files", )
	argparser.add_argument('-mode', dest='mode', help="The working mode. 1) <convert>: Converteix tots els arxius sense preguntar si es volen mourer."
	" 2) <move>: No converteix res. Mode interactiu per mourer els arxius. 3) <complete>. Converteix + mode interactiu.", required=True)
	argparser.add_argument('-ip', dest='incoming_path', help="Path de l'incoming", required=False)
	argparser.add_argument('-mp', dest='multimedia_path', help="Path del multimedia", required=False)

	args = argparser.parse_args()

	#Path Ruta multimedia muntat en local
	if not args.incoming_path:
		multimedia_path = "/home/dmartin/Mounted/multimedia/01-Incomming"
	else:
		multimedia_path = args.incoming_path

	if not args.multimedia_path:
		multimedia_base = "/home/dmartin/Mounted/multimedia"
	else:
		multimedia_base = args.multimedia_path

	converted_videos_dirname = '_converted_videos'

	#Directoris exclosos
	excluded_dirs = ['_NO_CONTENT', '_converted_videos']

	#Extensions incloses
	included_ext = ['.jpg', '.png', '.gif', '.tif', ]
	video_ext = ['.mov', '.mpg', '.mp4', ]

	contarxius = 0
	gained_space = 0
	progress = 1
	total_dirs = 0
	excluded = False

	print 'hi'

	for root, dirs, files in os.walk(multimedia_path):
		total_dirs = total_dirs + 1

	print ' '
	print '>>>>>>>>>> Multimedia Incoming Manager Script <<<<<<<<<< Versió 1.0 (Data: 2015-11-09)'
	print ' '
	print '- S\'han trobat '+str(total_dirs)+' directori/s a analitzar! Començant...'

	for root, dirs, files in os.walk(multimedia_path):
		excluded = False

		for ed in excluded_dirs:
			if root.find(ed) is not -1:

				excluded = True

		if not excluded:
			print '----> Directori '+str(progress)+' de '+str(total_dirs)+' : '+str(os.path.basename(root))
			info = os.stat(root)
			if args.mode != 'move':
				print 'Començant la conversió...'
				for arxiu in files:
					after_size = os.path.getsize(os.path.join(root, arxiu)) / 1000
					
					filename, extension = os.path.splitext(arxiu)
					if str(extension).lower() in included_ext:
						if after_size > 800:
							print 'Convertint: '+arxiu
							try:
								convert(os.path.join(root, arxiu))
							except:
								pass
								print '%s No s\'ha pogut convertir!' % os.path.join(root, arxiu)
					elif str(extension).lower() in video_ext:
						#Convert Videos
						if converted_videos_dirname not in root:
							print 'Convertint Video: '+arxiu
							#Mirem que el directori actual no sigui el dels videos ja convertits
							print 'Arxiu: %s/%s' % (root,arxiu)
							mi = MediaInfo.parse(os.path.join(root, arxiu).decode('utf-8'))
							#Obtenim el track de video
							for track in mi.tracks:
								print track.track_type
								if track.track_type == "Video":
									track_video = track
									if check_video_track(track):
										if is_video_vertical(track):
											resolution = '720x1280'
											call(['sudo', 'nautilus', root])
										else:
											resolution = '1280x720'
										if not os.path.exists(os.path.join(root, converted_videos_dirname)):
											os.makedirs(os.path.join(root, converted_videos_dirname))
										if str(extension).lower() == ".mpg":
											call(['ffmpeg', '-n', '-i', os.path.join(root, arxiu), '-target', 'pal-svcd', '-s', resolution, '-crf', '27', os.path.join(root, converted_videos_dirname, arxiu)])
										elif str(extension).lower() == ".mov":
											call(['ffmpeg', '-n', '-i', os.path.join(root, arxiu), '-target', 'pal-dvd', '-s', resolution, '-crf', '27', os.path.join(root, converted_videos_dirname, arxiu)])
										elif str(extension).lower() == ".mp4":
											call(['ffmpeg', '-n', '-i', os.path.join(root, arxiu), '-vcodec', 'libx264', '-s', resolution, '-crf', '27', os.path.join(root, converted_videos_dirname, arxiu)])
										elif str(extension).lower() == ".avi":
											call(['ffmpeg', '-n', '-i', os.path.join(root, arxiu), '-vcodec', 'libx264', '-s', resolution, '-crf', '27', os.path.join(root, converted_videos_dirname, arxiu)])

										#Si l'arxiu generat es mes gran que el original, mantenim original, sino, esborrem original.
										if os.path.getsize(os.path.join(root, converted_videos_dirname, arxiu)) / 1000 >= after_size:
											os.remove(os.path.join(root, converted_videos_dirname, arxiu))
										else:
											os.remove(os.path.join(root, arxiu))
									else:
										print '- Video don\'t need conversion!'
					contarxius = contarxius + 1

				
				print 'Conversió Finalitzada! '
				#raw_input('Seguir conversió (prem enter)... ')

			if args.mode != 'convert':
				confirm_moure = raw_input('- Vols mourer el contigut a la ubicació final?: ')
				if confirm_moure.lower() == "s":
					#Mirem arxiu content.txt (si hi es)
					try:
						f = open(os.path.join(root,'content.txt'))
						content = ""
						for line in f:
							content += line
						f.close()

						path = re.search("\nPath:.*", content)
						path = path.group()
						path = path.replace('V:\\','')
						path = path.replace('Path:','')
						path = path.replace('\\','/')
						path = path.strip()
						print '- Content Path: '+path
						if not os.path.exists(os.path.join(multimedia_base,path)):
							option = raw_input("- El directori de destí no existeix. Vols crearlo?: ")
							if(option.lower() == "s"):
								os.makedirs(os.path.join(multimedia_base,path))
							else:
								path = raw_input("- Indical manualment (Nom Carpeta: "+root+"): ")
								if not os.path.exists(os.path.join(multimedia_base, path)):
									print 'El directori indicat ('+path+') no existeix. Es creara...'
									os.makedirs(os.path.join(multimedia_base, path))
					except:
						pass
						print 'ALERTA: Arxiu content no trobat!'
						print 'Es moura la carpeta a \"NO_CONTENT\"!'


						content = False
					if not content:
						path = raw_input("-> Introdueix el directori de destí (Nom Carpeta: "+root+"): ")
						if path is '':
							print 'Es mou el directori a carpeta NO_CONTENT'
							if not os.path.exists(os.path.join(multimedia_base, "_NO_CONTENT")):
								os.makedirs(os.path.join(multimedia_base, "_NO_CONTENT"))
							call(['mv', root, os.path.join(multimedia_base, "_NO_CONTENT")])
						else:
							if not os.path.exists(os.path.join(multimedia_base, path)):
								print 'El directori indicat ('+path+') no existeix. Es creara...'
								os.makedirs(os.path.join(multimedia_base, path))
					else:
						print 'O: %s \nD: %s \n' % (root, os.path.join(multimedia_base,path,os.path.basename(root)))
						confirm_moure_2 = raw_input('- Es moura el contingut. Estas segur? (s/n): ')
						if confirm_moure_2.lower() == "s":
							#Movem la carpeta
							checkok = md5.new(str(os.listdir(root)))
							print 'Directori Incomming:' +str(os.listdir(root))
							call(['mv', '-f', root, os.path.join(multimedia_base,path)])
							print 'Directori Multimedia:' +str(os.listdir(os.path.join(multimedia_base,path,os.path.basename(root))))
							if md5.new(str(os.listdir(os.path.join(multimedia_base,path,os.path.basename(root))))) == checkok:
								print 'Copia correcta!'
			progress = progress + 1
		else:
			print 'EXCLUDED!: %s' % root

if __name__ == "__main__":
	main()
