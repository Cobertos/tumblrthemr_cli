## Tumblr Themr: CLI fork

This is a fork of the original [TumblrThemr application by Kalyan Chakravarthy](https://github.com/kalyan02/tumblrthemr). It has no native UI nor web interface (as of now).

It is meant to be:
* Cross platform (I couldn't get WX to work on Windows)
* Cross Python (Should work with 2 or 3)
* Simple (run from CLI and your dev server is up, no fuddling unless you need to)

### Download

 * Download Python 2 or Python 3
 * Install prerequisites
  * flask
  * jinja2
  * dateutil
  * BeautifulSoup
 * There are some command line flags [Defaults in brackets]
  * `--data` A json file of post data, samples are included. [`./src/data/sampleData.json`]
  * `--port` The port to run on [`8080`]
  * `--index` The filename of the index file [`index.html`]
  * `--project` The path to your project folder, used as root to serve files from. `--index` should be here. [`No default, you must pass this`]

### License
MIT License
