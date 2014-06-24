import logging
import wx
import wx.lib.agw.ultimatelistctrl as ULC
##used for Series Selector
from common.logger import LoggerTool

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


class clsULC(ULC.UltimateListCtrl):
    def __init__(self, *args, **kwargs):
        self.modelObjects = []
        self.subList = []
        self.columns = []
        self.filter = None
        self.useAlternateBackColors = True
        self.evenRowsBackColor = "White"  #wx.Colour(240, 248, 255) # ALICE BLUE
        self.oddRowsBackColor = "SlateGray"  #wx.Colour(255, 250, 205) # LEMON CHIFFON
        #self.cursor = None
        self.checkCount = 0
        self.checkLimit = 6
        # wx.ListCtrl.__init__(self, *args, **kwargs)
        ULC.UltimateListCtrl.__init__(self, *args, **kwargs)


    def clear(self):
        self.emptyTable()
        self.checkCount = 0

    def setColumns(self, columns):
        # self.columns = columns
        # # for c in columns:
        # 	self.columns.append(c)
        ULC.UltimateListCtrl.ClearAll(self)
        colnum = 0
        self.InsertColumn(col=colnum, format=wx.LIST_FORMAT_CENTRE, heading=u'',
                          width=25)
        for c in columns:
            colnum += 1
            self.columns.append({'title': c, 'colid': colnum})
            if "ID" in c:
                self.InsertColumn(col=colnum, format=wx.LIST_FORMAT_LEFT,
                                  heading=c, width=50)
            elif "Selected" in c:
                pass
            #do nothing this is the isSelected column
            else:
                self.InsertColumn(col=colnum, format=wx.LIST_FORMAT_LEFT,
                                  heading=c, width=140)

    def emptyTable(self):
        self.ModelObjects = None
        self.repopulateList()


    def setObjects(self, modelObjects):
        self.modelObjects = modelObjects
        self.repopulateList()


    # remaining values after filtering
    def _buildInnerList(self):
        if self.filter:
            self.subList = self.filter(self.modelObjects)
        else:
            self.subList = self.modelObjects


    def repopulateList(self):
        #self.DeleteAllItems()
        self._buildInnerList()


        '''
        for series in self.subList:
            ind = self.GetItemCount()

            self.Append([False] + series[:-1])
            self.SetStringItem(ind, 0, "", it_kind=1)

            #if item isSelected is true check the box when drawing the row
            if series[-1] == 1:
                self._mainWin.CheckItem(self.GetItem(ind, 0), True, False)
                #self.Select(0, True)
        '''

    def getSelection(self):
        #returns the one highlighted row in the table
        return self.GetFirstSelected()

    def getObjectAt(self, index):
        return self.subList[index]

    # 	def GetObjectAt(self, index):
    # 	# """
    # 	# Return the model object at the given row of the list.
    # 	# """
    # 	# Because of sorting, index can't be used directly, which is
    # 	# why we set the item data to be the real index
    # 	return self.innerList[self.GetItemData(index)]

    # def AddCheckedItem(self, id):
    # 	pass

    # def RemoveCheckedItem(self, id):
    # 	pass
    def removeChecked(self):
        self.checkCount = 0
        for model in self.modelObjects:
            if model[-1]:
                model[-1] = False

    def isChecked(self, index):
        return self.modelObjects[index][-1]

    def getChecked(self):
        #returns a list of the checked ids
        return [x[0] for x in self.modelObjects if x[-1]]

    # Return True if the number selected is less than 6
    # Return False if the box isn't checked
    def enableCheck(self, id, isChecked):
        # Keeping adding
        if self.checkCount < self.checkLimit and isChecked:
            self.subList[id][-1] = isChecked
            self.checkCount += 1
            #logger.debug("CheckCount: %d" % (self.checkCount))
            return True
        # Uncheck series case
        elif not isChecked:
            self.subList[id][-1] = isChecked
            self.checkCount -= 1
            #logger.debug("CheckCount: %d" % (self.checkCount))
            return False

        # Trying to check but reached max
        else:
            # uncheck it visibly
            self.checkItem(id, isChecked=False)
            self.subList[id][-1] = False
            #logger.debug("CheckCount: %d" % (self.checkCount))
            return False

    # check visibly on SeriesSelector gui
    def checkItem(self, index, isChecked=True, sendEvent=False):
        self.subList[index][-1] = 1
        # TODO clsUCL object has no attribute 'getItem'
        self._mainWin.CheckItem(self.GetItem(index, 0), isChecked, sendEvent)

    def getColumnText(self, index, colid):
        # print self.GetItemData(index)
        item = self.GetItem(index, colid)
        # print item
        return item.GetText()

    def getStringValue(self, col, modelObject=None, row=None):
        if modelObject:
            return modelObject[self.getColID(col['title'])]
        else:
            return self.modelObjects[row][self.getColID(col['title'])]

    def setStringValue(self, col, Value, modelObject=None, row=None):
        if modelObject:
            modelObject[self.getColID(col['title'])] = Value
        else:
            self.modelObjects[row][self.getColID(col['title'])] = Value

    def getFilter(self):
        return self.filter

    def getFilteredObjects(self):
        return self.subList

    def setFilter(self, filter):
        self.filter = filter

    def clearFilter(self):
        self.filter = None

    def getColID(self, element):
        if element == 'SeriesID':
            return 0
        elif element == 'SiteID':
            return 1
        elif element == 'SiteCode':
            return 2
        elif element == 'SiteName':
            return 3
        elif element == 'VariableID':
            return 4
        elif element == 'VariableCode':
            return 5
        elif element == 'VariableName':
            return 6
        elif element == 'Speciation':
            return 7
        elif element == 'VariableUnitsID':
            return 8
        elif element == 'VariableUnitsName':
            return 9
        elif element == 'SampleMedium':
            return 10
        elif element == 'ValueType':
            return 11
        elif element == 'TimeSupport':
            return 12
        elif element == 'TimeUnitsID':
            return 13
        elif element == 'TimeUnitsName':
            return 14
        elif element == 'DataType':
            return 15
        elif element == 'GeneralCategory':
            return 16
        elif element == 'MethodID':
            return 17
        elif element == 'MethodDescription':
            return 18
        elif element == 'SourceID':
            return 19
        elif element == 'SourceDescription':
            return 20
        elif element == 'Organization':
            return 21
        elif element == 'Citation':
            return 22
        elif element == 'QualityControlLevelID':
            return 23
        elif element == 'QualityControlLevelCode':
            return 24
        elif element == 'BeginDateTime':
            return 25
        elif element == 'EndDateTime':
            return 26
        elif element == 'BeginDateTimeUTC':
            return 27
        elif element == 'EndDateTimeUTC':
            return 28
        elif element == 'ValueCount':
            return 29
        elif element == 'isSelected':
            return 30
        else:
            return None


