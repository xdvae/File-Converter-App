from flask import Flask,render_template,request,send_file
from PIL import Image, ImageOps
from io import BytesIO
# import pypandoc
# Upload folder / allowed ext.
ALLOWED_EXT_IMG = {'png','jpeg','jpg'}
ALLOWED_EXT_DOX = {'docx','doc'}
app = Flask(__name__)

# Check Allowed Files
def allowed_file(filename,image_or_word):
    if image_or_word == 1:
        return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT_IMG
    elif image_or_word == 2:
        return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT_DOX

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
        
        # Make PDF func.
        def make_pdf():
            Images = []

            for file in files:
                if file.filename == '':
                    return render_template('errors.html',ErrorMessage="Files Uploaded Failed. Extension not found!") # Case: No File Name
                else:
                    if file and allowed_file(file.filename,1): # For Image files
                        img = Image.open(file).convert("RGB")
                        img = ImageOps.exif_transpose(img)
                        Images.append(img)
                    else:
                        return render_template('errors.html',ErrorMessage="Files Uploaded Failed. Extension Not Allowed!")
                    if Images:
                        pdf_buffer = BytesIO()
                        Images[0].save(pdf_buffer, format="PDF",save_all=True,append_images=Images[1:])
                        pdf_buffer.seek(0)
                    
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"{user_file_name}.pdf"
            )
        return make_pdf() # Return will send Download req to browser.
    

    return render_template('get_data.html',func_type="Images To PDF",file_type="Images")

@app.route('/convert-word-to-pdf',methods=['GET','POST'])
def upload_2():

    # if request.method == 'POST':
        # if 'file' not in request.files:
        #     pass # Case: No file.

        # user_file_name = request.form.get("name") # Get name/Files.
        # files = request.files.getlist('file')
        
        # # Make PDF func.
        # def make_pdf():
        #     Images = []

        #     for file in files:
        #         if file.filename == '':
        #             return render_template('errors.html',ErrorMessage="Files Uploaded Failed. Extension not found!") # Case: No File Name
                
                # NOTE: The Error starts from below. I am leaving this code as is so i can fix it tommorow.
                # I dont think this library i am using currently is going to work so i will comment it out.
                # TODO: FInd the isssue with the word file not being sent and fix it.
            #    else:
            #         if file and allowed_file(file.filename,2): # For Image files
            #             img = Image.open(file).convert("RGB")
            #             img = ImageOps.exif_transpose(img)
            #             Images.append(img)
            #         else:
            #             return render_template('errors.html',ErrorMessage="Files Uploaded Failed. Extension Not Allowed!")
            #         if Images:
            #             pdf_buffer = BytesIO()
            #             Images[0].save(pdf_buffer, format="PDF",save_all=True,append_images=Images[1:])
            #             pdf_buffer.seek(0)
                    
            # return send_file(
            #     pdf_buffer,
            #     mimetype='application/pdf',
            #     as_attachment=True,
            #     download_name=f"{user_file_name}.pdf"
            # )
        # NOTE: Uncomment the return pdf below.
       # return make_pdf() # Return will send Download req to browser.
    
    # if request.method == 'POST':
    #     if 'file' not in request.files:
    #         print("Meow") # Case: No file.

    #     user_file_name = request.form.get("name") # Get name/Files.
    #     file = request.files.getlist('file')
        
    #     def make_pdf():
    #         if file.filename == '':
    #             return render_template('errors.html',ErrorMessage="Files Uploaded Failed. Extension not found!") # Case: No File Name
    #         else:
    #             if file and allowed_file(file.filename,2): # 2. For Docx files.
    #                 word_content = file.read() # Read File
    #                 pdf_content = pypandoc.convert_text(word_content, "pdf", format="docx") # Convert to PDF
    #             else:
    #                 return render_template('errors.html',ErrorMessage="Files Uploaded Failed. Extension Not Allowed!")
    #             if pdf_content:
    #                 pdf_buffer = BytesIO(pdf_content)
    #                 pdf_buffer.seek(0)

    #         return send_file(
    #             pdf_buffer,
    #             mimetype='application/pdf',
    #             as_attachment=True,
    #             download_name=f"{user_file_name}.pdf"
    #         )
    #     return make_pdf()
            
    return render_template('coming_soon.html',func_type="Word To PDF",file_type="Word File",drag_n_drop=1)

@app.route('/coming-soon')
def coming_soon():
    return render_template('coming_soon.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)