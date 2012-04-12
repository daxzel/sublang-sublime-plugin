import sublime, sublime_plugin
import re
import sys
import urllib
import urllib2


GOOLGE_TRANSLATE = "http://ajax.googleapis.com/ajax/services/language/translate?"


from BeautifulSoup import BeautifulSoup 

def translate(sl, tl, text): 
	opener = urllib2.build_opener() 
	opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]   
	translated_page = opener.open( "http://translate.google.com/translate_t?" + urllib.urlencode({'sl': sl, 'tl': tl}), 
		data=urllib.urlencode({'hl': 'en', 'ie': 'UTF8', 'text': text.encode('utf-8'), 'sl': sl, 'tl': tl}) )   
	translated_soup = BeautifulSoup(translated_page)

	return translated_soup('div', id='result_box')[0].string


def translate2(sl, tl, text):
	opener = urllib2.build_opener() 
	opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]   
	url = "http://translate.google.com/?tl=ru&sl=en#en|ru|Hello"
	translated_page = opener.open( "http://translate.google.com/translate_t?" + urllib.urlencode({'sl': sl, 'tl': tl}), 
	data=urllib.urlencode({'hl': 'en', 'ie': 'UTF8', 'text': text.encode('utf-8'), 'sl': sl, 'tl': ()}) )   
	translated_soup = BeautifulSoup(translated_page)
	return translated_soup('span', title=text)[0].string



class SubLang(sublime_plugin.TextCommand):
	def run(self, edit):
		v = self.view

		mes = v.substr(v.sel()[0])
		sublime.message_dialog(translate("en", "ru", mes))




    		


