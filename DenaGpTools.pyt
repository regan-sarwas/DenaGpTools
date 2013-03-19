import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "DENA 2013 Tools"
        self.alias = "GP Tools for Denali"

        # List of tool classes associated with this toolbox
        self.tools = [ShapeImport]


class ShapeImport(object):
    # For a class definition, see http://resources.arcgis.com/en/help/main/10.1/index.html#/Defining_a_tool_in_a_Python_toolbox/001500000024000000/
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ShapeImport"
        self.description = "Adds a shapefile to a GDB with a column for the shape name"
        self.canRunInBackground = False

    def getParameterInfo(self):
        #See http://resources.arcgis.com/en/help/main/10.1/index.html#/Defining_parameters_in_a_Python_toolbox/001500000028000000/

        param0 = arcpy.Parameter(
            displayName="Shapefile",
            name="shapefile",
            datatype="DEShapefile",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="GDB Feature Class",
            name="geodatabase",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName="Name Field",
            name="name_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
            
        #param2 must be a text field from param1
        param2.parameterDependencies = [param1.name]
        param2.filter.list = ["Text"]
        
        param3 = arcpy.Parameter(
            displayName="Field Mapping",
            name="field_mapping",
            datatype="GPFieldMapping",
            parameterType="Optional",
            direction="Input")
        
        return [param0, param1, param2, param3]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        #See http://resources.arcgis.com/en/help/main/10.1/index.html#/Customizing_tool_behavior_in_a_Python_toolbox/00150000002m000000/
        
        #set default field name - this does not work.  Can't set the parameter to a field object
        #if parameters[1].value:
        #    if not parameters[2].altered:
        #        for field in arcpy.Describe(parameters[1].value).fields:
        #            if field.type == "String" and field.name.lower() == "filename":
        #                parameters[2].value = field.name
        #                break
        
        #Setup field mapping
        if (not parameters[0].hasBeenValidated or not parameters[1].hasBeenValidated):
            targetFeatures = parameters[1].value
            joinFeatures = parameters[0].value
            fieldMappings = arcpy.FieldMappings()
            if targetFeatures:
                fieldMappings.addTable(targetFeatures)
                if joinFeatures:
                    fieldMappings.addTable(joinFeatures)
                    #idx = fieldMappings.findFieldMapIndex("PRIORITY")
                    #fieldMap = fieldMappings.getFieldMap(idx)
                    #fieldMap.mergeRule = 'Sum'
                    #fieldMappings.replaceFieldMap(idx, fieldMap) # if this line is commented out, the merge rule reverts to 'First'
            parameters[3].value = fieldMappings.exportToString()
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        # check that geometries match
        if parameters[0].value and parameters[1].value:
            if arcpy.Describe(parameters[0].value).shapeType != arcpy.Describe(parameters[1].value).shapeType:
                parameters[1].setErrorMessage("Geometry does not match Shapefile.")
        
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # copy shapefile.
        # add filename field to shapefile if it doesn't exist
        # calculate value of filename field in new temp shapefile
        # append shapefile to output FC, using field mapping.
        #delete temp shapefile
        return
