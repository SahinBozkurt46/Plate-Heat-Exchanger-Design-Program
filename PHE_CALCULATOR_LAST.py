


## Sahin Bozkurt , Summer Intern at Alfa Laval Turkiye

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import threading
import time



class OpeningInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Opening Interface")
        
        # Load and display an image
        self.load_and_display_image()
        self.load_and_display_gif()
        
        
        

    def load_and_display_image(self):
        try:
            
            
            image = Image.open("alfalaval.jpg")
            image = image.resize((500, 350), Image.ANTIALIAS)
            
            # Convert the image to a PhotoImage object (Tkinter-compatible)
            self.photo = ImageTk.PhotoImage(image)

            # Create a label to display the image
            
            image_label = ttk.Label(self.root, image=self.photo)
            image_label.pack()
            # Add a title label
            title_label = ttk.Label(self.root, text="Welcome to GPE Designer!", font=("Helvetica", 24))
            title_label.pack(pady=20)
           

        except Exception as e:
            print(f"Error loading image: {e}")
        
        self.root.after(5000, self.open_main_gui)
      
    def load_and_display_gif(self):
        try:
            
            gif = Image.open("openinggif.gif")

            # Convert the GIF frames to PhotoImage objects (Tkinter-compatible)
            self.gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

            # Create a label to display the GIF
            gif_label = ttk.Label(self.root)
            gif_label.pack()

            # Display the first frame of the GIF
            gif_label.configure(image=self.gif_frames[0])

            # Schedule the update of the GIF frames to create animation
            self.update_gif_frame(gif_label, frame_index=1)

        except Exception as e:
            print(f"Error loading GIF: {e}")

    def update_gif_frame(self, label, frame_index):
        try:
            # Display the next frame
            label.configure(image=self.gif_frames[frame_index])

            # Schedule the update of the next frame 
            delay = 100  # Delay in milliseconds
            frame_index = (frame_index + 1) % len(self.gif_frames)
            self.root.after(delay, self.update_gif_frame, label, frame_index)
        except Exception as e:
            print(f"Error updating GIF frame: {e}")

    def open_main_gui(self):
        # Close the opening interface
        self.root.destroy()

        # Open the main GUI
        main_root = tk.Tk()
        app = PlateHeatExchangerApp(main_root)
        main_root.mainloop()
        

