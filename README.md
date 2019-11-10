# autograder
#### An OCR-based autograder for handwritten free-response answers using TensorFlow and OpenCV.

### Motivation
Hand-grading free-response questions is a daunting task for many teachers. Current technology allows for autograding of multiple-choice questions (e.g., Illuminate has built-in scoring and gradebook update capabilities). However, OCR-based handwriting recognition is not yet readily available to the public. This tool aims to alleviate the grading burden for teachers.

# Overview


### Inspiration

Current technology is proprietary. I aim to create a lighter-weight, opensource tool with similar functionality. 

1. Illuminate Education software integrates OCR autograding and gradebook updating for multiple choice tests. As a former teacher, this tool was invaluable. It is the primary inspiration for my project.
![illuminate](images/Illuminate.png "Illuminate" ) 
2. Microsoft has powerful on-the-fly penstroke capturing software, Windows Ink, which parses handwritten digits and symbols into mathematical expressions.  
![microsoft](images/MicrosoftInk.png "Windows Ink" ) 


## Table of content


- [Product Design](#product-design)
    - [General](#general-design)
    - [Detailed](#detailed-design)
- [Data Sources](#data-sources)
    - [Upload the page tree file](#upload-the-page-tree-file)
    - [Go to the import view](#go-to-the-import-view)
    - [Import the uploaded page tree file](#import-the-uploaded-page-tree-file)
- [Preprocessing](#image-processing)
    - [TER](#typo3-extension-repository)
    - [Composer](#composer)
- [License](#license)
- [Links](#links)

# Product Design

| General | Detailed |
| --- | --- |
| ![general-design](images/Nina_AutoGrader-1.png "general design" ) | ![detailed-design](images/Nina_AutoGrader-2.png "detailed design")|


# Data Sources
| Name | Description | Link | Usage |
| --- | --- | --- | --- |
| MNIST | Well-known repository for handwritten digits | http://yann.lecun.com/exdb/mnist/ | Training |
| HASYv2 | Over 150,000 handwritten characters <br>(including LaTeX mathematical symbols) | https://zenodo.org/record/259444 | Training |
| Kenasata | Over 16,000 labeled handwritten digits <br>(includes gender, country, age) | https://github.com/kensanata/numbers | Testing |
| CROHME | Competition on Recognition of Online Handwritten <br>Mathematical Expressions (InkML format) |https://www.isical.ac.in/~crohme/CROHME_data.html | Future Directions |

## Obtaining Data
#### MNIST
Data can be loaded using keras or sklearn.

##### keras has the full MNIST set
- 70,000 total images split into train (60K) and test (10K)
- image size: 28 x 28 pixels

```
from tensorflow.keras.datasets import mnist
(X_train,y_train),(X_test,y_test) = mnist.load_data()
```

##### sklearn has a small subset of MNIST
- 1,797 total images
- image size: 8 x 8 pixels

```
from sklearn.datasets import load_digits
digits = load_digits()
X = digits.data
y = digits.target
```





## Image Processing


| Stage | Image | Issues |
| --- | --- | --- | 
| Raw Image | ![raw-image](images/0734.jpg "Raw Image" ) | From the human eye, 4 distinct segments are readily apparent. However, shadows and other subtle artifacts are detected by the computer as objects.  | 
| Preprocessed Binary | ![binary-image](images/0734_original.jpg "Binary Image" ) | Results in 4000+ segments (expected 4) due to noisy, non-white background. Dots are each considered separate segments. Requires processing. | 
| Postprocessed Binary | ![processed-image](images/postprocessed_binary.jpg "Processed Image" ) | Adjusting alpha levels and gaussian blurring reduces noise from raw image. Segmentation ready.  | 
| Segmented Image | ![segmented-image](images/0734_segmented.png "Segmented Image" ) | Proper segmentation detects 4 objects.  | 

