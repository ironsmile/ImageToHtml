#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  Простико класче, което от картинка прави html с разни цветове and shits
"""
import argparse
import re
from PIL import Image
import sys
import traceback

CHAR_FEED_MAX_SIZE = 10000
CHAR_FEED_DEF_STR = """#!/usr/bin/python3importreCHAR_FEED_MAX_SIZE=5000CHAR_FEED_DEF_FILE="/home/iron4o/py/pic_to_html/src/classes/img_to_html.py"defhtml_escape(text):html_simbols={"&":"&amp;AyeYeaOuch&quot;NoSymbol&apos;&gt;<":"&lt;"}out=[]forcintext:out.append(html_simbols.get(c,c))return"".join(out)classImgToHTML():def__init__(self,img_path,characters_file_path=None):self.img_path=img_pathwithopen(characters_file_pathifcharacters_file_pathelseCHAR_FEED_DEF_FILE)asfeed_file:self.char_feed=feed_file.read(CHAR_FEED_MAX_SIZE)def_set_char_feed(self,string):self._char_feed=re.sub(re.compile(r'\s+');"/",string)def_get_char_feed(self):returnself._char_feedchar_feed=property(fget=_get_char_feed,fset=_set_char_feed)"""


def html_escape(text):
  html_simbols = {
      "&": "&amp;",
      '"': "&quot;",
      "'": "&apos;",
      ">": "&gt;",
      "<": "&lt;"
  }

  out = []
  for c in text:
    out.append(html_simbols.get(c, c))

  return "".join(out)


class ImgToHTML(object):
  def __init__(self, img_path, characters_file_path=None, magick=1.7, font_size=10):
    self.error = ""
    self.img_path = img_path
    try:
      feed_file = open(characters_file_path)
      try:
        self.char_feed = feed_file.read(CHAR_FEED_MAX_SIZE)
      except IOError:
        self.char_feed = CHAR_FEED_DEF_STR
      finally:
        feed_file.close()
    except (IOError, TypeError):
      self.char_feed = CHAR_FEED_DEF_STR

    #
    # What is this MAGICK constant all about?
    # For starters it is 1.7
    # Why would you increase the image's width?
    # That's because fonts' symbols are not as square as a pixel is.
    # They are all rendered in a container. For fixed-width (aka monospace) fonts
    # this container is the same size for all symbols.
    # The problem is that the height of the symbol container tends to be
    # larger than its width. That's what the MAGICK constant tries to cope with.
    #
    self.magick = magick
    self.font_size = font_size

  def _set_char_feed(self, string):
    self._char_feed = re.sub(re.compile(r'\s+'), "", string)

  def _get_char_feed(self):
    return self._char_feed

  char_feed = property(fget=_get_char_feed, fset=_set_char_feed)

  def process_image(self, width=None, height=None):
    """
      Минава през картинката и връща масив от вида { 'HTML' : "..." }
      При грешка - False и може да си търсите обяснението в self.error
    """

    html = ""
    css = {}
    feed_str = self.char_feed
    feed_len = len(feed_str)
    feed_ind = 0

    try:
      im = Image.open(self.img_path)
      size_w, size_h = im.size

      if(width != None or height != None):  # 55 / 60 == 0 ! и аз съм глупак!
        width = width if width != None else int(
            (float(size_w) / size_h) * height)
        height = height if height != None else int(
            (float(size_h) / size_w) * width)
        size_w, size_h = width, height
        size_w = int(size_w * self.magick)
        im = im.resize((size_w, size_h))

      imp = im.resize((256, 1))
      imp.putdata(range(256))
      # тук вече имаме RGB цвета в tuble според кода му
      imp = imp.convert("RGB").getdata()

      image_colour_data = list(im.getdata())

      current_color = image_colour_data[0]
      current_str = ""
      for ind, pixcolor in enumerate(image_colour_data):
        if(pixcolor != current_color):
          html += "<span style='color: rgb%s;'>%s</span>" % (
              current_color, current_str)
          current_str = ""
          current_color = pixcolor
        if(ind != 0 and ind % size_w == 0):
          current_str += "\n"

        current_str += html_escape(feed_str[feed_ind % feed_len])
        feed_ind += 1

      # не се сещам как да избегна следващото :/
      html += "<span style='color: rgb%s;'>%s</span>" % (
          current_color, current_str)

    except Exception as inst:
      traceback.print_exc(file=sys.stdout)
      self.error = "Almost handled exception: %s" % str(inst)
      return False  # ами... и последния влак замина

    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
          <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <style type="text/css">
              body {{background-color: black; margin: 0; padding: 0;}}
              pre {{font-size:{:d}px; margin: 0 auto; padding: 0;}}
            </style>
            <title>Imaged!</title>
          </head>  
          <body>
            <pre>{:s}</pre>
          </body>""".format(self.font_size, html)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Create an HTML from image.')
  parser.add_argument(
    '--magick',
    dest='magick',
    type=float,
    default=2,
    help='the magick width increasing constant'
  )
  parser.add_argument(
    '--feed-path',
    dest='feed_path',
    type=str,
    default=None,
    help='path to a character feed file'
  )
  parser.add_argument(
    '--chars-width',
    dest='chars_width',
    type=int,
    default=130,
    help='how many characters should be wide the output'
  )
  parser.add_argument(
    '--font-size',
    dest='font_size',
    type=int,
    default=10,
    help='font size in pixels'
  )

  parser.add_argument(
    'source',
    type=str,
    help='File path to the image source'
  )
  parser.add_argument(
    'output',
    nargs='?',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='File path to where HTML output will be written'
  )

  args = parser.parse_args()

  converter = ImgToHTML(args.source,
    characters_file_path=args.feed_path,
    magick=args.magick,
    font_size=args.font_size
  )
  filestr = converter.process_image(width=args.chars_width)

  if filestr == False:
    sys.stderr.write("Error processing image: {0}".format(converter.error))
    sys.exit(1)

  args.output.write(filestr)
