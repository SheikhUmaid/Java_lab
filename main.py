from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/<filename>')
def serve_text(filename):
    return send_from_directory(
        'static',
        filename,
        mimetype='application/pdf',
        as_attachment=False,
    )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


