class AllocationEngine:
    def __init__(self, zones):
        self.zones = zones
    
    def allocate_slot(self, parking_request):
        """
        Allocate parking slot using:
        - Same-zone preference
        - First-available slot strategy
        - Cross-zone allocation if requested zone is full
        """
        requested_zone_name = parking_request.requested_zone
        
        # Try to find slot in requested zone first
        if requested_zone_name in self.zones:
            requested_zone = self.zones[requested_zone_name]
            slot = requested_zone.find_available_slot()
            
            if slot:
                # Same-zone allocation (preferred)
                parking_request.allocate_slot(slot, requested_zone_name)
                slot.occupy(parking_request.vehicle_id)
                parking_request.mark_occupied()
                return True
        
        # If requested zone is full, try adjacent zones (cross-zone allocation)
        if requested_zone_name in self.zones:
            requested_zone = self.zones[requested_zone_name]
            
            for adjacent_zone in requested_zone.adjacent_zones:
                slot = adjacent_zone.find_available_slot()
                if slot:
                    # Cross-zone allocation (incurs penalty)
                    parking_request.allocate_slot(slot, adjacent_zone.name)
                    slot.occupy(parking_request.vehicle_id)
                    parking_request.mark_occupied()
                    return True
        
        # No slot available anywhere
        return False
    
    def get_zone_utilization(self, zone_name):
        """Calculate zone utilization rate"""
        if zone_name not in self.zones:
            return 0.0
        
        zone = self.zones[zone_name]
        total_slots = len(zone.get_all_slots())
        if total_slots == 0:
            return 0.0
        
        occupied_slots = total_slots - zone.get_available_slots_count()
        return (occupied_slots / total_slots) * 100
