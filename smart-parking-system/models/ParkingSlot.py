class ParkingSlot:
    def __init__(self, slot_id, zone_id, area_id):
        self.slot_id = slot_id
        self.zone_id = zone_id
        self.area_id = area_id
        self.is_available = True
        self.current_vehicle_id = None
    
    def occupy(self, vehicle_id):
        if not self.is_available:
            return False
        self.is_available = False
        self.current_vehicle_id = vehicle_id
        return True
    
    def release(self):
        self.is_available = True
        self.current_vehicle_id = None
    
    def get_status(self):
        return "AVAILABLE" if self.is_available else "OCCUPIED"
