# Function to get a unique identifier
def get_unique_id(room_name, point_type):
    global global_counter
    unique_id = "Room-{0}-{1}-{2}".format(room_name, point_type, global_counter)
    global_counter += 1
    return unique_id

# Function to get point information including the True North angle
def get_point_info(point, point_type, level_name, level_id, room_identifier, room_id, north_angle):
    if point is None:
        return None
    unique_id = get_unique_id(room_identifier, point_type)
    north_angle_degrees = north_angle * 180.0 / math.pi  # Convert angle from radians to degrees
    return (unique_id, point.X, point.Y, point.Z, north_angle_degrees, point_type, level_name, level_id, room_identifier, room_id)

# Function to extract boundary points of a room and ensure the first point repeats at the end
def get_boundary_points(room):
    boundary_points = []
    opt = SpatialElementBoundaryOptions()
    for boundary in room.GetBoundarySegments(opt):
        loop_points = []
        for segment in boundary:
            start_pt = segment.GetCurve().GetEndPoint(0)
            loop_points.append(start_pt.ToPoint())
        if loop_points:
            loop_points.append(loop_points[0])
        boundary_points.extend(loop_points)
    return boundary_points

# Function to calculate the centroid of boundary points
def calculate_room_center(boundary_points):
    if not boundary_points:
        return None
    sum_x = sum_y = sum_z = 0
    num_points = len(boundary_points)
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