class TextSearch(object):
    def __init__(self, objectListView, columns=(), text="", var=""):

        self.objectListView = objectListView
        self.columns = columns
        self.text = text
        self.var = var

    def __call__(self, modelObjects):
        #if not self.text:
        #    return modelObjects
        if self.objectListView is None:
            logger.fatal("Unable to filter due to modelObjects being empty")
            return []

        def _filteredObjects(object):
            if self.text and self.var:
                return object.site.code == self.text and object.variable_code == self.var
            if self.text:
                return object.site.code == self.text
            if self.var:
                return object.variable_code == self.var

        test = [x for x in self.objectListView if _filteredObjects(x)]
        print test
        return test

        '''
        def _containsText(modelObject):

            for col in cols:
                logging.debug("text to find", textToFind)
                if textToFind == self.objectListView.getStringValue(
                        modelObject=modelObject, col=col).lower():  #col.GetStringValue(modelObject).lower():
                    return True
            return False
        '''

        #return [x for x in modelObjects if _containsText(x)]

    def setText(self, text):
        self.text = text


class Chain(object):
    def __init__(self, *filters):
        print "Filters: ", filters
        self.filters = filters

    def __call__(self, modelObjects):
        for filter in self.filters:
            modelObjects = filter(modelObjects)
        return modelObjects
