
(1) put the input hazardlog into /hazardlog_input folder (empty folder if there exits files already)
(2) put the screenshots into static/Screenshots folder (empty folder if there exits files already)
(2) choose needed data for final report by adjusting 6 FLags in data_process.py(line9-14)
(3) open cmd
(4) pip install Flask(only for first time)
(5) cd flask
(6) python3 main.py
(7) open link http://127.0.0.1:5000/ and see result



Directory Tree
flask---------------------------------------------------------------------------------Base directory
├── data_process.py---------------------------------------------------------main data process script
├── hazardlog_input
│   └── HazardLog.txt----------------------------------------------------------------input hazardlog
├── hazardlog_output
│   └── Output_HazardLog.txt-------------------------------------------------output report hazardlog
├── main.py-----------------------------------------------------------------------------flask script
├── __pycache__
│   ├── data_process.cpython-38.pyc
│   └── data_process.cpython-39.pyc
├── readme.txt---------------------------------------------------------------------------instruction
├── static
│   ├── bootstrap.min.css--------------------------------------------------------------css framework
│   ├── header_140.jpg
│   ├── img-------------------------------------------------------------------------generated images
│   │   ├── Affected Bodypart of all Hazardlogs.png
│   │   └── Distance Bar Figure.png
│   ├── IPR.png
│   ├── KIT.png
│   └── Screenshots----------------------------------------------------------------Screenshots images
│       ├── Hazard_ 1 2021_07_06-13_35_52.png
│       ├── Hazard_ 1 2021_07_06-13_36_52.png
│       ├── Hazard_ 1 2021_07_06-13_38_32.png
│       ├── Hazard_ 1 2021_07_06-13_38_41.png
│       └── Hazard_ 1 2021_07_07-16_15_05.png
└── templates
    └── Visuliazation Summary of HazardLog.html------------------------------------html file for flask

