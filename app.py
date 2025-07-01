from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code', '')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp:
        temp.write(code)
        filename = temp.name

    try:
        result = subprocess.run(
            ['python3', filename],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout
        error = result.stderr
    except Exception as e:
        output = ''
        error = str(e)
    finally:
        os.remove(filename)

    return jsonify({'output': output, 'error': error})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
