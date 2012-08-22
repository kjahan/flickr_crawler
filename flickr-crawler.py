import sys, string, math, time, socket
import flickrapi
from django.utils.encoding import smart_str, smart_unicode

class locations:
	def __init__(self, latit_, longit_, t_, id_, title_):
		self.latit = latit_
		self.longit = longit_
		self.time_ = t_
		self.ph_id = id_
		self.title = title_
			
api_key = 'your api key'
flickr = flickrapi.FlickrAPI(api_key)

g_ = open('id_lists.dat', 'r')
h_ = open('last_state.dat', 'r')
#let's find the last user we have trying to receive its data last time before interenet connection loss or hw failure
first_ = h_.readline()
starting_user = first_.replace("\n", "")
start_flag = False

for user_ in g_:
	user_ = user_.replace("\n", "")
	if user_ == starting_user:
		start_flag = True
	if start_flag == True:
		#let's continue our BFS from the last node
		print user_
#		time.sleep(1)
		try:
			outs_phs = flickr.photosets_getList(user_id=user_)
			photosets = outs_phs.find('photosets')
			sets = photosets.findall('photoset')	#the list of photo sets belong to the user
		except KeyboardInterrupt:
			print('Keyboard exception while querying for list of photosets, exiting\n')
			raise
		except:
			print sys.exc_info()[0]
			#print type(inst)     # the exception instance
			#print inst.args      # arguments stored in .args
			#print inst           # __str__ allows args to printed directly
			print ('Exception encountered while querying the list of photosets\n')
		else:
			#a list for storing longitude and latitude
			locs = []			
			#let's print all photo sets belong to this user
			for set in sets:
				#print "set id: ", set.attrib['id']
				#print "the set title:", set.find('title').text
				#print "no of photos: ", set.attrib['photos']
				try:
					outs_ph = flickr.photosets_getPhotos(photoset_id=set.attrib['id'])
					#now, let's crawl all photos which belong to the same photoset
					photoset = outs_ph.find('photoset')
					ph_ids = photoset.findall('photo')	# a list of ids for photos in the same set
				except KeyboardInterrupt:
					print('Keyboard exception while querying for photosets, exiting\n')
					raise
				except:
					print sys.exc_info()[0]
					#print type(inst)     # the exception instance
					#print inst.args      # arguments stored in .args
					#print inst           # __str__ allows args to printed directly
					print ('Exception encountered while querying a photoset\n')
				else:	
					#let's extract the location of each photo
					for id_ in ph_ids:
						try:
							out_loc = flickr.photos_geo_getLocation(photo_id=id_.attrib['id'])
							out_info = info=flickr.photos_getInfo(photo_id=id_.attrib['id'])
						except KeyboardInterrupt:
							print('Keyboard exception while querying for images, exiting\n')
							raise
						except:
							print sys.exc_info()[0]
							#print type(inst)     # the exception instance
							#print inst.args      # arguments stored in .args
							#print inst           # __str__ allows args to printed directly
							print ('Exception encountered while querying a location\n')
						else:
							loc_ = out_loc.find('photo').find('location')
							lat_ = loc_.attrib['latitude']
							lng_ = loc_.attrib['longitude']
							info = out_info.find('photo')
							date = info.find('dates')
							taken_time = date.attrib['taken']
							title = info.find('title').text
							loc = locations(lat_,lng_, taken_time, id_.attrib['id'], title)
							locs.append(loc)
							#print "lat:", lat_
							#print "long:", lng_
							
			print "the no of geo-tagged photos: ", len(locs)
			#write all photos locations as well as their taken time into a file for later processing
			if len(locs) > 0:
				#there are geo-tagged photo for this user
				file_name = "locations/locations_"
				file_name += user_
				file_name += ".dat"
				
				f_ = open(file_name, 'w')
				
				try:
					user = flickr.people_getinfo(user_id=user_)
					person = user.find('person')
					realname_ = person.find('realname').text
					location_ = person.find('location').text
					username_ = person.find('username').text
				except KeyboardInterrupt:
					print('Keyboard exception while querying for person info, exiting\n')
					raise
				except:
					print sys.exc_info()[0]
					#print type(inst)     # the exception instance
					#print inst.args      # arguments stored in .args
					#print inst           # __str__ allows args to printed directly
					print ('Exception encountered while querying a person info\n')
				else:
					entry_ = ""
					if realname_ is not None:
						entry_ += realname_.encode("utf-8")
						entry_ += ", "
					if username_ is not None:
						entry_ += username_.encode("utf-8")
						entry_ += ", " 
					if location_ is not None:
						entry_ += location_.encode("utf-8")
						entry_ += "\n"
					f_.write(entry_) 
				
				for loc in locs:
					#entry_ = "%s %s %s \"%s\"\n" % (loc.latit, loc.longit, loc.time_, smart_str(loc.title))
					entry_ = "%s %s %s\n" % (loc.latit, loc.longit, loc.time_)
					f_.write(entry_)
				
				f_.close()
		h_.close()
		h_ = open('last_state.dat', 'w')
		entry_ = "%s\n" % user_
		h_.write(entry_)
		h_.close()	
g_.close()	
