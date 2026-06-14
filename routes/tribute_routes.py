from flask import Blueprint, request, jsonify

tribute_bp = Blueprint('tribute', __name__)

# Tribute page content endpoint
@tribute_bp.route('/info', methods=['GET'])
def get_tribute_info():
    try:
        tribute_data = {
            'title': 'In Memory of Our Beloved Plants',
            'description': 'This page is dedicated to the plants that have touched our lives and enriched our environment.',
            'message': 'Every plant tells a story. Every leaf whispers wisdom. Every flower brings joy. Let us honor and remember the green companions that have made our world more beautiful.',
            'dedication': 'To all the plants that have been part of our journey - may your legacy continue to inspire us to nurture and protect nature.'
        }
        
        return jsonify(tribute_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tribute_bp.route('/submit', methods=['POST'])
def submit_tribute():
    try:
        data = request.get_json()
        plant_name = data.get('plant_name')
        message = data.get('message')
        submitted_by = data.get('submitted_by', 'Anonymous')
        
        if not plant_name or not message:
            return jsonify({'error': 'Plant name and message are required'}), 400
        
        # In a real application, you would save this to a database
        # For now, just return success
        
        return jsonify({
            'message': 'Tribute submitted successfully',
            'tribute': {
                'plant_name': plant_name,
                'message': message,
                'submitted_by': submitted_by
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
