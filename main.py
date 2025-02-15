from flask import Flask,render_template,request,send_file,make_response
from PIL import Image, ImageOps
from io import BytesIO
import os
from werkzeug.utils import secure_filename
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
# Allowed EXT/Uploads folder.
ALLOWED_EXT_IMG = {'png','jpeg','jpg'}
ALLOWED_EXT_DOX = {'docx','doc'} 
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def save_file(uploaded_file,upload_folder): # Function to save file in Uploads.
    if not uploaded_file or uploaded_file.filename == '':
        return None
    filename = uploaded_file.filename
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, secure_filename(filename))
    uploaded_file.save(file_path)
    return file_path

def allowed_file(filename,image_or_word): # Function to check file ext.
    print("In Allowed file function:",filename,"File Type:",image_or_word)
    if int(image_or_word) == 1:  # 1 for images to pdf
            print("The code was here.")
            if '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT_IMG:
                return True
            else:
                return False    
    elif int(image_or_word) == 2: # 2 for word to pdf
            print("Code was in word to pdf")
            if '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT_DOX:
                return True 
            else:
                 return False
    else:
         return render_template('errors.html',ErrorMessage="Unsupported File Type!")

def images_to_pdf(file_name,file,file_type): # Function to make images to pdf.
    file_name = secure_filename(file_name)
    photos = [] # Empty list to add images to.
    print("Secured filename, Entering Loop")
    for images in file:
            if images.filename == '':
                print("empty filename")
                return render_template('errors.html',ErrorMessage="Files Uploaded Failed.  Extension not found!") # Case: No File Name
            else:  
                print("Enters else block 2")
                print(allowed_file(filename=images.filename,image_or_word=file_type))
                if file and allowed_file(filename=images.filename,image_or_word=file_type) == True: # For Image files
                    img = Image.open(images).convert("RGB")
                    img = ImageOps.exif_transpose(img)
                    photos.append(img)
                else:
                    print("Enters else block 3")
                    return render_template('errors.html',ErrorMessage="Files Uploaded Failed.  Extension Not Allowed!")
                if images:
                    pdf_buffer = BytesIO()
                    photos[0].save(pdf_buffer, format="PDF",save_all=True,append_images=photos[1:])
                    pdf_buffer.seek(0)

    return send_download_req(pdf_buffer=pdf_buffer,user_file_name=file_name)

def word_to_pdf(file_name,file,file_type): # Function to make word to pdf.
    for i in file:
        if allowed_file(filename=i.filename,image_or_word=file_type):
            word_file_path = save_file(uploaded_file=i,upload_folder=UPLOAD_FOLDER)
            print("saved")
            # Code below converts the word into pdf
            doc = Document(word_file_path)
            pdf_file_path = os.path.splitext(word_file_path)[0] + '.pdf'
            c = canvas.Canvas(pdf_file_path, pagesize=letter)
            width, height = letter
            
            y = height - 40
            for para in doc.paragraphs:
                text = para.text
                c.drawString(40, y, text)
                y -= 20
                if y < 40:
                    c.showPage()
                    y = height - 40
            
            c.save()
            print(pdf_file_path)
            with open(pdf_file_path, "rb") as f:
                pdf_bytes = f.read()
                pdf_buffer = BytesIO(pdf_bytes)
                pdf_buffer.seek(0)
            os.remove(word_file_path)
            os.remove(pdf_file_path)
            return send_download_req(pdf_buffer=pdf_buffer,user_file_name=file_name)

def send_download_req(pdf_buffer,user_file_name): # Function to send download request.
    response = make_response(send_file(
    pdf_buffer,
    mimetype='application/pdf',
    as_attachment=True,
    download_name=f"{user_file_name}.pdf"
))
    response.set_cookie('fileDownload', 'true', max_age=60)
    return response


# App Routes.
@app.route('/')
@app.route('/main')
def main():    # Home page
    return render_template('index.html')

@app.route('/upload-image-to-pdf',  methods=['GET','POST'])
def img_to_pdf():    # Images to PDF page.
    if request.method == 'POST':
        if 'file' not in request.files:
            pass # Case: No file.
            print("Case no files triggered")
        else:
            user_file_name = request.form.get("name") # Get Name/Files/Type.
            files = request.files.getlist('file')
            file_type = request.form.get("file_type") # INT value (1 or 2)
            print("File Type: ",file_type)
            print("Else function triggered will go in the function")
            return images_to_pdf(file_name=user_file_name,file=files,file_type=file_type)

    return render_template ('get_data.html',func_type="Images To PDF",file_type="Images")

@app.route('/convert-word-to-pdf',methods=['GET','POST'])
def wrd_to_pdf():  # Word to PDF page.
    if request.method == 'POST':
        if 'file' not in request.files:
            pass # Case: No file.
            print("Case no files triggered")
        else:
            user_file_name = request.form.get("name") # Get Name/Files/Type.
            files = request.files.getlist('file')
            file_type = request.form.get("file_type") # INT value (1 or 2)
            print("File Type: ",file_type)
            print("Else function triggered will go in the function")
            return word_to_pdf(file_name=user_file_name,file=files,file_type=file_type)
        
    return render_template('get_data_2.html',func_type="Word To PDF",file_type="Word File")

@app.route('/coming-soon')
def coming_soon():  # Coming Soon..
    return render_template('coming_soon.html')

if __name__ == '__main__': # Root app.
    app.run(host='0.0.0.0', port=5000, debug=True)

# Dev notes:
    # 1. Rewrite whole code and make it reluctant. ✅ 15/02/25 
    # 2. Impliment all functions from older main.py file in a better way. ✅ 15/02/25 
    # 3. Make a working Word files to PDF converter. ❌ ...
    # 4. Only then. Move on.