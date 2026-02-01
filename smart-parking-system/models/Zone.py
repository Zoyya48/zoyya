class Zone:
    def __init__(self, zone_id, name, hourly_rate):
        self.zone_id = zone_id
        self.name = name
        self.hourly_rate = hourly_rate
        self.parking_areas = []
        self.adjacent_zones = []
    
    def add_parking_area(self, parking_area):
        self.parking_areas.append(parking_area)
    
    def add_adjacent_zone(self, zone):
        if zone not in self.adjacent_zones:
            self.adjacent_zones.append(zone)
    
    def get_available_slots_count(self):
        count = 0
        for area in self.parking_areas:
            count += area.get_available_slots_count()
        return count
    
    def get_all_slots(self):
        slots = []
        for area in self.parking_areas:
            slots.extend(area.slots)
        return slots
    
    def find_available_slot(self):
        for area in self.parking_areas:
            slot = area.find_available_slot()
            if slot:
                return slot
        return None
