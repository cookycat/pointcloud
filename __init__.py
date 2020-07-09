from vcApplication import *

def OnAppInitialized():
    cmduri = getApplicationPath() + "importer_pointcloud.py"
    cmd = loadCommand("importPointCloud",cmduri)

    addMenuItem("VcTabHome/VcRibbonImport", "Point Cloud", -1, "importPointCloud")