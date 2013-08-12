#Boa:FramePanel:pnlDataTable

import wx
import wx.grid
from ObjectListView import ColumnDefn, FastObjectListView
from wx.lib.pubsub import pub as Publisher
import odmdata
import sqlite3

[wxID_PNLDATATABLE, wxID_PNLDATATABLEDATAGRID,
] = [wx.NewId() for _init_ctrls in range(2)]


class pnlDataTable(wx.Panel):

    # selectedpoints = []
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLDATATABLE, name=u'pnlDataTable',
              parent=prnt,  size=wx.Size(677, 449),
              style=wx.TAB_TRAVERSAL)
        self.myOlv = FastObjectListView(self, -1, style=wx.LC_REPORT)#Virtual



        # self.myOlv.SetObjectGetter(self.fetchFromDatabase)
        self.myOlv.SetEmptyListMsg("")

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL|wx.EXPAND, 4)
        self.SetSizer(sizer_2)
        self.doneselecting=True

        self.myOlv._highlightBrush=wx.Brush("red")
        self.myOlv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected )
##        self.myOlv.Bind(wx.EVT_LIST_COL_END_DRAG , self.OnLUp,id=wxID_PNLDATATABLE )
##        self.myOlv.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeSelected )
##        self.myOlv.Bind(wx.EVT_LEFT_UP, self.OnLUp, id=wxID_PNLDATATABLE )
##        self.myOlv.Bind(wx.EVT_LEFT_DOWN, self.OnLDown, id=wxID_PNLDATATABLE)
        Publisher.subscribe(self.OnChangeSelection, ("changeTableSelection"))
        Publisher.subscribe(self.OnRefresh, ("refreshTable"))

        self.Layout()

    # def Init(self, DVConn):
    #     self.cursor = DVConn
    #     sql = "SELECT * FROM DataValuesEdit"
    #     self.cursor.execute(sql)

    #     self.myOlv.SetColumns( ColumnDefn(x[0], valueGetter=i, minimumWidth=40) for (i,x) in enumerate(self.cursor.description))

    #     #####table Settings
    #     self.myOlv.useAlternateBackColors = True
    #     self.myOlv.oddRowsBackColor = "SlateGray"
    #     self.myOlv.AutoSizeColumns()


    #     self.values = [list(x) for x in self.cursor.fetchall()]
    #     self.myOlv.SetObjects(self.values)


    def Init(self, dataRep, record_service):
        self.dataRep = dataRep
        self.record_service = record_service

        self.myOlv.SetColumns( ColumnDefn(x, valueGetter=i, minimumWidth=40) for x, i in self.dataRep.getEditColumns())

        #####table Settings
        self.myOlv.useAlternateBackColors = True
        self.myOlv.oddRowsBackColor = "SlateGray"
        self.myOlv.AutoSizeColumns()


        # self.values = [list(x) for x in self.cursor.fetchall()]
        self.myOlv.SetObjects(self.dataRep.getDataValuesforEdit())

    def OnRefresh(self, e):
        self.myOlv.SetObjects(self.dataRep.getDataValuesforEdit())

    def Clear(self):
        self.dataRep= None
        self.record_service = None
        self.myOlv.SetObjects(None)

    def OnLUp (self, event):
        print "in up"
        self.doneselecting = True

    def OnLDown(self, event):
        print "in down"
        self.doneselecting = False

    def OnItemSelected(self, event):
        # print "in onItemSelected"

        # if  not (event.m_itemIndex in self.selectedpoints):
        #     self.selectedpoints.Add(event.m_itemIndex)

        if self.doneselecting:
            selectedids = self.getSelectedIDs(self.myOlv.GetSelectedObjects())
            Publisher.sendMessage(("changePlotSelection"), sellist = selectedids)

    def OnItemDeSelected(self, event):
        print event.m_itemIndex
        # self.selectedpoints.remove(event.m_itemIndex)

    def getSelectedIDs(self, selobjects):
        idlist=[False] * self.dataRep.getEditRowCount()
        for sel in selobjects:
            idlist[self.myOlv.GetIndexOf(sel)]=True
        # print idlist
        return idlist


    def OnChangeSelection(self, sellist):
        objlist=[]
        # print sellist
        # print type(sellist)

        for i in range(len(sellist)):
            if sellist[i]:
                objlist.append(self.myOlv.GetObjectAt(i))
        # print objlist
        self.doneselecting = False
        self.myOlv.SelectObjects(objlist, deselectOthers=True)
        self.doneselecting = True
        self.myOlv.SetFocus()

    def stopEdit(self):
        self.Clear()


# a) Call self.list_ctrl.SetFocus() right after you click the button;
# b) Change the self._highlightUnfocusedBrush and self._highlightBrush
# colours in the ULC source code to always return the brush colours you
# want (not recommended).



#########self.myOlv.GetCheckedObjects
#########IsChecked(ModelObject)
########Uncheck(modelObject), Check(modelObject)







    def __init__(self, parent, id,  size, style, name, pos=None):
        self._init_ctrls(parent)

