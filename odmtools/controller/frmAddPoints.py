"""Subclass of AddPoints, which is generated by wxFormBuilder."""
import datetime

import wx

from odmtools.controller.frmBulkInsert import BulkInsert
import odmtools.view.clsAddPoints as clsAddPoints
try:
    from agw import genericmessagedialog as GMD
except ImportError:
    import wx.lib.agw.genericmessagedialog as GMD

# Implementing AddPoints
class AddPoints(clsAddPoints.AddPoints):
    def __init__(self, parent, **kwargs):
        if 'recordService' in kwargs:
            self.recordService = kwargs['recordService']
        clsAddPoints.AddPoints.__init__(self, parent, **kwargs)
        self.frame = BulkInsert(self)

        #self.cvService = serviceManager.get_cv_service()
        #self.recordService = recordService

        self.CenterOnParent()


    # Handlers for AddPoints events.
    def onAddBtn(self, event):
        """

        :param event:
        :return:
        """
        self.olv.AddObject(self.olv.sampleRow())
        self.sb.SetStatusText("Added a row")
        event.Skip()

    def onClearAllBtn(self, event):
        """

        :param event:
        :return:
        """
        if len(self.olv.GetObjects()) < 1:
            wx.MessageBox("Nothing to remove here", " ", wx.OK)
            return
        msg = GMD.GenericMessageDialog(None, 'Are you sure you want to delete your work?', 'Clear Everything?', wx.YES_NO | wx.ICON_WARNING |wx.NO_DEFAULT )
        value = msg.ShowModal()
        if value == wx.ID_YES:
            self.olv.SetObjects(None)
        return

    def onDeleteBtn(self, event):
        """

        :param event:
        :return:
        """
        try:
            if self.selectedObject:
                if len(self.selectedObject) > 1:
                    length = len(self.selectedObject)
                    msg = GMD.GenericMessageDialog(None, 'Are you sure you want to delete %d items' % length,
                                           'Clear items?',
                                           wx.YES_NO | wx.ICON_WARNING | wx.NO_DEFAULT)
                    value = msg.ShowModal()
                    if value == wx.ID_YES:
                        self.customRemove(self.selectedObject)
                        self.sb.SetStatusText("Removed %s items" % length)

                else:
                    self.customRemove(self.selectedObject)
                    self.sb.SetStatusText("Removing %s" % self.selectedObject.dataValue)
        except TypeError as e:

            msg = GMD.GenericMessageDialog(None, 'Are you sure you want to delete your work?', 'Clear items?',
                                   wx.YES_NO | wx.ICON_WARNING | wx.NO_DEFAULT)
            value = msg.ShowModal()
            if value == wx.ID_YES:
                self.customRemove(self.selectedObject)
                #self.sb.SetStatusText("Removing %s" % self.sb.SetStatusText("Removing %s" % self.selectedObject.dataValue))

        self.selectedObject = None

        ## Deleting a cell being edited doesn't finish editing
        if self.olv.cellEditor:
            self.olv.FinishCellEdit()
            
        event.Skip()

    def customRemove(self, object):
        """


        :param object:
        :return:
        """
        obj = self.olv.GetObjects()
        if isinstance(object, list):
            for x in object:
                obj.remove(x)
        else:
            obj.remove(object)
        self.olv.SetObjects(obj)

    def onUploadBtn(self, event):
        """

        :param event:
        :return:
        """
        if not self.frame.IsShown():
            self.frame.CenterOnParent()
            self.frame.Show()
            self.frame.SetFocus()
        else:
            self.frame.Hide()

        event.Skip()

    def onInfoBtn(self, event):
        """

        :param event:
        :return:
        """
        message = "DataValue: FLOAT\n" \
                  "Date: YYYY-MM-DD\n" \
                  "Time: HH:MM:SS\n" \
                  "UTCOffSet: INT (Range [-12,12])\n" \
                  "CensorCode: gt|nc|lt|nd|pnq\n" \
                  "ValueAccuracy: FLOAT\n" \
                  "OffSetValue: INT\n" \
                  "OffSetType: STRING\n" \
                  "QualifierCode: STRING\n" \
                  "LabSampleCode: STRING\n"

        dlg = GMD.GenericMessageDialog(self, message, "Format Guide",
                                       agwStyle=wx.ICON_INFORMATION | wx.OK | GMD.GMD_USE_GRADIENTBUTTONS)
        dlg.ShowModal()
        event.Skip()

    def onFinishedBtn(self, event):
        """

        :param event:
        :return:
        """

        points, isIncorrect = self.parseTable()

        message = ""

        if not points and not isIncorrect:
            #print "Leaving..."
            self.Close()
            return

        elif not points:
            message = "Unfortunately there are no points to add, " \
                      "please check that the data was entered correctly " \
                      "and try again. "
            dlg = GMD.GenericMessageDialog(None, message, "Nothing to add",
                                           agwStyle=wx.ICON_WARNING | wx.CANCEL | wx.OK | GMD.GMD_USE_GRADIENTBUTTONS)
            dlg.SetOKCancelLabels(ok="Return to AddPoint Menu", cancel="Quit to ODMTools")
            value = dlg.ShowModal()

            if value == wx.ID_OK:
                return
            else:
                self.Close()
                return

        elif isIncorrect:
            message = "Are you ready to add points? " \
                      "There are rows that are incorrectly formatted, " \
                      "those rows will not be added. Continue?"
        else:
            message = "Are you ready to add points? " \
                      "Ready to add points to the database?"

        msg = GMD.GenericMessageDialog(None, message, 'Add Points?',
                               wx.YES_NO | wx.ICON_QUESTION | wx.NO_DEFAULT | GMD.GMD_USE_GRADIENTBUTTONS)

        value = msg.ShowModal()
        if value == wx.ID_NO:
            return

        self.recordService.add_points(points)

        self.Close()
        event.Skip()

    def onSelected(self, event):
        obj = event.GetEventObject()
        object = obj.innerList[obj.FocusedItem]
        object = self.olv.GetSelectedObjects()

        #print event, dir(event)

        #print "Objects: ", object

        #event.GetEventObject().SetToolTipString("test")
        try:
            if len(object) > 1:
                self.selectedObject = object
            else:
                self.selectedObject = object[0]
        except TypeError as e:
            pass
        except IndexError as e:
            pass

        event.Skip()

    def parseTable(self):
        """

        :return:
        """
        series = self.recordService.get_series()
        #NULL = self.olv.NULL

        objects = self.olv.GetObjects()

        isIncorrect = False
        points = []

        for i in objects:
            if i.isCorrect():
                row = [None] * 10
                if i.valueAccuracy != "NULL":
                    row[1] = i.valueAccuracy
                if i.offSetType != "NULL":
                    row[6] = i.offSetType
                if i.qualifierCode != "NULL":
                    row[8] = i.qualifierCode
                if i.labSampleCode != "NULL":
                    row[9] = i.labSampleCode

                row[0] = i.dataValue

                dt = self.combineDateTime(i.date, i.time)
                row[2] = dt
                ## UTC Offset
                row[3] = i.utcOffSet
                ## Calculate UTC time based off the localdatetime and utcOffSet
                row[4] = dt - datetime.timedelta(hours=int(i.utcOffSet))
                row[7] = i.censorCode

                row.extend([
                    series.site_id, series.variable_id, series.method_id,
                    series.source_id, series.quality_control_level_id
                    ]
                )

                points.append(tuple(row))
            else:
                isIncorrect = True

        return points, isIncorrect

    def combineDateTime(self, date, time):
        t = datetime.datetime.strptime(time, "%H:%M:%S").time()
        return datetime.datetime.combine(date, t)

class Example(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)
        m = AddPoints(parent)
        m.Show()

if __name__ == '__main__':
    app = wx.App()
    ex = Example(None)
    app.MainLoop()