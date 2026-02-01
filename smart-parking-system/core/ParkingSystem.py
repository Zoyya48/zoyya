from models.Zone import Zone
from models.ParkingArea import ParkingArea
from models.ParkingSlot import ParkingSlot
from models.Vehicle import Vehicle
from models.ParkingRequest import ParkingRequest
from core.AllocationEngine import AllocationEngine
from core.RollbackManager import RollbackManager

class ParkingSystem:
    def __init__(self):
        self.zones = {}
        self.vehicles = {}
        self.requests = {}
        self.allocation_engine = None
        self.rollback_manager = RollbackManager()
        self.request_counter = 0
        
        # Initialize the city parking zones
        self._initialize_zones()
        
        # Create allocation engine
        self.allocation_engine = AllocationEngine(self.zones)
    
    def _initialize_zones(self):
        """Initialize zones with parking areas and slots"""
        # Create zones
        defence_zone = Zone("Z1", "Defence", 100)
        gulberg_zone = Zone("Z2", "Gulberg", 80)
        mall_road_zone = Zone("Z3", "Mall Road", 60)
        
        # Set up zone adjacency
        defence_zone.add_adjacent_zone(gulberg_zone)
        defence_zone.add_adjacent_zone(mall_road_zone)
        gulberg_zone.add_adjacent_zone(defence_zone)
        gulberg_zone.add_adjacent_zone(mall_road_zone)
        mall_road_zone.add_adjacent_zone(defence_zone)
        mall_road_zone.add_adjacent_zone(gulberg_zone)
        
        # Create parking area for each zone
        defence_area = ParkingArea("A1", "Z1")
        gulberg_area = ParkingArea("A2", "Z2")
        mall_area = ParkingArea("A3", "Z3")
        
        # Add 6 slots to each area
        for i in range(6):
            defence_area.add_slot(ParkingSlot(f"D{i+1}", "Z1", "A1"))
            gulberg_area.add_slot(ParkingSlot(f"G{i+1}", "Z2", "A2"))
            mall_area.add_slot(ParkingSlot(f"M{i+1}", "Z3", "A3"))
        
        # Add areas to zones
        defence_zone.add_parking_area(defence_area)
        gulberg_zone.add_parking_area(gulberg_area)
        mall_road_zone.add_parking_area(mall_area)
        
        # Store zones
        self.zones["Defence"] = defence_zone
        self.zones["Gulberg"] = gulberg_zone
        self.zones["Mall Road"] = mall_road_zone
    
    def create_parking_request(self, vehicle_id, vehicle_type, requested_zone):
        """Create a new parking request"""
        # Create or get vehicle
        if vehicle_id not in self.vehicles:
            vehicle = Vehicle(vehicle_id, vehicle_type)
            self.vehicles[vehicle_id] = vehicle
        
        # Generate request ID
        self.request_counter += 1
        request_id = f"REQ{self.request_counter:04d}"
        
        # Create request
        request = ParkingRequest(request_id, vehicle_id, requested_zone, vehicle_type)
        self.requests[request_id] = request
        
        # Try to allocate
        success = self.allocation_engine.allocate_slot(request)
        
        if success:
            # Record operation for rollback
            self.rollback_manager.record_operation(
                'ALLOCATION', request, request.allocated_slot
            )
        
        return request, success
    
    def cancel_request(self, request_id):
        """Cancel a parking request and rollback"""
        if request_id not in self.requests:
            return False
        
        request = self.requests[request_id]
        
        # Check if cancellation is valid
        if request.state not in [ParkingRequest.STATE_REQUESTED, 
                                  ParkingRequest.STATE_ALLOCATED,
                                  ParkingRequest.STATE_OCCUPIED]:
            return False
        
        # Release slot if allocated
        if request.allocated_slot:
            request.allocated_slot.release()
        
        # Cancel request
        request.cancel()
        
        return True
    
    def get_zone_slots(self, zone_name):
        """Get all slots in a zone with their status"""
        if zone_name not in self.zones:
            return []
        
        zone = self.zones[zone_name]
        slots = zone.get_all_slots()
        
        return [{
            'id': slot.slot_id,
            'available': slot.is_available,
            'vehicle_id': slot.current_vehicle_id
        } for slot in slots]
    
    def get_analytics(self):
        """Get parking usage analytics"""
        completed_requests = [
            r for r in self.requests.values() 
            if r.state == ParkingRequest.STATE_RELEASED
        ]
        
        cancelled_requests = [
            r for r in self.requests.values() 
            if r.state == ParkingRequest.STATE_CANCELLED
        ]
        
        # Average parking duration
        total_duration = sum(r.get_duration_minutes() for r in completed_requests)
        avg_duration = total_duration / len(completed_requests) if completed_requests else 0
        
        # Zone utilization
        zone_utilization = {
            name: self.allocation_engine.get_zone_utilization(name)
            for name in self.zones.keys()
        }
        
        # Peak usage zone
        peak_zone = max(zone_utilization.items(), key=lambda x: x[1])[0] if zone_utilization else None
        
        return {
            'average_duration_minutes': round(avg_duration, 2),
            'zone_utilization': zone_utilization,
            'completed_requests': len(completed_requests),
            'cancelled_requests': len(cancelled_requests),
            'peak_usage_zone': peak_zone
        }
    
    def rollback_operations(self, k=1):
        """Rollback last k operations"""
        return self.rollback_manager.rollback_last(k)
