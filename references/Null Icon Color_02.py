"""
Geo Color - Scripts Package v2.0
Thanks for download - for commercial and personal uses.
The Geo Color v2.0 granted shall not be copied, shared, distributed, re-sold, offered for re-sale, transferred in whole or in part except that you may make one copy for archive purposes only.

be.net/dyne
Writen by: Carlos Dordelly
Special thanks: Pancho Contreras, Terry Williams & Roberto Gonzalez

Now you can easily add a quickly reference colors to your objects without lost your applied materials (from any render engine).
Date: 26/06/2017
Written and tested in Cinema 4D R18 / R17 / R16 - Not tested in older versions.

"""

import c4d
from c4d import gui

def geo_color():
    
    #get Active Objects
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.')
        return

    #color dialog
    cdlg = c4d.gui.ColorDialog(1)
    if cdlg == None:
        gui.MessageDialog('No color selected.')
        return
    
    #start undo action
    doc.StartUndo()

    #geo color actions
    for obj in activeObjects:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE,obj)
        
        #activeObject = doc.GetActiveObject()
        typeObject = obj.GetType()
        print typeObject

        obj[c4d.ID_BASEOBJECT_USECOLOR]=2
        obj[c4d.ID_BASEOBJECT_COLOR]=cdlg
        obj[c4d.ID_BASEOBJECT_XRAY]=False
        obj.KillTag(c4d.Tdisplay)

    #end undo action
    doc.EndUndo()

    #do redo action
    doc.DoRedo()

    #update scene
    c4d.EventAdd()
   
 
if __name__=='__main__':
    geo_color()