import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from geopy.geocoders import Nominatim
from meteostat import Point, Hourly, Daily, Monthly, Normals
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import DateEntry
from datetime import time

class WeatherScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("M.E.T.E.O.R")
        self.root.geometry("1000x700")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.icon = tk.PhotoImage(file="./assets/ndmaLogo.png")
        root.iconphoto(False, self.icon)
        

        
        # Configure colors and fonts
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.font = ('Helvetica', 12, 'bold')
        
        # Header Frame
        self.header_frame = ttk.Frame(root)
        self.header_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        
        # Add clock frame at the top
        #self.clock_frame = ttk.Frame(root)
        #self.clock_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
                # Clock
        #self.clock_label = tk.Label(self.header_frame, 
                                  #font=("Helvetica", 24), 
                                  #fg="green")
        #self.clock_label.pack()
        
        # Subtitle
        self.subtitle_label = ttk.Label(self.header_frame,
                                      text="Meteorological Environment Tracking, Extraction, and Observation Resource",
                                      font=("Helvetica", 14, "bold"),
                                      foreground="#2c3e50")
        self.subtitle_label.pack(pady=5)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Rest of your existing GUI elements
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        #self.root.rowconfigure(0, weight=1)
        #self.root.columnconfigure(0, weight=1)
        #self.root.after(1000, self.update_clock)
        
        self.create_widgets()
        self.data = None
        

        

        

        


    def update_clock(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Location Input Section
        loc_frame = ttk.LabelFrame(main_frame, text=" Location Information ", padding=10)
        loc_frame.grid(row=0, column=0, sticky="ew", pady=5)
        
        ttk.Label(loc_frame, text="Location Name:").grid(row=0, column=0, sticky="w")
        self.location_entry = ttk.Entry(loc_frame, width=30)
        self.location_entry.grid(row=0, column=1, padx=5)
        
        ttk.Button(loc_frame, text="Search", command=self.geocode_location, 
                  style="Accent.TButton").grid(row=0, column=2, padx=5)
        
        ttk.Label(loc_frame, text="Latitude:").grid(row=1, column=0, sticky="w", pady=5)
        self.lat_entry = ttk.Entry(loc_frame, width=15)
        self.lat_entry.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Label(loc_frame, text="Longitude:").grid(row=2, column=0, sticky="w")
        self.lon_entry = ttk.Entry(loc_frame, width=15)
        self.lon_entry.grid(row=2, column=1, sticky="w", padx=5)
        
        # Data Type Selection
        data_frame = ttk.LabelFrame(main_frame, text=" Data Selection ", padding=10)
        data_frame.grid(row=1, column=0, sticky="ew", pady=5)
        
        self.data_type = tk.StringVar(value="current")
        ttk.Radiobutton(data_frame, text="Current Weather", variable=self.data_type,
                       value="current", command=self.toggle_controls).pack(anchor="w")
        ttk.Radiobutton(data_frame, text="Historical Data", variable=self.data_type,
                       value="historical", command=self.toggle_controls).pack(anchor="w")
        
        # Frequency Selection
        self.frequency_frame = ttk.Frame(data_frame)
        ttk.Label(self.frequency_frame, text="Data Frequency:").pack(side=tk.LEFT, padx=5)
        self.frequency = ttk.Combobox(self.frequency_frame, 
                                    values=["Hourly", "Daily", "Monthly", "Climate Normals"],
                                    state="readonly", width=15)
        self.frequency.pack(side=tk.LEFT)
        self.frequency.set("Daily")
        
        # Date Range Section
        self.date_frame = ttk.Frame(data_frame)
        self.create_date_fields("Daily")  # Initialize with default frequency
        
        # Action Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, pady=15)
        
        ttk.Button(btn_frame, text="Fetch Weather Data", 
                  command=self.fetch_data, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export Data", 
                  command=self.export_data).pack(side=tk.LEFT, padx=5)
        
        # Visualization Section
        viz_frame = ttk.LabelFrame(main_frame, text=" Data Visualization ", padding=10)
        viz_frame.grid(row=4, column=0, sticky="ew", pady=10)
        
        ttk.Button(viz_frame, text="Show Data Preview", 
                  command=self.show_data_preview).pack(side=tk.LEFT, padx=5)
        
        self.plot_var = tk.StringVar()
        ttk.Combobox(viz_frame, textvariable=self.plot_var, 
                    values=["Temperature", "Precipitation", "Wind Speed", "All Variables"],
                    state="readonly", width=15).pack(side=tk.LEFT, padx=5)
        self.plot_var.set("Temperature")
        
        ttk.Button(viz_frame, text="Plot Data", 
                  command=self.plot_data).pack(side=tk.LEFT, padx=5)
        
        # Visualization canvas
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().grid(row=5, column=0, sticky="nsew", pady=10)
        
        # Configure grid weights for proper resizing
        main_frame.rowconfigure(5, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Configure styles
        self.style.configure('Accent.TButton', background=self.secondary_color, 
                           foreground='white', font=self.font)
        self.style.map('Accent.TButton', 
                      background=[('active', self.primary_color)])
        
        self.toggle_controls()
    
    def create_date_fields(self, freq):
        """Create date input fields based on frequency"""
        for widget in self.date_frame.winfo_children():
            widget.destroy()
        
        if freq == "Climate Normals":
            ttk.Label(self.date_frame, text="Start Year:").grid(row=0, column=0)
            self.start_date = ttk.Entry(self.date_frame, width=10)
            self.start_date.grid(row=0, column=1, padx=5)
            
            ttk.Label(self.date_frame, text="End Year:").grid(row=0, column=2)
            self.end_date = ttk.Entry(self.date_frame, width=10)
            self.end_date.grid(row=0, column=3, padx=5)
        elif freq == "Monthly":
            ttk.Label(self.date_frame, text="Start Month:").grid(row=0, column=0)
            self.start_date = DateEntry(self.date_frame, width=12, 
                                       date_pattern="yyyy-MM", year=2020, month=1)
            self.start_date.grid(row=0, column=1, padx=5)
            
            ttk.Label(self.date_frame, text="End Month:").grid(row=0, column=2)
            self.end_date = DateEntry(self.date_frame, width=12, 
                                     date_pattern="yyyy-MM", year=2020, month=12)
            self.end_date.grid(row=0, column=3, padx=5)
        else:
            ttk.Label(self.date_frame, text="Start Date:").grid(row=0, column=0)
            self.start_date = DateEntry(self.date_frame, width=12)
            self.start_date.grid(row=0, column=1, padx=5)
            
            ttk.Label(self.date_frame, text="End Date:").grid(row=0, column=2)
            self.end_date = DateEntry(self.date_frame, width=12)
            self.end_date.grid(row=0, column=3, padx=5)
    
    def toggle_controls(self):
        """Toggle visibility of frequency and date controls"""
        if self.data_type.get() == "current":
            self.frequency_frame.pack_forget()
            self.date_frame.pack_forget()
        else:
            self.frequency_frame.pack(pady=5, anchor="w")
            self.date_frame.pack(pady=5, anchor="w")
            self.frequency.bind("<<ComboboxSelected>>", lambda e: self.create_date_fields(self.frequency.get()))
    
    def geocode_location(self):
        location = self.location_entry.get()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location name")
            return
        
        try:
            geolocator = Nominatim(user_agent="weather_scraper_app")
            location = geolocator.geocode(location)
            if location:
                self.lat_entry.delete(0, tk.END)
                self.lon_entry.delete(0, tk.END)
                self.lat_entry.insert(0, f"{location.latitude:.4f}")
                self.lon_entry.insert(0, f"{location.longitude:.4f}")
            else:
                messagebox.showerror("Geocoding Error", "Location not found")
        except Exception as e:
            messagebox.showerror("Geocoding Error", str(e))
    
    def validate_inputs(self):
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError
            return True
        except ValueError:
            messagebox.showerror("Input Error", "Invalid coordinates")
            return False
    
    def fetch_data(self):
        if not self.validate_inputs():
            return
        
        lat = float(self.lat_entry.get())
        lon = float(self.lon_entry.get())
        location = Point(lat, lon)
        
        try:
            if self.data_type.get() == 'current':
                start = datetime.today()
                data = Hourly(location, start, start).fetch()
            else:
                freq = self.frequency.get()
                
                # Convert date objects to datetime objects
                start_date = datetime.combine(
                    self.start_date.get_date(), 
                    datetime.min.time()
                )
                end_date = datetime.combine(
                    self.end_date.get_date(), 
                    datetime.max.time()
                )
                
                if freq == "Hourly":
                    data = Hourly(location, start_date, end_date).fetch()
                elif freq == "Daily":
                    data = Daily(location, start_date, end_date).fetch()
                elif freq == "Monthly":
                    # Ensure we're using first day of month
                    start_date = start_date.replace(day=1)
                    end_date = end_date.replace(day=1)
                    data = Monthly(location, start_date, end_date).fetch()
                elif freq == "Climate Normals":
                    data = Normals(location, start_date.year, end_date.year).fetch()
            
            self.data = data
            if self.data is not None and not self.data.empty:
                messagebox.showinfo("Success", f"Fetched {len(self.data)} weather records")
                self.plot_data()  # Auto-plot after fetch
            else:
                messagebox.showwarning("No Data", "No weather data found for this location/date range")
        
        except Exception as e:
            messagebox.showerror("Data Fetch Error", str(e))
    
    def export_data(self):
        if self.data is None or self.data.empty:
            messagebox.showwarning("Export Error", "No data to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.data.to_csv(file_path)
                else:
                    self.data.to_excel(file_path)
                messagebox.showinfo("Success", "Data exported successfully")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
    
    def show_data_preview(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please fetch data first")
            return
        
        preview = self.data.head().reset_index()
        
        preview_win = tk.Toplevel(self.root)
        preview_win.title("Data Preview")
        
        tree = ttk.Treeview(preview_win)
        tree["columns"] = list(preview.columns)
        tree["show"] = "headings"
        
        for col in preview.columns:
            tree.column(col, width=100)
            tree.heading(col, text=col)
        
        for _, row in preview.iterrows():
            tree.insert("", "end", values=list(row))
        
        tree.pack(expand=True, fill=tk.BOTH)
    
    def plot_data(self):
        if self.data is None or self.data.empty:
            messagebox.showwarning("No Data", "Please fetch data first")
            return
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        var = self.plot_var.get()
        
        try:
            if var == "All Variables":
                cols = [col for col in ['temp', 'prcp', 'wspd', "rhum", "wdir", "pres", "vis", "cloud", "tsun"] if col in self.data.columns]
                if not cols:
                    messagebox.showwarning("No Data", "No plottable variables found")
                    return
                
                self.data[cols].plot(ax=ax, subplots=True, layout=(-1, 2), 
                                   figsize=(8, 4), legend=True)
                ax.set_title("Weather Variables Overview")
            else:
                col_map = {
                    "Temperature": 'temp' if "temp" in self.data.columns else 'tavg',
                    "Precipitation": 'prcp',
                    "Wind Speed": 'wspd'
                }
                col = col_map[var]
                
                if col in self.data.columns:
                    self.data[col].plot(ax=ax, kind='line', marker='o', markersize=4)
                    ax.set_ylabel(var)
                    ax.set_title(f"{var} Trend")
                    ax.grid(True)
                else:
                    messagebox.showwarning("No Data", f"{var} data not available")
            
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Plot Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherScraperApp(root)
    root.mainloop()