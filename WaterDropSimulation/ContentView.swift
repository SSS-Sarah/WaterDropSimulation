//
//  ContentView.swift
//  WaterDropSimulation
//
//
import Foundation
import SwiftUI
import PythonKit
import Charts

// Load Python functions
let python = Python.import("PythonWaterDrop")  // Name of Python file

struct ContentView: View {
    // State variables
    @State private var dataPoints: [DataPoint] = []
    @State private var isDataLoaded = false
    @State private var error: String?

    var body: some View {
        VStack(spacing: 20) {
            
            if let error = error {
                Text(error)
                    .accessibilityLabel("Error: \(error)") // AX support
                
            } else if isDataLoaded {
                // Display fittedCurve against time chart
                Chart(dataPoints) { dataPoint in
                    LineMark(
                        x: .value("Time", dataPoint.time),
                        y: .value("Fitted Curve", dataPoint.fittedCurve)
                    )
                }
    
                // descriptive AX elements
                .accessibilityElement(children: .contain)
                .accessibilityLabel("Water Drop Analysis Graph")
                .accessibilityValue("The chart displays an exponential decay curve showing a decrease in the rate of change over time. The distance changes rapidly and then stabilizes over time.")

                
                .chartXAxis {
                    AxisMarks(preset: .extended, position: .bottom)
                }
                .chartYAxis {
                    AxisMarks(preset: .extended, position: .leading)
                }
                
                Button("End Program") {
                // Quits the program
                    NSApplication.shared.terminate(nil)
                }
                .accessibilityLabel("End program")
                .accessibilityHint("Closes the application.")
                
            } else {
                Text("Loading Data...")
                    .accessibilityLabel("Loading data")
            }
            Button("Analyze Water Drop") {
                Task {
                    await processData()
                }
            }
            .accessibilityLabel("Analyze water drop")
            .accessibilityHint("Models a water droplet's motion as it hits a surface and displays the results in a graph.")
        }
        .padding()
    }

    
    func processData() async {
        
        let result = python.analyze_water_drop("droplet_video.mp4", "droplet_data.csv")
        let success = Bool(Python.bool(result))!
        
        if !success {
            // error handling if false
            self.error = "Error processing video with Python."
        } else {
            do {
                // If there's no error, proceed to load data from CSV
                try loadCSVData()
                self.isDataLoaded = true
            } catch {
                // Handle errors from loading CSV data
                self.error = "Error processing data: \(error.localizedDescription)"
            }
        }
    }

    // loads the relevant csv data into
    func loadCSVData() throws {
        
        let csvPath = FileManager.default.currentDirectoryPath + "/droplet_data.csv"
        let csvData = try String(contentsOfFile: csvPath, encoding: .utf8)
        let rows = csvData.components(separatedBy: "\n")

        var loadedDataPoints: [DataPoint] = []
        for row in rows.dropFirst() {  // Skips header row
            let columns = row.components(separatedBy: ",")
            
            //Time = first columns, fittedCurve = last column
            if columns.count == 5, let time = Double(columns[0]), let fittedCurve = Double(columns[4]) {
                loadedDataPoints.append(DataPoint(time: time, fittedCurve: fittedCurve))
            }
        }
        self.dataPoints = loadedDataPoints
    }
}

// Data model for the chart
struct DataPoint: Identifiable {
    let id = UUID()
    let time: Double
    let fittedCurve: Double
}


#Preview {
    ContentView()
}
