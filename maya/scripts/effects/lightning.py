# coding=utf-8
# version 1.0
import pymel.core as pm
import maya.cmds as mc
def build_50():
    return main(50)
def build_100():
    return main(100)
def build_150():
    return main(150)
def build_200():
    return main(200)
def main(count=100):
    # create locators
    start_locator = pm.spaceLocator(name="start_point")
    end_locator = pm.spaceLocator(name="end_point")
    pm.setAttr(end_locator.tx, 5)

    start_x = pm.getAttr(start_locator.tx)
    start_y = pm.getAttr(start_locator.ty)
    start_z = pm.getAttr(start_locator.tz)

    end_x = pm.getAttr(end_locator.tx)
    end_y = pm.getAttr(end_locator.ty)
    end_z = pm.getAttr(end_locator.tz)

    # create guide curve and divide into select spans
    guide_curve_transform = pm.curve(name='guide_curve', degree=1, p=([start_x, start_y, start_z], [end_x, end_y, end_z]))

    guide_curve = pm.listRelatives(guide_curve_transform,children=True)[0]
    pm.rebuildCurve(guide_curve, spans=(count-3), degree=3)

    # convert to soft body
    particle_pack = pm.nSoft(guide_curve, convert=True)
    particle_transform = particle_pack[0]
    index=guide_curve[-1]
    try:
        index=int(index)
        particle_transform = pm.rename(particle_transform, "lightning_particle%s"%index)
    except:
        particle_transform = pm.rename(particle_transform, "lightning_particle")
    particle_system = pm.listRelatives(particle_transform, children=True)[0]

    # turn off gravity effects
    pm.setAttr(particle_system.ignoreSolverGravity, 1)

    pm.dynExpression(particle_system, creation=1, string=str(
        "{ps}.position = hermite ( <<{sp}.translateX,{sp}.translateY,{sp}.translateZ>>, \n\t\t\t    <<{ep}.translateX,{ep}.translateY,{ep}.translateZ>>,\n                <<{ep}.translateX-{sp}.translateX,{ep}.translateY-{sp}.translateY,{ep}.translateZ-{sp}.translateZ>>,<<{sp}.translateX-{sp}.translateX,{ep}.translateY-{sp}.translateY,{ep}.translateZ-{sp}.translateZ>>,\n                linstep(0,{ps}.count-1,{ps}.particleId)  );\n\nfloat $inNoise = (0.5- abs(0.5- linstep(0,{ps}.count,{ps}.particleId) ) )*2;\nfloat $speed_1 =  0.5;\nfloat $speed_2 =  2;\nfloat $speed_3 =  2; \n{ps}.position += <<  noise({ps}.particleId/50           + $speed_1*time ), \n\t\t\t   \t\t\t\t\t\tnoise(({ps}.particleId-{ps}.count/2)/50 + $speed_1*time ),\n\t\t\t   \t\t\t\t\t\tnoise(({ps}.particleId-{ps}.count)/50   + $speed_1*time ) >>   * 1 *$inNoise;\n{ps}.position += <<  noise({ps}.particleId/10           + $speed_2*time ),\n\t\t\t   \t\t\t\t\t\tnoise(({ps}.particleId-{ps}.count/2)/10 + $speed_2*time ),\n\t\t\t  \t\t\t\t\t\tnoise(({ps}.particleId-{ps}.count)/10   + $speed_2*time ) >>   *0.3  *$inNoise;\n{ps}.position += <<  noise({ps}.particleId/2            + $speed_3*time ),\n\t\t \t   \t\t\t\t\t\tnoise(({ps}.particleId-{ps}.count/2)/2  + $speed_3*time ),\n\t\t\t   \t\t\t\t\t\tnoise(({ps}.particleId-{ps}.count)/2    + $speed_3*time ) >>   *0.1  *$inNoise;".format(ps=particle_system,sp=start_locator,ep=end_locator)))

    pm.dynExpression(particle_system, runtimeBeforeDynamics=1, string=str(
        "{ps}.position = hermite ( <<{sp}.translateX,{sp}.translateY,{sp}.translateZ>>,\n             <<{ep}.translateX,{ep}.translateY,{ep}.translateZ>>,\n                <<{ep}.translateX-{sp}.translateX,{ep}.translateY-{sp}.translateY,{ep}.translateZ-{sp}.translateZ>>,<<{ep}.translateX-{sp}.translateX,{ep}.translateY-{sp}.translateY,{ep}.translateZ-{sp}.translateZ>>,\n                linstep(0,{ps}.count-1,{ps}.particleId)  );\n\nfloat $inNoise = (0.5- abs(0.5- linstep(0,{ps}.count,{ps}.particleId) ) )*2;\nfloat $speed_1 =  6;\nfloat $speed_2 =  5;\nfloat $speed_3 =  5;\n{ps}.position += <<   noise({ps}.particleId/50           + $speed_1*-time ),\n          noise(({ps}.particleId-{ps}.count/2)/50 + $speed_1*-time ),\n         noise(({ps}.particleId-{ps}.count)/50   + $speed_1*-time ) >>   * 1.3 *$inNoise;\n{ps}.position += <<   noise({ps}.particleId/10           + $speed_2*-time ),\n         noise(({ps}.particleId-{ps}.count/2)/10 + $speed_2*-time ),\n         noise(({ps}.particleId-{ps}.count)/10   + $speed_2*-time ) >>   *0.2  *$inNoise;\n{ps}.position += <<   noise({ps}.particleId/2            + $speed_3*-time ),\n         noise(({ps}.particleId-{ps}.count/2)/2  + $speed_3*-time ),\n         noise(({ps}.particleId-{ps}.count)/2    + $speed_3*-time ) >>   *0.05  *$inNoise;".format(ps=particle_system,sp=start_locator,ep=end_locator)))

    # do the extrude for the nurbcurve
    # make the circle curve
    makeNurbCircle = pm.createNode("makeNurbCircle")
    pm.setAttr(makeNurbCircle.radius, 1.35)
    pm.setAttr(makeNurbCircle.normal, [1, 0, 0])

    circle_curve = pm.createNode('nurbsCurve', n='circle_curve')

    circle_curve_transform = pm.listRelatives(circle_curve, fullPath=True, allParents=True)[0]
    pm.connectAttr(start_locator.translate,circle_curve_transform.translate)
    pm.setAttr(circle_curve_transform.scale, [0.019, 0.019, 0.019])
    pm.getAttr(circle_curve_transform.scale)

    pm.rename(circle_curve_transform, "%s_transform" % circle_curve)

    pm.connectAttr(makeNurbCircle.outputCurve, circle_curve.create)

    # create extrude node
    extrude_node = pm.createNode('extrude', n='extrude_node')
    pm.setAttr(extrude_node.useProfileNormal,0)
    pm.setAttr(extrude_node.fixedPath,0)
    pm.setAttr(extrude_node.useComponentPivot,0)
    pm.setAttr(extrude_node.scale,0.25)

    pm.connectAttr(guide_curve.worldSpace[0], extrude_node.path)
    pm.connectAttr(circle_curve.worldSpace[0], extrude_node.profile)
    #create tessellate node
    nurbsTessellate = pm.createNode('nurbsTessellate', n='nurbsTessellate')

    pm.setAttr(nurbsTessellate.polygonType,1)
    pm.setAttr("%s.format"%nurbsTessellate,2)
    pm.setAttr(nurbsTessellate.uNumber,1)
    pm.setAttr(nurbsTessellate.useChordHeightRatio, 0)
    pm.setAttr(nurbsTessellate.vNumber, 1)

    pm.connectAttr(extrude_node.outputSurface, nurbsTessellate.inputSurface)
    #create a mesh for curve extrude
    extrude_mesh = pm.createNode('mesh', name='extrude_mesh')
    extrude_mesh_transform=pm.listRelatives(extrude_mesh,parent=True)[0]
    extrude_mesh_transform = pm.rename(extrude_mesh_transform, "%s_transform"%extrude_mesh)
    pm.connectAttr(nurbsTessellate.outputPolygon, extrude_mesh.inMesh)


    brush=pm.createNode("brush",name="lightning_spark")
    pm.setAttr(brush.brushType,5)
    pm.setAttr(brush.globalScale,7.458)
    pm.setAttr(brush.depth,1)
    pm.setAttr(brush.brushWidth,0)
    pm.setAttr(brush.softness,0)
    pm.setAttr(brush.mapDisplacement,1)
    pm.setAttr(brush.luminanceIsDisplacement,0)

    pm.setAttr(brush.textureType,3)
    pm.setAttr(brush.texAlpha1,0.386)
    pm.setAttr(brush.texAlpha2,1)
    pm.setAttr(brush.repeatU,2.542)
    pm.setAttr(brush.blurMult,5)
    pm.setAttr(brush.smear,251)
    pm.setAttr(brush.fractalAmplitude,2.094)
    pm.setAttr(brush.fractalRatio,0.592)
    pm.setAttr(brush.tubes,1)
    pm.setAttr(brush.tubeCompletion,0)

    pm.setAttr(brush.tubesPerStep,0.061)
    pm.setAttr(brush.segments,70)
    pm.setAttr(brush.lengthMin,0.061)
    pm.setAttr(brush.lengthMax,1.104)
    pm.setAttr(brush.blurMult,5)
    pm.setAttr(brush.tubeWidth1,0.04)
    pm.setAttr(brush.tubeWidth2,0)
    pm.setAttr(brush.widthRand,0.282)
    pm.setAttr(brush.widthBias,-0.215)
    #the width scale
    pm.setAttr (brush.widthScale[1].widthScale_FloatValue,0.96)
    pm.setAttr (brush.widthScale[1].widthScale_Position,0.982609)
    pm.setAttr (brush.widthScale[1].widthScale_Interp,1)
    pm.setAttr (brush.widthScale[1].widthScale_Position,1)
    pm.setAttr (brush.widthScale[1].widthScale_FloatValue,0.72)

    pm.setAttr (brush.elevationMin,0)
    pm.setAttr (brush.elevationMax,0.160)
    pm.setAttr (brush.azimuthMin,-0.068)
    pm.setAttr (brush.azimuthMax,0.006)
    #growth
    pm.setAttr (brush.branches,1)
    #branches
    pm.setAttr (brush.numBranches,3)
    pm.setAttr (brush.branchDropout,0.359)
    pm.setAttr (brush.splitAngle,36.7)
    pm.setAttr (brush.splitBias,0.368)
    pm.setAttr (brush.minSize,0.003)
    #behavior
    #displacement
    pm.setAttr (brush.displacementDelay,0.117)
    pm.setAttr (brush.noise,10)
    pm.setAttr (brush.noiseFrequency,0.074)
    pm.setAttr (brush.wiggleFrequency,5)
    #force
    pm.setAttr (brush.gravity,0.107)
    #gaps
    pm.setAttr (brush.gapSpacing,0.02)
    pm.setAttr (brush.gapRand,1)
    #flow animation
    pm.connectAttr("time1.outTime",brush.time)





    ##################
    #create stroke
    stroke=pm.createNode("stroke",name="lightning_stroke")
    stroke_transform = pm.listRelatives(stroke, fullPath=True, allParents=True)[0]
    stroke_transform=pm.rename(stroke_transform, "%s_transform" % stroke)
    pm.connectAttr(guide_curve.worldSpace,stroke.pathCurve[0].curve)
    pm.connectAttr(brush.outBrush,stroke.brush)
    #basic
    pm.expression(string="float $a = rand(1);\nif($a>0.5)\n{\n\t%s.seed=frame;\n}"%stroke,object=stroke,alwaysEvaluate=True,unitConversion=all)
    pm.setAttr (stroke.sampleDensity,0.109)
    #normal_direction
    pm.setAttr (stroke.minimalTwist,1)
    #pressure mapping
    pm.setAttr (stroke.minimalTwist,1)
    pm.setAttr (stroke.pressureScale[0].pressureScale_Position,0)
    pm.setAttr (stroke.pressureScale[0].pressureScale_FloatValue, 0.12)

    pm.setAttr (stroke.pressureScale[1].pressureScale_FloatValue,0)
    pm.setAttr (stroke.pressureScale[1].pressureScale_Position,1)

    pm.setAttr (stroke.pressureMap1,6)

    #input curves
    #********************
    #path curve
    pm.setAttr (stroke.pathCurve[0].samples,588)
    pm.setAttr (stroke.mainVertBufSize,906)
    #mesh output
    pm.setAttr (stroke.meshQuadOutput, 1)
    #object display
    pm.setAttr (stroke.visibility, 0)

    #############
    #create a mesh for the strock
    stroke_mesh=pm.createNode("mesh",name="stroke_mesh")

    pm.connectAttr(stroke.worldMainMesh,stroke_mesh.inMesh)
    stroke_mesh_transform=pm.listRelatives(stroke_mesh,parent=True)[0]
    stroke_mesh_transform = pm.rename(stroke_mesh_transform, "%s_transform"%stroke_mesh)

    #hide the curve and particle
    pm.hide(guide_curve_transform)
    pm.hide(circle_curve_transform)
    pm.hide(stroke_transform)

    ##
    #group all elements in a group
    trans_list=[start_locator,end_locator,guide_curve_transform,circle_curve_transform,stroke_mesh_transform,stroke_transform,extrude_mesh_transform]
    group_lightning=pm.group(trans_list)
    group_lightning=pm.rename(group_lightning,"lightning_group")
    return group_lightning