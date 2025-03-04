# File Conversion and Download Toolkit

A Flask web application that handles file conversions and media downloads. Currently supports image-to-PDF conversion, with plans to expand functionality for document format conversions and media downloading capabilities.

## Features

### Current Features
- **Image to PDF Conversion**:  
  Convert multiple images (PNG, JPG, JPEG) into a single PDF file.  
  - Preserves image orientation using EXIF data
  - Custom output filename support
  - Word (.docx) to PDF

### Planned Features
- **Document Conversions**:
  - PowerPoint (.pptx) to PDF
  - PDF to Word
  - PDF to PowerPoint
- **Media Downloader**:
  - Download music/videos from URLs (YouTube, SoundCloud, etc.)
  - Format selection (MP3, MP4, etc.)

## To use
- https://xdvaibhav.pythonanywhere.com
- The above site is hosting the App with limited features.
## Installation

### Prerequisites (to run locally)
- Python 3.8+
- pip package manager
- docx2pdf 
- Flask
- pillow 
- Werkzeug 

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/xdvae/File-Converter-App
   cd file_converter

2. Install Requirements:
    ```bash
    pip install -r requirements.txt