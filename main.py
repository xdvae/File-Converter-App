from flask import Flask,render_template,request,send_file,after_this_request
import os
from PIL import Image, ImageOps



# Upload folder / allowed ext.
UPLOAD = 'uploads'
ALLOWED_EXT = {'pdf','png','jpeg','jpg'}

app = Flask(__name__)
app.config['uploads'] = UPLOAD

# Download Function
def send_file_to_download(name_of_pdf,name_by_user):
    print("It triggered this")

    @after_this_request
    def remove_file(response):
        try:
            os.remove(name_of_pdf)  
            print(f"Deleted: x")  
        except Exception as e:
            print(f"Error deleting file: {e}")
        return response
    
    response = send_file(
        name_of_pdf, 
        as_attachment=True,
        mimetype='application/pdf',
        download_name=f"{name_by_user}.pdf"
        )
    
    return response

# Check Allowed Files
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/')
@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/upload-image-to-pdf',  methods=['GET','POST'])
def upload():

    if request.method == 'POST':
        if 'file' not in request.files:
            pass # Case: No file.

        user_file_name = request.form.get("name") # Get name/Files.
        files = request.files.getlist('file')
        
        # Make PDF func.
        def make_pdf():
            Images = []
            pdf_name = os.path.join(app.config['uploads'], "My_PDF.pdf")

            for file in files:
                if file.filename == '':
                    return "<h1>Files Uploaded Failed. Extension not found!</h1>" # Case: No File Name
                else:
                    if file and allowed_file(file.filename):
                        img = Image.open(file).convert("RGB")
                        img = ImageOps.exif_transpose(img)
                        Images.append(img)
                    else:
                        return "<h1>Files Uploaded Failed. Extension Not Allowed!</h1>"
                    if Images:
                        Images[0].save(pdf_name, save_all=True,append_images=Images[1:])
                    
            return send_file_to_download(pdf_name, user_file_name)
            
        return make_pdf() # Return will send Download req to browser.
    

    return render_template('get_data.html',func_type="Images To PDF",file_type="Images")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)