# autograder
#### An OCR-based autograder for handwritten free-response answers using TensorFlow and OpenCV.

### Motivation
Hand-grading free-response questions is a daunting task for many teachers. Current technology allows for autograding of multiple-choice questions (e.g., Illuminate has built-in scoring and gradebook update capabilities). However, OCR-based handwriting recognition is not yet readily available to the public. This tool aims to alleviate the grading burden for teachers.

# Overview


### Inspiration

Current technology is proprietary. I aim to create a lighter-weight, opensource tool with similar functionality. 

1. Illuminate Education software integrates OCR autograding and gradebook updating for multiple choice tests. As a former teacher, this tool was invaluable. It is the primary inspiration for my project.
![illuminate](images/Illuminate.png "Illuminate" ) 
2. Microsoft has very strong on-the-fly penstroke capturing software, Windows Ink, which parses handwritten digits and symbols into mathematical expressions.  
![microsoft](images/MicrosoftInk.png "Windows Ink" ) 


## Table of content

- [Preprocessing](#image-processing)
    - [TER](#typo3-extension-repository)
    - [Composer](#composer)
- [Product Design](#product-design)
    - [General](#general-design)
    - [Detailed](#detailed-design)
- [Data Sources](#data-sources)
    - [Upload the page tree file](#upload-the-page-tree-file)
    - [Go to the import view](#go-to-the-import-view)
    - [Import the uploaded page tree file](#import-the-uploaded-page-tree-file)
- [License](#license)
- [Links](#links)


# Data Sources
| Name | Description | Link | Usage |
| --- | --- | --- | --- |
| MNIST | Well-known repository for handwritten digits | http://yann.lecun.com/exdb/mnist/ | Training |
| HASYv2 | Over 150,000 handwritten characters <br>(including LaTeX mathematical symbols) | https://zenodo.org/record/259444 | Training |
| Kenasata | Over 16,000 labeled handwritten digits <br>(includes gender, country, age) | https://github.com/kensanata/numbers | Testing |
| CROHME | Competition on Recognition of Online Handwritten <br>Mathematical Expressions (InkML format) |https://www.isical.ac.in/~crohme/CROHME_data.html | Future Directions |



# Product Design


| General | Detailed |
| --- | --- |
| ![general-design](images/Nina_AutoGrader-1.png "general design" ) | ![detailed-design](images/Nina_AutoGrader-2.png "detailed design")|

## Image Processing

### Raw Image
Image taken from smartphone\
<img src="images/0734.jpg"
     style="float: left; margin-right: 10px;" />
     
### Preprocessing
PIL image from raw image file\
<img src="images/0734_preprocessed.png"
     style="float: left; margin-right: 10px;" />

     
#### Issue: Segmentation fails. 
Results in 4000+ segments (expected 4) due to noisy, non-white background. 
<br>Dots are each considered separate segments. Requires processing.\

### Preprocessing
PIL image from raw image file\
<img src="images/0734_postprocessed.png"
     style="float: left; margin-right: 10px;" />\
     
     
### Segmented Image
Proper segmentation using skimage package\
<img src="images/0734_segmented.png"
     style="float: left; margin-right: 10px;" />\
    
 