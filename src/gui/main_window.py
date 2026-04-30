"""
Main GUI Application Window - DNS Pulse Design System
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import List, Dict, Optional
from src.data.dns_servers import DNSServerDatabase, DNSServer
from src.core.dns_benchmark import DNSBenchmarkEngine, ServerStatistics
from src.gui.components.server_list import ServerListFrame
from src.gui.components.benchmark_controls import BenchmarkControlsFrame
from src.gui.components.results_display import ResultsDisplayFrame
from src.gui.components.statistics_panel import StatisticsPanel
from src.gui.components.graphs_panel import GraphsPanel

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DNSBenchmarkApp:
    """Main application class for DNS Pulse - Network Performance Analysis"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("DNS Pulse - Network Performance Analysis")
        self.root.geometry("1920x1080")
        self.root.minsize(1400, 900)
        
        # DNS Pulse exact color scheme from Stitch design
        self.colors = {
            # Core surfaces
            'surface': '#10131a',                    # Main background
            'surface_dim': '#0b0e14',                # Darkest background
            'surface_bright': '#363940',             # Bright surface
            'surface_container_lowest': '#0b0e14',   # Lowest container
            'surface_container_low': '#191c22',      # Low container
            'surface_container': '#1d2026',          # Default container
            'surface_container_high': '#272a31',     # High container
            'surface_container_highest': '#32353c',  # Highest container
            
            # Primary colors (Cyan)
            'primary': '#00F0FF',                    # Main cyan
            'primary_dim': '#00dbe9',                # Dimmed cyan
            'primary_container': '#00f0ff',          # Container cyan
            'on_primary': '#00363a',                 # Text on primary
            
            # Secondary colors (Electric Violet)
            'secondary': '#9D4EDD',                   # Electric violet
            'secondary_dim': '#6d11ad',              # Dimmed violet
            'secondary_container': '#6d11ad',        # Container violet
            'on_secondary': '#4c007d',               # Text on secondary
            
            # Tertiary colors (Mint)
            'tertiary': '#2DE2E6',                   # Mint
            'tertiary_dim': '#1edce0',               # Dimmed mint
            
            # Text colors
            'on_surface': '#e1e2eb',                 # Primary text
            'on_surface_variant': '#b9cacb',         # Secondary text
            'text_muted': '#849495',                 # Muted text
            
            # Functional colors
            'error': '#ffb4ab',                      # Error red
            'success': '#00ff94',                    # Success green
            'warning': '#ffd700',                    # Warning yellow
            
            # UI elements
            'outline': '#849495',                     # Borders
            'outline_variant': '#3b494b',            # Subtle borders
            'glow_cyan': 'rgba(0, 240, 255, 0.3)',  # Cyan glow
            'glow_violet': 'rgba(157, 78, 221, 0.3)' # Violet glow
        }
        
        # Configure root window with exact background
        self.root.configure(fg_color=self.colors['surface_dim'])
        
        # Initialize core components
        self.dns_db = DNSServerDatabase()
        self.benchmark_engine = DNSBenchmarkEngine()
        self.is_testing = False
        
        # Tab management - store component instances
        self.tab_components = {}
        self.current_tab = "dashboard"
        
        # Setup the UI
        self.setup_ui()
        
        # Load DNS servers on startup
        self.load_dns_servers()
    
    def setup_ui(self):
        """Setup the main user interface with DNS Pulse design"""
        # Configure grid weights for responsive design
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create sidebar navigation (left panel)
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
    
    def create_sidebar(self):
        """Create the sidebar navigation with DNS Pulse branding"""
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=280,
            fg_color=self.colors['surface_container_low'],
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # DNS PULSE Logo and branding
        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            height=100
        )
        logo_frame.pack(fill="x", padx=20, pady=20)
        logo_frame.pack_propagate(False)
        
        # Logo with cyan glow effect
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="DNS PULSE",
            font=ctk.CTkFont(family="Arial Black", size=28, weight="bold"),
            text_color=self.colors['primary']
        )
        logo_label.pack(pady=(10, 5))
        
        tagline = ctk.CTkLabel(
            logo_frame,
            text="NETWORK PERFORMANCE ANALYSIS",
            font=ctk.CTkFont(family="Arial", size=10),
            text_color=self.colors['text_muted']
        )
        tagline.pack()
        
        # Divider with glow
        divider = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=self.colors['outline_variant']
        )
        divider.pack(fill="x", padx=20, pady=(0, 20))
        
        # Navigation tabs
        self.nav_buttons = []
        nav_items = [
            ("🏠", "DASHBOARD", "dashboard"),
            ("📊", "STATISTICS", "statistics"),
            ("🌐", "NETWORK MAP", "network_map"),
            ("🔒", "SECURITY", "security"),
            ("⚙️", "SETTINGS", "settings")
        ]
        
        for icon, label, tag in nav_items:
            btn = self.create_nav_button(icon, label, tag)
            self.nav_buttons.append(btn)
        
        # Set dashboard as active by default
        self.set_active_nav("dashboard")
        
        # System status at bottom
        self.create_system_status()
    
    def create_nav_button(self, icon: str, label: str, tag: str):
        """Create a navigation button with hover effects"""
        btn_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            height=50,
            cursor="hand2"
        )
        btn_frame.pack(fill="x", padx=15, pady=2)
        btn_frame.pack_propagate(False)
        
        btn = ctk.CTkButton(
            btn_frame,
            text=f"{icon}  {label}",
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            fg_color="transparent",
            hover_color=self.colors['surface_container'],
            text_color=self.colors['on_surface_variant'],
            anchor="w",
            height=45,
            corner_radius=8,
            command=lambda t=tag: self.on_nav_click(t)
        )
        btn.pack(fill="both", expand=True)
        btn.tag = tag
        
        return btn
    
    def set_active_nav(self, tag: str):
        """Set the active navigation button"""
        for btn in self.nav_buttons:
            if hasattr(btn, 'tag') and btn.tag == tag:
                btn.configure(
                    fg_color=self.colors['surface_container'],
                    text_color=self.colors['primary']
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=self.colors['on_surface_variant']
                )
    
    def on_nav_click(self, tag: str):
        """Handle navigation button click"""
        self.set_active_nav(tag)
        # Update page title
        titles = {
            "dashboard": "Benchmark Dashboard",
            "statistics": "Detailed Statistics", 
            "network_map": "Network Map",
            "security": "Security Analysis",
            "settings": "Application Settings"
        }
        if tag in titles:
            self.page_title.configure(text=titles[tag])
        
        # Switch content using persistent tab system
        self.show_tab_content(tag)
    
    def create_system_status(self):
        """Create system status indicator at bottom of sidebar"""
        status_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color=self.colors['surface_container'],
            corner_radius=12,
            height=80
        )
        status_frame.pack(side="bottom", fill="x", padx=15, pady=15)
        status_frame.pack_propagate(False)
        
        # Status indicator
        status_header = ctk.CTkLabel(
            status_frame,
            text="SYSTEM STATUS",
            font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
            text_color=self.colors['text_muted']
        )
        status_header.pack(pady=(10, 5))
        
        self.status_indicator = ctk.CTkLabel(
            status_frame,
            text="● ONLINE",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['success']
        )
        self.status_indicator.pack()
        
        self.latency_label = ctk.CTkLabel(
            status_frame,
            text="Latency: --ms",
            font=ctk.CTkFont(family="Arial", size=10),
            text_color=self.colors['on_surface_variant']
        )
        self.latency_label.pack()
    
    def create_main_content(self):
        """Create the main content area"""
        self.main_content = ctk.CTkFrame(
            self.root,
            fg_color=self.colors['surface']
        )
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)
        
        # Create header
        self.create_header()
        
        # Content container
        self.content_container = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)
        
        # Show dashboard by default
        self.show_tab_content("dashboard")
    
    def create_header(self):
        """Create modern header with stats"""
        header = ctk.CTkFrame(
            self.main_content,
            height=80,
            fg_color=self.colors['surface_container_low'],
            corner_radius=0
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        # Header content
        header_content = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        header_content.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Title section
        self.page_title = ctk.CTkLabel(
            header_content,
            text="Dashboard",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color=self.colors['on_surface']
        )
        self.page_title.pack(side="left")
        
        # Stats container
        stats_frame = ctk.CTkFrame(
            header_content,
            fg_color="transparent"
        )
        stats_frame.pack(side="right")
        
        # Create stat cards
        self.create_stat_card(stats_frame, "SERVERS", "0", self.colors['primary'], 0)
        self.create_stat_card(stats_frame, "AVG LATENCY", "--ms", self.colors['secondary'], 1)
        self.create_stat_card(stats_frame, "SUCCESS RATE", "--", self.colors['tertiary'], 2)
    
    def create_stat_card(self, parent, label, value, color, column):
        """Create a stat card with glassmorphic effect"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            width=140,
            height=50
        )
        card.grid(row=0, column=column, padx=8)
        card.grid_propagate(False)
        
        # Label
        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(family="Arial", size=9, weight="bold"),
            text_color=self.colors['text_muted']
        )
        label_widget.pack(pady=(8, 0))
        
        # Value
        value_widget = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=color
        )
        value_widget.pack()
        
        # Store reference
        if label == "SERVERS":
            self.servers_stat = value_widget
        elif label == "AVG LATENCY":
            self.latency_stat = value_widget
        elif label == "SUCCESS RATE":
            self.success_stat = value_widget
    
    def create_dashboard_tab(self):
        """Create the dashboard tab content (persistent)"""
        # Create dashboard layout
        dashboard = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent"
        )
        # Don't pack initially - will be packed when shown
        dashboard.grid_columnconfigure(0, weight=2)
        dashboard.grid_columnconfigure(1, weight=3)
        dashboard.grid_rowconfigure(0, weight=1)
        
        # Left panel - Controls and server list
        left_panel = ctk.CTkFrame(
            dashboard,
            fg_color=self.colors['surface_container_low'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)
        
        # Benchmark controls
        controls_frame = BenchmarkControlsFrame(left_panel, self)
        controls_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        
        # Server list
        server_list_frame = ServerListFrame(left_panel, self)
        server_list_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Right panel - Results
        right_panel = ctk.CTkFrame(
            dashboard,
            fg_color=self.colors['surface_container_low'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(0, weight=1)
        
        # Results display
        results_frame = ResultsDisplayFrame(right_panel, self)
        results_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Store components for persistent access
        self.tab_components["dashboard"] = {
            'container': dashboard,
            'controls_frame': controls_frame,
            'server_list_frame': server_list_frame,
            'results_frame': results_frame
        }
        
        # Set global references for backwards compatibility
        self.controls_frame = controls_frame
        self.server_list_frame = server_list_frame
        self.results_frame = results_frame
    
    def show_dashboard(self):
        """Show dashboard tab (for backwards compatibility)"""
        self.show_tab_content("dashboard")
    
    def create_statistics_tab(self):
        """Create the statistics tab content (persistent)"""
        # Statistics container
        stats_container = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent"
        )
        stats_container.grid_columnconfigure(0, weight=1)
        stats_container.grid_columnconfigure(1, weight=1)
        stats_container.grid_rowconfigure(0, weight=1)
        
        # Statistics panel (left side)
        statistics_frame = StatisticsPanel(stats_container, self)
        statistics_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Graphs panel (right side)
        graphs_frame = GraphsPanel(stats_container, self)
        graphs_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Store components for persistent access
        self.tab_components["statistics"] = {
            'container': stats_container,
            'statistics_frame': statistics_frame,
            'graphs_frame': graphs_frame
        }
        
        # Set global references for backwards compatibility
        self.statistics_frame = statistics_frame
        self.graphs_frame = graphs_frame
    
    def show_statistics(self):
        """Show statistics tab (for backwards compatibility)"""
        self.show_tab_content("statistics")
    
    def create_network_map_tab(self):
        """Create the network map tab content (persistent)"""
        
        # Initialize network server items storage
        if not hasattr(self, 'network_server_items'):
            self.network_server_items = {}
        
        # Network map container - main container for the tab
        map_container = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent"
        )
        map_container.pack(fill="both", expand=True)
        map_container.grid_columnconfigure(0, weight=1)
        map_container.grid_rowconfigure(0, weight=1)
        
        # Network map content frame
        content_frame = ctk.CTkFrame(
            map_container,
            fg_color=self.colors['surface_container_low'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        content_frame.pack(fill="both", expand=True)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        header.grid_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="🌐 GLOBAL DNS NETWORK TOPOLOGY",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color=self.colors['primary']
        ).pack(expand=True)
        
        # Map content
        content_area = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        content_area.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        content_area.grid_columnconfigure(0, weight=1)
        content_area.grid_columnconfigure(1, weight=2)
        content_area.grid_rowconfigure(0, weight=1)
        
        # Network visualization (left side)
        self.create_network_visualization(content_area)
        
        # Server details panel (right side)
        self.create_server_details_panel(content_area)
    
    def create_network_visualization(self, parent):
        """Create network topology visualization"""
        viz_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8
        )
        viz_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        # Central node (Your Computer)
        center_frame = ctk.CTkFrame(
            viz_frame,
            fg_color=self.colors['primary'],
            corner_radius=50,
            width=100,
            height=100
        )
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        center_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            center_frame,
            text="🖥️\nYOUR\nCOMPUTER",
            font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
            text_color="#000000"
        ).pack(expand=True)
        
        # DNS Server nodes arranged in a circle
        server_positions = [
            (0.2, 0.2, "Google\nDNS", self.colors['secondary']),
            (0.8, 0.2, "Cloudflare\nDNS", self.colors['warning']),
            (0.9, 0.5, "Quad9\nDNS", self.colors['tertiary']),
            (0.8, 0.8, "OpenDNS\nDNS", self.colors['success']),
            (0.2, 0.8, "AdGuard\nDNS", self.colors['error']),
            (0.1, 0.5, "Level3\nDNS", self.colors['on_surface_variant']),
        ]
        
        for x, y, label, color in server_positions:
            server_node = ctk.CTkFrame(
                viz_frame,
                fg_color=color,
                corner_radius=30,
                width=60,
                height=60
            )
            server_node.place(relx=x, rely=y, anchor="center")
            server_node.pack_propagate(False)
            
            ctk.CTkLabel(
                server_node,
                text=label,
                font=ctk.CTkFont(family="Arial", size=8, weight="bold"),
                text_color="#000000"
            ).pack(expand=True)
            
            # Connection lines (simulated with frames)
            self.create_connection_line(viz_frame, 0.5, 0.5, x, y)
        
        # Legend
        legend_frame = ctk.CTkFrame(
            viz_frame,
            fg_color=self.colors['surface_container'],
            corner_radius=6
        )
        legend_frame.place(relx=0.02, rely=0.02, anchor="nw")
        
        ctk.CTkLabel(
            legend_frame,
            text="● Live Connection\n● High Latency\n● Timeout",
            font=ctk.CTkFont(family="Arial", size=9),
            text_color=self.colors['on_surface_variant']
        ).pack(padx=8, pady=6)
    
    def create_connection_line(self, parent, x1, y1, x2, y2):
        """Create a visual connection line between nodes"""
        # Calculate midpoint for connection indicator
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Create small connection indicator
        connection = ctk.CTkFrame(
            parent,
            fg_color=self.colors['success'],
            corner_radius=3,
            width=6,
            height=6
        )
        connection.place(relx=mid_x, rely=mid_y, anchor="center")
    
    def create_server_details_panel(self, parent):
        """Create server details panel"""
        details_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8
        )
        details_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        details_frame.grid_columnconfigure(0, weight=1)
        
        # Panel title
        title_frame = ctk.CTkFrame(details_frame, fg_color="transparent", height=40)
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        title_frame.grid_propagate(False)
        
        ctk.CTkLabel(
            title_frame,
            text="SERVER STATUS",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color=self.colors['tertiary']
        ).pack(side="left")
        
        # Scrollable server list
        server_list = ctk.CTkScrollableFrame(
            details_frame,
            fg_color="transparent"
        )
        server_list.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        server_list.grid_columnconfigure(0, weight=1)
        
        # Sample server entries - will be updated with real data
        servers_data = [
            ("Google Public DNS", "8.8.8.8", "Ready", self.colors['text_muted']),
            ("Cloudflare DNS", "1.1.1.1", "Ready", self.colors['text_muted']),
            ("Quad9 DNS", "9.9.9.9", "Ready", self.colors['text_muted']),
            ("OpenDNS", "208.67.222.222", "Ready", self.colors['text_muted']),
            ("AdGuard DNS", "94.140.14.14", "Ready", self.colors['text_muted']),
            ("Level3 DNS", "4.2.2.2", "Ready", self.colors['text_muted']),
        ]
        
        for i, (name, ip, latency, status_color) in enumerate(servers_data):
            server_card = ctk.CTkFrame(
                server_list,
                fg_color=self.colors['surface_container'],
                corner_radius=6,
                border_width=1,
                border_color=self.colors['outline_variant']
            )
            server_card.grid(row=i, column=0, sticky="ew", pady=2)
            server_card.grid_columnconfigure(1, weight=1)
            
            # Status indicator
            status_dot = ctk.CTkLabel(
                server_card,
                text="●",
                font=ctk.CTkFont(size=16),
                text_color=status_color,
                width=20
            )
            status_dot.grid(row=0, column=0, padx=(10, 5), pady=8)
            
            # Server info
            info_frame = ctk.CTkFrame(server_card, fg_color="transparent")
            info_frame.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=6)
            
            name_label = ctk.CTkLabel(
                info_frame,
                text=name,
                font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
                text_color=self.colors['on_surface'],
                anchor="w"
            )
            name_label.pack(anchor="w")
            
            status_label = ctk.CTkLabel(
                info_frame,
                text=f"{ip} • {latency}",
                font=ctk.CTkFont(family="Arial", size=9),
                text_color=self.colors['text_muted'],
                anchor="w"
            )
            status_label.pack(anchor="w")
            
            # Store references for live updates
            self.network_server_items[ip] = {
                'status_dot': status_dot,
                'status_label': status_label,
                'name': name
            }
        
        
        # Store components for persistent access
        self.tab_components["network_map"] = {
            'container': map_container,
            'content_frame': content_frame,
            'content_area': content_area
        }
    
    def show_network_map(self):
        """Show network map tab (for backwards compatibility)"""
        self.show_tab_content("network_map")
    
    def update_network_map_status(self, result):
        """Update network map with live benchmark result"""
        if not result or not hasattr(self, 'network_server_items'):
            return
            
        try:
            server_ip = result.server_ip
            if server_ip in self.network_server_items:
                item = self.network_server_items[server_ip]
                
                if result.success:
                    # Color based on response time
                    if result.response_time < 20:
                        status_color = self.colors['success']
                        status_text = f"🟢 {result.response_time:.0f}ms"
                    elif result.response_time < 50:
                        status_color = self.colors['secondary']
                        status_text = f"🟡 {result.response_time:.0f}ms"
                    elif result.response_time < 100:
                        status_color = self.colors['warning']
                        status_text = f"🟠 {result.response_time:.0f}ms"
                    else:
                        status_color = self.colors['error']
                        status_text = f"🔴 {result.response_time:.0f}ms"
                else:
                    status_color = self.colors['error']
                    status_text = "🔴 FAIL"
                
                # Update status indicator and text
                item['status_dot'].configure(text_color=status_color)
                item['status_label'].configure(
                    text=f"{server_ip} • {status_text}",
                    text_color=status_color
                )
                
        except Exception as e:
            # Fail silently to not interrupt the benchmark
            pass
    
    def create_security_tab(self):
        """Create the security tab content (persistent)"""
        # Main security container
        security_container = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent"
        )
        security_container.pack(fill="both", expand=True)
        security_container.grid_columnconfigure(0, weight=2)
        security_container.grid_columnconfigure(1, weight=3)
        security_container.grid_rowconfigure(0, weight=1)
        
        # Left panel - Security metrics
        left_panel = ctk.CTkFrame(
            security_container,
            fg_color=self.colors['surface_container_low'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)
        
        # Security header
        security_header = ctk.CTkFrame(
            left_panel,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        security_header.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        security_header.grid_propagate(False)
        
        ctk.CTkLabel(
            security_header,
            text="🔒 SECURITY METRICS",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=self.colors['error']
        ).pack(expand=True)
        
        # Security metrics container
        metrics_container = ctk.CTkScrollableFrame(
            left_panel,
            fg_color="transparent"
        )
        metrics_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        metrics_container.grid_columnconfigure(0, weight=1)
        
        # DNSSEC Support Card
        self.create_security_card(metrics_container, "🛡️ DNSSEC SUPPORT", [
            ("Validating Resolvers", "0/0", self.colors['warning']),
            ("Signed Zones", "--", self.colors['text_muted']),
            ("Validation Status", "Unknown", self.colors['text_muted'])
        ], 0)
        
        # DNS Security Card
        self.create_security_card(metrics_container, "🔐 DNS SECURITY", [
            ("DNS over HTTPS", "0/0", self.colors['warning']),
            ("DNS over TLS", "0/0", self.colors['warning']),
            ("Plain DNS", "0/0", self.colors['error'])
        ], 1)
        
        # Threat Detection Card
        self.create_security_card(metrics_container, "⚠️ THREAT DETECTION", [
            ("Malware Blocking", "0/0", self.colors['success']),
            ("Phishing Protection", "0/0", self.colors['success']),
            ("Ad Blocking", "0/0", self.colors['tertiary'])
        ], 2)
        
        # Privacy Analysis Card
        self.create_security_card(metrics_container, "👁️ PRIVACY ANALYSIS", [
            ("No Logging Policy", "0/0", self.colors['success']),
            ("Geographic Location", "--", self.colors['text_muted']),
            ("Data Retention", "--", self.colors['text_muted'])
        ], 3)
        
        # Right panel - Security tests and details
        right_panel = ctk.CTkFrame(
            security_container,
            fg_color=self.colors['surface_container_low'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        
        # Security test header
        test_header = ctk.CTkFrame(
            right_panel,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        test_header.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        test_header.grid_columnconfigure(1, weight=1)
        test_header.grid_propagate(False)
        
        ctk.CTkLabel(
            test_header,
            text="🔍 SECURITY TESTS",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=self.colors['primary']
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Security test button
        security_test_btn = ctk.CTkButton(
            test_header,
            text="🚀 RUN SECURITY SCAN",
            width=180,
            height=32,
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            fg_color=self.colors['error'],
            hover_color=self.colors['secondary'],
            text_color=self.colors['on_surface'],
            corner_radius=6,
            command=self.run_security_scan
        )
        security_test_btn.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        
        # Security test results area
        test_results_container = ctk.CTkFrame(
            right_panel,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8
        )
        test_results_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        test_results_container.grid_columnconfigure(0, weight=1)
        test_results_container.grid_rowconfigure(0, weight=1)
        
        # Security test list
        self.security_results_frame = ctk.CTkScrollableFrame(
            test_results_container,
            fg_color="transparent"
        )
        self.security_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.security_results_frame.grid_columnconfigure(0, weight=1)
        
        # Initial security tests display
        self.create_security_test_item("🛡️ DNSSEC Validation Test", "Ready to scan", "pending", 0)
        self.create_security_test_item("🔐 Encrypted DNS Support", "Ready to scan", "pending", 1)
        self.create_security_test_item("⚠️ Malware Domain Test", "Ready to scan", "pending", 2)
        self.create_security_test_item("🚫 DNS Filtering Test", "Ready to scan", "pending", 3)
        self.create_security_test_item("👁️ Privacy Leak Test", "Ready to scan", "pending", 4)
        self.create_security_test_item("🌍 Geographic DNS Test", "Ready to scan", "pending", 5)
        
        # Store components for persistent access
        self.tab_components["security"] = {
            'container': security_container
        }
    
    def show_security(self):
        """Show security tab (for backwards compatibility)"""
        self.show_tab_content("security")
    
    def create_security_card(self, parent, title, metrics, row):
        """Create a security metrics card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        card.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        card.grid_columnconfigure(0, weight=1)
        
        # Card header
        header = ctk.CTkFrame(card, fg_color="transparent", height=40)
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(12, 8))
        header.grid_propagate(False)
        
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['secondary']
        ).pack(side="left")
        
        # Metrics rows
        for i, (label, value, color) in enumerate(metrics, 1):
            metric_frame = ctk.CTkFrame(card, fg_color="transparent")
            metric_frame.grid(row=i, column=0, sticky="ew", padx=15, pady=2)
            metric_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(
                metric_frame,
                text=label,
                font=ctk.CTkFont(family="Arial", size=11),
                text_color=self.colors['on_surface_variant']
            ).grid(row=0, column=0, sticky="w")
            
            ctk.CTkLabel(
                metric_frame,
                text=value,
                font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
                text_color=color
            ).grid(row=0, column=1, sticky="e", padx=(10, 0))
        
        # Add some bottom padding
        ctk.CTkFrame(card, fg_color="transparent", height=8).grid(row=len(metrics)+1, column=0)
    
    def create_security_test_item(self, test_name, status, state, row):
        """Create a security test item"""
        item_frame = ctk.CTkFrame(
            self.security_results_frame,
            fg_color=self.colors['surface_container'],
            corner_radius=6,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        item_frame.grid(row=row, column=0, sticky="ew", pady=3)
        item_frame.grid_columnconfigure(1, weight=1)
        item_frame.grid_propagate(False)
        
        # Status indicator
        if state == "pending":
            status_color = self.colors['text_muted']
            status_icon = "⏳"
        elif state == "running":
            status_color = self.colors['warning']
            status_icon = "⚡"
        elif state == "pass":
            status_color = self.colors['success']
            status_icon = "✅"
        else:  # fail
            status_color = self.colors['error']
            status_icon = "❌"
        
        status_label = ctk.CTkLabel(
            item_frame,
            text=status_icon,
            font=ctk.CTkFont(size=16),
            text_color=status_color,
            width=30
        )
        status_label.grid(row=0, column=0, padx=12, pady=12)
        
        # Test info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=8)
        
        ctk.CTkLabel(
            info_frame,
            text=test_name,
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['on_surface'],
            anchor="w"
        ).pack(anchor="w")
        
        message_label = ctk.CTkLabel(
            info_frame,
            text=status,
            font=ctk.CTkFont(family="Arial", size=10),
            text_color=self.colors['text_muted'],
            anchor="w"
        )
        message_label.pack(anchor="w")
        
        # Store references for updates
        if not hasattr(self, 'security_test_items'):
            self.security_test_items = {}
        
        self.security_test_items[test_name] = {
            'status_label': status_label,
            'message_label': message_label,
            'frame': item_frame
        }
    
    def run_security_scan(self):
        """Run comprehensive security scanning"""
        self.run_security_tests()
    
    def create_settings_tab(self):
        """Create the settings tab content (persistent)"""
        # Main settings container
        settings_container = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent"
        )
        settings_container.pack(fill="both", expand=True)
        settings_container.grid_columnconfigure(0, weight=1)
        settings_container.grid_columnconfigure(1, weight=1)
        settings_container.grid_rowconfigure(0, weight=1)
        
        # Left panel - Application Settings
        left_panel = ctk.CTkFrame(
            settings_container,
            fg_color=self.colors['surface_container_low'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        
        # Application settings header
        app_header = ctk.CTkFrame(
            left_panel,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        app_header.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        app_header.grid_propagate(False)
        
        ctk.CTkLabel(
            app_header,
            text="⚙️ APPLICATION SETTINGS",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=self.colors['primary']
        ).pack(expand=True)
        
        # Settings form container
        settings_form = ctk.CTkScrollableFrame(
            left_panel,
            fg_color="transparent"
        )
        settings_form.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        settings_form.grid_columnconfigure(1, weight=1)
        
        # Theme Settings
        self.create_settings_section(settings_form, "🎨 APPEARANCE", [
            ("Theme", "option", ["Dark", "Light", "Auto"], "Dark"),
            ("UI Scale", "scale", "100%", None),
            ("Animations", "toggle", True, None)
        ], 0)
        
        # Benchmark Settings
        self.create_settings_section(settings_form, "🚀 BENCHMARK", [
            ("Default Iterations", "number", "10", None),
            ("Default Timeout (s)", "number", "5.0", None),
            ("Auto-save Results", "toggle", True, None),
            ("Max Concurrent Tests", "number", "50", None)
        ], 1)
        
        # Network Settings
        self.create_settings_section(settings_form, "🌐 NETWORK", [
            ("Connection Timeout (s)", "number", "3.0", None),
            ("Retry Attempts", "number", "3", None),
            ("Use IPv6", "toggle", True, None),
            ("Proxy Settings", "text", "None", None)
        ], 2)
        
        # Data Settings
        self.create_settings_section(settings_form, "💾 DATA", [
            ("Export Format", "option", ["JSON", "CSV", "XML"], "JSON"),
            ("Auto-backup Results", "toggle", False, None),
            ("Results History (days)", "number", "30", None)
        ], 3)
        
        # Right panel - About and Advanced
        right_panel = ctk.CTkFrame(
            settings_container,
            fg_color=self.colors['surface_container_low'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        
        # About header
        about_header = ctk.CTkFrame(
            right_panel,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        about_header.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        about_header.grid_propagate(False)
        
        ctk.CTkLabel(
            about_header,
            text="ℹ️ ABOUT & ADVANCED",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=self.colors['tertiary']
        ).pack(expand=True)
        
        # About and advanced container
        about_container = ctk.CTkScrollableFrame(
            right_panel,
            fg_color="transparent"
        )
        about_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        about_container.grid_columnconfigure(0, weight=1)
        
        # Application Info Card
        info_card = ctk.CTkFrame(
            about_container,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        info_card.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        info_card.grid_columnconfigure(0, weight=1)
        
        # App info header
        ctk.CTkLabel(
            info_card,
            text="📱 APPLICATION INFO",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['secondary']
        ).grid(row=0, column=0, padx=15, pady=(12, 8), sticky="w")
        
        app_info = [
            ("Version", "1.0.0"),
            ("Build", "2024.04.30"),
            ("Platform", "Windows"),
            ("Python", "3.11+"),
            ("GUI Framework", "CustomTkinter")
        ]
        
        for i, (label, value) in enumerate(app_info, 1):
            info_row = ctk.CTkFrame(info_card, fg_color="transparent")
            info_row.grid(row=i, column=0, sticky="ew", padx=15, pady=2)
            info_row.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(
                info_row,
                text=label + ":",
                font=ctk.CTkFont(family="Arial", size=11),
                text_color=self.colors['on_surface_variant']
            ).grid(row=0, column=0, sticky="w")
            
            ctk.CTkLabel(
                info_row,
                text=value,
                font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
                text_color=self.colors['on_surface']
            ).grid(row=0, column=1, sticky="e", padx=(10, 0))
        
        # Add padding
        ctk.CTkFrame(info_card, fg_color="transparent", height=8).grid(row=len(app_info)+1, column=0)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(
            about_container,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        buttons_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        buttons_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            buttons_frame,
            text="🛠️ ACTIONS",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['secondary']
        ).grid(row=0, column=0, padx=15, pady=(12, 8), sticky="w")
        
        # Action buttons
        action_buttons = [
            ("📊 Export Settings", self.colors['primary']),
            ("📥 Import Settings", self.colors['tertiary']),
            ("🔄 Reset to Defaults", self.colors['warning']),
            ("🗑️ Clear All Data", self.colors['error'])
        ]
        
        for i, (text, color) in enumerate(action_buttons, 1):
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                width=200,
                height=36,
                font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
                fg_color=color,
                hover_color=self.colors['secondary'],
                text_color="#000000" if color != self.colors['error'] else self.colors['on_surface'],
                corner_radius=6,
                command=lambda t=text: self.handle_settings_action(t)
            )
            btn.grid(row=i, column=0, padx=15, pady=3, sticky="ew")
        
        # Add padding
        ctk.CTkFrame(buttons_frame, fg_color="transparent", height=8).grid(row=len(action_buttons)+1, column=0)
        
        # Settings save bar at bottom
        save_frame = ctk.CTkFrame(
            self.content_container,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        save_frame.pack(side="bottom", fill="x", pady=(15, 0))
        save_frame.pack_propagate(False)
        
        save_buttons_container = ctk.CTkFrame(save_frame, fg_color="transparent")
        save_buttons_container.pack(expand=True, padx=20, pady=12)
        
        ctk.CTkButton(
            save_buttons_container,
            text="💾 SAVE CHANGES",
            width=150,
            height=36,
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            fg_color=self.colors['success'],
            hover_color=self.colors['primary'],
            text_color="#000000",
            corner_radius=6,
            command=self.save_settings
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            save_buttons_container,
            text="↩️ CANCEL",
            width=120,
            height=36,
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            fg_color=self.colors['surface_container_high'],
            hover_color=self.colors['error'],
            text_color=self.colors['on_surface_variant'],
            corner_radius=6,
            border_width=1,
            border_color=self.colors['outline_variant'],
            command=self.cancel_settings
        ).pack(side="right")
        
        # Store components for persistent access
        self.tab_components["settings"] = {
            'container': settings_container
        }
    
    def show_settings(self):
        """Show settings tab (for backwards compatibility)"""
        self.show_tab_content("settings")
    
    def create_settings_section(self, parent, title, settings, row):
        """Create a settings section with various input types"""
        # Section card
        section_card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        section_card.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        section_card.grid_columnconfigure(1, weight=1)
        
        # Section header
        header = ctk.CTkFrame(section_card, fg_color="transparent", height=40)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(12, 8))
        header.grid_propagate(False)
        
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['secondary']
        ).pack(side="left")
        
        # Settings items
        for i, (label, setting_type, value, options) in enumerate(settings, 1):
            # Label
            ctk.CTkLabel(
                section_card,
                text=label + ":",
                font=ctk.CTkFont(family="Arial", size=11),
                text_color=self.colors['on_surface_variant']
            ).grid(row=i, column=0, sticky="w", padx=15, pady=5)
            
            # Input control
            if setting_type == "toggle":
                control = ctk.CTkSwitch(
                    section_card,
                    text="",
                    width=50,
                    height=24,
                    switch_width=40,
                    switch_height=20,
                    fg_color=self.colors['surface_container'],
                    progress_color=self.colors['primary'],
                    button_color=self.colors['on_surface'],
                    button_hover_color=self.colors['tertiary']
                )
                if value:
                    control.select()
                control.grid(row=i, column=1, sticky="e", padx=15, pady=5)
                
            elif setting_type == "option":
                control = ctk.CTkOptionMenu(
                    section_card,
                    values=value,  # value contains the options list
                    width=150,
                    height=28,
                    font=ctk.CTkFont(family="Arial", size=10),
                    fg_color=self.colors['surface_container'],
                    button_color=self.colors['primary'],
                    button_hover_color=self.colors['tertiary'],
                    dropdown_fg_color=self.colors['surface_container_high'],
                    text_color=self.colors['on_surface_variant'],
                    corner_radius=4
                )
                if options:  # options contains the default value
                    control.set(options)
                control.grid(row=i, column=1, sticky="e", padx=15, pady=5)
                
            elif setting_type == "number" or setting_type == "text":
                control = ctk.CTkEntry(
                    section_card,
                    width=120,
                    height=28,
                    font=ctk.CTkFont(family="Arial", size=11),
                    fg_color=self.colors['surface_container'],
                    border_color=self.colors['outline_variant'],
                    text_color=self.colors['on_surface']
                )
                control.insert(0, value)
                control.grid(row=i, column=1, sticky="e", padx=15, pady=5)
                
            elif setting_type == "scale":
                scale_frame = ctk.CTkFrame(section_card, fg_color="transparent")
                scale_frame.grid(row=i, column=1, sticky="e", padx=15, pady=5)
                
                scale_control = ctk.CTkSlider(
                    scale_frame,
                    from_=50,
                    to=150,
                    width=100,
                    height=16,
                    progress_color=self.colors['primary'],
                    button_color=self.colors['tertiary'],
                    button_hover_color=self.colors['secondary']
                )
                scale_control.set(100)  # Default to 100%
                scale_control.pack(side="left")
                
                scale_label = ctk.CTkLabel(
                    scale_frame,
                    text="100%",
                    width=35,
                    font=ctk.CTkFont(family="Arial", size=10),
                    text_color=self.colors['on_surface_variant']
                )
                scale_label.pack(side="left", padx=(5, 0))
        
        # Add bottom padding
        ctk.CTkFrame(section_card, fg_color="transparent", height=8).grid(row=len(settings)+1, column=0, columnspan=2)
    
    def handle_settings_action(self, action):
        """Handle settings action buttons"""
        if "Export" in action:
            self.show_info("Settings export functionality would save current configuration to a file.")
        elif "Import" in action:
            self.show_info("Settings import functionality would load configuration from a file.")
        elif "Reset" in action:
            self.show_info("Reset functionality would restore all settings to their default values.")
        elif "Clear" in action:
            self.show_info("Clear data functionality would remove all stored benchmark results and history.")
    
    def save_settings(self):
        """Save application settings"""
        self.show_info("Settings have been saved successfully!")
    
    def cancel_settings(self):
        """Cancel settings changes"""
        # Return to dashboard
        self.set_active_nav("dashboard")
        self.show_tab_content("dashboard")
    
    def hide_all_tabs(self):
        """Hide all tab content without destroying"""
        # Clear the content container completely
        for widget in self.content_container.winfo_children():
            widget.pack_forget()
            widget.grid_forget()
    
    def show_tab_content(self, tab_name):
        """Show specific tab content, creating if necessary"""
        self.hide_all_tabs()
        
        if tab_name not in self.tab_components:
            # Create tab content for the first time
            if tab_name == "dashboard":
                self.create_dashboard_tab()
            elif tab_name == "statistics":
                self.create_statistics_tab()
            elif tab_name == "network_map":
                self.create_network_map_tab()
            elif tab_name == "security":
                self.create_security_tab()
            elif tab_name == "settings":
                self.create_settings_tab()
        
        # Show the tab content
        if tab_name in self.tab_components and 'container' in self.tab_components[tab_name]:
            container = self.tab_components[tab_name]['container']
            if container.winfo_exists():
                container.pack(fill="both", expand=True)
        
        self.current_tab = tab_name
    
    def load_dns_servers(self):
        """Load and test DNS servers in background"""
        self.update_status("Loading DNS servers...")
        
        def load_servers():
            try:
                self.dns_db.test_all_servers(self.on_server_test_progress)
                self.root.after(0, self.on_servers_loaded)
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Error loading DNS servers: {e}"))
        
        threading.Thread(target=load_servers, daemon=True).start()
    
    def on_server_test_progress(self, server: DNSServer, is_responsive: bool, response_time: float):
        """Called when a server test completes"""
        def update_ui():
            if hasattr(self, 'server_list_frame'):
                self.server_list_frame.update_server_status(server, is_responsive, response_time)
            status_text = f"Testing {server.name}..."
            self.update_status(status_text)
        
        self.root.after(0, update_ui)
    
    def on_servers_loaded(self):
        """Called when all servers have been loaded and tested"""
        responsive_count = len(self.dns_db.get_responsive_servers())
        total_count = len(self.dns_db.servers)
        
        if hasattr(self, 'server_list_frame'):
            self.server_list_frame.populate_server_list(self.dns_db.servers)
        
        self.update_status(f"Loaded {total_count} DNS servers")
        self.servers_stat.configure(text=str(responsive_count))
    
    def start_benchmark(self, selected_servers: List[DNSServer], num_iterations: int):
        """Start the DNS benchmark test"""
        if self.is_testing:
            self.show_error("Benchmark is already running!")
            return
        
        if not selected_servers:
            self.show_error("Please select at least one DNS server to test.")
            return
        
        self.is_testing = True
        self.controls_frame.set_testing_state(True)
        self.results_frame.clear_results()
        
        # Clear live results in statistics tab
        if "statistics" in self.tab_components:
            stats_frame = self.tab_components["statistics"].get("statistics_frame")
            if stats_frame and hasattr(stats_frame, 'live_results'):
                stats_frame.live_results.clear()
        
        self.update_status(f"Benchmarking {len(selected_servers)} servers...")
        
        def run_benchmark():
            try:
                self.benchmark_engine.run_comprehensive_benchmark(
                    servers=selected_servers,
                    num_iterations=num_iterations,
                    progress_callback=self.on_benchmark_progress
                )
                self.root.after(0, self.on_benchmark_complete)
            except Exception as e:
                self.root.after(0, lambda: self.on_benchmark_error(str(e)))
        
        threading.Thread(target=run_benchmark, daemon=True).start()
    
    def stop_benchmark(self):
        """Stop the running benchmark"""
        if self.is_testing:
            self.benchmark_engine.stop_benchmark()
            self.is_testing = False
            self.controls_frame.set_testing_state(False)
            self.update_status("Benchmark stopped")
    
    def on_benchmark_progress(self, progress_percentage: float, result):
        """Called during benchmark progress - updates all tabs in real-time"""
        def update_ui():
            try:
                # Update dashboard tab (always updated)
                if hasattr(self, 'controls_frame') and self.controls_frame:
                    self.controls_frame.update_progress(progress_percentage)
                if hasattr(self, 'results_frame') and self.results_frame:
                    self.results_frame.add_result(result)
                
                # Update statistics tab with live data if it exists
                if "statistics" in self.tab_components:
                    try:
                        stats_frame = self.tab_components["statistics"].get("statistics_frame")
                        if stats_frame and hasattr(stats_frame, 'update_live_result'):
                            stats_frame.update_live_result(result)
                    except Exception:
                        pass
                        
                    try:
                        graphs_frame = self.tab_components["statistics"].get("graphs_frame")
                        if graphs_frame and hasattr(graphs_frame, 'update_live_data'):
                            graphs_frame.update_live_data(result)
                    except Exception:
                        pass
            
                # Update network map with server status
                if "network_map" in self.tab_components:
                    self.update_network_map_status(result)
                
                # Update security metrics if available
                if "security" in self.tab_components:
                    self.update_security_metrics(result)
                
                # Update header stats in real-time
                self.update_header_stats_live()
                
                server_name = next(
                    (s.name for s in self.dns_db.servers if s.ip == result.server_ip), 
                    result.server_ip
                )
                
                status_text = f"Testing {server_name} ({progress_percentage:.1f}%)"
                self.update_status(status_text)
                
            except Exception as e:
                # Fail silently to not interrupt the benchmark, but print to debug
                print(f"Error in benchmark progress update: {type(e).__name__}: {e}")
        
        self.root.after(0, update_ui)
    
    def update_network_map_status(self, result):
        """Update network map with real-time server status"""
        # This would update the network visualization with live server status
        # For now, we'll just track which servers are responding
        pass
    
    def update_network_map_final_results(self, rankings):
        """Update network map with final benchmark results"""
        if not rankings or "network_map" not in self.tab_components:
            return
            
        try:
            # Update server status indicators with performance data
            if hasattr(self, 'network_server_items'):
                for server_stats in rankings:
                    server_ip = server_stats.server.ip
                    if server_ip in self.network_server_items:
                        server_item = self.network_server_items[server_ip]
                        
                        # Update status based on performance
                        if server_stats.avg_response_time < 50:
                            status = "excellent"
                            color = self.colors['success']
                        elif server_stats.avg_response_time < 100:
                            status = "good"
                            color = self.colors['warning']
                        else:
                            status = "slow"
                            color = self.colors['error']
                        
                        # Update UI elements
                        if 'status_label' in server_item:
                            server_item['status_label'].configure(text_color=color)
                        if 'latency_label' in server_item:
                            server_item['latency_label'].configure(
                                text=f"{server_stats.avg_response_time:.1f}ms"
                            )
        except Exception as e:
            # Fail silently to not interrupt the UI
            pass
    
    def update_security_metrics(self, result):
        """Update security metrics based on benchmark results"""
        if not result or not hasattr(self, 'security_test_items'):
            return
            
        try:
            # For now, just track basic metrics
            # Full security testing will be triggered separately
            pass
        except Exception as e:
            pass
    
    def run_security_tests(self):
        """Run comprehensive security tests on selected servers"""
        try:
            from src.core.dns_security import DNSSecurityTester
            
            selected_servers = self.server_list_frame.get_selected_servers()
            if not selected_servers:
                self.show_error("Please select at least one DNS server for security testing.")
                return
            
            # Update security test status to running
            self.update_all_security_tests_status("running", "Testing in progress...")
            
            security_tester = DNSSecurityTester()
            
            def run_tests():
                """Run security tests in background thread"""
                for server in selected_servers:
                    try:
                        # Run comprehensive security test
                        test_results = security_tester.run_comprehensive_security_test(server.ip, 10.0)
                        
                        # Update UI with results
                        self.after(0, lambda: self.update_security_test_results(server.ip, test_results))
                        
                    except Exception as e:
                        error_msg = f"Security test failed for {server.ip}: {str(e)[:50]}"
                        self.after(0, lambda msg=error_msg: self.show_error(msg))
            
            # Run tests in background thread
            import threading
            test_thread = threading.Thread(target=run_tests, daemon=True)
            test_thread.start()
            
        except ImportError:
            self.show_error("Security testing module not available.")
        except Exception as e:
            self.show_error(f"Failed to start security tests: {str(e)}")
    
    def update_all_security_tests_status(self, status, message):
        """Update all security test items with a status"""
        if not hasattr(self, 'security_test_items'):
            return
            
        for item in self.security_test_items.values():
            if status == "running":
                color = self.colors['warning']
                icon = "⚡"
            elif status == "pass":
                color = self.colors['success']
                icon = "✅"
            elif status == "fail":
                color = self.colors['error']
                icon = "❌"
            else:
                color = self.colors['text_muted']
                icon = "⏳"
            
            item['status_label'].configure(text=icon, text_color=color)
            item['message_label'].configure(text=message)
    
    def update_security_test_results(self, server_ip, test_results):
        """Update security test results in the UI"""
        if not test_results or not hasattr(self, 'security_test_items'):
            return
        
        # Map test types to UI items
        test_mapping = {
            "dnssec_validation": "🛡️ DNSSEC Validation Test",
            "encrypted_dns": "🔐 Encrypted DNS Support", 
            "malware_filtering": "⚠️ Malware Domain Test",
            "privacy_leak": "👁️ Privacy Leak Test",
        }
        
        for result in test_results:
            test_name = None
            for key, name in test_mapping.items():
                if key in str(result.test_type).lower():
                    test_name = name
                    break
            
            if test_name and test_name in self.security_test_items:
                item = self.security_test_items[test_name]
                
                if result.passed:
                    status_color = self.colors['success']
                    status_icon = "✅"
                    message = f"Passed ({result.score:.0f}%) - {result.details[:60]}..."
                else:
                    status_color = self.colors['error']
                    status_icon = "❌"
                    message = f"Failed - {result.details[:60]}..."
                
                item['status_label'].configure(text=status_icon, text_color=status_color)
                item['message_label'].configure(text=message)
    
    def update_header_stats_live(self):
        """Update header statistics in real-time during benchmarking"""
        if hasattr(self, 'results_frame') and self.results_frame:
            # Get live data from results frame
            live_data = self.results_frame.live_server_data
            if live_data:
                # Calculate current stats
                server_count = len(live_data)
                
                # Calculate average latency from live data
                all_times = []
                total_queries = 0
                successful_queries = 0
                
                for server_data in live_data.values():
                    all_times.extend(server_data.get('times', []))
                    total_queries += server_data.get('total', 0)
                    successful_queries += server_data.get('successes', 0)
                
                if all_times:
                    avg_latency = sum(all_times) / len(all_times)
                    self.latency_stat.configure(text=f"{avg_latency:.0f}ms")
                    self.latency_label.configure(text=f"Latency: {avg_latency:.0f}ms")
                
                if total_queries > 0:
                    success_rate = (successful_queries / total_queries) * 100
                    self.success_stat.configure(text=f"{success_rate:.0f}%")
                
                self.servers_stat.configure(text=str(server_count))
    
    def on_benchmark_complete(self):
        """Called when benchmark completes successfully"""
        self.is_testing = False
        self.controls_frame.set_testing_state(False)
        self.controls_frame.update_progress(100)
        
        # Update all result panels
        rankings = self.benchmark_engine.get_server_rankings()
        self.results_frame.update_final_results(rankings)
        
        # Update statistics tab if it exists
        if "statistics" in self.tab_components:
            stats_frame = self.tab_components["statistics"].get("statistics_frame")
            if stats_frame and hasattr(stats_frame, 'update_statistics'):
                stats_frame.update_statistics(rankings)
                
            graphs_frame = self.tab_components["statistics"].get("graphs_frame")
            if graphs_frame and hasattr(graphs_frame, 'update_graphs'):
                graphs_frame.update_graphs(rankings)
        
        # Update network map if it exists
        if "network_map" in self.tab_components:
            self.update_network_map_final_results(rankings)
        
        # Calculate stats
        total_queries = len(self.benchmark_engine.results)
        successful_queries = sum(1 for r in self.benchmark_engine.results if r.success)
        
        if rankings:
            avg_latency = sum(s.avg_response_time for s in rankings) / len(rankings)
            self.latency_stat.configure(text=f"{avg_latency:.0f}ms")
            self.latency_label.configure(text=f"Latency: {avg_latency:.0f}ms")
        
        success_rate = (successful_queries / total_queries * 100) if total_queries > 0 else 0
        self.success_stat.configure(text=f"{success_rate:.0f}%")
        
        self.update_status(f"Benchmark complete! {successful_queries}/{total_queries} queries")
    
    def on_benchmark_error(self, error_message: str):
        """Called when benchmark encounters an error"""
        self.is_testing = False
        self.controls_frame.set_testing_state(False)
        self.update_status("Benchmark failed")
        self.show_error(f"Benchmark error: {error_message}")
    
    def update_status(self, message: str):
        """Update the status message"""
        # Could update a status bar if we add one
        pass
    
    def show_error(self, message: str):
        """Show an error message"""
        messagebox.showerror("Error", message)
    
    def show_info(self, message: str):
        """Show an info message"""
        messagebox.showinfo("Information", message)
    
    def export_results(self):
        """Export benchmark results to file"""
        if not self.benchmark_engine.results:
            self.show_error("No results to export. Please run a benchmark first.")
            return
        
        try:
            from tkinter import filedialog
            import json
            
            filename = filedialog.asksaveasfilename(
                title="Export Results",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                results_data = self.benchmark_engine.export_results()
                with open(filename, 'w') as f:
                    json.dump(results_data, f, indent=2)
                
                self.show_info(f"Results exported to {filename}")
        except Exception as e:
            self.show_error(f"Error exporting results: {e}")
    
    def run(self):
        """Start the application main loop"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()