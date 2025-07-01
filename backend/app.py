from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')

    # Save code to a temp .py file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as temp_file:
        temp_file.write(code)
        temp_filename = temp_file.name

    try:
        # Run the python code using subprocess
        result = subprocess.run(
            ['python3', temp_filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5  # prevent infinite loops
        )
        output = result.stdout
        errors = result.stderr
    except Exception as e:
        output = ''
        errors = f'Error: {str(e)}'
    finally:
        os.remove(temp_filename)  # cleanup

    return jsonify({
        'output': output,
        'errors': errors
    })

if __name__ == '__main__':
    app.run(debug=True)
