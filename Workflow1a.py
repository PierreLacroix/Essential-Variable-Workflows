# -*- coding: cp1252 -*-
# ------------------------------------------------------------------------------
# GEOEssential workflow - Work Package 5
# Monitoring of forest cover at national level
# Case study of Dem. Rep. of Congo
# This script calculates surface of forest currently
#    recognized that it covered by mining concessions
# Inputs: mining concessions (CAMI 2016) and forest Cover (Hansen et al. 2013)
# ------------------------------------------------------------------------------

# Importing des modules systeme
import sys, string, os, arcpy, urllib # is for downloading images from HTTP

arcpy.overwriteoutput = 1

# Retrieve Spatial Analyst license
if arcpy.CheckExtension("Spatial") == "Available":
    print(".....Checking out Spatial")
    arcpy.CheckOutExtension("Spatial")
else:
    print(".....Unable to get spatial analyst extension")
    sys.exit(0)

# Input and scratch workspaces
inputWorkspace = arcpy.env.workspace = "Z:\\Downloads\\Script_Workflows_ArcGIS"
outWorkspace = arcpy.env.scratchworkspace = "Z:\\Downloads\\Script_Workflows_ArcGIS\\Outputs"

# Download input forest dataset (TIFF)
print "5 tiles of forests cover will be downloaded..."
print "..... downloading tile 1"
tile1 = urllib.urlretrieve ("http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2014/Hansen_GFC2014_treecover2000_00N_020E.tif", "tile1.tif")
print "..... downloading tile 2"
tile2 = urllib.urlretrieve ("http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2014/Hansen_GFC2014_treecover2000_10N_020E.tif", "tile2.tif")
print "..... downloading tile 3"
tile3 = urllib.urlretrieve ("http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2014/Hansen_GFC2014_treecover2000_10S_020E.tif", "tile3.tif")
print "..... downloading tile 4"
tile4 = urllib.urlretrieve ("http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2014/Hansen_GFC2014_treecover2000_10N_030E.tif", "tile4.tif")
print "..... downloading tile 5"
tile5 = urllib.urlretrieve ("http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2014/Hansen_GFC2014_treecover2000_00N_010E.tif", "tile5.tif")
##tile1 = "Z:\Downloads\\Script_Workflows_ArcGIS\\tile1.tif"
##tile2 = "Z:\Downloads\\Script_Workflows_ArcGIS\\tile2.tif"
##tile3 = "Z:\Downloads\\Script_Workflows_ArcGIS\\tile3.tif"
##tile4 = "Z:\Downloads\\Script_Workflows_ArcGIS\\tile4.tif"
##tile5 = "Z:\Downloads\\Script_Workflows_ArcGIS\\tile5.tif"

# Mosaick input forest dataset
print "Mosaicking forest cover in one tile..."
inputForestCover = arcpy.MosaicToNewRaster_management("tile1.tif;tile2.tif;tile3.tif;tile4.tif;tile5.tif", outWorkspace, "inputForestCover.tif", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "8_BIT_UNSIGNED", "0.00025", "1", "LAST", "FIRST")
##inputForestCover = "Z:\\Downloads\\Script_Workflows_ArcGIS\\Outputs\\inputForestCover.tif"
# Input mining concessions
inputMiningConcessions = inputWorkspace + "\\LicenseExport.shp"
# Dissolve all mines into one polygon
print "Dissolving all mining concessions in DR Congo into one polygon..."
inputMine = arcpy.Dissolve_management(inputMiningConcessions, "inputMine.shp")
##inputMine = "Z:\\Downloads\\Script_Workflows_ArcGIS\\inputMine.shp"
# Clip forest (raster mosaick) by the dissolved mining concession => one raster with two attributes:
#   1) value between 0 and 100 (representing the percentage of forest within the pixel)
#   2) number of pixels for each of these values
print "Clipping forest cover by mines..."
clippedForest = arcpy.gp.ExtractByMask_sa(inputForestCover, inputMine,"Z:\\Downloads\\Script_Workflows_ArcGIS\\Outputs\\clippedForest.tif")
##clippedForest = "Z:\\Downloads\\Script_Workflows_ArcGIS\\Outputs\\clippedForestCopy.tif"
# Create new attribute (type = float) and calculate surface of forest in each pixel
print "Adding new attribute to raster table for calculation of the surface..."
surfaceField = arcpy.AddField_management(clippedForest, "surface", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "Calculating new field as forest coverage percentage x pixel count x pixel size, in square kilometers..."
arcpy.CalculateField_management(clippedForest, "surface", "[Value]* [Count]* 625 / 1000000", "VB", "")
# Sum all values => overall surface of forest in the country
arcpy.Statistics_analysis(clippedForest, "Z:\\Downloads\\Script_Workflows_ArcGIS\\Outputs\\sumSurface.dbf", "surface SUM", "")
