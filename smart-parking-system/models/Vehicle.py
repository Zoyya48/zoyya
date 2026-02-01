class Vehicle:
    def __init__(self, vehicle_id, vehicle_type):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.preferred_zone = None
    
    def set_preferred_zone(self, zone_name):
        self.preferred_zone = zone_name
