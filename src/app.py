#! /usr/bin/python
# -*- coding: utf-8 -*-

from classes.img_to_html import ImgToHTML
import os, wx
ID_ABOUT=101
ID_EXIT=110
ID_BUTTON_OPEN_IMG = 10
ID_BUTTON_OPEN_FEED = 11
ID_BUTTON_SAVE = 12
ID_TXT_IMG = 30
ID_TXT_FEED = 31

DEFAULT_RES_IMG_WIDTH = 130

class MainWindow(wx.Frame):
  
    # =================================================================================
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, size = (400,200))
        self.Centre()
        self.dirname=""
        
        self.CreateStatusBar() # A StatusBar in the bottom of the window
        # Setting up the menu.
        filemenu= wx.Menu()
        filemenu.Append(ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h4 = wx.BoxSizer(wx.HORIZONTAL)
        self.open_button = wx.Button(self, ID_BUTTON_OPEN_IMG, "Browse")
        self.feed_button = wx.Button(self, ID_BUTTON_OPEN_FEED, "Browse")
        self.save_button = wx.Button(self, ID_BUTTON_SAVE, "Save")
        img_txt = wx.StaticText(self, -1, "Image : ")
        feed_txt = wx.StaticText(self, -1, "Text to be used to fill the image (optional) : ")
        self.img_control = wx.TextCtrl(self, ID_TXT_IMG )
        self.feed_control = wx.TextCtrl(self, ID_TXT_FEED )
        
        self.sizer_h1.Add(img_txt,0,wx.ALIGN_CENTER_VERTICAL)
        self.sizer_h1.Add(self.img_control,1,wx.EXPAND)
        self.sizer_h1.Add(self.open_button,0,wx.ALIGN_CENTER_VERTICAL)
        
        
        self.sizer_h2.Add(feed_txt,0,wx.ALIGN_CENTER_VERTICAL)
        self.sizer_h2.Add(self.feed_control,1,wx.EXPAND)
        self.sizer_h2.Add(self.feed_button,0,wx.ALIGN_CENTER_VERTICAL)
        
        self.width_controler = wx.TextCtrl(self, -1 )
        width_txt = wx.StaticText(self, -1, "Width (Integer. Default is %d) : " % DEFAULT_RES_IMG_WIDTH)
        self.sizer_h4.Add(width_txt,0,wx.ALIGN_CENTER_VERTICAL)
        self.sizer_h4.Add(self.width_controler,0,wx.ALIGN_CENTER_VERTICAL)
        
        self.sizer_h3.Add(self.save_button,0,wx.ALIGN_RIGHT)
        
        self.sizer.Add(self.sizer_h1,0,wx.EXPAND)
        self.sizer.Add(self.sizer_h2,0,wx.EXPAND)
        self.sizer.Add(self.sizer_h4,0)
        self.sizer.Add(self.sizer_h3,1,wx.ALIGN_RIGHT)
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        
        wx.EVT_BUTTON( self, ID_BUTTON_OPEN_IMG, self.OnCustmOpen(self.img_control) )
        wx.EVT_BUTTON( self, ID_BUTTON_OPEN_FEED, self.OnCustmOpen(self.feed_control) )
        wx.EVT_BUTTON( self, ID_BUTTON_SAVE, self.OnSave )
        wx.EVT_MENU( self, ID_ABOUT, self.OnAbout )
        wx.EVT_MENU( self, ID_EXIT, self.OnExit )
        
        self.Show(True)
        
        
    # =================================================================================
    def OnAbout(self,e):
      d= wx.MessageDialog( self, "Choose a image file and and save it as a colorful HTML file filled with custom text!", "About" , wx.OK)
      d.ShowModal() # Shows it
      d.Destroy() # finally destroy it when finished.
        
        
    # =================================================================================        
    def OnExit(self,e):
      self.Close(True)  # Close the frame.

    # =================================================================================    
    def OnCustmOpen(self, where):
      
      def OnOpen(e):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetDirectory()
            where.SetValue(dlg.GetPath())
        dlg.Destroy()
      
      return OnOpen

    # =================================================================================    
    def OnSave(self,e):
      dlg = wx.FileDialog(self, "Save As", self.dirname, "", "*.html", wx.SAVE)
      if dlg.ShowModal() == wx.ID_OK:
        output_file = dlg.GetPath()
        if( os.path.isfile(output_file) ):
          overwrite = wx.MessageDialog( self, "File already exists.\nDo you wish to overwrite it?", "Overwrite?", wx.YES_NO | wx.ICON_QUESTION )
          answer = overwrite.ShowModal()
          overwrite.Destroy()
          if( answer == wx.ID_NO ):
            return
          
        converter = ImgToHTML(self.img_control.GetValue(), self.feed_control.GetValue())
        
        try:
          rwidth = int(self.width_controler.GetValue())
        except ValueError:
          rwidth = DEFAULT_RES_IMG_WIDTH
        filestr = converter.process_image(width=rwidth)
        if( filestr != False ):
          try:
            fh = open(output_file, "w")
            fh.write(filestr)
          except IOError, desc:
            msg_txt, msg_title
          else:
            msg_txt, msg_title = "file %s has been saved successfully!" % output_file, "Saved!"
          finally:
            fh.close()
            
        else:
          msg_txt, msg_title = converter.error, "Error!"

      dlg.Destroy()
      
      mb=wx.MessageDialog( self, msg_txt, msg_title, wx.OK )
      mb.ShowModal()
      mb.Destroy()
      
      
app = wx.PySimpleApp()
frame = MainWindow(None, -1, "Image to HTML")

if __name__ == "__main__":
  app.MainLoop()