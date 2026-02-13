
import os
from flask import Flask, send_from_directory, render_template_string

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

if __name__ == '__main__':
    print(f"Starting server on port {PORT}...")
    print(f"Directory being served: {OUTPUT_DIR}")
    # Host on 0.0.0.0 to be accessible externally if firewall allows
    app.run(host='0.0.0.0', port=PORT, debug=True)
