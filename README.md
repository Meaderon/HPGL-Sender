HPGL Plotter Sender

![Screenshot 2024-11-27 141724](https://github.com/user-attachments/assets/19e70523-94cf-4ab3-beba-e39d6f4e9e38)


HPGL Plotter Sender is a user-friendly Python application designed to send HPGL (Hewlett-Packard Graphics Language) commands directly to plotters via a serial connection. 
Whether you're working with traditional pen plotters or modern CNC machines, this tool simplifies the process of transferring and visualizing your HPGL files.
Table of Contents

    Features
    Installation
    Usage
        Generating HPGL Files in Inkscape
    Dependencies
    Contributing
    License
    Acknowledgements

Features

    Load HPGL Files: Easily load .hpgl, .plt, or .hpg files.
    Serial Port Management: Automatically detect and refresh available serial ports.
    Dimension Controls: Set custom dimensions (width and height) with unit selection (mm or inches).
    Uniform Scaling: Maintain aspect ratio while scaling your drawings.
    HPGL Code Preview: View the raw HPGL commands before sending.
    Canvas Visualization: Preview your HPGL drawing within the application.
    Progress Tracking: Monitor the progress of data transmission to the plotter.
    Error Handling: Informative messages for successful operations and error conditions.

Installation

    Clone the Repository

git clone https://github.com/meaderon/HPGL-sender.git


Install Dependencies

1. Python 3.6+

    Description: The application is built using Python, and it's crucial to have Python version 3.6 or higher.
    Installation: Download Python

2. Tkinter

    Description: Tkinter is Python's standard GUI library and is used extensively in your application for creating the user interface.
    Availability:
        Windows: Typically included with Python installations.
        macOS: Included with Python installations.
        Linux: May require separate installation.
    Installation on Linux:

    sudo apt-get update
    sudo apt-get install python3-tk

    Note: If Tkinter is not installed, users may encounter import errors. 
3. PySerial

    Description: PySerial is a Python library that encapsulates the access for the serial port. It's essential for serial communication with the plotter.
    Installation:

    pip install pyserial

    Version Recommendation: While your code doesn't specify a version, it's advisable to use a stable version. You can specify it in your requirements.txt (e.g., pyserial>=3.4).

4. Standard Libraries

    Description: The following Python standard libraries are used and do not require separate installation:
        threading
        re
        time
        tkinter.ttk (part of Tkinter)

Run the Application

    python hpgl_plotter_app.py

Usage

    Load an HPGL File
        Click on the "Load HPGL File" button.
        Select your .hpgl, .plt, or .hpg file from the file dialog.

    Preview the HPGL Code
        Navigate to the "HPGL Code" tab to view the raw commands.
        The "HPGL Drawing" tab displays a visual representation of the loaded file.

    Configure Plotter Settings
        Refresh Ports: Click "Refresh Ports" to update the list of available serial ports.
        Select Serial Port: Choose the appropriate port from the dropdown menu.
        Set Dimensions: Enter the desired width and height. Toggle "Uniform Scaling" to maintain aspect ratio.
        Select Units: Choose between millimeters (mm) and inches.

    Send to Plotter
        Once all settings are configured, click "Send to Plotter".
        Monitor the progress bar for transmission status.
        Upon successful completion, a confirmation message will appear.
