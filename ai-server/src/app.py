import os
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import cv2
import insightface
from insightface.app import FaceAnalysis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check GPU availability
print("GPU available:", tf.config.list_physical_devices('GPU'))

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize face detection models
try:
    # Initialize InsightFace SCRFD model for face detection
    face_detector = FaceAnalysis(name='buffalo_sc', 
                                root='../models/insightface', 
                                providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    face_detector.prepare(ctx_id=0, det_size=(640, 640))
    print("InsightFace model loaded successfully")
except Exception as e:
    print(f"Error loading InsightFace model: {e}")
    face_detector = None

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'face_detector': face_detector is not None,
    })

# Face detection route
@app.route('/detect-faces', methods=['POST'])
def detect_faces():
    if face_detector is None:
        return jsonify({'error': 'Face detection model not loaded'}), 500
        
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    try:
        # Read image
        file = request.files['image']
        img_bytes = file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect faces
        faces = face_detector.get(img)
        
        # Format results
        results = []
        for face in faces:
            bbox = face.bbox.astype(int).tolist()
            confidence = float(face.det_score)
            
            results.append({
                'bbox': bbox,  # [x1, y1, x2, y2]
                'confidence': confidence,
            })
        
        return jsonify({
            'success': True,
            'faces': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Face embedding route (placeholder - will be implemented in Phase 1)
@app.route('/get-face-embedding', methods=['POST'])
def get_face_embedding():
    return jsonify({
        'success': True,
        'message': 'This endpoint will be implemented in Phase 1'
    })

# Liveness detection route (placeholder - will be implemented in Phase 1)
@app.route('/liveness-detection', methods=['POST'])
def liveness_detection():
    return jsonify({
        'success': True,
        'message': 'This endpoint will be implemented in Phase 1'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)