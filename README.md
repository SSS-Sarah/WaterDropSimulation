# Project Description
This Water Drop Simulation project models the motion of a drop of water falling onto a plain surface and displays the result in a VoiceOver-supported UI that a visually impaired or blind user can interact with.

## Key Features:

- VoiceOver Support: The single-page SwiftUI macOS application offers VoiceOver compatibility, allowing users to navigate and interpret the graph representing the water drop's motion.
- Data-Driven Graphs: The simulation utilizes video processing from Python's OpenCV library to generate data points on the water drop's position over time. This data is then curve-fitted and displayed as a graph using the Swift Charts framework within the SwiftUI interface.
- Accessibility Labels: Descriptive labels are implemented to enhance user experience for those using VoiceOver.

## Process overview:  

- Data Collection: A video of a water drop falling is recorded using phone camera and included in the repository.
- Python Processing: The video is processed using OpenCV to extract time-series position data for velocity and acceleration calculations (powered by NumPy).
- Curve Fitting: The data points are fitted with an exponential decay formula to create a smooth representation of the motion.
- Data Visualization in Python for model analysis (Commented Out): (For development purposes only) Matplotlib is used within the Python script to generate three separate graphs for visual analysis of the data.
- Data Storage: The final fitted curve data is stored in a CSV file.
- SwiftUI Integration: The SwiftUI application retrieves the data from the CSV file and utilizes the Swift Charts framework to display it as a graph within the app window.
- Accessibility Implementation: VoiceOver support and accessibility labels are integrated throughout the SwiftUI interface for optimal user experience.


## Limitations for AX and Possible Improvements:

- Static AX Descriptions: Currently, the accessibility descriptions for the graph are static. For dynamic charts, utilizing Apple's AudioGraph API could provide a more immersive experience. While attempted, the current project scope limited its implementation.
- Enhancing Model Comprehension: The CSV file stores additional data points for acceleration and velocity. These could be visualized in future iterations to provide a more comprehensive understanding of the water droplet's motion.

## Tech Stack:

- Python: Leverages libraries like OpenCV, NumPy, and Matplotlib for video processing, calculations, curve fitting, and data analysis.
- SwiftUI: Creates the user interface and integrates data visualization using Swift Charts.
- PythonKit: Enables seamless interoperability between Python and Swift within the same Xcode project.
- Xcode: Development and deployment platform chosen for its built-in VoiceOver support and testing tools.

## Required Installations

```
pip install opencv-python numpy matplotlib
```

## Additional Notes on Hardware Limitations:

- Water droplet detection was made more manageable by mixing soy sauce with water to create higher contrast for image processing.
- The video's 30fps frame rate (hardware limitation) is likely to cause data quality variations during processing and calculations and any subsequent graphs.

## To Run:

Ensure you have a macOS system with Xcode installed.
Fork this repository.
Verify that the video file is located in the same directory as the PythonWaterDrop.py script.


## References:

- https://developer.apple.com/documentation/accessibility/representing-chart-data-as-an-audio-graph
- https://developer.apple.com/documentation/accessibility/audio-graphs
- https://github.com/pvieito/PythonKit
