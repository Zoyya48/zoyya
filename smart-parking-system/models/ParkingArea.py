class ParkingArea:
    def __init__(self, area_id, zone_id):
        self.area_id = area_id
        self.zone_id = zone_id
        self.slots = []
    
    def add_slot(self, slot):
        self.slots.append(slot)
    
    def get_available_slots_count(self):
        return sum(1 for slot in self.slots if slot.is_available)
    
    def find_available_slot(self):
        for slot in self.slots:
            if slot.is_available:
                return slot
        return None
