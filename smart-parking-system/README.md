# Smart Parking Allocation & Zone Management System

A Flask-based smart parking management system for Lahore city with zone-based allocation, state management, and rollback capabilities.

## Project Structure

```
smart-parking-system/
│
├── app.py                      # Flask application (main entry point)
├── requirements.txt            # Python dependencies
│
├── templates/
│   └── index.html             # Frontend UI (fully designed with animations)
│
├── models/                    # Data models
│   ├── __init__.py
│   ├── Zone.py               # Zone representation
│   ├── ParkingArea.py        # Parking area within zones
│   ├── ParkingSlot.py        # Individual parking slots
│   ├── Vehicle.py            # Vehicle information
│   └── ParkingRequest.py     # Request lifecycle & state machine
│
└── core/                      # Core logic
    ├── __init__.py
    ├── AllocationEngine.py   # Slot allocation logic
    ├── RollbackManager.py    # Rollback operations
    └── ParkingSystem.py      # Main system orchestrator
```

## Features

### Backend (Python/Flask)
- **Zone Management**: 3 zones (Defence, Gulberg, Mall Road)
- **Slot Allocation**: Same-zone preference with cross-zone fallback
- **State Management**: Strict lifecycle (REQUESTED → ALLOCATED → OCCUPIED → RELEASED)
- **Rollback System**: Undo last k allocation operations
- **Analytics**: Duration, utilization, peak zones

### Frontend (HTML/CSS/JS)
- Animated backgrounds for each screen
- 4-step booking process
- Real-time slot availability
- Visual car parking animation
- Responsive design

## API Endpoints

- `GET /` - Main UI
- `GET /api/zones` - Get all zones with availability
- `GET /api/slots/<zone_name>` - Get slots for specific zone
- `POST /api/book` - Book a parking slot
- `POST /api/cancel/<request_id>` - Cancel a request
- `GET /api/analytics` - Get usage analytics
- `POST /api/rollback` - Rollback operations

## Data Flow

1. User selects vehicle type and enters ID
2. System shows available zones
3. User selects zone → Backend loads real-time slot data
4. User selects slot → Backend creates request and allocates
5. System confirms booking with ticket

## Key Implementation Details

### State Machine (ParkingRequest)
```
REQUESTED → ALLOCATED → OCCUPIED → RELEASED
         ↘ CANCELLED ↙
```

### Allocation Strategy
1. Try requested zone first (same-zone preference)
2. If full, try adjacent zones (cross-zone with penalty flag)
3. Return failure if no slots available

### Rollback Mechanism
- Stores operation history
- Can undo last k allocations
- Restores slot availability and request states

## Requirements Met

✅ Zone-based city representation
✅ Multiple parking areas per zone
✅ Request lifecycle state management
✅ Same-zone preference allocation
✅ Cross-zone allocation support
✅ Cancellation & rollback
✅ Trip history & analytics
✅ No STL containers (pure Python classes)
✅ Multi-file implementation
✅ Header/implementation separation
