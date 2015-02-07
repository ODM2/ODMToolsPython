# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------
# Name:         ListCtrlPrinter.py
# Author:       Phillip Piper
# Created:      17 July 2008
# SVN-ID:       $Id$
# Copyright:    (c) 2008 by Phillip Piper, 2008
# License:      wxWindows license
#----------------------------------------------------------------------------
# Change log:
# 2008/07/17  JPP   Initial version
#----------------------------------------------------------------------------
# To do:
# - scaling
# - gradients
# - images
# - attributes from ListCtrl
# - persistence of ReportFormat
# - use wx.wordwrap and DrawLabel
# - investigate DrawImageLabel

"""
An ListCtrlPrinter takes an ObjectListView and turns it into a pretty report.

As always, the goal is for this to be as easy to use as possible. A typical
usage should be as simple as::

   printer = ListCtrlPrinter(self.myOlv, "My Report Title")
   printer.PrintPreview()

"""

import wx

#======================================================================

class TestPrinter(wx.Printout):

    def __init__(self, margins=None):
        """
        """
        wx.Printout.__init__(self, "The title")

        self.printData = wx.PrintData()
        self.printData.SetPaperId(wx.PAPER_A4)
        self.printData.SetOrientation(wx.PORTRAIT)
        self.printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        self.printData.SetNoCopies(1)
        self.margins = margins or (wx.Point(0, 0), wx.Point(0, 0))


    #----------------------------------------------------------------------------
    # Accessing

    def HasPage(self, page):
        return page <= 3

    def GetPageInfo(self):
        return (1, 3, 1, 1)

    #----------------------------------------------------------------------------
    # Commands


    def PageSetup(self):
        data = wx.PageSetupDialogData()
        data.SetPrintData(self.printData)
        data.SetDefaultMinMargins(True)
        data.SetMarginTopLeft(self.margins[0])
        data.SetMarginBottomRight(self.margins[1])
        dlg = wx.PageSetupDialog(None, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetPageSetupData()
            self.printData = wx.PrintData(data.GetPrintData())
            self.printData.SetPaperId(data.GetPaperId())
            self.margins = (data.GetMarginTopLeft(),
                            data.GetMarginBottomRight())
        dlg.Destroy()

    def PrintPreview(self, parent=None, title="ObjectListView Print Preview", bounds=(20, 50, 800, 800)):
        """
        Show a Print Preview of this report
        """
        data = wx.PrintDialogData(self.printData)
        t = TestPrinter(self.margins)
        t2 = TestPrinter(self.margins)
        self.preview = wx.PrintPreview(t, t2, data)

        if not self.preview.Ok():
            return False

        pfrm = wx.PreviewFrame(self.preview, parent, title)

        pfrm.Initialize()
        pfrm.SetPosition(bounds[0:2])
        pfrm.SetSize(bounds[2:4])
        pfrm.Show(True)

        return True


    def DoPrint(self, parent=None):
        """
        Send the report to the configured printer
        """
        pdd = wx.PrintDialogData(self.printData)
        printer = wx.Printer(pdd)

        if printer.Print(parent, self, True):
            self.printData = wx.PrintData(printer.GetPrintDialogData().GetPrintData())
        else:
            wx.MessageBox("There was a problem printing.\nPerhaps your current printer is not set correctly?", "Printing", wx.OK)

        printout.Destroy()


    #----------------------------------------------------------------------------
    # Event handlers

    def OnPreparePrinting(self):
        """
        Prepare for printing. This event is sent before any of the others
        """
        print "OnPreparePrinting"
        print "self.GetDC() = %s" % self.GetDC()

    def OnBeginDocument(self, start, end):
        """
        Begin printing one copy of the document. Return False to cancel the job
        """
        print "OnBeginDocument(%d, %d)" % (start, end)
        if not super(TestPrinter, self).OnBeginDocument(start, end):
            return False

        return True

    def OnEndDocument(self):
        print "OnEndDocument"
        super(TestPrinter, self).OnEndDocument()

    def OnBeginPrinting(self):
        print "OnBeginPrinting"
        super(TestPrinter, self).OnBeginPrinting()

    def OnEndPrinting(self):
        print "OnEndPrinting"
        super(TestPrinter, self).OnEndPrinting()

    def OnPrintPage(self, page):
        print "OnPrintPage(%d)" % page
        dc = self.GetDC()
        self.CalculateScale(dc)
        self.CalculateLayout(dc)
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        bounds = (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1)
        print bounds
        print self.pageHeight
        dc.DrawRectangle(*bounds)
        font = wx.Font(10, wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        dc.DrawText("this is a string", bounds[0], bounds[1])

    def CalculateScale(self, dc):
        # Scaling the DC to screen size
        ppiPrinterX, ppiPrinterY = self.GetPPIPrinter()
        ppiScreenX, ppiScreenY = self.GetPPIScreen()
        logScale = float(ppiPrinterX)/float(ppiScreenX)
        pw, ph = self.GetPageSizePixels() # Adjusting scale
        dw, dh = dc.GetSize()
        scale = logScale * float(dw)/float(pw)
        dc.SetUserScale(scale, scale)
        self.logUnitsMM = float(ppiPrinterX)/(logScale*25.4)

    def CalculateLayout(self, dc):
        topLeft, bottomRight = self.margins
        dw, dh = dc.GetSize()
        self.x1 = topLeft.x * self.logUnitsMM
        self.y1 = topLeft.y * self.logUnitsMM
        self.x2 = dc.DeviceToLogicalYRel(dw) - bottomRight.x * self.logUnitsMM
        self.y2 = dc.DeviceToLogicalYRel(dh) - bottomRight.y * self.logUnitsMM
        self.pageHeight = self.y2 - self.y1 - 2*self.logUnitsMM



#======================================================================
# TESTING ONLY
#======================================================================

if __name__ == '__main__':
    import wx

    # Where can we find the Example module?
    import sys

    class MyFrame(wx.Frame):
        def __init__(self, *args, **kwds):
            kwds["style"] = wx.DEFAULT_FRAME_STYLE
            wx.Frame.__init__(self, *args, **kwds)

            self.panel = wx.Panel(self, -1)
            self.olv = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

            sizer_2 = wx.BoxSizer(wx.VERTICAL)
            sizer_2.Add(self.olv, 1, wx.ALL|wx.EXPAND, 4)
            self.panel.SetSizer(sizer_2)
            self.panel.Layout()

            sizer_1 = wx.BoxSizer(wx.VERTICAL)
            sizer_1.Add(self.panel, 1, wx.EXPAND)
            self.SetSizer(sizer_1)
            self.Layout()

            wx.CallLater(50, self.run)

        def run(self):
            printer = TestPrinter()
            printer.PageSetup()
            printer.PrintPreview(self)


    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
