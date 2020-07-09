from vcCommand import *
from vcHelpers.Selection import getGivenComponentsGeosets, filterGeosets, getGivenComponentsFeatures, filterFeatures
import vcVector

def OnStart():
    #set of options in task pane for importing point cloud
    file.Value = ""
    color_mode.Value = "RGBA"
    size.Value = 1.0
    scale.Value = vcVector.new(1.0, 1.0, 1.0)
    offset.Value = vcVector.new()
    executeInActionPanel()


def loadFile(prop):
    #imports file and configures point sets
    if cmd.File:
        pc_importer = app.findCommand("loadGeometryAsComponent")
        pc_importer.execute(cmd.File, cmd.Offset)
        configurePointSets()
        
    
def configurePointSets():
    #defines points according to import options
    component = app.Components[-1]
    
    #point sets
    point_sets = getGivenComponentsGeosets(component)
    point_sets = filterGeosets(point_sets, VC_POINTSET)
    for set in point_sets:
        set.ColorConfiguration = color_config[cmd.ColorMode]
        set.PointSize = cmd.PointSize
        #set.Scale = cmd.Scale  #does not seem to have any effect
    
    #scale using transform
    feats = getGivenComponentsFeatures(component)
    feats = filterFeatures(feats, VC_GEOMETRY)
    
    transform = component.RootFeature.createFeature(VC_TRANSFORM, "Transform")
    v = cmd.Scale
    transform.Expression = "Sx({}).Sy({}).Sz({})".format(v.X, v.Y, v.Z)
    for f in feats:
        transform.attach(f)
    component.rebuild()
    app.render()


app = getApplication()
cmd = getCommand()
cmd.addState(None)

file = cmd.createProperty(VC_URI, "File")

color_mode = cmd.createProperty(VC_STRING, "ColorMode", VC_PROPERTY_STEP)
color_mode.StepValues = ["RGBA", "BGRA"]
color_mode.Value = "RGBA"
color_config = {
    "RGBA": VC_COLOR_CONFIGURATION_RGBA,
    "BGRA": VC_COLOR_CONFIGURATION_BGRA
}

size = cmd.createProperty(VC_REAL, "PointSize", VC_PROPERTY_LIMIT)
size.MinValue = 0.0
size.MaxValue = 100.0
size.Value = 1.0

##vcPointSet.Scale does not seem to work anymore; will use Transform Scale instead
#scale = cmd.createProperty(VC_REAL, "Scale", VC_PROPERTY_LIMIT)
#scale.MinValue = 0.0
#scale.MaxValue = 100.0
#scale.Value = 1.0

scale = cmd.createProperty(VC_VECTOR, "Scale")
offset = cmd.createProperty(VC_VECTOR, "Offset")

import_file = createProperty(VC_BUTTON, 'Import')
import_file.OnChanged = loadFile