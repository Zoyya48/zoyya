from datetime import datetime

class ParkingRequest:
    # State constants
    STATE_REQUESTED = "REQUESTED"
    STATE_ALLOCATED = "ALLOCATED"
    STATE_OCCUPIED = "OCCUPIED"
    STATE_RELEASED = "RELEASED"
    STATE_CANCELLED = "CANCELLED"
    
    # Valid state transitions
    VALID_TRANSITIONS = {
        STATE_REQUESTED: [STATE_ALLOCATED, STATE_CANCELLED],
        STATE_ALLOCATED: [STATE_OCCUPIED, STATE_CANCELLED],
        STATE_OCCUPIED: [STATE_RELEASED],
        STATE_RELEASED: [],
        STATE_CANCELLED: []
    }
    
    def __init__(self, request_id, vehicle_id, requested_zone, vehicle_type):
        self.request_id = request_id
        self.vehicle_id = vehicle_id
        self.requested_zone = requested_zone
        self.vehicle_type = vehicle_type
        self.state = self.STATE_REQUESTED
        self.request_time = datetime.now()
        self.allocated_slot = None
        self.allocated_zone = None
        self.check_in_time = None
        self.check_out_time = None
        self.is_cross_zone = False
    
    def transition_to(self, new_state):
        """Transition to a new state if valid"""
        if new_state not in self.VALID_TRANSITIONS.get(self.state, []):
            raise ValueError(
                f"Invalid transition from {self.state} to {new_state}"
            )
        self.state = new_state
        
        # Set timestamps based on state
        if new_state == self.STATE_OCCUPIED:
            self.check_in_time = datetime.now()
        elif new_state == self.STATE_RELEASED:
            self.check_out_time = datetime.now()
    
    def allocate_slot(self, slot, zone_name):
        """Allocate a parking slot to this request"""
        self.allocated_slot = slot
        self.allocated_zone = zone_name
        self.is_cross_zone = (zone_name != self.requested_zone)
        self.transition_to(self.STATE_ALLOCATED)
    
    def mark_occupied(self):
        """Mark the parking as occupied"""
        self.transition_to(self.STATE_OCCUPIED)
    
    def release(self):
        """Release the parking"""
        self.transition_to(self.STATE_RELEASED)
    
    def cancel(self):
        """Cancel the request"""
        self.transition_to(self.STATE_CANCELLED)
    
    def get_duration_minutes(self):
        """Calculate parking duration in minutes"""
        if self.check_in_time and self.check_out_time:
            delta = self.check_out_time - self.check_in_time
            return delta.total_seconds() / 60
        return 0