class PlateHeatExchangerApp:
    def __init__(self, root):
        self.use_checkboxes = {}
        self.root = root
        self.root.title("Gasketed Plate Heat Exchanger Calculator")

        self.create_hot_properties_widgets_section()
        self.create_cold_properties_widgets_section()
        self.create_plate_properties_widgets_section()
        self.create_result_section()
       
   
    def create_hot_properties_widgets_section(self):
        hot_frame = ttk.LabelFrame(self.root, text="Hot Side Properties")
        hot_frame.grid(row=0, column=0, padx=10, pady=10)
        self.create_use_buttons(hot_frame, ["hot_flow_rate", "hot_inlet_temp", "hot_outlet_temp"])
        self.hot_properties_widgets = {
        "Plate Flow Rate (Hot) (kg/s)": "hot_flow_rate",
        "Inlet Temperature (°C)": "hot_inlet_temp",
        "Outlet Temperature (°C)": "hot_outlet_temp",
        "Specific Heat Capacity (J/kg·°C)": "hot_cp",
        "Thermal Conductivity (W/m·°C)": "hot_conductivity",
        "Viscosity (kg/m·s)": "hot_viscosity",
        "Density (kg/m³)": "hot_density",
        "Prandl Number": "hot_prandl",
        "Fouling Factor": "hot_fouling",
            
           
        }
        self.create_properties_widgets(hot_frame, self.hot_properties_widgets)

    def create_cold_properties_widgets_section(self):
        cold_frame = ttk.LabelFrame(self.root, text="Cold Side Properties")
        cold_frame.grid(row=0, column=1, padx=10, pady=10)
        self.create_use_buttons(cold_frame, ["cold_flow_rate", "cold_inlet_temp", "cold_outlet_temp"])
        self.cold_properties_widgets = {
        "Plate Flow Rate (Cold) (kg/s)": "cold_flow_rate",
        "Inlet Temperature (°C)": "cold_inlet_temp",
        "Outlet Temperature (°C)": "cold_outlet_temp",
        "Specific Heat Capacity (J/kg·°C)": "cold_cp",
        "Thermal Conductivity (W/m·°C)": "cold_conductivity",
        "Viscosity (kg/m·s)": "cold_viscosity",
        "Density (kg/m³)": "cold_density",
        "Prandl Number": "cold_prandl",
        "Fouling Factor": "cold_fouling",
            
           
        }
        self.create_properties_widgets(cold_frame, self.cold_properties_widgets)

    def create_plate_properties_widgets_section(self):
        plate_frame = ttk.LabelFrame(self.root, text="Plate  Properties")
        plate_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.plate_properties_widgets = {
        "Plate Width (m)": "plate_width",
        "Plate Length (m)": "plate_length",
        "Plate Thickness (m)": "plate_thickness",
        "Thermal Conductivity of Plates (W/m·°C)": "plate_conductivity",
        "Port Diameter of Plates (m)": "port_diameter",
        "Angles of Plates (°)": "plate_angles",
        "Number of Plates": "number_of_plates",
            
        }
        self.create_properties_widgets(plate_frame, self.plate_properties_widgets)

    def create_properties_widgets(self, parent, properties_widgets):
        row_counter = 0
        self.selected_variables = []

        for label_text, widget_name in properties_widgets.items():
            label = ttk.Label(parent, text=label_text)
            label.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
            
            setattr(self, f"{widget_name}_entry", ttk.Entry(parent))
            getattr(self, f"{widget_name}_entry").grid(row=row_counter, column=1, padx=5, pady=5)
            
            if widget_name in ["hot_flow_rate", "cold_flow_rate", "hot_inlet_temp", "cold_inlet_temp", "hot_outlet_temp", "cold_outlet_temp"]:
                checkbox = ttk.Checkbutton(parent, text="Use", command=lambda wn=widget_name: self.toggle_variable(wn))
                checkbox.grid(row=row_counter, column=2, padx=5, pady=5, sticky="w")
                self.selected_variables.append(widget_name)
            
            row_counter += 1
 
    def create_use_buttons(self, parent, variable_names):
        for widget_name in variable_names:
            checkbox = ttk.Checkbutton(parent, text="Use", command=lambda wn=widget_name: self.toggle_variable(wn))
            checkbox.grid(row=variable_names.index(widget_name), column=2, padx=5, pady=5, sticky="w")
            self.use_checkboxes[widget_name] = checkbox  # Store the checkbox reference

    def toggle_variable(self, widget_name):
          #if len(self.selected_variables) > 4:
           #   return  # Limit selection to 5 variables
          if widget_name in self.selected_variables:
              self.selected_variables.remove(widget_name)
          else:
              self.selected_variables.append(widget_name)
          return  widget_name  

    def calculate(self):
        # Get data from GUI elements
        self.hot_properties_widgets["hot_flow_rate"] = 0
        self.hot_properties_widgets["hot_inlet_temp"] = 0
        self.hot_properties_widgets["hot_outlet_temp"] = 0
        self.hot_properties_widgets["hot_conductivity"]= 0
        self.hot_properties_widgets["hot_cp"]= 0
        self.hot_properties_widgets["hot_density"]= 0
        self.hot_properties_widgets["hot_fouling"]= 0
        self.hot_properties_widgets["hot_viscosity"]= 0
        self.hot_properties_widgets["hot_prandl"]= 0
      
        self.cold_properties_widgets["cold_flow_rate"] = 0
        self.cold_properties_widgets["cold_inlet_temp"] = 0
        self.cold_properties_widgets["cold_outlet_temp"] = 0
        self.cold_properties_widgets["cold_conductivity"]= 0
        self.cold_properties_widgets["cold_cp"]= 0
        self.cold_properties_widgets["cold_density"]=0
        self.cold_properties_widgets["cold_fouling"]= 0
        self.cold_properties_widgets["cold_viscosity"]= 0
        self.cold_properties_widgets["cold_prandl"]= 0
      
        self.plate_properties_widgets["plate_width"] = 0
        self.plate_properties_widgets["plate_length"] = 0
        self.plate_properties_widgets["plate_thickness"] = 0
        self.plate_properties_widgets["plate_conductivity"] = 0
        self.plate_properties_widgets["port_diameter"] = 0
        self.plate_properties_widgets["plate_angles"] = 0 
        self.plate_properties_widgets["number_of_plates"]=0
        
       
        try:
            self.hot_properties_widgets["hot_flow_rate"] = float(self.hot_flow_rate_entry.get())
        except ValueError:
            self.hot_properties_widgets["hot_flow_rate"] = 0

        try:
                self.cold_properties_widgets["cold_outlet_temp"] = float(self.cold_outlet_temp_entry.get())
        except ValueError:
                self.cold_properties_widgets["cold_outlet_temp"] = 0
        try:
            self.hot_properties_widgets["cold_flow_rate"] = float(self.cold_flow_rate_entry.get())
        except ValueError:
            self.hot_properties_widgets["cold_flow_rate"] = 0

        try:
                self.cold_properties_widgets["cold_inlet_temp"] = float(self.cold_inlet_temp_entry.get())
        except ValueError:
                self.cold_properties_widgets["cold_inlet_temp"] = 0
        try:
            self.hot_properties_widgets["hot_inlet_temp"] = float(self.hot_inlet_temp_entry.get())
        except ValueError:
            self.hot_properties_widgets["hot_inlet_temp"] = 0

        try:
                self.cold_properties_widgets["hot_outlet_temp"] = float(self.hot_outlet_temp_entry.get())
        except ValueError:
                self.cold_properties_widgets["hot_outlet_temp"] = 0
        
        
        self.hot_properties_widgets["hot_conductivity"]=float(self.hot_conductivity_entry.get())
        self.hot_properties_widgets["hot_cp"]=float(self.hot_cp_entry.get())
        self.hot_properties_widgets["hot_density"]=float(self.hot_density_entry.get())
        self.hot_properties_widgets["hot_fouling"]= float(self.hot_fouling_entry.get())
        self.hot_properties_widgets["hot_viscosity"]= float(self.hot_viscosity_entry.get())
        self.hot_properties_widgets["hot_prandl"]= float(self.hot_prandl_entry.get())
        

       
        self.cold_properties_widgets["cold_conductivity"]=float(self.cold_conductivity_entry.get())
        self.cold_properties_widgets["cold_cp"]=float(self.cold_cp_entry.get())
        self.cold_properties_widgets["cold_density"]=float(self.cold_density_entry.get())
        self.cold_properties_widgets["cold_fouling"]= float(self.cold_fouling_entry.get())
        self.cold_properties_widgets["cold_viscosity"]= float(self.cold_viscosity_entry.get())
        self.hot_properties_widgets["hot_prandl"]= float(self.cold_prandl_entry.get())

        
        self.plate_properties_widgets["plate_width"] = float(self.plate_width_entry.get())
        self.plate_properties_widgets["plate_length"] = float(self.plate_length_entry.get())
        self.plate_properties_widgets["plate_thickness"] = float(self.plate_thickness_entry.get())
        self.plate_properties_widgets["plate_conductivity"] = float(self.plate_conductivity_entry.get())
        self.plate_properties_widgets["port_diameter"] = float(self.port_diameter_entry.get())
        self.plate_properties_widgets["plate_angles"] = float(self.plate_angles_entry.get())
        self.plate_properties_widgets["number_of_plates"] = float(self.number_of_plates_entry.get())

        
            
            
        # Determine the missing variable and calculate it if selected
        missing_variable = self.determine_missing_variable(self.hot_properties_widgets, self.cold_properties_widgets)
        missing_variable=self.calculate_missing_variable(self.hot_properties_widgets, self.cold_properties_widgets,self.plate_properties_widgets, missing_variable)
        
        # Perform calculations
        heat_load = self.calculate_heat_load(self.hot_properties_widgets, self.cold_properties_widgets)

        # Recalculate other values with the updated heat_load
        surface_area = self.calculate_surface_area(self.plate_properties_widgets)
        compressed_plate_pack_length = self.calculate_compressed_plate_pack_length(self.plate_properties_widgets)
        pressure_drop = self.calculate_pressure_drop(self.hot_properties_widgets, self.cold_properties_widgets, self.plate_properties_widgets)


        result_root = tk.Toplevel(self.root)
        result_root.title("Results")
        result_app = ResultInterface(result_root, heat_load, surface_area, compressed_plate_pack_length, pressure_drop)
        
        # Display results
        self.display_results(heat_load, surface_area, compressed_plate_pack_length, pressure_drop)


    def determine_missing_variable(self, hot_properties_widgets, cold_properties_widgets):
        missing_variable = None

        # Create a dictionary to map variable names to their values
        variable_values = {
            "hot_flow_rate": hot_properties_widgets["hot_flow_rate"],
            "cold_flow_rate": cold_properties_widgets["cold_flow_rate"],
            "hot_inlet_temp": hot_properties_widgets["hot_inlet_temp"],
            "cold_inlet_temp": cold_properties_widgets["cold_inlet_temp"],
            "hot_outlet_temp": hot_properties_widgets["hot_outlet_temp"],
            "cold_outlet_temp": cold_properties_widgets["cold_outlet_temp"],
            }   

        for var in self.selected_variables:
            if var not in hot_properties_widgets or var not in cold_properties_widgets:
                missing_variable = var
                break
            elif variable_values[var] == 0:
                missing_variable = var
                break

        return missing_variable


    
    def calculate_missing_variable(self, hot_properties_widgets, cold_properties_widgets,plate_properties_widgets, missing_variable):
    
    
        if missing_variable == "hot_inlet_temp":
            hot_properties_widgets["hot_inlet_temp"] = (float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp")) * float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp"))) / (float(hot_properties_widgets.get("hot_flow_rate")) * float(hot_properties_widgets.get("hot_cp")) * float(hot_properties_widgets.get("hot_density")) + float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp")))
            return missing_variable
        elif missing_variable == "cold_inlet_temp":
            cold_properties_widgets["cold_inlet_temp"] = (float(hot_properties_widgets.get("hot_flow_rate")) * float(hot_properties_widgets.get("hot_cp")) * float(hot_properties_widgets.get("hot_density")) * float(hot_properties_widgets.get("hot_outlet_temp")) - float(hot_properties_widgets.get("hot_inlet_temp"))) / (float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp")) + float(hot_properties_widgets.get("hot_flow_rate")) * float(hot_properties_widgets.get("hot_cp")) * float(hot_properties_widgets.get("hot_density")))
            return missing_variable
        elif missing_variable == "hot_outlet_temp":
            hot_properties_widgets["hot_outlet_temp"] = (float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp")) * float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp"))) / (float(hot_properties_widgets.get("hot_flow_rate")) * float(hot_properties_widgets.get("hot_cp")) * float(hot_properties_widgets.get("hot_density")) - float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp")))
            return missing_variable
        elif missing_variable == "cold_outlet_temp":
            cold_properties_widgets["cold_outlet_temp"] = (float(hot_properties_widgets.get("hot_flow_rate")) * float(hot_properties_widgets.get("hot_cp")) * float(hot_properties_widgets.get("hot_density")) * float(hot_properties_widgets.get("hot_outlet_temp")) - float(hot_properties_widgets.get("hot_inlet_temp"))) / (float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp")) - float(hot_properties_widgets.get("hot_flow_rate")) * float(hot_properties_widgets.get("hot_cp")) * float(hot_properties_widgets.get("hot_density")))
            return missing_variable
        elif missing_variable == "hot_flow_rate":
            hot_properties_widgets["hot_flow_rate"] = (float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp")) * float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp"))) / (float(hot_properties_widgets.get("hot_outlet_temp")) - float(hot_properties_widgets.get("hot_inlet_temp")) * float(hot_properties_widgets.get("hot_density")))
            return missing_variable
        elif missing_variable == "cold_flow_rate":
            cold_properties_widgets["cold_flow_rate"] = (float(hot_properties_widgets.get("hot_flow_rate")) * float(hot_properties_widgets.get("hot_cp")) * float(hot_properties_widgets.get("hot_density")) * float(hot_properties_widgets.get("hot_outlet_temp")) - float(hot_properties_widgets.get("hot_inlet_temp"))) / (float(cold_properties_widgets.get("cold_outlet_temp")) - float(cold_properties_widgets.get("cold_inlet_temp")) * float(cold_properties_widgets.get("cold_density")))
            return missing_variable
        return missing_variable
   
    def calculate_heat_load(self, hot_properties_widgets, cold_properties_widgets):
        hot_flow_rate = hot_properties_widgets["hot_flow_rate"]
        cold_flow_rate = cold_properties_widgets["cold_flow_rate"]
        hot_inlet_temp = hot_properties_widgets["hot_inlet_temp"]
        hot_outlet_temp = hot_properties_widgets["hot_outlet_temp"]
        cold_inlet_temp = cold_properties_widgets["cold_inlet_temp"]
        cold_outlet_temp = cold_properties_widgets["cold_outlet_temp"]
        heat_load = hot_flow_rate * hot_properties_widgets["hot_cp"] * hot_properties_widgets["hot_density"] * (hot_outlet_temp - hot_inlet_temp) +cold_flow_rate * cold_properties_widgets["cold_cp"] * cold_properties_widgets["cold_density"] * (cold_outlet_temp - cold_inlet_temp)
        return heat_load

    def calculate_surface_area(self,plate_properties_widgets):
        plate_width = plate_properties_widgets["plate_width"]
        plate_length = plate_properties_widgets["plate_length"]
        surface_area = plate_width * plate_length * plate_properties_widgets["number_of_plates"]
        return surface_area


    def calculate_compressed_plate_pack_length(self,plate_properties_widgets):
        uncompressed_length = 0.06  # meters (example)
        compression_ratio = 0.9  # ratio (example)
        compressed_length = uncompressed_length * compression_ratio * plate_properties_widgets["number_of_plates"]
        return compressed_length

    def calculate_pressure_drop(self, hot_properties_widgets, cold_properties_widgets, plate_properties_widgets):
        # Get relevant properties
        hot_flow_rate = hot_properties_widgets["hot_flow_rate"]
        cold_flow_rate = cold_properties_widgets["cold_flow_rate"]
        plate_width = plate_properties_widgets["plate_width"]
        plate_length = plate_properties_widgets["plate_length"]
        channel_height = 0.002  # Example channel height in meters

        # Calculate velocity in the channel
        hot_velocity = hot_flow_rate / (plate_width * channel_height)
        cold_velocity = cold_flow_rate / (plate_width * channel_height)

        # Calculate pressure drop using a simplified formula (you may use a more accurate formula)
        pressure_drop = 0.5 * (hot_velocity ** 2 - cold_velocity ** 2) * 1e-5  # Example formula, adjust as needed
        
        return pressure_drop


    #def create_calculate_sixth_variable_button(self):
     #  calculate_sixth_button = ttk.Button(self.root, text="Calculate Sixth Variable", command=self.calculate_missing_variable)
     # calculate_sixth_button.grid(row=3, column=0, columnspan=2, pady=5)

   
  
    def create_result_section(self):
       calculate_button = ttk.Button(self.root, text="Calculate", command=self.calculate)
       calculate_button.grid(row=2, column=0, columnspan=2, pady=10)
       
      # calculate_sixth_button = ttk.Button(self.root, text="Calculate Sixth Variable", command=self.calculate_missing_variable)
      #calculate_sixth_button.grid(row=3, column=0, columnspan=2, pady=5)

       self.result_text = tk.StringVar()
       self.result_label = ttk.Label(self.root, textvariable=self.result_text)
       self.result_label.grid(row=4, column=0, columnspan=2)
       


