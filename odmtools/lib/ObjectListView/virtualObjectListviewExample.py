import wx
import wx.xrc
import sys

sys.path.insert(0, "/home/jmeline/Projects/ODMToolsPython/odmtools/lib")
from ObjectListView import VirtualObjectListView as OLV, ColumnDefn
import pandas as pd
import numpy as np
# Simple minded model objects for our examples

import datetime


class Track(object):
    """
    Simple minded object that represents a song in a music library
    """

    def __init__(self, title, artist, album, sizeInBytes, lastPlayed, rating):
        self.title = title
        self.artist = artist
        self.album = album
        a = datetime.datetime.strptime(lastPlayed, "%d/%m/%Y %H:%M")
        datenp = np.datetime64(a)
        self.lastPlayed = datenp
        # self.date = datenp - datenp.astype('datetime64[M]') + 1

        self.years = datenp.astype('datetime64[Y]').astype(int) + 1970
        #months = dates.astype('datetime64[M]').astype(int) % 12 + 1

        #self.lastPlayed = datetime.datetime.strptime(lastPlayed, "%d/%m/%Y %H:%M")
        #self.date = datetime.datetime.strptime(lastPlayed, "%d/%m/%Y %H:%M").date()
        #self.time = unicode(datetime.datetime.strptime(lastPlayed, "%d/%m/%Y %H:%M").time())
        # print "type of self.time: ", type(self.time), str(self.time)

        self.sizeInBytes = sizeInBytes
        self.rating = rating

    def GetSizeInMb(self):
        return self.sizeInBytes / (1024.0 * 1024.0)

    def __repr__(self):
        return "%s - %s " % (self.artist, self.title)


