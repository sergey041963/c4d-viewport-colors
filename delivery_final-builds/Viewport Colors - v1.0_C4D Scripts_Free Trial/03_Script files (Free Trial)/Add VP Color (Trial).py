"""
Viewport Colors - Scripts Package v1.0 (Trial Version)
Thanks for download - for commercial and personal uses.
The Viewport Colors v1.0 (Trial Version) granted shall not be copied, distributed, or-sold, offered for resale, transferred in whole or in part except that you may make one copy for archive purposes only.

be.net/dyne
Writen by: Carlos Dordelly
Special thanks: Pancho Contreras, Terry Williams & Roberto Gonzalez

Now you can easily add a quickly reference colors to your objects without lost your applied materials (from any render engine).
Date: 05/08/2017
Written and tested in Cinema 4D R18 / R17 / R16 - Not tested in older versions.

If you like this trial version you can purchase the full version from viewport colors with a lot of more features in aescripts.com

"""

import c4d, random, colorsys
from c4d import gui

DEG30 = 30/360.

def adjacent_colors((r, g, b), d=DEG30):
    h, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
    h = [(h+d) % 1 for d in (-d, d)]           # Rotation by d
    adjacent = [map(lambda x: int(round(x*255)), colorsys.hls_to_rgb(hi, l, s))
            for hi in h] # H'LS -> new RGB
    return adjacent
    #credit of this function from mmgp user from stackoverflow, thxs

def color_dialog():
    cdlg = c4d.gui.ColorDialog(1)
    if cdlg == None:
        gui.MessageDialog('No color selected.')
        #trial version dialog <---- you can delete this and next line if you want to delete trial dialogs.
        gui.MessageDialog('Thanks for use the trial version of Viewport Colors.\n You can download the full version in aescripts.com')
        return
    return cdlg

def vp_color():
    
    #get active objects
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.')
        #trial version dialog <---- you can delete this and next line if you want to delete trial dialogs.
        gui.MessageDialog('Thanks for use the trial version of Viewport Colors.\n You can download the full version in aescripts.com')
        return

    #shorcuts to random functions
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT: 
            cdlg = color_dialog ()
            if cdlg == None:
                return
            cdlg_bckp = cdlg
            inputv = 1
             
        elif  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: 
            cdlg = color_dialog ()
            if cdlg == None:
                return
            cdlg_bckp = cdlg
            inputv = 2

        else:
            cdlg = color_dialog ()
            if cdlg == None:
                return
            inputv = 0

    #start undo action
    doc.StartUndo()

    #viewport color actions
    for obj in activeObjects:
        #if input key is SHIFT
        if inputv == 1:
            cdlg = cdlg_bckp
            #set random variables values
            rvalue=0.8
            #random red value
            rr=(cdlg[0])+(round(random.uniform(0, rvalue),3))
            if rr >= 1:
                rr=(cdlg[0])-((cdlg[0]/64)-(round(random.uniform(0, rvalue),3)))
            elif rr<= 0.4:
                rr=(cdlg[0])-(round(random.uniform(0, (rvalue/32)),3))
            #random green value
            rg=(cdlg[1])+(round(random.uniform(0, rvalue),3))
            if rg >= 1:
                rg=(cdlg[1])-((cdlg[1]/64)-(round(random.uniform(0, rvalue),3)))
            elif rg<= 0.4:
                rg=(cdlg[1])-(round(random.uniform(0, (rvalue/32)),3))
            #random blue value
            rb=(cdlg[2])+(round(random.uniform(0, rvalue),3))
            if rb >= 1:
                rb=(cdlg[2])-((cdlg[2]/64)-(round(random.uniform(0, rvalue),3)))
            elif rb<= 0.4:
                rb=(cdlg[2])-(round(random.uniform(0, (rvalue/32)),3))
            #clamp values
            rclamp = max(min(rr, 1), 0)
            gclamp = max(min(rg, 1), 0)
            bclamp = max(min(rb, 1), 0)
            #reasign variables
            rr=rclamp
            rg=gclamp
            rb=bclamp
            rcdlg = c4d.Vector(rr,rg,rb)
            cdlg = rcdlg

        #if input key is ALT
        elif inputv == 2:
            #redifine cdlg list
            cdlg = cdlg_bckp
            r=cdlg[0]
            g=cdlg[1]
            b=cdlg[2]
            cdlg = [r,g,b]
            cdlg = [round(x,3) for x in cdlg]

            #define adjacent colors
            adjc_01 = adjacent_colors (cdlg)[0]
            adjc_02 = adjacent_colors (cdlg)[1]
            adjc_01_float = [x / 255.0 for x in adjc_01]
            adjc_02_float = [x / 255.0 for x in adjc_02]
            adjc_01_float = [round(x,3) for x in adjc_01_float]
            adjc_02_float = [round(x,3) for x in adjc_02_float]

            #random values in adjacent range <- if you understand this you can switch between adjacent random mode ;)
            #rr=round(random.uniform(adjc_01_float[0], adjc_02_float[0]),3)
            #rg=round(random.uniform(adjc_01_float[1], adjc_02_float[1]),3)
            #rb=round(random.uniform(adjc_01_float[2], adjc_02_float[2]),3)
            #cdlg = c4d.Vector(rr,rg,rb)
            
            #random choices from key color and adjacent colors <- if you understand this you can switch between adjacent random mode ;)
            rlist = [cdlg, adjc_01_float, adjc_02_float]
            vlist = random.choice(rlist)
            cdlg = c4d.Vector(vlist[0],vlist[1],vlist[2])

        else:
            cdlg = cdlg            

        doc.AddUndo(c4d.UNDOTYPE_CHANGE,obj)
        obj[c4d.ID_BASEOBJECT_USECOLOR]=2
        obj[c4d.ID_BASEOBJECT_COLOR]=cdlg

        #if obj is a null delete vcolor 
        obj_type=obj.GetType()
        null_id = 5140
        if obj_type == null_id:
            obj[c4d.ID_BASEOBJECT_COLOR]=c4d.Vector(1,1,1) #set to default
            obj[c4d.ID_BASEOBJECT_USECOLOR]=0 #set to default

    #end undo action
    doc.EndUndo()

    #do redo action
    doc.DoRedo()

    #update scene
    c4d.EventAdd()
   

if __name__=='__main__':
    vp_color()