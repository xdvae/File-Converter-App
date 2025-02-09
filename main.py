from flask import Flask,render_template,request,send_file,make_response
from PIL import Image, ImageOps
from io import BytesIO
import os
from docx2pdf import convert
import pythoncom 
from werkzeug.utils import secure_filename

# import pypandoc
# Upload folder / allowed ext.               
ALLOWED_EXT_IMG = {'png','jpeg','jpg'}
ALLOWED_EXT_DOX = {'docx','doc'}
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def save_file(uploaded_file, upload_folder):
    if not uploaded_file or uploaded_file.filename == '':
        return None
    filename = uploaded_file.filename
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, "my_pdf.docx")
    uploaded_file.save(file_path)
    return file_path

# Make PDF func.
def make_pdf(files,user_file_name,file_type):
    file_type = int(file_type)
    user_file_name = secure_filename(user_file_name) #Secure filename to prevent getting malicious inputs

    if file_type == 1: # 1 is for Images to PDF. Will take images and make them into a PDF.

        Images = []
        for file in files:
            if file.filename == '':
                return render_template('errors.html',ErrorMessage="Files Uploaded Failed. 1 Extension not found!") # Case: No File Name
            else:
                print(allowed_file(filename=file.filename,image_or_word=file_type))
                if file and allowed_file(filename=file.filename,image_or_word=file_type) == True: # For Image files
                    img = Image.open(file).convert("RGB")
                    img = ImageOps.exif_transpose(img)
                    Images.append(img)
                else:
                    return render_template('errors.html',ErrorMessage="Files Uploaded Failed. 2 Extension Not Allowed!")
                if Images:
                    pdf_buffer = BytesIO()
                    Images[0].save(pdf_buffer, format="PDF",save_all=True,append_images=Images[1:])
                    pdf_buffer.seek(0)
                
        response = make_response(send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{user_file_name}.pdf"
        ))
        response.set_cookie('fileDownload', 'true', max_age=60)
        return response # Response will also send a cookie. TO know when to stop showing loader.
    
    elif file_type == 2: # 2 is for Word files. It will take word files. convert them to PDF.

        Images = []
        for file in files:
            if file.filename == '':
                return render_template('errors.html',ErrorMessage="Files Uploaded Failed. 1 Extension not found!") # Case: No File Name
            else:
                print(allowed_file(filename=file.filename,image_or_word=file_type))
                if file and allowed_file(filename=file.filename,image_or_word=file_type) == True: # For Image files
                    save_file(file,UPLOAD_FOLDER) # This will save the word file in the upload folder.
                    input_path = os.path.join(UPLOAD_FOLDER, "my_pdf.docx")
                    print("Issue lies here")
                    pythoncom.CoInitialize() 
                    file_name_made = f"{user_file_name}.pdf"
                    try:
                        # Build the full output path by joining the uploads folder with the file name
                        output_path = os.path.join(UPLOAD_FOLDER, file_name_made)

                        # Call your conversion function, which should write the PDF to the output_path
                        convert(input_path, output_path)
                    finally:
                        pythoncom.CoUninitialize() 
                    with open(output_path, "rb") as f:
                        pdf_bytes = f.read()

                    pdf_buffer = BytesIO(pdf_bytes)
                    pdf_buffer.seek(0)

                    os.remove(output_path)
                    os.remove(input_path)
                else:
                    return render_template('errors.html',ErrorMessage="Files Uploaded Failed. 2 Extension Not Allowed!")
        
        response = make_response(send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{user_file_name}.pdf"
        ))

    response.set_cookie('fileDownload', 'true', max_age=60)
    return response

# Check Allowed Files
def allowed_file(filename,image_or_word):
    if image_or_word == 1:  # 1 for images to pdf
            if '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT_IMG:
                return True
            else:
                return False
        
    elif image_or_word == 2: # 2 for word to pdf
            if '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT_DOX:
                return True 
            else:
                 return False
            
    else:
         return True

@app.route('/')
@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/upload-image-to-pdf',  methods=['GET','POST'])
def upload_1():

    if request.method == 'POST':
        if 'file' not in request.files:
            pass # Case: No file.

        user_file_name = request.form.get("name") # Get name/Files.
        files = request.files.getlist('file')
        file_type = request.form.get("file_type")
        print(file_type)
        return make_pdf(files,user_file_name,file_type) # Return will send Download req to browser.
    
    return render_template('get_data.html',func_type="Images To PDF",file_type="Images")


@app.route('/convert-word-to-pdf',methods=['GET','POST'])
def upload_2():

    if request.method == 'POST':
        if 'file' not in request.files:
            pass # Case: No file.
        
        user_file_name = request.form.get("name") # Get name/Files.
        files = request.files.getlist('file')
        file_type = request.form.get("file_type")
        print(file_type)
        print("The code was here")
        return make_pdf(files=files,user_file_name=user_file_name,file_type=file_type)

    return render_template('get_data_2.html',func_type="Word To PDF",file_type="Word File",drag_n_drop=1)


@app.route('/coming-soon')
def coming_soon():
    return render_template('coming_soon.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)