class ExampleOlv(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 700), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        #self.dataframe = pd.DataFrame(self.GetTracks(), columns=['Title', 'Artist', 'Album', 'Last Played',
        #                                                              'SizeInBytes', 'Rating'])
        self.dataObjects = self.GetTracks()
        print "self.dataObjects[index % len(self.dataObjects)]: ", self.dataObjects[0 % len(self.dataObjects)]

        boxSizer = wx.BoxSizer(wx.VERTICAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"%s" % len(self.dataObjects)), wx.VERTICAL)
        self.olv = OLV(self, wx.ID_ANY, style=wx.LC_REPORT)
        self.olv.useAlternateBackColors = True
        self.olv.oddRowsBackColor = wx.Colour(191, 239, 255)
        self.olv.SetEmptyListMsg("Add points either by csv or manually")

        columns = [
            ColumnDefn("Title", "left", -1, valueGetter="title", minimumWidth=125),
            ColumnDefn("Artist", "left", -1, valueGetter="artist", minimumWidth=125),
            ColumnDefn("Album", "left", -1, valueGetter="album", minimumWidth=125),
            ColumnDefn("Last Played", "left", -1, valueGetter="lastPlayed", minimumWidth=125),
            # ColumnDefn("Date Played", "left", -1, valueGetter="date", minimumWidth=125),
            #ColumnDefn("Time Played", "left", -1, valueGetter="time", minimumWidth=125),
            ColumnDefn("SizeInBytes", "left", -1, valueGetter="sizeInBytes", minimumWidth=125),
            ColumnDefn("Rating", "left", -1, valueGetter="rating", minimumWidth=125),
        ]
        self.olv.SetColumns(columns)

        self.olv.SetObjectGetter(self.objectGetter)
        self.olv.SetItemCount(len(self.dataObjects))

        self.selectBtn = wx.Button(self, wx.ID_ANY, "Select 5 points randomly")
        boxSizer.Add(self.olv, 1, wx.ALL | wx.EXPAND, 5)
        boxSizer.Add(self.selectBtn, 0, wx.ALL, 5)

        sbSizer1.Add(boxSizer, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sbSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        self.selectBtn.Bind(wx.EVT_BUTTON, self.onButton)
        self.olv.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onItemSelected)
        self.olv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.GetOLVColClicked)

        # for wxMSW
        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)

        # Register the "editor factory" for wx.Colour objects
        # CellEditorRegistry().RegisterCreatorFunction(time, self.timeEditor)
        self.Show()

    def OnRightClick(self, event):
        """
        Allow users to sort based off of column
        """
        ## Get column clicked
        selected_column = self.GetOLVColClicked(event=None)
        print "OnrightClick", selected_column


    def objectGetter(self, index):
        """
        A Virtual list has to have a callable installed that says which model object is shown
        at a given index
        """
        return self.dataObjects[index % len(self.dataObjects)]

    def GetOLVColClicked(self, event):

        # DevPlayer@gmail.com  2011-01 Jan-13
        # For use with a 3rd party module named ObjectListView
        # used with wxPython.

        """
        GetColClicked( event ) -> int Column number of mouse click.

        Get ObjectListView() column the user single-left-clicked the mouse in.

        You can use the column number to set the modelObject's attributes
        without removing, re-adding, resorting the items in the OVL.

        This event handler is often bound to the event handler of the
        wx.EVT_LIST_ITEM_SELECTED event. Other events may be needed for
        the column's labels - the labels visually naming a column.

        This assumes the OLV.LayoutDirection() is LTR.
        """

        # ----------------------------------------------------------
        # Get the mouse position. Determine which column the user
        # clicked in.
        # This could probably all be done in some list hit test event.
        # Not all OS platforms set all events m_...atributes. This is a
        # work around.

        # Get point user clicked, here in screen coordinates.
        # Then convert the point to OVL control coordinates.

        spt = wx.GetMousePosition()
        fpt = self.olv.ScreenToClient(spt)  # USE THIS ONE
        x, y = fpt

        # log( o, "GetOLVColClicked()                                   event.m_col: %d "% event.m_col)
        #log( o, "GetOLVColClicked()    folv.ScreenToClient(wx.GetMousePosition()): %d "% x)

        # Get all column widths, individually, of the OLV control .
        # Then compare if the mouse clicked in that column.

        # Make this a per-click calculation as column widths can
        # change often by the user and dynamically by different
        # lengths of data strings in rows.

        last_col = 0
        col_selected = None
        for col in range(self.olv.GetColumnCount()):

            # Get this OLV column's width in pixels.

            col_width = self.olv.GetColumnWidth(col)

            # Calculate the left and right vertical pixel positions
            # of this current column.

            left_pxl_col = last_col
            right_pxl_col = last_col + col_width - 1

            # Compare mouse click point in control coordinates,
            # (verse screen coordinates) to left and right coordinate of
            # each column consecutively until found.

            if left_pxl_col <= x <= right_pxl_col:
                # Mouse was clicked in the current column "col"; done

                col_selected = col
                break

            col_selected = None
            # prep for next calculation of next column

            last_col = last_col + col_width
        print "Col_selected: ", col_selected
        return col_selected

    def onItemSelected(self, event):
        item = event.m_itemIndex
        # focusedItem = obj.GetFocusedItem()
        # obj.GetSelectedItems()
        # item = self.dataObjects[focusedItem]
        # for i in dir(obj):
        #   print i
        print "Selected Object: ", item, self.olv.GetItemText(item)  #, self.olv.GetItem(item, "SizeInBytes")

    def onButton(self, event):
        results = self.GetSelections()
        items = [0,1,5,6,8,9,10, 11, 15]

        #print items
        for i in items:
            self.olv.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
            self.olv.Focus(i)
        # self.olv.SelectObjects(self.dataObjects[:5])
        print "Selecting ", len(results)

    def GetSelections(self):  # helper / used internally
        # return a (possibly empty) list of the
        # currently selected ROW indexes

        result = []
        iRow = -1
        while True:
            iRow = self.olv.GetNextItem(iRow, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if iRow < 0:
                break
            result.append(iRow)
        # print "GetSelections:", result
        return result

    def returnDatetime(self, i):
        return datetime.datetime.strptime(i, "%d/%m/%Y %H:%M")
    def GetTracks(self):
        """
        Return a collection of tracks
        """
        return [
                   Track("shiver", "Natalie Imbruglia", "Counting Down the Days", 8.6 * 1024 * 1024 * 1024,
                         "9/03/2008 9:51", 80),
                   Track("Who's Gonna Ride Your Wild Horses", "U2", "Achtung Baby", 6.3 * 1024 * 1024,
                         "9/10/2007 11:32", 80),
                   Track("So Cruel", "U2", "Achtung Baby", 6.9 * 1024 * 1024, "19/10/2007 11:42", 60),
                   Track("The Fly", "U2", "Achtung Baby", 5.4 * 1024 * 1024, "9/10/2007 11:42", 60),
                   Track("Tryin' To Throw Your Arms Around The World", "U2", "Achtung Baby", 4.7 * 1024 * 1024,
                         "9/10/2007 11:46", 60),
                   Track("Ultraviolet (Light My Way)", "U2", "Achtung Baby", 6.6 * 1024 * 1024, "9/10/2007 11:52", 60),
                   Track("Acrobat", "U2", "Achtung Baby", 5.4 * 1024 * 1024, "9/10/2007 11:56", 60),
                   Track("Love Is Blindness", "U2", "Achtung Baby", 5.3 * 1024, "9/10/2007 12:00", 60),
                   Track("Elevation", "U2", "All That You Can't Leave Behind", 459, "25/01/2008 11:46", 60),
                   Track("Walk On", "U2", "All That You Can't Leave Behind", 5.8 * 1024 * 1024, "18/03/2008 11:39",
                         100),
                   Track("Kite", "U2", "All That You Can't Leave Behind", 5.2 * 1024 * 1024, "23/01/2008 10:36", 40),
                   Track("In A Little While", "U2", "All That You Can't Leave Behind", 4.3 * 1024 * 1024,
                         "20/01/2008 7:48", 60),
                   Track("Wild Honey", "U2", "All That You Can't Leave Behind", 4.5 * 1024 * 1024, "13/04/2007 11:50",
                         40),
                   Track("Peace On Earth", "U2", "All That You Can't Leave Behind", 5.6 * 1024 * 1024,
                         "22/12/2007 2:51", 40),
                   Track("When I Look At The World", "U2", "All That You Can't Leave Behind", 5.1 * 1024 * 1024,
                         "22/12/2007 2:55", 40),
                   Track("New York", "U2", "All That You Can't Leave Behind", 6.4 * 1024 * 1024, "22/12/2007 3:01", 60),
                   Track("Grace", "U2", "All That You Can't Leave Behind", 6.5 * 1024 * 1024, "22/12/2007 3:06", 40),
                   Track("The Ground Beneath Her Feet(Bonus Track)", "U2", "All That You Can't Leave Behind",
                         4.4 * 1024 * 1024, "22/12/2007 3:10", 40),
                   Track("Follow You Home", "Nickelback", "All The Right Reasons", 6 * 1024 * 1024, "6/03/2008 10:42",
                         40),
                   Track("Fight For All The Wrong Reason", "Nickelback", "All The Right Reasons", 5.2 * 1024 * 1024,
                         "15/03/2008 5:04", 60),
                   Track("Photograph", "Nickelback", "All The Right Reasons", 6 * 1024 * 1024, "15/03/2008 5:08", 60),
                   Track("Animals", "Nickelback", "All The Right Reasons", 4.3 * 1024 * 1024, "16/02/2008 12:12", 40),
                   Track("Savin' Me", "Nickelback", "All The Right Reasons", 5.1 * 1024 * 1024, "24/03/2008 10:41", 80),
               ] * 50000  # * 1000000

    def GetTracksForDF(self):
        """
        Return a collection of tracks
        """
        return [
                   ["shiver", "Natalie Imbruglia", "Counting Down the Days", 8.6 * 1024 * 1024 * 1024,
                    "9/03/2008 9:51", 80],
                   ["Who's Gonna Ride Your Wild Horses", "U2", "Achtung Baby", 6.3 * 1024 * 1024,
                    "9/10/2007 11:32", 80],
                   ["So Cruel", "U2", "Achtung Baby", 6.9 * 1024 * 1024, "19/10/2007 11:42", 60],
                   ["The Fly", "U2", "Achtung Baby", 5.4 * 1024 * 1024, "9/10/2007 11:42", 60],
                   ["Tryin' To Throw Your Arms Around The World", "U2", "Achtung Baby", 4.7 * 1024 * 1024,
                    "9/10/2007 11:46", 60],
                   ["Ultraviolet (Light My Way)", "U2", "Achtung Baby", 6.6 * 1024 * 1024, "9/10/2007 11:52", 60],
                   ["Acrobat", "U2", "Achtung Baby", 5.4 * 1024 * 1024, "9/10/2007 11:56", 60],
                   ["Love Is Blindness", "U2", "Achtung Baby", 5.3 * 1024, "9/10/2007 12:00", 60],
                   ["Elevation", "U2", "All That You Can't Leave Behind", 459, "25/01/2008 11:46", 60],
                   ["Walk On", "U2", "All That You Can't Leave Behind", 5.8 * 1024 * 1024, "18/03/2008 11:39",
                    100],
                   ["Kite", "U2", "All That You Can't Leave Behind", 5.2 * 1024 * 1024, "23/01/2008 10:36", 40],
                   ["In A Little While", "U2", "All That You Can't Leave Behind", 4.3 * 1024 * 1024,
                    "20/01/2008 7:48", 60],
                   ["Wild Honey", "U2", "All That You Can't Leave Behind", 4.5 * 1024 * 1024, "13/04/2007 11:50",
                    40],
                   ["Peace On Earth", "U2", "All That You Can't Leave Behind", 5.6 * 1024 * 1024,
                    "22/12/2007 2:51", 40],
                   ["When I Look At The World", "U2", "All That You Can't Leave Behind", 5.1 * 1024 * 1024,
                    "22/12/2007 2:55", 40],
                   ["New York", "U2", "All That You Can't Leave Behind", 6.4 * 1024 * 1024, "22/12/2007 3:01", 60],
                   ["Grace", "U2", "All That You Can't Leave Behind", 6.5 * 1024 * 1024, "22/12/2007 3:06", 40],
                   ["The Ground Beneath Her Feet(Bonus Track)", "U2", "All That You Can't Leave Behind",
                    4.4 * 1024 * 1024, "22/12/2007 3:10", 40],
                   ["Follow You Home", "Nickelback", "All The Right Reasons", 6 * 1024 * 1024, "6/03/2008 10:42",
                    40],
                   ["Fight For All The Wrong Reason", "Nickelback", "All The Right Reasons", 5.2 * 1024 * 1024,
                    "15/03/2008 5:04", 60],
                   ["Photograph", "Nickelback", "All The Right Reasons", 6 * 1024 * 1024, "15/03/2008 5:08", 60],
                   ["Animals", "Nickelback", "All The Right Reasons", 4.3 * 1024 * 1024, "16/02/2008 12:12", 40],
                   ["Savin' Me", "Nickelback", "All The Right Reasons", 5.1 * 1024 * 1024, "24/03/2008 10:41", 80]
               ] * 50000  # * 1000000

    def GetSample(self):

        return [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],

        ] * 9999


if __name__ == '__main__':
    app = wx.App()
    frame = ExampleOlv(None)
    app.MainLoop()