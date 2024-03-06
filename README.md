This Water Drop Simulation project models the motion of a drop of water falling onto a plain surface and displays the result in a VoiceOver-supported UI that a visually impaired or blind user can interact with.


Process overview:  

I recorded a video of a drop of water falling on a surface using my phone’s back camera (also included in the repo). 
This video is then processed by Python’s OpenCV library to generate a list of time and position data points for velocity and acceleration calculations using numPy.
The subsequent data points are then curve-fitted using an exponential decay formula.
To assess the model’s fit, I plotted the data (3 graphs) using the matploblib library (commented out in the code) in python for visual analysis. 
The final fitted graph’s data points are then stored in a .csv file which is called by SwiftUI and then using Swift’s Chart library, is represented in graph view on a single-page macOS app window. This resulting graph is then made accessible to blind/visually impaired users using VoiceOver support, accessibility labels.


Limitations for AX and what I could have done better:

The AX descriptions for the model are static. If the data were to change, perhaps a more meaningful way to support dynamic (or otherwise) charts is to effectively use the AudioGraph API by Apple. I attempted to integrate it but given the scope of the project, stuck to AX elements.


Code components:

- WaterDropModel.py: Python is used for video processing, subsequent calculations, curve fitting and data analysis using appropriate libraries.
- ContentView.swift: SwiftUI is used to display the results with VoiceOver accessibility compatibility.
    - Some way to start
    - Some way to end → button.


Design choices:

- Chose to deploy and develop on XCode for integrated VoiceOver support and testing.
- Single page SwiftUI since it’s a representation.
- MacOS project setup:
    - data persistence or results are not required and therefore no storage support.
- Python for the core program because of its vast library choices for video processing, calculations, graph fitting, and data analysis.
- PythonKit (a python interoperability library for Swift) package is used to run both Python and Swift in the same XCode project.
- OpenCV (an image processing library in Python)
    - pip install opencv-python matplotlib
    - OpenCV is an image processing library in python that was used to track the position of the water drop in each extracted frame. This created a list of positions vs. time data points, which were then used to calculate velocity and acceleration data.
- Other considerations: I tried using the Audio graph API but it seemed overkill for something as simple as the description of a non-dynamic project so I stuck to using custom Accessibility elements.
- Water droplet detection was difficult due to not having a distinct background, bright enough lighting, and a higher resolution camera. Therefore, after trial and error, to make image processing and droplet detection easier, I took the liberty of mixing some soy sauce with water to enhance contrast detection.
- Due to device limitation, video is 30 fps. This may have some repercussions on data quality during image processing and subsequent calculations.


To Run:

You will need a macOS system for XCode support. Fork this repository and ensure the media file (containing the video) is in the same project directory as [PythonWaterDrop.py](http://WaterDropSimulation.py) file.


References:

- https://developer.apple.com/documentation/accessibility/representing-chart-data-as-an-audio-graph
- https://developer.apple.com/documentation/accessibility/audio-graphs
- https://github.com/pvieito/PythonKit
