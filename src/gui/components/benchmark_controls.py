"""
Benchmark Controls Component
"""

import customtkinter as ctk
from typing import Optional

class BenchmarkControlsFrame(ctk.CTkFrame):
    """Frame containing benchmark control buttons and settings"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.is_testing = False
        
        # DNS Pulse exact color scheme from Stitch design
        self.colors = {
            # Core surfaces
            'surface': '#10131a',                    # Main background
            'surface_container': '#1d2026',          # Default container
            'surface_container_high': '#272a31',     # High container
            
            # Primary colors (Cyan)
            'primary': '#00F0FF',                    # Main cyan
            'primary_dim': '#00dbe9',                # Dimmed cyan
            
            # Secondary colors (Electric Violet)  
            'secondary': '#9D4EDD',                   # Electric violet
            'secondary_dim': '#6d11ad',              # Dimmed violet
            
            # Tertiary colors (Mint)
            'tertiary': '#2DE2E6',                   # Mint
            
            # Text colors
            'on_surface': '#e1e2eb',                 # Primary text
            'on_surface_variant': '#b9cacb',         # Secondary text
            'text_muted': '#849495',                 # Muted text
            
            # Functional colors
            'error': '#ffb4ab',                      # Error red
            'success': '#00ff94',                    # Success green
            'warning': '#ffd700',                    # Warning yellow
            
            # UI elements
            'outline_variant': '#3b494b',            # Subtle borders
        }
        
        # Configure frame styling with transparent bg (parent already has card styling)
        self.configure(
            fg_color="transparent",
            corner_radius=0
        )
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the controls UI"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Modern title with gradient effect
        title_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=50
        )
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        title_frame.grid_propagate(False)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="⚡ BENCHMARK CONTROL",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(side="left")
        
        # Settings card
        settings_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        settings_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # Number of iterations
        iterations_label = ctk.CTkLabel(
            settings_frame,
            text="Iterations:",
            font=ctk.CTkFont(family="Arial", size=11),
            text_color=self.colors['on_surface_variant']
        )
        iterations_label.grid(row=0, column=0, padx=15, pady=12, sticky="w")
        
        self.iterations_var = ctk.StringVar(value="10")
        self.iterations_entry = ctk.CTkEntry(
            settings_frame,
            textvariable=self.iterations_var,
            width=80,
            height=32,
            fg_color=self.colors['surface_container_high'],
            border_color=self.colors['primary'],
            border_width=1,
            text_color=self.colors['on_surface']
        )
        self.iterations_entry.grid(row=0, column=1, padx=10, pady=12, sticky="w")
        
        # Timeout setting
        timeout_label = ctk.CTkLabel(
            settings_frame,
            text="Timeout (s):",
            font=ctk.CTkFont(family="Arial", size=11),
            text_color=self.colors['on_surface_variant']
        )
        timeout_label.grid(row=1, column=0, padx=15, pady=12, sticky="w")
        
        self.timeout_var = ctk.StringVar(value="5.0")
        self.timeout_entry = ctk.CTkEntry(
            settings_frame,
            textvariable=self.timeout_var,
            width=80,
            height=32,
            fg_color=self.colors['surface_container_high'],
            border_color=self.colors['primary'],
            border_width=1,
            text_color=self.colors['on_surface']
        )
        self.timeout_entry.grid(row=1, column=1, padx=10, pady=12, sticky="w")
        
        # Test types card
        test_types_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        test_types_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        
        test_types_label = ctk.CTkLabel(
            test_types_frame,
            text="TEST MODES",
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            text_color=self.colors['tertiary']
        )
        test_types_label.grid(row=0, column=0, padx=15, pady=(12, 8), sticky="w")
        
        # Checkboxes for test types with modern styling
        self.test_cached = ctk.BooleanVar(value=True)
        self.test_uncached = ctk.BooleanVar(value=True)
        self.test_dotcom = ctk.BooleanVar(value=True)
        
        cached_cb = ctk.CTkCheckBox(
            test_types_frame,
            text="Cached queries",
            variable=self.test_cached,
            font=ctk.CTkFont(family="Arial", size=12),
            text_color=self.colors['on_surface_variant'],
            fg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_dim'],
            border_color=self.colors['outline_variant']
        )
        cached_cb.grid(row=1, column=0, padx=15, pady=3, sticky="w")
        
        uncached_cb = ctk.CTkCheckBox(
            test_types_frame,
            text="Uncached queries",
            variable=self.test_uncached,
            font=ctk.CTkFont(family="Arial", size=12),
            text_color=self.colors['on_surface_variant'],
            fg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_dim'],
            border_color=self.colors['outline_variant']
        )
        uncached_cb.grid(row=2, column=0, padx=15, pady=3, sticky="w")
        
        dotcom_cb = ctk.CTkCheckBox(
            test_types_frame,
            text=".com domain focus",
            variable=self.test_dotcom,
            font=ctk.CTkFont(family="Arial", size=12),
            text_color=self.colors['on_surface_variant'],
            fg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_dim'],
            border_color=self.colors['outline_variant']
        )
        dotcom_cb.grid(row=3, column=0, padx=15, pady=(3, 12), sticky="w")
        
        # Progress card
        self.progress_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        self.progress_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=5)
        
        progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="PROGRESS",
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            text_color=self.colors['primary']
        )
        progress_label.grid(row=0, column=0, padx=15, pady=(12, 8), sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            fg_color=self.colors['surface_container_high'],
            progress_color=self.colors['primary'],
            corner_radius=6,
            height=10
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=15, pady=(5, 12))
        self.progress_bar.set(0)
        
        # Control buttons with modern glass effect
        buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        buttons_frame.grid(row=4, column=0, sticky="ew", padx=15, pady=(10, 10))
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        self.start_button = ctk.CTkButton(
            buttons_frame,
            text="🚀 START",
            height=48,
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            fg_color=self.colors['success'],
            hover_color=self.colors['secondary'],
            text_color="#000000",
            corner_radius=8,
            border_width=0,
            command=self.on_start_clicked
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.stop_button = ctk.CTkButton(
            buttons_frame,
            text="⏹ STOP",
            height=48,
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            fg_color=self.colors['error'],
            hover_color=self.colors['secondary_dim'],
            text_color=self.colors['on_surface'],
            corner_radius=8,
            border_width=0,
            command=self.on_stop_clicked,
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Export button with gradient effect
        self.export_button = ctk.CTkButton(
            self,
            text="📊 EXPORT RESULTS",
            height=42,
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            fg_color=self.colors['tertiary'],
            hover_color=self.colors['warning'],
            text_color="#000000",
            corner_radius=8,
            border_width=0,
            command=self.app.export_results
        )
        self.export_button.grid(row=5, column=0, padx=15, pady=(5, 15), sticky="ew")
    
    def on_start_clicked(self):
        """Handle start benchmark button click"""
        try:
            num_iterations = int(self.iterations_var.get())
            if num_iterations <= 0:
                raise ValueError("Iterations must be positive")
        except ValueError:
            self.app.show_error("Please enter a valid number of iterations (1-100)")
            return
        
        selected_servers = self.app.server_list_frame.get_selected_servers()
        if not selected_servers:
            self.app.show_error("Please select at least one DNS server to test.")
            return
        
        self.app.start_benchmark(selected_servers, num_iterations)
    
    def on_stop_clicked(self):
        """Handle stop benchmark button click"""
        self.app.stop_benchmark()
    
    def set_testing_state(self, is_testing: bool):
        """Update UI state based on testing status"""
        self.is_testing = is_testing
        
        if is_testing:
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.iterations_entry.configure(state="disabled")
            self.timeout_entry.configure(state="disabled")
        else:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.iterations_entry.configure(state="normal")
            self.timeout_entry.configure(state="normal")
            self.progress_bar.set(0)
    
    def update_progress(self, percentage: float):
        """Update the progress bar"""
        self.progress_bar.set(percentage / 100.0)
    
    def get_settings(self) -> dict:
        """Get current benchmark settings"""
        return {
            "iterations": int(self.iterations_var.get()),
            "timeout": float(self.timeout_var.get()),
            "test_cached": self.test_cached.get(),
            "test_uncached": self.test_uncached.get(),
            "test_dotcom": self.test_dotcom.get()
        }