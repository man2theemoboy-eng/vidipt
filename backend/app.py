from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import logging
from pathlib import Path
import subprocess
import json

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'jpg', 'jpeg', 'png', 'gif', 'webp', 'txt', 'pdf'}

CORS(app)

# Create necessary directories
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store job metadata
jobs = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get supported languages and accents"""
    return jsonify({
        'languages': [
            {'code': 'hi', 'name': 'Hindi', 'accents': ['standard', 'north', 'northeast', 'south']},
            {'code': 'en', 'name': 'English', 'accents': ['standard', 'northeast', 'hindi-english']},
            {'code': 'as', 'name': 'Assamese', 'accents': ['standard', 'northeast']},
            {'code': 'ta', 'name': 'Tamil', 'accents': ['standard', 'south']},
            {'code': 'te', 'name': 'Telugu', 'accents': ['standard', 'south']},
            {'code': 'kn', 'name': 'Kannada', 'accents': ['standard', 'south']},
            {'code': 'ml', 'name': 'Malayalam', 'accents': ['standard', 'south']}
        ]
    })

@app.route('/api/video-configs', methods=['GET'])
def get_video_configs():
    """Get available video configurations"""
    return jsonify({
        'sizes': [
            {'label': '720p', 'width': 1280, 'height': 720},
            {'label': '1080p', 'width': 1920, 'height': 1080},
            {'label': '4K', 'width': 3840, 'height': 2160},
            {'label': 'Portrait (9:16)', 'width': 1080, 'height': 1920},
            {'label': 'Square (1:1)', 'width': 1080, 'height': 1080}
        ],
        'frameRates': [24, 30, 60],
        'effects': ['none', 'fade', 'slide', 'zoom', 'typewriter', 'bounce']
    })

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle file uploads"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        uploaded_files = []
        
        for file in files:
            if file.filename == '':
                continue
            
            # Validate file extension
            if '.' not in file.filename:
                return jsonify({'error': 'File must have an extension'}), 400
            
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            if file_ext not in app.config['ALLOWED_EXTENSIONS']:
                return jsonify({'error': f'File type .{file_ext} not allowed'}), 400
            
            # Save file
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            uploaded_files.append({
                'id': uuid.uuid4().hex,
                'filename': file.filename,
                'path': filepath,
                'size': os.path.getsize(filepath),
                'type': file.content_type
            })
        
        return jsonify({
            'success': True,
            'files': uploaded_files
        })
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    """Generate video from script and media"""
    try:
        data = request.get_json()
        
        # Validate request
        if not data.get('script'):
            return jsonify({'error': 'Script is required'}), 400
        
        if not data.get('language'):
            return jsonify({'error': 'Language is required'}), 400
        
        # Create job ID
        job_id = uuid.uuid4().hex
        
        # Store job metadata
        jobs[job_id] = {
            'status': 'processing',
            'progress': 0,
            'created_at': datetime.now().isoformat(),
            'stage': 'initializing',
            'script': data.get('script', ''),
            'language': data.get('language', 'en'),
            'accent': data.get('accent', 'standard'),
            'video_size': data.get('video_size', '1080p'),
            'frame_rate': data.get('frame_rate', 30),
            'effects': data.get('effects', 'none'),
            'background_music': data.get('background_music', True),
            'animation_style': data.get('animation_style', 'standard')
        }
        
        # Simulate video generation process
        _process_video_job(job_id)
        
        logger.info(f"Starting video generation job: {job_id}")
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'status': 'processing',
            'message': 'Video generation started'
        }), 202
    
    except Exception as e:
        logger.error(f"Video generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get job status"""
    try:
        if job_id not in jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(jobs[job_id])
    
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<job_id>', methods=['GET'])
def download_video(job_id):
    """Download generated video"""
    try:
        if job_id not in jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = jobs[job_id]
        if job['status'] != 'completed':
            return jsonify({'error': 'Video not ready yet'}), 400
        
        video_path = job.get('output_path')
        if not video_path or not os.path.exists(video_path):
            return jsonify({'error': 'Video file not found'}), 404
        
        return send_file(
            video_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name=f'vidipt_{job_id}.mp4'
        )
    
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview', methods=['POST'])
def preview_script():
    """Generate audio preview of script"""
    try:
        data = request.get_json()
        script = data.get('script', '')
        language = data.get('language', 'en')
        accent = data.get('accent', 'standard')
        
        if not script:
            return jsonify({'error': 'Script is required'}), 400
        
        # For now, return a placeholder
        # In production, this would use Google Cloud TTS or similar
        audio_filename = f'preview_{uuid.uuid4().hex}.wav'
        
        return jsonify({
            'success': True,
            'audio_url': f'/api/stream-audio/{audio_filename}'
        })
    
    except Exception as e:
        logger.error(f"Preview error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/music-search', methods=['POST'])
def search_music():
    """Search for copyright-free background music"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        # Return sample music results
        music_results = [
            {'title': 'Ambient Background', 'url': '/music/ambient.mp3', 'source': 'Pixabay'},
            {'title': 'Uplifting Strings', 'url': '/music/uplifting.mp3', 'source': 'Pixabay'},
            {'title': 'Corporate', 'url': '/music/corporate.mp3', 'source': 'Pixabay'},
        ]
        
        return jsonify({
            'success': True,
            'results': music_results
        })
    
    except Exception as e:
        logger.error(f"Music search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def _process_video_job(job_id):
    """Process video generation job (simulated)"""
    try:
        job = jobs[job_id]
        
        # Simulate processing stages
        stages = [
            ('generating_audio', 20),
            ('processing_media', 35),
            ('adding_music', 50),
            ('composing_video', 70),
            ('finalizing', 90)
        ]
        
        for stage, progress in stages:
            job['stage'] = stage
            job['progress'] = progress
            logger.info(f"Job {job_id}: {stage} - {progress}%")
        
        # Create dummy output video file
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{job_id}_final.mp4')
        
        # Create a simple test video (in production, FFmpeg would be used)
        _create_test_video(output_path)
        
        job['status'] = 'completed'
        job['progress'] = 100
        job['output_path'] = output_path
        job['completed_at'] = datetime.now().isoformat()
        
        logger.info(f"Video generation completed: {job_id}")
        
    except Exception as e:
        logger.error(f"Video processing error for {job_id}: {str(e)}")
        job['status'] = 'failed'
        job['error'] = str(e)

def _create_test_video(output_path):
    """Create a simple test video file"""
    # Create a minimal MP4 file for testing
    # In production, FFmpeg would be used to create actual videos
    try:
        # Check if FFmpeg is available
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        
        # Create a simple test video using FFmpeg
        cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'color=c=blue:s=1920x1080:d=5',
            '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono:d=5',
            '-pix_fmt', 'yuv420p', '-y', output_path
        ]
        subprocess.run(cmd, capture_output=True, check=False)
    except:
        # If FFmpeg not available, create empty file
        with open(output_path, 'wb') as f:
            f.write(b'MOCK_VIDEO_FILE')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
