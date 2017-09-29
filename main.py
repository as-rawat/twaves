import os
import jinja2
import webapp2
import urllib2
import json

template_dir = os.path.join(os.path.dirname(__file__), '.')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template):
        t = jinja_env.get_template(template)
        return t.render()

    def render(self, template):
        self.write(self.render_str(template))

class index(Handler):
    def get(self):
        self.render('index.html')

    def post(self):
        self.response.out.write("response")

class searchByLyrics(Handler):
    def post(self):
        q = self.request.body
        type = "+lyrics"
        q = q.replace(" ", "+")
        ot = ''
        site = "https://www.google.com/search?q=%s%s"%(q,type)
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

        request = urllib2.Request(site, headers=header)

        try:
          page = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
          print e.fp.read()

        content = page.read()

        index = content.find("kno-ecr-pt kno-fb-ctx")
        print index
        if index != -1:
          tval = content[index:]
          index1 = tval.find("<span>") + 6
          index2 = tval.find("</span>")
          val = tval[index1:index2]
          print val
          ot = val + ' - '
          print " - "
          index = tval.find("a href")
          tval = tval[index:]
          index1 = tval.find(">") + 1
          index2 = tval.find("<")
          val = tval[index1:index2]
          print val
          ot += val
        elif content.find(" - YouTube") != -1:
          index = content.find("- YouTube")
          tval = content[:index]
          index1 = tval.rfind(">") + 1
          index2 = index - 1
          val = tval[index1:index2]
          print val
          ot = val
        else:
          print "Not found!"
          ot = "Not found!"

        self.response.out.write(ot)

    def get(self):
        self.render('sBL.html')

app = webapp2.WSGIApplication([
    ('/searchByLyrics', searchByLyrics),
    ('/', index),
], debug=True)
