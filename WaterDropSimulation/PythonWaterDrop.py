# python script that takes droplet video as input and processes it to model motion.
# outputs a csv file with data to be plotted in Swift
# run from ContentView.swift with the use of PythonKit's interoperability support

import sys
import cv2
import numpy as np
import csv
import matplotlib.pyplot as plt #comment out after initial analysis
from scipy.optimize import curve_fit


def exponential_decay(t, a, b, c):
    return a * np.exp(-b * t) + c
    
    
def analyze_water_drop(video_path, output_csv):
    try:
        # Opens the video file
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # print("fps = ", fps) # 30 fps
        
        # Lists to store data from frame processing
        frames = []
        time_points = []
        distances = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Converted to grayscale for ease of analysis
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Used Thresholding (image processing technique) to identify the droplet
            _, threshold = cv2.threshold(gray_frame, 50, 255, cv2.THRESH_BINARY)

            # Find contours
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Bounding rectangle of largest contour is considered the droplet's position
                max_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(max_contour)

                # Store data
                frames.append(frame)
                time_points.append(len(frames) / fps)
                distances.append(y + h / 2)  # droplet center is used as its position

        cap.release() # frame processing over

        # Calculate velocity and acceleration using numpy
        velocities = np.gradient(distances, time_points)
        accelerations = np.gradient(velocities, time_points)

        # Fit exponential decay curve (for distance)
        popt, _ = curve_fit(exponential_decay, time_points, distances)

        # Save data to CSV for data transfer to swiftUI and interoperability
        with open(output_csv, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Time', 'Distance', 'Velocity', 'Acceleration', 'FittedCurve'])
            for t, d, v, a in zip(time_points, distances, velocities, accelerations):
                fitted_curve = exponential_decay(t, *popt) # fitted_curve is the fitted distance
                writer.writerow([t, d, v, a, fitted_curve])
        
        
        # # Visualization and fit assessment -> COMMENT OUT
        
        # plt.figure(figsize=(8, 6))
        # plt.plot(time_points, distances, 'o', label='Actual Distance')  # Plot actual data points

        # # Calculate fitted curve using optimized parameters
        # fitted_curve = [popt[0] * np.exp(-popt[1] * t) + popt[2] for t in time_points]
        # # Plot fitted curve
        # plt.plot(time_points, fitted_curve, label='Fitted Curve')

        # plt.xlabel('Time (s)')
        # plt.ylabel('Distance (pixels)')
        # plt.title('Fitted Curve vs. Time')
        # plt.legend()
        # plt.grid(True)
        # plt.show()
        
        # # DEBUG process: Checking which data length needs adjustment: all are 37.
        # print("distances array length: ", len(distances))
        # print("time points array length: ", len(time_points))
        # print("velocity array length: ", len(velocities))
        # print("acceleration array length: ", len(accelerations))
        
        # plt.figure(figsize=(12, 6)) # leave out figsize and see what it looks like
        
        # # Plotting velocity vs time - needs y axis range adjustment
        # plt.subplot(3, 1, 1)  # Create subplot in a 3x1 grid (middle row)
        # plt.plot(time_points, velocities, label='Velocity')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Velocity (pixels/s)')
        # plt.title('Droplet Velocity over Time')

        # # Plotting acceleration vs time - needs y axis range adjustment
        # plt.subplot(3, 1, 3)  # Create subplot in a 3x1 grid (bottom row)
        # plt.plot(time_points, accelerations, label='Acceleration')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Acceleration (pixels/sÂ²)')
        # plt.title('Droplet Acceleration over Time')

        # #plt.tight.layout() #layout adjustment
        # plt.show()
        
        return True  # Indicate success
        
    except Exception as e:
        print(e)  # Optionally log the exception to the console or a log file
        return False  # Indicate failure
        

if __name__ == "__main__":
    video_path = "droplet_video.mp4" # relative path; assumes video is in the same directory as this script
    output_csv = "droplet_data.csv"
    analyze_water_drop(video_path, output_csv)
