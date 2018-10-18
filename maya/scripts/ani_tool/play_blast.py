#coding=utf-8
import os
import pymel.core as pm

def main():
    current_path = pm.mel.eval("file -q -sn")
    filename = os.path.basename(current_path)
    filename = os.path.splitext(filename)[0] + ".mov"

    rp_code = os.path.dirname(current_path).split("/")[-1]
    render_path = os.path.join(os.path.dirname(current_path)[:-len(rp_code)], "mov")

    filename = os.path.join(render_path, filename).replace("\\", "/")

    start = pm.playbackOptions(q=True, minTime=True)
    end = pm.playbackOptions(q=True, maxTime=True)
    width = pm.getAttr('defaultResolution.width')
    height = pm.getAttr('defaultResolution.height')

    media_temp_file = filename

    pm.mel.eval(
        'playblast  -format qt -filename "%s" -forceOverwrite  -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -offScreen  -fp 4 -percent 50 -compression "H.264" -quality 100 -widthHeight %s %s;' % (
        media_temp_file, width, height))


