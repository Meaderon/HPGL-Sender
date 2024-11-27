HPGL Plotter Sender

(Replace with an actual screenshot if available)

HPGL Plotter Sender is a user-friendly Python application designed to send HPGL (Hewlett-Packard Graphics Language) commands directly to plotters via a serial connection. Whether you're working with traditional pen plotters or modern CNC machines, this tool simplifies the process of transferring and visualizing your HPGL files.
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

git clone https://github.com/yourusername/hpgl-plotter-sender.git
cd hpgl-plotter-sender

Create a Virtual Environment (Optional but Recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies

 you can install dependencies manually:

pip install pyserial

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