class ResultInterface:
    def __init__(self, root, heat_load, surface_area, compressed_plate_pack_length, pressure_drop):
        self.root = root

        # Load and display an animated GIF
        self.load_and_display_gif()

        # Display results
        self.display_results(heat_load, surface_area, compressed_plate_pack_length, pressure_drop)

    def load_and_display_gif(self):
        try:
            # Open the animated GIF using Pillow
            gif = Image.open("maingif.gif")

            # Convert the GIF frames to PhotoImage objects (Tkinter-compatible)
            self.gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

            # Create a label to display the GIF
            gif_label = ttk.Label(self.root)
            gif_label.pack()

            # Display the first frame of the GIF
            gif_label.configure(image=self.gif_frames[0])

            # Schedule the update of the GIF frames to create animation
            self.update_gif_frame(gif_label, frame_index=1)

        except Exception as e:
            print(f"Error loading GIF: {e}")

   
    def update_gif_frame(self, label, frame_index):
        try:
            # Display the next frame
            label.configure(image=self.gif_frames[frame_index])

            # Schedule the update of the next frame (adjust delay time as needed)
            delay = 100  # Delay in milliseconds
            frame_index = (frame_index + 1) % len(self.gif_frames)
            self.root.after(delay, self.update_gif_frame, label, frame_index)
        except Exception as e:
            print(f"Error updating GIF frame: {e}")

    
    def display_results(self, heat_load, surface_area, compressed_plate_pack_length, pressure_drop):
        result_text = (
            f"Total Heat Transfer: {heat_load:.2f} kW\n"
            f"Total Surface Area: {surface_area:.2f} m²\n"
            f"Compressed Plate Pack Length: {compressed_plate_pack_length:.2f} m\n"
            f"Pressure Drop: {pressure_drop:.2f} bar"
            #f"Missing Variable: {missing_variable:.2f} "
        )

        result_label = ttk.Label(self.root, text=result_text,font=("Helvetica", 16))
        result_label.pack()


        
def main():
    root = tk.Tk()
    opening_app = OpeningInterface(root)
    root.mainloop()
    


if __name__ == "__main__":
    main()