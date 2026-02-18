
import os
import glob
import subprocess
import json
from flask import Flask, send_from_directory, render_template_string, request, jsonify

app = Flask(__name__)

# Config
PORT = 1101
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# HTML Template for Index Page
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Available Audit Reports</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-gray-50 min-h-screen p-10">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">Available Audit Reports</h1>
        <div class="bg-white shadow rounded-lg overflow-hidden">
            <ul class="divide-y divide-gray-200">
                {% for report in reports %}
                <li class="px-6 py-4 hover:bg-gray-50 flex items-center justify-between">
                    <div>
                        <a href="/view/{{ report }}" class="text-indigo-600 font-semibold hover:text-indigo-900 text-lg">
                            {{ report }}
                        </a>
                    </div>
                    <a href="/view/{{ report }}" class="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded hover:bg-indigo-700">
                        View Report
                    </a>
                </li>
                {% else %}
                <li class="px-6 py-10 text-center text-gray-500">
                    No reports generated yet. Run <code>execution/create_audit_report.py</code> first.
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """List all available HTML reports in the outputs directory."""
    try:
        reports = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.html')]
        reports.sort(reverse=True) # Show newest first
    except FileNotFoundError:
        reports = []
    
    return render_template_string(INDEX_TEMPLATE, reports=reports)

@app.route('/view/<path:filename>')
def serve_report(filename):
    """Serve a specific report file."""
    return send_from_directory(OUTPUT_DIR, filename)

@app.route('/api/generate', methods=['POST'])
def api_generate_report():
    """
    API Endpoint to generate a report from JSON data.
    """
    try:
        data = request.get_json(force=True)
        if not data:
             return jsonify({"status": "error", "message": "No JSON data provided"}), 400
             
        # Create temp file
        temp_dir = os.path.join(BASE_DIR, '.tmp')
        os.makedirs(temp_dir, exist_ok=True)
        timestamp = int(os.path.getmtime(os.path.abspath(__file__))) # just a number
        from datetime import datetime
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        
        input_file = os.path.join(temp_dir, f"input_{timestamp_str}.json")
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
            
        # Run generation script
        script_path = os.path.join(BASE_DIR, 'execution', 'create_audit_report.py')
        
        # We start the script as a separate process to avoid blocking too much (though verify waits)
        # For simplicity in this v1, we block to return the result immediately.
        cmd = ["python", script_path, "--input-json", input_file]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
             return jsonify({"status": "error", "message": "Generation failed", "details": result.stderr}), 500
             
        # Extract filename from stdout or predict it
        # The script prints "Report generated successfully: ...path..."
        # But we can also look for the newest file in outputs/
        
        # Get newest file in output dir
        list_of_files = glob.glob(os.path.join(OUTPUT_DIR, '*.html')) 
        if not list_of_files:
            return jsonify({"status": "error", "message": "Report not created"}), 500
            
        latest_file = max(list_of_files, key=os.path.getctime)
        filename = os.path.basename(latest_file)
        
        # Clean up temp input
        # os.remove(input_file) # Optional: keep for debugging
        
        return jsonify({
            "status": "success",
            "message": "Report generated successfully",
            "report_url": f"{request.host_url}view/{filename}?t={timestamp_str}",
            "filename": filename
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print(f"Starting server on port {PORT}...")
    print(f"Directory being served: {OUTPUT_DIR}")
    # Host on 0.0.0.0 to be accessible externally if firewall allows
    app.run(host='0.0.0.0', port=PORT, debug=True)
