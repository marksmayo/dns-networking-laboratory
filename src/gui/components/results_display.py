"""
Results Display Component - DNS Pulse Design
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import List, Optional
from src.core.dns_benchmark import ServerStatistics, BenchmarkResult

class ResultsDisplayFrame(ctk.CTkFrame):
    """Frame for displaying benchmark results in DNS Pulse style"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.result_count = 0
        self.live_server_data = {}
        self.current_sort_column = "avg_time"
        self.sort_reverse = False
        
        # DNS Pulse exact color scheme
        self.colors = {
            'surface': '#10131a',
            'surface_container': '#1d2026',
            'surface_container_high': '#272a31',
            'primary': '#00F0FF',
            'secondary': '#9D4EDD',
            'tertiary': '#2DE2E6',
            'on_surface': '#e1e2eb',
            'on_surface_variant': '#b9cacb',
            'text_muted': '#849495',
            'error': '#ffb4ab',
            'success': '#00ff94',
            'warning': '#ffd700',
            'outline_variant': '#3b494b',
        }
        
        self.configure(fg_color="transparent")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the results display UI with DNS Pulse design"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Modern header
        self.create_header()
        
        # Main results table
        self.create_results_table()
        
        # Live stats footer
        self.create_live_stats()
    
    def create_header(self):
        """Create modern header with DNS Pulse styling"""
        header = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)
        
        # Title with icon
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="⚡ LIVE RESULTS",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(side="left")
        
        # Results count badge
        self.results_count_badge = ctk.CTkLabel(
            title_frame,
            text="0",
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            text_color=self.colors['tertiary'],
            fg_color=self.colors['surface_container_high'],
            corner_radius=10,
            width=30,
            height=20
        )
        self.results_count_badge.pack(side="left", padx=(10, 0))
        
        # Controls frame
        controls_frame = ctk.CTkFrame(header, fg_color="transparent")
        controls_frame.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        
        # Sort controls
        sort_label = ctk.CTkLabel(
            controls_frame,
            text="SORT BY:",
            font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
            text_color=self.colors['text_muted']
        )
        sort_label.pack(side="left", padx=(0, 8))
        
        self.sort_var = ctk.StringVar(value="Average Time")
        self.sort_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=["Average Time", "Reliability", "Min Time", "Provider", "Server Name"],
            variable=self.sort_var,
            width=130,
            height=32,
            font=ctk.CTkFont(family="Arial", size=11),
            fg_color=self.colors['surface_container_high'],
            button_color=self.colors['secondary'],
            button_hover_color=self.colors['primary'],
            dropdown_fg_color=self.colors['surface_container_high'],
            text_color=self.colors['on_surface_variant'],
            corner_radius=6,
            command=self.on_sort_changed
        )
        self.sort_menu.pack(side="left")
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            controls_frame,
            text="🗑",
            width=35,
            height=32,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color=self.colors['surface_container_high'],
            hover_color=self.colors['error'],
            text_color=self.colors['text_muted'],
            corner_radius=6,
            command=self.clear_results
        )
        self.clear_button.pack(side="left", padx=(8, 0))
    
    def create_results_table(self):
        """Create modern results table with glassmorphic design"""
        # Table container
        table_container = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        table_container.grid(row=1, column=0, sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)
        
        # Custom styled Treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure dark theme for Treeview
        style.configure("DNSPulse.Treeview",
            background=self.colors['surface_container_high'],
            foreground=self.colors['on_surface'],
            fieldbackground=self.colors['surface_container_high'],
            borderwidth=0,
            font=('Arial', 11)
        )
        
        style.configure("DNSPulse.Treeview.Heading",
            background=self.colors['surface_container'],
            foreground=self.colors['primary'],
            borderwidth=1,
            relief="flat",
            font=('Arial', 10, 'bold')
        )
        
        style.map("DNSPulse.Treeview",
            background=[('selected', self.colors['secondary'])],
            foreground=[('selected', self.colors['on_surface'])]
        )
        
        style.map("DNSPulse.Treeview.Heading",
            background=[('active', self.colors['primary'])]
        )
        
        # Create tree frame
        self.tree_frame = tk.Frame(table_container, bg=self.colors['surface_container_high'])
        self.tree_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        
        # Define columns
        columns = ("rank", "name", "ip", "provider", "avg_time", "min_time", "reliability", "status")
        
        self.results_tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings",
            height=20,
            style="DNSPulse.Treeview"
        )
        
        # Configure columns
        column_configs = {
            "rank": ("RANK", 60),
            "name": ("SERVER", 180),
            "ip": ("IP ADDRESS", 120),
            "provider": ("PROVIDER", 100),
            "avg_time": ("AVG (ms)", 80),
            "min_time": ("MIN (ms)", 80),
            "reliability": ("UPTIME", 80),
            "status": ("STATUS", 80)
        }
        
        for col, (text, width) in column_configs.items():
            self.results_tree.heading(col, text=text, anchor="w")
            self.results_tree.column(col, width=width, anchor="w", stretch=False)
        
        # Scrollbars with custom styling
        v_scrollbar = ttk.Scrollbar(
            self.tree_frame,
            orient="vertical",
            command=self.results_tree.yview
        )
        self.results_tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Grid layout
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind double-click for sorting
        self.results_tree.bind("<Double-1>", self.on_column_double_click)
    
    def create_live_stats(self):
        """Create live statistics footer"""
        stats_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=50
        )
        stats_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        stats_frame.grid_propagate(False)
        stats_frame.grid_columnconfigure(1, weight=1)
        
        # Live indicator
        live_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        live_frame.grid(row=0, column=0, padx=20, pady=12, sticky="w")
        
        self.live_dot = ctk.CTkLabel(
            live_frame,
            text="●",
            font=ctk.CTkFont(size=16),
            text_color=self.colors['success']
        )
        self.live_dot.pack(side="left")
        
        self.live_label = ctk.CTkLabel(
            live_frame,
            text="LIVE MONITORING",
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            text_color=self.colors['on_surface_variant']
        )
        self.live_label.pack(side="left", padx=(5, 0))
        
        # Stats metrics
        metrics_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        metrics_frame.grid(row=0, column=1, padx=20, pady=12, sticky="e")
        
        self.stats_label = ctk.CTkLabel(
            metrics_frame,
            text="0 SERVERS • 0 QUERIES • 0ms AVG",
            font=ctk.CTkFont(family="Arial", size=11),
            text_color=self.colors['text_muted']
        )
        self.stats_label.pack()
    
    def add_result(self, result: BenchmarkResult):
        """Add a new benchmark result"""
        if not result.success:
            return
        
        server_ip = result.server_ip
        
        # Update live server data
        if server_ip not in self.live_server_data:
            self.live_server_data[server_ip] = {
                'times': [],
                'successes': 0,
                'total': 0,
                'server_name': '',
                'provider': ''
            }
        
        data = self.live_server_data[server_ip]
        data['times'].append(result.response_time)
        data['successes'] += 1 if result.success else 0
        data['total'] += 1
        
        # Find server details
        for server in self.app.dns_db.servers:
            if server.ip == server_ip:
                data['server_name'] = server.name
                data['provider'] = server.provider
                break
        
        self.update_live_display()
        self.result_count += 1
        self.results_count_badge.configure(text=str(len(self.live_server_data)))
    
    def update_live_display(self):
        """Update the live results display"""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Calculate stats and sort
        ranked_servers = []
        for ip, data in self.live_server_data.items():
            if data['times']:
                avg_time = sum(data['times']) / len(data['times'])
                min_time = min(data['times'])
                reliability = (data['successes'] / data['total']) * 100
                
                ranked_servers.append({
                    'ip': ip,
                    'name': data['server_name'],
                    'provider': data['provider'],
                    'avg_time': avg_time,
                    'min_time': min_time,
                    'reliability': reliability,
                    'status': 'ONLINE' if reliability > 90 else 'DEGRADED'
                })
        
        # Sort by average time
        ranked_servers.sort(key=lambda x: x['avg_time'])
        
        # Populate tree
        for rank, server in enumerate(ranked_servers, 1):
            # Color code status
            if server['avg_time'] < 20:
                status_color = 'green'
            elif server['avg_time'] < 50:
                status_color = 'orange'
            else:
                status_color = 'red'
            
            values = (
                f"#{rank}",
                server['name'],
                server['ip'],
                server['provider'].upper(),
                f"{server['avg_time']:.1f}",
                f"{server['min_time']:.1f}",
                f"{server['reliability']:.1f}%",
                server['status']
            )
            
            item = self.results_tree.insert("", "end", values=values)
            # Tag for styling (would need custom implementation for colors in Treeview)
        
        # Update stats
        if ranked_servers:
            avg_latency = sum(s['avg_time'] for s in ranked_servers) / len(ranked_servers)
            total_queries = sum(data['total'] for data in self.live_server_data.values())
            self.stats_label.configure(
                text=f"{len(ranked_servers)} SERVERS • {total_queries} QUERIES • {avg_latency:.0f}ms AVG"
            )
    
    def update_final_results(self, rankings: List[ServerStatistics]):
        """Update with final benchmark results"""
        # Clear live data and populate with final results
        self.live_server_data.clear()
        
        for rank, server in enumerate(rankings, 1):
            self.live_server_data[server.ip] = {
                'times': [server.avg_response_time],
                'successes': 1,
                'total': 1,
                'server_name': server.name,
                'provider': server.provider
            }
        
        self.update_live_display()
        self.results_count_badge.configure(text=str(len(rankings)))
    
    def clear_results(self):
        """Clear all results"""
        self.live_server_data.clear()
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.result_count = 0
        self.results_count_badge.configure(text="0")
        self.stats_label.configure(text="0 SERVERS • 0 QUERIES • 0ms AVG")
    
    def on_sort_changed(self, value):
        """Handle sort option change"""
        self.update_live_display()
    
    def on_column_double_click(self, event):
        """Handle column double-click for sorting"""
        region = self.results_tree.identify("region", event.x, event.y)
        if region == "heading":
            col = self.results_tree.identify_column(event.x, event.y)
            self.sort_by_column(int(col) - 1)
    
    def sort_by_column(self, col_index):
        """Sort results by column"""
        self.update_live_display()