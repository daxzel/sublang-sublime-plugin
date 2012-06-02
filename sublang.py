# -- coding: utf-8 --
import sublime, sublime_plugin
import threading  
import re
import sys
import urllib
import urllib2
import json

url = "http://translate.google.com/translate_a/t?client=t&text={0}&hl=en&sl={1}&tl={2}&multires=1"

def translate(text, sourcelang, targetlang):
	try:
		
		request = urllib2.Request(url.format(text.encode('utf-8'), sourcelang.encode('utf-8'), targetlang.encode('utf-8')),headers={ 'User-Agent': 'Mozilla/5.0', 'Accept-Charset': 'utf-8' })
		response = urllib2.urlopen(request).read()
		
		fixed_json = re.sub(r',{2,}', ',', response).replace(',]', ']')
		data = json.loads(fixed_json)
		sublime.status_message(data[0][0][0])
		print data[0][0][0]
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
    	translate(self.text,self.sl, self.tl )


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


