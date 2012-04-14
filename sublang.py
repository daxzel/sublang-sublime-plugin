import sublime, sublime_plugin
import threading  
import re
import sys
import urllib
import urllib2

def get_translated_result(page,text):

	p = re.compile('<span title="'+text+'"[^>]*>[^<]*</span>')

	span = p.findall(page,re.DOTALL)[0]

	p = re.compile('>[^<]*<')

	result = p.findall(span)[0]

	result = result[1:len(result)-1]

	return result


def translate(sl, tl, text):

	try:

		opener = urllib2.build_opener() 

		opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]   


		translated_page = opener.open( "http://translate.google.com/translate_t?" + urllib.urlencode({'sl': sl, 'tl': tl}), 
		data=urllib.urlencode({'hl': 'en', 'ie': 'UTF8', 'text': text.encode('utf-8'), 'sl': sl, 'tl': ()}) )   

		page = translated_page.read().decode('utf-8')


		sublime.status_message(get_translated_result(page,text))

	except (urllib2.HTTPError) as (e):  
		sublime.error_message('%s: HTTP error %s contacting Google Translate' % (__name__, str(e.code)))  
	except (urllib2.URLError) as (e):  
		sublime.error_message('%s: URL error %s contacting Google Tsanslate' % (__name__, str(e.reason)))

class GoolgeTsanslateCaller(threading.Thread):  
    def __init__(self, sl, tl, text, timeout):  
        self.sl = sl
        self.tl = tl
        self.text = text  
        threading.Thread.__init__(self)  
  
    def run(self):  
    	translate(self.sl, self.tl, self.text)


class TranslateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		try:
			v = self.view

			mes = v.substr(v.sel()[0])

			str = sublime.load_settings('Preferences.sublime-settings').get("sublang");
			
			if str is None:
				raise Exception, u'Erorr configuration. Not found sublang in config'
			else:
				langs = str.split('>')
				if len(langs)!=2: 
					raise Exception, u'Erorr configuration. Value sublang requre {1}>{2}'
				else:
					sl = langs[0].strip()
					tl = langs[1].strip()
					thread = GoolgeTsanslateCaller(sl, tl, mes, 5)  	
					thread.start()

		except Exception as ex:
			sublime.message_dialog(ex.message)


