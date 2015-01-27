#Editing Data Series#

ODM Tools Python includes functionality to edit data values, add qualifiers to data values, derive new data series, and save edits to data series stored within an ODM database. Data editing is important for performing quality control and post processing on data series where some data values may need to be deleted, adjusted, or interpolated. Deriving data series is useful for aggregating data (e.g., daily average derived from high frequency measurements) or generating a data series that is a function of one or more other data series (e.g., discharge as a function of stage). Currently the functionality to derive new data series is not built into ODMTools Python.

##Selecting Series for Editing##

The 'Edit' tab is used to perform edits on data series. The visualizations that are created in the 'View' tab will carry over to the 'Edit' tab, and the Series Selector is used to show/hide data series in the plot. This way, multiple data series can still be viewed while edits are made. Only one data series can be edited at a time. To select a series for editing, the series of interest should be the highlighted in the Series Selector. Click on the 'Edit Series' button in the ribbon to begin editing. When a series is in editing mode, a few aspects of the plot change:

   1. The symbology of the series of interest changes from the plot type and color selected in the 'Plot' tab to black squares and lines. The symbology of any additional displayed series are made more subtle. ![EditingSeriesMultiple](images/EditingSeriesMultiple.png)

   1. The 'No Data' values that were previously hidden are now be plotted. This will often change the zoom level on the plot since large, negative numbers are typically used to indicate 'No Data' (e.g., -9999). ![EditingSeries](images/EditingSeries.png)

   1. If the series selected for editing was not plotted previously, it will automatically be plotted.

