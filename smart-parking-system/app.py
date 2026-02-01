from flask import Flask, render_template, request, jsonify
from core.ParkingSystem import ParkingSystem

app = Flask(__name__)

# Initialize parking system
parking_system = ParkingSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/zones', methods=['GET'])
def get_zones():
    """Get all zones with available slots count"""
    zones_data = []
    for zone_name, zone in parking_system.zones.items():
        zones_data.append({
            'name': zone_name,
            'available_slots': zone.get_available_slots_count(),
            'hourly_rate': zone.hourly_rate
        })
    return jsonify(zones_data)

@app.route('/api/slots/<zone_name>', methods=['GET'])
def get_slots(zone_name):
    """Get slots for a specific zone"""
    slots = parking_system.get_zone_slots(zone_name)
    return jsonify(slots)

@app.route('/api/book', methods=['POST'])
def book_parking():
    """Book a parking slot"""
    data = request.json
    vehicle_id = data.get('vehicle_id')
    vehicle_type = data.get('vehicle_type')
    requested_zone = data.get('zone')
    
    # Create parking request
    parking_request, success = parking_system.create_parking_request(
        vehicle_id, vehicle_type, requested_zone
    )
    
    if success:
        return jsonify({
            'success': True,
            'request_id': parking_request.request_id,
            'slot_id': parking_request.allocated_slot.slot_id,
            'zone': parking_request.allocated_zone,
            'is_cross_zone': parking_request.is_cross_zone,
            'check_in_time': parking_request.check_in_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No available slots in requested or adjacent zones'
        }), 400

@app.route('/api/cancel/<request_id>', methods=['POST'])
def cancel_parking(request_id):
    """Cancel a parking request"""
    success = parking_system.cancel_request(request_id)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({
            'success': False,
            'message': 'Cannot cancel this request'
        }), 400

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get parking analytics"""
    analytics = parking_system.get_analytics()
    return jsonify(analytics)

@app.route('/api/rollback', methods=['POST'])
def rollback():
    """Rollback last k operations"""
    data = request.json
    k = data.get('k', 1)
    
    count = parking_system.rollback_operations(k)
    return jsonify({
        'success': True,
        'rolled_back_count': count
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
