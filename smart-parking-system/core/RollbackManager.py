class RollbackManager:
    def __init__(self):
        self.operation_history = []
    
    def record_operation(self, operation_type, request, slot):
        """Record an operation for potential rollback"""
        operation = {
            'type': operation_type,
            'request': request,
            'slot': slot,
            'previous_state': request.state
        }
        self.operation_history.append(operation)
    
    def rollback_last(self, k=1):
        """Rollback the last k operations"""
        rollback_count = min(k, len(self.operation_history))
        
        for _ in range(rollback_count):
            if not self.operation_history:
                break
            
            operation = self.operation_history.pop()
            request = operation['request']
            slot = operation['slot']
            
            # Restore slot availability
            if slot:
                slot.release()
            
            # Restore request state
            request.state = operation['previous_state']
            request.allocated_slot = None
            request.allocated_zone = None
        
        return rollback_count
    
    def clear_history(self):
        """Clear operation history"""
        self.operation_history.clear()
