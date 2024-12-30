import os
import zipfile
from flask import Flask, render_template, request, redirect, url_for, session
from project import process_files
from flask import send_from_directory

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y_that_should_be_kept_s3cr3t'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("zipfiles")

        if len(files) != 2:
            return "Please upload exactly two ZIP files.", 400

        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        extracted_files = []
        for file in files:
            zip_path = os.path.join(upload_dir, file.filename)
            file.save(zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                extract_dir = os.path.join(upload_dir, os.path.splitext(file.filename)[0])
                zip_ref.extractall(extract_dir)
                extracted_files.extend(
                    [os.path.join(extract_dir, f) for f in os.listdir(extract_dir)]
                )

        # Save the extracted files in the session
        session['file_paths'] = extracted_files
        return redirect(url_for('analysis_choice'))
    
    return render_template('upload.html')


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         files = request.files.getlist("datafile")

#         if len(files) < 2:
#             return "Please upload at least two .db files.", 400

#         upload_dir = "uploads"
#         if not os.path.exists(upload_dir):
#             os.makedirs(upload_dir)

#         file_paths = []
#         for file in files:
#             file_path = os.path.join(upload_dir, file.filename)
#             file.save(file_path)
#             file_paths.append(file_path)

#         session['file_paths'] = file_paths
#         return redirect(url_for('analysis_choice'))

#     return render_template('upload.html')

@app.route('/analysis-choice', methods=['GET', 'POST'])
def analysis_choice():
    if request.method == 'POST':
        analysis_type = request.form['analysis_type']
        file_paths = session.get('file_paths', None)

        if not file_paths:
            return "No files uploaded. Please upload the necessary files.", 400

        if analysis_type == 'general':
            return redirect(url_for('mobile_similarities'))
        elif analysis_type == 'customized':
            return redirect(url_for('mobile_similarities'))

    return render_template('analysis_choice.html')

@app.route('/mobile-similarities', methods=['GET'])
def mobile_similarities():
    results = session.get('analysis_results', None)

    if not results:
        file_paths = session.get('file_paths', None)
        if not file_paths or len(file_paths) < 2:
            return "No files uploaded. Please upload at least two .db files.", 400

        results = process_files(file_paths)
        session['analysis_results'] = results

    # Initialize a variable to calculate the overall similarity
    overall_common_count = 0
    overall_total_count = 0

    for category, data in results.items():
        common_count = 0
        if category == "contacts":
            common_count = len(data.get("common_numbers", []))
        elif category == "calllogs":
            common_count = len(data.get("common_call_logs", []))
        elif category == "wifi":
            common_count = len(data.get("common_wifi", []))
        elif category == "similar_images":
            common_count = len(data.get("similar_images", []))

        total_device1 = data.get("total_device1", 0)
        total_device2 = data.get("total_device2", 0)

        # Add the category-specific counts to the overall total
        overall_common_count += common_count
        overall_total_count += max((total_device1 + total_device2), 1)

    # Calculate the overall similarity percentage
    overall_similarity = (overall_common_count / overall_total_count) * 10

    return render_template('mobile_similarities.html', overall_percentage=overall_similarity)

@app.route('/dashboard')
def dashboard():
    upload_dir = 'uploads'
    wifi_total = 0
    image_total = 0

    files = os.listdir(upload_dir)
    for file in files:
        if file.endswith('.txt'):
            wifi_total += 1
        elif file.endswith('.png'):
            image_total += 1

    results = session.get('analysis_results', None)

    if not results:
        return "No results available. Please upload files and perform analysis.", 400

    percentages = {}
    for category, data in results.items():
        common_count = 0
        if category == "contacts":
            common_count = len(data.get("common_numbers", []))
        elif category == "calllogs":
            common_count = len(data.get("common_call_logs", []))
        elif category == "wifi":
            common_count = len(data.get("common_wifi", []))
        elif category == "similar_images":
            common_count = len(data.get("similar_images", []))

        total_device1 = data.get("total_device1", 0)
        total_device2 = data.get("total_device2", 0)

        percentages[category] = int(common_count / max((total_device1 + total_device2), 1)) * 10

    return render_template('dashboard.html', 
                           percentages=percentages, 
                           wifi_total=wifi_total, 
                           image_total=image_total)

@app.route('/analysis-result')
def analysis_result():
    category = request.args.get('category')
    results = session.get('analysis_results', None)

    if not results or category not in results:
        return "No results available for the selected category.", 400

    category_data = results[category]
    return render_template('analysis_result.html', category=category, data=category_data)

if __name__ == '__main__':
    app.run(debug=True)
