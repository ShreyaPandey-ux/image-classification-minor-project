from flask import Flask, render_template, request, redirect, url_for, flash,session,send_from_directory
from werkzeug.utils import secure_filename
import os
from flask import jsonify
from classifier import classify_image
app = Flask(__name__)
app.secret_key = 'supersecretmre'
app.config['UPLOAD_FOLDER'] = "static/uploads"  

ALLOWED_FILETYPES = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILETYPES

@app.route('/')
def index():
    flash('Welcome to the Image Classification App', 'info')
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    images = os.listdir("static/uploads")
    return render_template("gallery.html", images=images)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['file'] =  os.path.join('/',app.config['UPLOAD_FOLDER'], filename)
            return jsonify({'success': True, 'message': 'File uploaded successfully'})
        else:
            return jsonify({'success': False, 'message': 'File type not allowed'})
    return render_template('form.html')

@app.route('/delete/<image>')
def delete(image):
    filepath = os.path.join('static/uploads', image)
    os.remove(filepath)
    flash('File deleted successfully', 'success')
    return redirect(url_for('gallery'))

@app.route('/download/<image>')
def download(image):
    return send_from_directory('static/uploads', image, as_attachment=True)

@app.route('/classify/<filename>')
def select(filename):
    BASE_DIR = 'static/uploads'
    filepath = os.path.join(BASE_DIR, secure_filename(filename))
    session['file'] = "/"+filepath
    classification = classify_image(filepath)
    return render_template('results.html', classification=classification)

@app.route('/classification', methods=['GET','POST'])
def result():
    return render_template('results.html')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)