from __future__ import print_function

import webbrowser
import argparse
import sys
import time
import json
import re
import os
import os.path
import traceback

from flask import Flask, safe_join, send_from_directory
from BeautifulSoup import BeautifulSoup as Soup
from jinja2 import Template

import engine

def getApp(projPath, dataSrc, indexFile):
	#Create our server
	app = Flask(__name__)
	app.debug = True

	#def render(name, values):
	#	template_content = open("templates/%s" % name, 'r').read()
	#	template = Template(template_content)
	#	return template.render(**values)

	# fetches data from current active data souce and renders the theme
	def render_theme(the_path):
		#global dataSrc
		s_time = time.time()
		try:
			content = open(the_path, 'r').read()
			# Soupify and Extract meta tags
			soup = Soup( content )
			metaTags = { tag['name'] : tag['content'] for tag in soup.findAll('meta', attrs={'name':re.compile('^([a-zA-Z]+):.*')} ) }
			tpl = engine.Template( content )
			# Compile the template
			tpl.compile()
			# Fetch the default template to map the data to template
			# this basically has rules on how to render each tag from raw json
			contextTemplate = engine.defaultContextMapperTemplate()
			# Update data template with info on how to map meta data
			contextTemplate.update( engine.metaContextTemplate( metaTags ) )
			# create the mapper object
			contextDataMap = engine.ContextDataMapper( dataSrc['response'], contextTemplate )
			# Render the tumblr template with the data map we constructed
			output = tpl.render(contextDataMap)
		except Exception as e:
			e = 'Template Compile Error : ' + traceback.format_exc(e)
			e = '<pre>' + e + '</pre>'
			return e

		# Fetch hthe default context mapper template 
		e_time = time.time()
		debug_info = "\n<!-- Time to compile and render: %s -->" % (e_time-s_time)
		return output + debug_info
		
	@app.route('/')
	def default():
		return render_page("")
		
	@app.route("/<path:file>")
	def render_page(file):
		if file is "":
			file = indexFile
		
		filePath = safe_join(projPath, file)
		# If its ending with html, render it as a tumblr theme
		if os.path.exists(filePath) and (filePath.lower().endswith('.html') or filePath.lower().endswith('.htm')):
			return render_theme(filePath)
		else:
			# Serve it from the theme's directory]
			print(filePath, file=sys.stderr)
			return send_from_directory(projPath, file)
	
	return app
	
def main():
	print("TumblrThemr")
	print("Current working directory:" + os.path.abspath("."))
	#Parse args
	argp = argparse.ArgumentParser()
	argp.add_argument( '--data', default="./src/data/sampleData.json")
	argp.add_argument( '--project' )
	argp.add_argument( '--port', default=8080 )
	argp.add_argument( '--index', default="index.html")
	args = argp.parse_args( sys.argv[1:] )

	indexFile = args.index.strip()
	dataPath = os.path.abspath(args.data.strip().rstrip("/").rstrip("\\"))
	projPath = os.path.abspath(args.project.strip().rstrip("/").rstrip("\\")) + "\\"
	port = args.port

	#Fail on improper args
	if not projPath or not os.path.isdir(projPath):
		print("No --project provided or --project was not directory!")
		sys.exit(-1)
		
	if not dataPath or not os.path.isfile(dataPath):
		print("--data not found")
	
	#Load the json data
	dataSrc = json.load( open(dataPath,'r') )
	
	#Start the test server
	app = getApp(projPath, dataSrc, indexFile)
	
	#Open the web browser
	#webbrowser.open( "http://localhost:%s" %(port) )
	#Start the web server
	#print("DO START (%s,%s)" % (projPath,port), file=sys.stderr)
	#Run the app
	app.run(host='localhost', port=port)

# Get things from command line - makes it easy for testing
if __name__ == "__main__":
	main()



