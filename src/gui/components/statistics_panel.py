"""
Statistics Panel Component - DNS Pulse Design
"""

import customtkinter as ctk
import tkinter as tk
from typing import List, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from src.core.dns_benchmark import ServerStatistics

class StatisticsPanel(ctk.CTkFrame):
    """Comprehensive statistics panel with DNS Pulse design"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.current_stats = []
        
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
        self.live_results = {}  # Store live benchmark results
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the statistics UI with DNS Pulse design"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Main content area
        content_container = ctk.CTkFrame(self, fg_color="transparent")
        content_container.grid(row=1, column=0, sticky="nsew")
        content_container.grid_columnconfigure(0, weight=2)
        content_container.grid_columnconfigure(1, weight=3)
        content_container.grid_rowconfigure(0, weight=1)
        
        # Left panel - Key metrics and summaries
        self.create_metrics_panel(content_container)
        
        # Right panel - Charts and visualizations
        self.create_charts_panel(content_container)
    
    def create_header(self):
        """Create modern header"""
        header = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header.grid_propagate(False)
        
        title_label = ctk.CTkLabel(
            header,
            text="📊 DETAILED STATISTICS",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(expand=True)
    
    def create_metrics_panel(self, parent):
        """Create key metrics panel"""
        metrics_panel = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_container'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        metrics_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        metrics_panel.grid_columnconfigure(0, weight=1)
        
        # Panel title
        title_frame = ctk.CTkFrame(metrics_panel, fg_color="transparent", height=50)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))
        title_frame.grid_propagate(False)
        
        ctk.CTkLabel(
            title_frame,
            text="KEY METRICS",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color=self.colors['secondary']
        ).pack(side="left")
        
        # Scrollable metrics container
        self.metrics_container = ctk.CTkScrollableFrame(
            metrics_panel,
            fg_color="transparent"
        )
        self.metrics_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.metrics_container.grid_columnconfigure(0, weight=1)
        
        # Performance Overview Card
        self.create_performance_card()
        
        # Top Performers Card
        self.create_top_performers_card()
        
        # Reliability Analysis Card
        self.create_reliability_card()
        
        # Geographic Distribution Card
        self.create_geographic_card()
    
    def create_performance_card(self):
        """Create performance overview card"""
        card = ctk.CTkFrame(
            self.metrics_container,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        card.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        card.grid_columnconfigure(1, weight=1)
        
        # Card header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(12, 8))
        
        ctk.CTkLabel(
            header,
            text="⚡ PERFORMANCE OVERVIEW",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['primary']
        ).pack(side="left")
        
        # Metrics
        self.fastest_server_label = self.create_metric_row(card, "Fastest Server:", "--", 1)
        self.avg_latency_label = self.create_metric_row(card, "Average Latency:", "--ms", 2)
        self.median_latency_label = self.create_metric_row(card, "Median Latency:", "--ms", 3)
        self.slowest_server_label = self.create_metric_row(card, "Slowest Server:", "--", 4)
        
    def create_top_performers_card(self):
        """Create top performers card"""
        card = ctk.CTkFrame(
            self.metrics_container,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        card.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Card header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(12, 8))
        
        ctk.CTkLabel(
            header,
            text="🏆 TOP PERFORMERS",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['success']
        ).pack(side="left")
        
        # Top 5 servers list
        self.top_servers_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.top_servers_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 12))
        
    def create_reliability_card(self):
        """Create reliability analysis card"""
        card = ctk.CTkFrame(
            self.metrics_container,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        card.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        # Card header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(12, 8))
        
        ctk.CTkLabel(
            header,
            text="🛡 RELIABILITY ANALYSIS",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['warning']
        ).pack(side="left")
        
        # Reliability metrics
        self.success_rate_label = self.create_metric_row(card, "Overall Success Rate:", "--", 1)
        self.timeout_count_label = self.create_metric_row(card, "Timeout Events:", "--", 2)
        self.error_rate_label = self.create_metric_row(card, "Error Rate:", "--", 3)
        
    def create_geographic_card(self):
        """Create geographic distribution card"""
        card = ctk.CTkFrame(
            self.metrics_container,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        card.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        # Card header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(12, 8))
        
        ctk.CTkLabel(
            header,
            text="🌍 GEOGRAPHIC DISTRIBUTION",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['tertiary']
        ).pack(side="left")
        
        # Geographic metrics
        self.create_metric_row(card, "Provider Count:", "--", 1)
        self.create_metric_row(card, "Global Coverage:", "--", 2)
        self.create_metric_row(card, "Best Region:", "--", 3)
    
    def create_metric_row(self, parent, label_text, value_text, row):
        """Create a metric row"""
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=ctk.CTkFont(family="Arial", size=11),
            text_color=self.colors['on_surface_variant']
        )
        label.grid(row=row, column=0, sticky="w", padx=(15, 10), pady=2)
        
        value = ctk.CTkLabel(
            parent,
            text=value_text,
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            text_color=self.colors['on_surface']
        )
        value.grid(row=row, column=1, sticky="e", padx=(10, 15), pady=2)
        
        return value
    
    def create_charts_panel(self, parent):
        """Create charts and visualizations panel"""
        charts_panel = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_container'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        charts_panel.grid(row=0, column=1, sticky="nsew")
        charts_panel.grid_columnconfigure(0, weight=1)
        charts_panel.grid_rowconfigure(1, weight=1)
        
        # Panel title
        title_frame = ctk.CTkFrame(charts_panel, fg_color="transparent", height=50)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))
        title_frame.grid_propagate(False)
        
        ctk.CTkLabel(
            title_frame,
            text="PERFORMANCE ANALYTICS",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color=self.colors['secondary']
        ).pack(side="left")
        
        # Chart container
        chart_container = ctk.CTkFrame(
            charts_panel,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8
        )
        chart_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        chart_container.grid_columnconfigure(0, weight=1)
        chart_container.grid_rowconfigure(0, weight=1)
        chart_container.grid_rowconfigure(1, weight=1)
        
        # Create matplotlib figures
        self.create_response_time_chart(chart_container)
        self.create_distribution_chart(chart_container)
    
    def create_response_time_chart(self, parent):
        """Create response time comparison chart"""
        # Chart frame
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        chart_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        chart_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_rowconfigure(0, weight=1)
        
        # Create matplotlib figure with dark theme
        self.response_fig = Figure(figsize=(8, 4), facecolor=self.colors['surface_container_high'])
        self.response_fig.patch.set_facecolor(self.colors['surface_container_high'])
        
        self.response_ax = self.response_fig.add_subplot(111)
        self.response_ax.set_facecolor(self.colors['surface_container_high'])
        
        # Style the chart
        self.response_ax.tick_params(colors=self.colors['on_surface_variant'])
        self.response_ax.spines['bottom'].set_color(self.colors['outline_variant'])
        self.response_ax.spines['top'].set_color(self.colors['outline_variant'])
        self.response_ax.spines['left'].set_color(self.colors['outline_variant'])
        self.response_ax.spines['right'].set_color(self.colors['outline_variant'])
        
        # Create canvas
        self.response_canvas = FigureCanvasTkAgg(self.response_fig, chart_frame)
        self.response_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Initial empty chart
        self.response_ax.set_title("Response Time Comparison", color=self.colors['primary'], fontsize=12, weight='bold')
        self.response_ax.set_xlabel("DNS Servers", color=self.colors['on_surface_variant'])
        self.response_ax.set_ylabel("Response Time (ms)", color=self.colors['on_surface_variant'])
    
    def create_distribution_chart(self, parent):
        """Create response time distribution chart"""
        # Chart frame
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        chart_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        chart_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_rowconfigure(0, weight=1)
        
        # Create matplotlib figure
        self.dist_fig = Figure(figsize=(8, 4), facecolor=self.colors['surface_container_high'])
        self.dist_fig.patch.set_facecolor(self.colors['surface_container_high'])
        
        self.dist_ax = self.dist_fig.add_subplot(111)
        self.dist_ax.set_facecolor(self.colors['surface_container_high'])
        
        # Style the chart
        self.dist_ax.tick_params(colors=self.colors['on_surface_variant'])
        self.dist_ax.spines['bottom'].set_color(self.colors['outline_variant'])
        self.dist_ax.spines['top'].set_color(self.colors['outline_variant'])
        self.dist_ax.spines['left'].set_color(self.colors['outline_variant'])
        self.dist_ax.spines['right'].set_color(self.colors['outline_variant'])
        
        # Create canvas
        self.dist_canvas = FigureCanvasTkAgg(self.dist_fig, chart_frame)
        self.dist_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Initial empty chart
        self.dist_ax.set_title("Response Time Distribution", color=self.colors['secondary'], fontsize=12, weight='bold')
        self.dist_ax.set_xlabel("Response Time (ms)", color=self.colors['on_surface_variant'])
        self.dist_ax.set_ylabel("Frequency", color=self.colors['on_surface_variant'])
    
    def update_statistics(self, rankings: List[ServerStatistics]):
        """Update statistics with new data"""
        if not rankings:
            return
        
        self.current_stats = rankings
        
        # Update key metrics
        self.update_performance_metrics(rankings)
        self.update_top_performers(rankings)
        self.update_reliability_metrics(rankings)
        self.update_charts(rankings)
    
    def update_performance_metrics(self, rankings: List[ServerStatistics]):
        """Update performance metrics"""
        if not rankings:
            return
        
        response_times = [s.avg_response_time for s in rankings if s.avg_response_time > 0]
        
        if response_times:
            fastest = min(rankings, key=lambda s: s.avg_response_time)
            slowest = max(rankings, key=lambda s: s.avg_response_time)
            avg_latency = sum(response_times) / len(response_times)
            median_latency = sorted(response_times)[len(response_times) // 2]
            
            self.fastest_server_label.configure(text=f"{fastest.name} ({fastest.avg_response_time:.1f}ms)")
            self.slowest_server_label.configure(text=f"{slowest.name} ({slowest.avg_response_time:.1f}ms)")
            self.avg_latency_label.configure(text=f"{avg_latency:.1f}ms")
            self.median_latency_label.configure(text=f"{median_latency:.1f}ms")
    
    def update_top_performers(self, rankings: List[ServerStatistics]):
        """Update top performers list"""
        # Clear existing top servers
        for widget in self.top_servers_frame.winfo_children():
            widget.destroy()
        
        # Show top 5 servers
        top_5 = rankings[:5]
        for i, server in enumerate(top_5):
            rank_frame = ctk.CTkFrame(self.top_servers_frame, fg_color="transparent")
            rank_frame.grid(row=i, column=0, sticky="ew", pady=1)
            rank_frame.grid_columnconfigure(1, weight=1)
            
            # Rank number with color
            rank_colors = [self.colors['warning'], self.colors['text_muted'], 
                          self.colors['tertiary'], self.colors['on_surface_variant'], 
                          self.colors['on_surface_variant']]
            
            ctk.CTkLabel(
                rank_frame,
                text=f"#{i+1}",
                font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
                text_color=rank_colors[i] if i < len(rank_colors) else self.colors['on_surface_variant'],
                width=30
            ).grid(row=0, column=0, sticky="w")
            
            ctk.CTkLabel(
                rank_frame,
                text=f"{server.name}",
                font=ctk.CTkFont(family="Arial", size=10),
                text_color=self.colors['on_surface']
            ).grid(row=0, column=1, sticky="w", padx=(5, 0))
            
            ctk.CTkLabel(
                rank_frame,
                text=f"{server.avg_response_time:.1f}ms",
                font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
                text_color=self.colors['primary']
            ).grid(row=0, column=2, sticky="e")
    
    def update_reliability_metrics(self, rankings: List[ServerStatistics]):
        """Update reliability metrics"""
        if not rankings:
            return
        
        # Calculate reliability stats
        total_queries = len(rankings) * 10  # Assuming 10 queries per server
        timeout_count = sum(1 for s in rankings if s.avg_response_time > 1000)  # Consider >1s as timeout
        success_rate = ((total_queries - timeout_count) / total_queries) * 100 if total_queries > 0 else 0
        error_rate = 100 - success_rate
        
        self.success_rate_label.configure(text=f"{success_rate:.1f}%")
        self.timeout_count_label.configure(text=str(timeout_count))
        self.error_rate_label.configure(text=f"{error_rate:.1f}%")
    
    def update_charts(self, rankings: List[ServerStatistics]):
        """Update all charts with new data"""
        self.update_response_time_chart(rankings)
        self.update_distribution_chart(rankings)
    
    def update_response_time_chart(self, rankings: List[ServerStatistics]):
        """Update the response time comparison chart"""
        if not rankings:
            return
        
        self.response_ax.clear()
        
        # Prepare data
        names = [s.name[:10] + '...' if len(s.name) > 10 else s.name for s in rankings[:10]]
        times = [s.avg_response_time for s in rankings[:10]]
        
        # Create gradient colors
        colors = []
        for time in times:
            if time < 20:
                colors.append(self.colors['success'])
            elif time < 50:
                colors.append(self.colors['tertiary'])
            elif time < 100:
                colors.append(self.colors['warning'])
            else:
                colors.append(self.colors['error'])
        
        # Create bar chart
        bars = self.response_ax.bar(names, times, color=colors, alpha=0.8)
        
        # Style the chart
        self.response_ax.set_title("Response Time Comparison (Top 10)", 
                                 color=self.colors['primary'], fontsize=12, weight='bold')
        self.response_ax.set_xlabel("DNS Servers", color=self.colors['on_surface_variant'])
        self.response_ax.set_ylabel("Response Time (ms)", color=self.colors['on_surface_variant'])
        
        # Rotate x-axis labels
        plt.setp(self.response_ax.get_xticklabels(), rotation=45, ha='right')
        
        # Style axes
        self.response_ax.tick_params(colors=self.colors['on_surface_variant'])
        for spine in self.response_ax.spines.values():
            spine.set_color(self.colors['outline_variant'])
        
        self.response_fig.tight_layout()
        self.response_canvas.draw()
    
    def update_distribution_chart(self, rankings: List[ServerStatistics]):
        """Update the response time distribution chart"""
        if not rankings:
            return
        
        self.dist_ax.clear()
        
        # Prepare data
        times = [s.avg_response_time for s in rankings]
        
        # Create histogram
        n, bins, patches = self.dist_ax.hist(times, bins=20, alpha=0.7, 
                                           color=self.colors['secondary'], 
                                           edgecolor=self.colors['primary'])
        
        # Color patches based on response time ranges
        for i, patch in enumerate(patches):
            if bins[i] < 20:
                patch.set_facecolor(self.colors['success'])
            elif bins[i] < 50:
                patch.set_facecolor(self.colors['tertiary'])
            elif bins[i] < 100:
                patch.set_facecolor(self.colors['warning'])
            else:
                patch.set_facecolor(self.colors['error'])
        
        # Style the chart
        self.dist_ax.set_title("Response Time Distribution", 
                             color=self.colors['secondary'], fontsize=12, weight='bold')
        self.dist_ax.set_xlabel("Response Time (ms)", color=self.colors['on_surface_variant'])
        self.dist_ax.set_ylabel("Frequency", color=self.colors['on_surface_variant'])
        
        # Style axes
        self.dist_ax.tick_params(colors=self.colors['on_surface_variant'])
        for spine in self.dist_ax.spines.values():
            spine.set_color(self.colors['outline_variant'])
        
        self.dist_fig.tight_layout()
        self.dist_canvas.draw()
    
    def update_live_result(self, result):
        """Update statistics with a single live benchmark result"""
        if not result.success:
            return
            
        try:
            server_ip = result.server_ip
            response_time = result.response_time
            
            # Accumulate live results
            if server_ip not in self.live_results:
                self.live_results[server_ip] = {
                    'times': [],
                    'name': server_ip,  # Default to IP, could be enhanced
                    'total': 0,
                    'successful': 0
                }
            
            data = self.live_results[server_ip]
            data['times'].append(response_time)
            data['total'] += 1
            data['successful'] += 1
            
            # Update live performance metrics (throttled updates)
            if len(self.live_results) > 0 and data['total'] % 5 == 0:  # Update every 5 results
                self.update_live_performance_metrics()
                
        except Exception as e:
            # Fail silently to not interrupt the benchmark
            pass
    
    def update_live_performance_metrics(self):
        """Update performance metrics with live data"""
        try:
            if not self.live_results:
                return
                
            # Calculate live stats
            all_times = []
            for data in self.live_results.values():
                all_times.extend(data['times'])
            
            if all_times and hasattr(self, 'fastest_server_label'):
                # Find current fastest
                fastest_avg = float('inf')
                fastest_name = ""
                slowest_avg = 0
                slowest_name = ""
                
                for ip, data in self.live_results.items():
                    if data['times']:
                        avg_time = sum(data['times']) / len(data['times'])
                        if avg_time < fastest_avg:
                            fastest_avg = avg_time
                            fastest_name = data['name']
                        if avg_time > slowest_avg:
                            slowest_avg = avg_time
                            slowest_name = data['name']
                
                # Update labels if they exist
                if hasattr(self, 'fastest_server_label'):
                    self.fastest_server_label.configure(text=f"{fastest_name} ({fastest_avg:.1f}ms)")
                if hasattr(self, 'slowest_server_label'):
                    self.slowest_server_label.configure(text=f"{slowest_name} ({slowest_avg:.1f}ms)")
                if hasattr(self, 'avg_latency_label'):
                    avg_latency = sum(all_times) / len(all_times)
                    self.avg_latency_label.configure(text=f"{avg_latency:.1f}ms")
                if hasattr(self, 'median_latency_label'):
                    sorted_times = sorted(all_times)
                    median_latency = sorted_times[len(sorted_times) // 2]
                    self.median_latency_label.configure(text=f"{median_latency:.1f}ms")
                    
        except Exception as e:
            # Fail silently to not interrupt the benchmark
            pass