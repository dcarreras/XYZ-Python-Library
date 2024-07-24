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

# Global counter for unique IDs
global_counter = 0

# Function to get a unique identifier
def get_unique_id(room_name, point_type):
    global global_counter
    unique_id = "Room-{0}-{1}-{2}".format(room_name, point_type, global_counter)
    global_counter += 1
    return unique_id

# Function to get point information including the True North angle
def get_point_info(point, point_type, level_name, level_id, room_name, room_id, north_angle):
    if point is None:  # If no point is provided, return None to indicate an issue
        return None
    unique_id = get_unique_id(room_name, point_type)
    north_angle_degrees = north_angle * 180.0 / math.pi  # Convert angle from radians to degrees
    return (unique_id, point.X, point.Y, point.Z, north_angle_degrees, point_type, level_name, level_id, room_name, room_id)

# Adjusted function to extract boundary points of a room and ensure the first point repeats at the end
def get_boundary_points(room):
    boundary_points = []
    opt = SpatialElementBoundaryOptions()
    for boundary in room.GetBoundarySegments(opt):
        loop_points = []  # Temporary list to store points for the current loop
        for segment in boundary:
            start_pt = segment.GetCurve().GetEndPoint(0)
            # Append the start point of each segment to the loop points
            loop_points.append(start_pt.ToPoint())
            # The end point will be considered as the start point in the next segment
        # Ensure the loop is closed by appending the first point to the end of the loop points list
        if loop_points:
            loop_points.append(loop_points[0])
        boundary_points.extend(loop_points)
    return boundary_points
    
# Function to calculate the centroid of boundary points
def calculate_room_center(boundary_points):
    sum_x = sum_y = sum_z = 0
    num_points = len(boundary_points)
    if num_points == 0:  # Check if there are no boundary points
        return None  # Return None to indicate no centroid could be calculated
    for point in boundary_points:
        sum_x += point.X
        sum_y += point.Y
        sum_z += point.Z
    return Point.ByCoordinates(sum_x / num_points, sum_y / num_points, sum_z / num_points)

# Function to get the Project Base Point location
def get_project_base_point_location(doc):
    base_point = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ProjectBasePoint).ToElements()
    if base_point:
        base_point = base_point[0]
        position = base_point.get_BoundingBox(None).Min
        return position
    else:
        return XYZ.Zero

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
    room_number = revit_room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()  # Extracting the room number
    room_id = revit_room.Id.ToString()

    # The rest of your processing code will go here...


    # Get the level of the room
    level_id = revit_room.LevelId
    level = doc.GetElement(level_id)
    level_name = level.Name if level else "Unknown Level"

    # Get boundary points of the room
    boundary_points = get_boundary_points(revit_room)

    # Calculate the room centroid and adjust based on Project Base Point
    center_point = calculate_room_center(boundary_points)
    if center_point is None:
        continue  # Skip this room if no centroid could be calculated
    adjusted_center = XYZ(center_point.X + project_base_point.X, center_point.Y + project_base_point.Y, center_point.Z + project_base_point.Z)
    point_info = get_point_info(adjusted_center, 'CENTER', level_name, level_id.ToString(), room_name, room_id, north_rotation_angle)
    if point_info is not None:  # Ensure that the point information was successfully created
        output_data.append(point_info)

    # Process and adjust corner points based on Project Base Point
    for point in boundary_points:
        adjusted_point = XYZ(point.X + project_base_point.X, point.Y + project_base_point.Y, point.Z + project_base_point.Z)
        point_info = get_point_info(adjusted_point, 'CORNER', level_name, level_id.ToString(), room_name, room_id, north_rotation_angle)
        if point_info is not None:  # Ensure that the point information was successfully created
            output_data.append(point_info)

# Assign the data to the node output
OUT = output_data
