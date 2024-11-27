import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import serial
import serial.tools.list_ports
import threading
import re
import time
import tkinter.ttk as ttk


class HPGLPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HPGL Plotter")
        self.root.geometry("1300x800")

        # Initialize serial port variables
        self.hpgl_commands = ""
        self.serial_port = None
        self.serial_baudrate = 9600  # Default baudrate
        self.unit = "inches"  # Default unit
        self.width = 0  # Width in mm
        self.height = 0  # Height in mm
        self.original_width = 0  # Original width of the drawing
        self.original_height = 0  # Original height of the drawing
        self.uniform_scaling = tk.BooleanVar(value=True)  # Enable uniform scaling by default
        self.scaled_hpgl_commands = ""  # Scaled HPGL commands

        # Create UI components
        self.create_widgets()

        # HPGL data
        self.hpgl_commands = ""

    def create_widgets(self):
        
        
        

        # Frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Load HPGL File Button
        load_button = tk.Button(control_frame, text="Load HPGL File", command=self.load_hpgl_file)
        load_button.pack(side=tk.LEFT, padx=5)

        # Refresh Plotter Ports Button
        refresh_button = tk.Button(control_frame, text="Refresh Ports", command=self.refresh_serial_ports)
        refresh_button.pack(side=tk.LEFT, padx=5)

        # Serial Port Dropdown
        self.port_var = tk.StringVar()
        self.port_dropdown = tk.OptionMenu(control_frame, self.port_var, [])
        self.port_dropdown.pack(side=tk.LEFT, padx=5)
        self.refresh_serial_ports()

        # Dimension Controls
        dim_label = tk.Label(control_frame, text="Width (mm/in):")
        dim_label.pack(side=tk.LEFT, padx=5)
        self.width_var = tk.DoubleVar(value=self.width)
        width_entry = tk.Entry(control_frame, textvariable=self.width_var, width=5)
        width_entry.pack(side=tk.LEFT, padx=5)
        self.width_var.trace("w", self.update_height_from_width)

        height_label = tk.Label(control_frame, text="Height (mm/in):")
        height_label.pack(side=tk.LEFT, padx=5)
        self.height_var = tk.DoubleVar(value=self.height)
        height_entry = tk.Entry(control_frame, textvariable=self.height_var, width=5)
        height_entry.pack(side=tk.LEFT, padx=5)
        self.height_var.trace("w", self.update_width_from_height)

        # Uniform Scaling Checkbox
        uniform_checkbox = tk.Checkbutton(
        control_frame, text="Uniform Scaling", variable=self.uniform_scaling, command=self.toggle_uniform_scaling
        )
        uniform_checkbox.pack(side=tk.LEFT, padx=5)

        # Unit Selection
        unit_label = tk.Label(control_frame, text="Units:")
        unit_label.pack(side=tk.LEFT, padx=5)
        self.unit_var = tk.StringVar(value=self.unit)
        unit_menu = tk.OptionMenu(control_frame, self.unit_var, "mm", "inches", command=self.update_units)
        unit_menu.pack(side=tk.LEFT, padx=5)

        set_dim_button = tk.Button(control_frame, text="Set Dimensions", command=self.set_dimensions)
        set_dim_button.pack(side=tk.LEFT, padx=5)

        

        # Send to Plotter Button
        send_button = tk.Button(control_frame, text="Send to Plotter", command=self.send_to_plotter)
        send_button.pack(side=tk.LEFT, padx=5)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Notebook for Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tab 1: HPGL Drawing
        self.drawing_tab = tk.Frame(self.notebook)
        self.notebook.add(self.drawing_tab, text="HPGL Drawing")

         # Canvas for displaying HPGL
        canvas_frame = tk.Frame(self.drawing_tab, height=500, width=500)  # Constrain canvas size
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Bind resizing event to adjust the canvas dynamically
        self.canvas.bind("<Configure>", self.adjust_canvas_size)

        # Tab 2: HPGL Code Preview
        self.code_tab = tk.Frame(self.notebook)
        self.notebook.add(self.code_tab, text="HPGL Code")

        # ScrolledText widget for HPGL code preview
        self.code_text = scrolledtext.ScrolledText(self.code_tab, wrap=tk.NONE)
        self.code_text.pack(fill=tk.BOTH, expand=True)

    def update_units(self, *args):
        # Conversion factor between mm and inches
        to_mm = 25.4
        to_inches = 1 / 25.4

        # Get the currently selected unit and the previous unit
        new_unit = self.unit_var.get()
        if new_unit == self.unit:
            return  # No change in unit

        # Get current width and height values
        current_width = self.width_var.get()
        current_height = self.height_var.get()

        # Perform conversion
        if new_unit == "mm":
            # Convert from inches to mm
            new_width = current_width * to_mm
            new_height = current_height * to_mm
        elif new_unit == "inches":
            # Convert from mm to inches
            new_width = current_width * to_inches
            new_height = current_height * to_inches
        else:
            return

        # Update the input fields with the converted values
        self.width_var.set(round(new_width, 2))
        self.height_var.set(round(new_height, 2))

        # Update the current unit
        self.unit = new_unit




    def adjust_canvas_size(self, event):
        # Dynamically resize the canvas within the parent frame
        canvas_width = event.width
        canvas_height = event.height

        # Update canvas size limits here if necessary
        max_width = self.root.winfo_width() - 20
        max_height = self.root.winfo_height() - 150

        if canvas_width > max_width:
            canvas_width = max_width
        if canvas_height > max_height:
            canvas_height = max_height

        self.canvas.config(width=canvas_width, height=canvas_height)



    def refresh_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        menu = self.port_dropdown["menu"]
        menu.delete(0, "end")
        for port in port_list:
            menu.add_command(label=port, command=lambda p=port: self.port_var.set(p))
        if port_list:
            self.port_var.set(port_list[0])
        else:
            self.port_var.set("")

    def load_hpgl_file(self):
        file_path = filedialog.askopenfilename(
            title="Select HPGL File",
            filetypes=(("HPGL Files", "*.hpgl *.plt *.hpg"), ("All Files", "*.*"))
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.hpgl_commands = file.read()
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(tk.END, self.hpgl_commands)
                self.calculate_original_size()
                self.update_dimension_fields()  # Update fields with actual size
                self.set_dimensions()
                messagebox.showinfo("Success", f"Loaded HPGL file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def update_dimension_fields(self):
        # Conversion factor between mm and inches
        to_mm = 25.4

        # Get the current unit
        unit = self.unit_var.get()

        # Convert dimensions to the selected unit
        if unit == "mm":
            width = self.original_width * to_mm
            height = self.original_height * to_mm
        else:  # Default to mm
            width = self.original_width
            height = self.original_height

        # Update the input fields
        self.width_var.set(round(width, 2))
        self.height_var.set(round(height, 2))


    def calculate_original_size(self):
        # Calculate the bounding box of the HPGL commands
        commands = re.findall(r'([A-Z]{2})([^A-Z]*)', self.hpgl_commands, re.IGNORECASE)
        all_coords = []
        for cmd, params in commands:
            param_values = list(map(int, re.findall(r'-?\d+', params)))
            for i in range(0, len(param_values), 2):
                if i + 1 < len(param_values):
                    all_coords.append((param_values[i], param_values[i + 1]))

        if not all_coords:
            self.original_width = 0
            self.original_height = 0
            return

        min_x = min(coord[0] for coord in all_coords)
        max_x = max(coord[0] for coord in all_coords)
        min_y = min(coord[1] for coord in all_coords)
        max_y = max(coord[1] for coord in all_coords)

        # Conversion factor: 1 plotter unit = 0.000984 inches
        units_to_inches = 0.025 / 25.4
        self.original_width = (max_x - min_x) * units_to_inches
        self.original_height = (max_y - min_y) * units_to_inches


    def populate_dimension_fields(self):
        self.width_var.set(self.original_width)
        self.height_var.set(self.original_height)

    def show_original_size(self):
        unit_to_mm = 25.4 if self.unit_var.get() == "inches" else 1
        width_in_unit = self.original_width / unit_to_mm
        height_in_unit = self.original_height / unit_to_mm
        unit_label = "inches" if self.unit_var.get() == "inches" else "mm"
        messagebox.showinfo(
            "Original Size",
            f"Original Width: {width_in_unit:.2f} {unit_label}\nOriginal Height: {height_in_unit:.2f} {unit_label}",
        )

    def toggle_uniform_scaling(self):
        # Update the height or width automatically if uniform scaling is enabled
        if self.uniform_scaling.get():
            self.update_height_from_width()
            self.update_width_from_height()

    def update_height_from_width(self, *args):
        if self.uniform_scaling.get() and self.original_width:
            try:
                width = self.width_var.get()
                height = (width / self.original_width) * self.original_height
                self.height_var.set(round(height, 2))
            except tk.TclError:
                pass  # Ignore invalid inputs

    def update_width_from_height(self, *args):
        if self.uniform_scaling.get() and self.original_height:
            try:
                height = self.height_var.get()
                width = (height / self.original_height) * self.original_width
                self.width_var.set(round(width, 2))
            except tk.TclError:
                pass  # Ignore invalid inputs

    def scale_hpgl_commands(self):
        # Apply uniform scaling to HPGL commands
        self.scaled_hpgl_commands = ""
        commands = re.findall(r'([A-Z]{2})([^A-Z]*)', self.hpgl_commands, re.IGNORECASE)
        unit_to_mm = 25.4 if self.unit_var.get() == "inches" else 1
        width_in_mm = self.width_var.get() * unit_to_mm
        height_in_mm = self.height_var.get() * unit_to_mm

        scale_x = width_in_mm / self.original_width if self.original_width else 1.0
        scale_y = height_in_mm / self.original_height if self.original_height else 1.0
        scale = scale_x if self.uniform_scaling.get() else min(scale_x, scale_y)

        for cmd, params in commands:
            if not params.strip():
                self.scaled_hpgl_commands += f"{cmd};"
                continue

            param_values = list(map(int, re.findall(r'-?\d+', params)))
            scaled_values = [
                int(value * scale) for value in param_values
            ]
            scaled_params = ",".join(map(str, scaled_values))
            self.scaled_hpgl_commands += f"{cmd}{scaled_params};"

    def set_dimensions(self):
        try:
            self.width = float(self.width_var.get())
            self.height = float(self.height_var.get())
            if self.width <= 0 or self.height <= 0:
                raise ValueError("Dimensions must be positive.")
            self.unit = self.unit_var.get()
            self.scale_hpgl_commands()  # Apply scaling to the commands
            self.parse_and_draw_hpgl()  # Redraw the scaled commands
        except ValueError:
            messagebox.showerror("Error", "Please enter valid positive dimensions.")

    def parse_and_draw_hpgl(self):
        self.canvas.delete("all")  # Clear previous drawings

        # Extract commands and parameters using regex
        commands = re.findall(r'([A-Z]{2})([^A-Z]*)', self.scaled_hpgl_commands, re.IGNORECASE)

        # Calculate bounding box for the drawing
        all_coords = []
        for cmd, params in commands:
            param_values = list(map(int, re.findall(r'-?\d+', params)))
            for i in range(0, len(param_values), 2):
                if i + 1 < len(param_values):
                    all_coords.append((param_values[i], param_values[i + 1]))

        if not all_coords:
            return  # Nothing to draw

        min_x = min(coord[0] for coord in all_coords)
        max_x = max(coord[0] for coord in all_coords)
        min_y = min(coord[1] for coord in all_coords)
        max_y = max(coord[1] for coord in all_coords)

        drawing_width = max_x - min_x
        drawing_height = max_y - min_y

        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate scale to fit drawing into canvas
        scale_x = canvas_width / drawing_width
        scale_y = canvas_height / drawing_height
        scale = min(scale_x, scale_y)  # Maintain aspect ratio

        # Calculate offsets to center the drawing
        offset_x = (canvas_width - (drawing_width * scale)) / 2
        offset_y = (canvas_height - (drawing_height * scale)) / 2

        # Adjust all coordinates using scale and offset
        pen_up = True
        current_pos = (0, 0)

        for cmd, params in commands:
            cmd = cmd.upper()
            params = params.strip().rstrip(';')  # Remove trailing semicolon

            if not params:
                continue

            param_values = list(map(int, re.findall(r'-?\d+', params)))

            if cmd == 'PU':  # Pen Up
                pen_up = True
                if len(param_values) >= 2:
                    x, y = param_values[:2]
                    current_pos = self.transform_coordinates(x, y, scale, offset_x, offset_y, min_x, min_y)
            elif cmd == 'PD':  # Pen Down
                pen_up = False
                points = [
                    self.transform_coordinates(param_values[i], param_values[i + 1], scale, offset_x, offset_y, min_x, min_y)
                    for i in range(0, len(param_values), 2)
                    if i + 1 < len(param_values)
                ]
                if points:
                    self.draw_hpgl_lines(current_pos, points)
                    current_pos = points[-1]

    def transform_coordinates(self, x, y, scale, offset_x, offset_y, min_x, min_y):
        # Scale and offset HPGL coordinates to fit canvas
        x = (x - min_x) * scale + offset_x
        # Flip Y-axis by subtracting scaled Y-coordinate from canvas height
        y = self.canvas.winfo_height() - ((y - min_y) * scale + offset_y)
        return x, y


    def draw_hpgl_lines(self, start_pos, points):
        # Draw scaled and transformed lines on the canvas
        for end_pos in points:
            self.canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], fill="black", width=2)
            start_pos = end_pos


    def send_to_plotter(self):
        if not self.hpgl_commands:
            messagebox.showwarning("No Data", "Please load an HPGL file first.")
            return

        port = self.port_var.get()
        if not port:
            messagebox.showwarning("No Port", "Please select a serial port.")
            return

        # Reset progress bar
        self.progress_var.set(0)
        self.progress_bar.update()

        # Send HPGL commands in a separate thread to avoid blocking the GUI
        threading.Thread(target=self._send_serial, args=(port, self.scaled_hpgl_commands), daemon=True).start()

    def _send_serial(self, port, data):
        try:
            with serial.Serial(port, self.serial_baudrate, timeout=1) as ser:
                # Clear buffers
                ser.reset_input_buffer()
                ser.reset_output_buffer()

                # Send data in chunks
                total_length = len(data)
                chunk_size = 1024
                sent_length = 0
                for i in range(0, total_length, chunk_size):
                    chunk = data[i:i + chunk_size]
                    ser.write(chunk.encode('ascii'))
                    ser.flush()
                    sent_length += len(chunk)
                    progress = (sent_length / total_length) * 100
                    self.progress_var.set(progress)
                    self.progress_bar.update()

                time.sleep(2)
                ser.write(b"IN;\n")  # Reset plotter
                ser.flush()

            self.progress_var.set(100)
            self.progress_bar.update()
            messagebox.showinfo("Success", f"Data sent to plotter on {port}")

        except serial.SerialException as e:
            messagebox.showerror("Serial Error", f"Failed to send data:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
        finally:
            self.progress_var.set(0)  # Reset progress bar


def main():
    root = tk.Tk()
    app = HPGLPlotterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()