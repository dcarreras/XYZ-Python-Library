import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Point, Vector, CoordinateSystem
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
import math

# Importar funciones desde f_main.py
from functions.f_main import get_unique_id, get_point_info, get_boundary_points, calculate_room_center, get_project_base_point_location

# Global counter for unique IDs
global_counter = 0

# Get the Revit Document
doc = DocumentManager.Instance.CurrentDBDocument

# Get the location of Project Base Point
project_base_point = get_project_base_point_location(doc)

# Get the True North rotation angle from input
north_rotation_angle = IN[1]  # Angle in radians

# Initialize output data list
output_data = []

# Iterate over each room
for room in IN[0]:
    revit_room = UnwrapElement(room)
    room_name = revit_room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
    room_number = revit_room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
    room_id = revit_room.Id.ToString()

    # Concatenate room number and room name
    room_identifier = "{0} - {1}".format(room_number, room_name)

    # Get the level of the room
    level_id = revit_room.LevelId
    level = doc.GetElement(level_id)
    level_name = level.Name if level else "Unknown Level"

    # Get boundary points of the room
    boundary_points = get_boundary_points(revit_room)

    # Calculate the room centroid and adjust based on Project Base Point
    center_point = calculate_room_center(boundary_points)
    if center_point is None:
        continue
    adjusted_center = XYZ(center_point.X + project_base_point.X, center_point.Y + project_base_point.Y, center_point.Z + project_base_point.Z)
    point_info = get_point_info(adjusted_center, 'CENTER', level_name, level_id.ToString(), room_identifier, room_id, north_rotation_angle)
    if point_info is not None:
        output_data.append(point_info)

    # Process and adjust corner points based on Project Base Point
    for point in boundary_points:
        adjusted_point = XYZ(point.X + project_base_point.X, point.Y + project_base_point.Y, point.Z + project_base_point.Z)
        point_info = get_point_info(adjusted_point, 'CORNER', level_name, level_id.ToString(), room_identifier, room_id, north_rotation_angle)
        if point_info is not None:
            output_data.append(point_info)

# Assign the data to the node output
OUT = output_data
