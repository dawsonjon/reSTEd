#!/usr/bin/env python

import webbrowser
import threading

import wx
import wx.html as html
import docutils.core
from docutils.writers.odf_odt import Writer as odt_writer

class DocWin(html.HtmlWindow):

    """RsT Help viewer window"""

    def __init__(self, *args):
        html.HtmlWindow.__init__(self, *args)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

        self.lock = threading.Lock()
        self.html = False
        self.timer = wx.Timer(self)
        self.timer.Start(250)
        self.Bind(wx.EVT_TIMER, self.on_timer)

    def set_RsT(self, reST):
        self.reST = reST
        threading.Thread(target=self.update).start()

    def on_timer(self, evt):
        self.lock.acquire()
        if self.html:
            scroll_pos = self.GetScrollPos(wx.VERTICAL)
            try:
                self.SetPage(self.html)
            except Exception as e:
                print e
            self.Scroll(0, scroll_pos)
            self.html = False
        self.lock.release()

    def update(self):
        self.lock.acquire()
        self.document = docutils.core.publish_doctree(self.reST)
        self.html = docutils.core.publish_from_doctree(self.document, writer_name="html")
        self.lock.release()

    def export_html(self, filename):
        html = docutils.core.publish_from_doctree(self.document, writer_name="html")
        export_file = open(filename, "w")
        export_file.write(html)

    def export_latex(self, filename):
        html = docutils.core.publish_from_doctree(self.document, writer_name="latex")
        export_file = open(filename, "w")
        export_file.write(html)

    def export_odt(self, filename):
        html = docutils.core.publish_from_doctree(self.document, writer = odt_writer())
        export_file = open(filename, "w")
        export_file.write(html)


if __name__ == "__main__":

    test_document = """

section
=======

subsection
----------

Some text in a paragraph.

Some text in a paragraph.

subsection
----------

A bulleted list of random characters:

+ asdfasdf
+ asdfasdfasdfasdf
+ asds

A numbered list:

1. blah
2. blah blah
3. blah blah

subsection
----------

Table:

+---------+---------------+
| Header  | Other Header  |
+=========+===============+
| row1    |  column 2     |
+---------+---------------+
| row2    |  column 2     |
+---------+---------------+

Preformatted Text::
    def myfunction():
        pass

You can also add links_ to addresses.

.. _links: http://www.google.com

"""

    app = wx.App()
    frame = wx.Frame(None, size=(800,600), title="Test Help Window")
    docwin = DocWin(frame, -1)
    docwin.set_RsT(test_document)
    frame.Show()
    #frame.SetSizer(docwin)
    app.MainLoop()
