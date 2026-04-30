"""
Graphs Panel Component - DNS Pulse Design
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import List, Dict
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from src.core.dns_benchmark import ServerStatistics

# Set DNS Pulse dark theme for matplotlib
mplstyle.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#10131a',
    'axes.facecolor': '#1d2026',
    'axes.edgecolor': '#3b494b',
    'axes.labelcolor': '#e1e2eb',
    'text.color': '#e1e2eb',
    'xtick.color': '#b9cacb',
    'ytick.color': '#b9cacb',
    'grid.color': '#3b494b',
    'grid.alpha': 0.3,
    'font.family': 'Arial'
})

class GraphsPanel(ctk.CTkFrame):
    """Advanced panel for displaying real-time graphs and visualizations with DNS Pulse design"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # DNS Pulse exact color scheme from Stitch design
        self.colors = {
            # Core surfaces
            'surface': '#10131a',                    # Main background
            'surface_dim': '#0b0e14',                # Darkest background
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
            'outline_variant': '#3b494b',            # Subtle borders
        }
        
        # Configure frame styling
        self.configure(
            fg_color="transparent",
            corner_radius=0
        )
        
        self.setup_ui()
        self.current_data = []
    
    def setup_ui(self):
        """Setup the graphs panel UI"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header with DNS Pulse styling
        header_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=60
        )
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📈 PERFORMANCE GRAPHS",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=self.colors['primary']
        )
        title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Chart type selector with DNS Pulse styling
        self.chart_var = ctk.StringVar(value="Response Times")
        chart_menu = ctk.CTkOptionMenu(
            header_frame,
            values=[
                "Response Times",
                "Response Distribution", 
                "Provider Comparison",
                "Reliability vs Speed",
                "Live Performance"
            ],
            variable=self.chart_var,
            width=200,
            height=32,
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            fg_color=self.colors['surface_container_high'],
            button_color=self.colors['secondary'],
            button_hover_color=self.colors['primary'],
            dropdown_fg_color=self.colors['surface_container_high'],
            text_color=self.colors['on_surface_variant'],
            corner_radius=6,
            command=self.on_chart_type_changed
        )
        chart_menu.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        
        # Create matplotlib figure
        self.create_matplotlib_frame()
    
    def create_matplotlib_frame(self):
        """Create the matplotlib canvas"""
        # Main canvas frame with DNS Pulse styling
        canvas_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        
        # Create figure with DNS Pulse colors
        self.fig = Figure(figsize=(12, 8), facecolor=self.colors['surface_container'])
        self.fig.patch.set_facecolor(self.colors['surface_container'])
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add navigation toolbar with DNS Pulse styling
        toolbar_frame = tk.Frame(canvas_frame, bg=self.colors['surface_container_high'])
        toolbar_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.config(bg=self.colors['surface_container_high'])
        self.toolbar.update()
        
        # Initialize with placeholder
        self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder when no data available"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(self.colors['surface_container_high'])
        
        ax.text(0.5, 0.5, '📊 Performance Charts\n\nStart a benchmark to see real-time visualizations!\n\n• Response time comparisons\n• Distribution histograms\n• Provider performance analysis\n• Reliability vs Speed scatter plots',
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes,
                fontsize=14,
                color=self.colors['text_muted'],
                bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['surface_container'], alpha=0.8))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        self.canvas.draw()
    
    def update_graphs(self, server_rankings: List[ServerStatistics]):
        """Update graphs with new data"""
        if not server_rankings:
            self.show_placeholder()
            return
        
        # Filter valid data
        valid_servers = [s for s in server_rankings if s.response_times]
        if not valid_servers:
            self.show_placeholder()
            return
        
        self.current_data = valid_servers
        chart_type = self.chart_var.get()
        
        if chart_type == "Response Times":
            self.create_response_times_chart()
        elif chart_type == "Response Distribution":
            self.create_distribution_chart()
        elif chart_type == "Provider Comparison":
            self.create_provider_comparison_chart()
        elif chart_type == "Reliability vs Speed":
            self.create_reliability_speed_chart()
        elif chart_type == "Live Performance":
            self.create_live_performance_chart()
        
        self.canvas.draw()
    
    def create_response_times_chart(self):
        """Create response times bar chart"""
        self.fig.clear()
        
        # Sort by avg response time
        sorted_servers = sorted(self.current_data, key=lambda x: x.avg_response_time)[:15]  # Top 15
        
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(self.colors['surface_container_high'])
        
        names = [s.server.name[:20] for s in sorted_servers]
        avg_times = [s.avg_response_time for s in sorted_servers]
        min_times = [s.min_response_time for s in sorted_servers]
        max_times = [s.max_response_time for s in sorted_servers]
        
        x = np.arange(len(names))
        width = 0.25
        
        bars1 = ax.bar(x - width, min_times, width, label='Min', color=self.colors['success'], alpha=0.8)
        bars2 = ax.bar(x, avg_times, width, label='Avg', color=self.colors['primary'], alpha=0.8)
        bars3 = ax.bar(x + width, max_times, width, label='Max', color=self.colors['error'], alpha=0.8)
        
        ax.set_ylabel('Response Time (ms)', fontweight='bold')
        ax.set_title('🚀 DNS Server Response Times', fontweight='bold', fontsize=14, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{height:.1f}ms', ha='center', va='bottom', fontsize=8)
        
        self.fig.tight_layout()
    
    def create_distribution_chart(self):
        """Create response time distribution histogram"""
        self.fig.clear()
        
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(self.colors['surface_container_high'])
        
        # Collect all response times
        all_times = []
        for server in self.current_data:
            all_times.extend(server.response_times)
        
        if not all_times:
            self.show_placeholder()
            return
        
        # Create histogram
        n, bins, patches = ax.hist(all_times, bins=30, color=self.colors['primary'], 
                                  alpha=0.7, edgecolor=self.colors['outline_variant'])
        
        # Color bars based on performance
        for i, p in enumerate(patches):
            if bins[i] < 50:  # Fast
                p.set_facecolor(self.colors['success'])
            elif bins[i] < 100:  # Medium
                p.set_facecolor(self.colors['warning'])
            else:  # Slow
                p.set_facecolor(self.colors['error'])
        
        ax.set_xlabel('Response Time (ms)', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('📊 Response Time Distribution', fontweight='bold', fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        mean_time = np.mean(all_times)
        median_time = np.median(all_times)
        ax.axvline(mean_time, color=self.colors['error'], linestyle='--', 
                  linewidth=2, label=f'Mean: {mean_time:.1f}ms')
        ax.axvline(median_time, color=self.colors['success'], linestyle='--', 
                  linewidth=2, label=f'Median: {median_time:.1f}ms')
        ax.legend()
        
        self.fig.tight_layout()
    
    def create_provider_comparison_chart(self):
        """Create provider comparison chart"""
        self.fig.clear()
        
        # Group by provider
        provider_data = {}
        for server in self.current_data:
            provider = server.server.provider
            if provider not in provider_data:
                provider_data[provider] = []
            provider_data[provider].append(server.avg_response_time)
        
        if not provider_data:
            self.show_placeholder()
            return
        
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(self.colors['surface_container_high'])
        
        providers = list(provider_data.keys())
        avg_times = [np.mean(times) for times in provider_data.values()]
        
        # Create horizontal bar chart with DNS Pulse colors
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['tertiary'], self.colors['success']]
        bars = ax.barh(providers, avg_times, 
                      color=[colors[i % len(colors)] for i in range(len(providers))],
                      alpha=0.8)
        
        ax.set_xlabel('Average Response Time (ms)', fontweight='bold')
        ax.set_title('🏢 Provider Performance Comparison', fontweight='bold', fontsize=14, pad=20)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, time) in enumerate(zip(bars, avg_times)):
            ax.text(time + max(avg_times) * 0.01, bar.get_y() + bar.get_height()/2,
                   f'{time:.1f}ms', va='center', fontweight='bold')
        
        self.fig.tight_layout()
    
    def create_reliability_speed_chart(self):
        """Create reliability vs speed scatter plot"""
        self.fig.clear()
        
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(self.colors['surface_container_high'])
        
        speeds = [s.avg_response_time for s in self.current_data]
        reliabilities = [s.reliability_score for s in self.current_data]
        names = [s.server.name for s in self.current_data]
        
        # Color points based on provider with DNS Pulse colors
        providers = list(set(s.server.provider for s in self.current_data))
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['tertiary'], self.colors['success'],
                 self.colors['text_muted']]
        
        for i, provider in enumerate(providers):
            provider_servers = [s for s in self.current_data if s.server.provider == provider]
            provider_speeds = [s.avg_response_time for s in provider_servers]
            provider_reliabilities = [s.reliability_score for s in provider_servers]
            
            ax.scatter(provider_speeds, provider_reliabilities, 
                      c=colors[i % len(colors)], label=provider, 
                      alpha=0.7, s=100, edgecolors='white', linewidth=1)
        
        ax.set_xlabel('Average Response Time (ms)', fontweight='bold')
        ax.set_ylabel('Reliability Score (%)', fontweight='bold')
        ax.set_title('⚡ Reliability vs Speed Analysis', fontweight='bold', fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='lower left', framealpha=0.9)
        
        # Add trend line
        if len(speeds) > 1:
            z = np.polyfit(speeds, reliabilities, 1)
            p = np.poly1d(z)
            ax.plot(sorted(speeds), p(sorted(speeds)), "--", 
                   color=self.colors['error'], alpha=0.8, linewidth=2)
        
        # Highlight best performers (top right quadrant)
        median_speed = np.median(speeds)
        median_reliability = np.median(reliabilities)
        ax.axvline(median_speed, color=self.colors['outline_variant'], linestyle=':', alpha=0.5)
        ax.axhline(median_reliability, color=self.colors['outline_variant'], linestyle=':', alpha=0.5)
        
        self.fig.tight_layout()
    
    def create_live_performance_chart(self):
        """Create live performance monitoring chart"""
        self.fig.clear()
        
        # Create subplots for multiple metrics
        gs = self.fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Top performers
        ax1 = self.fig.add_subplot(gs[0, :])
        ax1.set_facecolor(self.colors['surface_container_high'])
        
        top_5 = sorted(self.current_data, key=lambda x: x.avg_response_time)[:5]
        names = [s.server.name[:15] for s in top_5]
        times = [s.avg_response_time for s in top_5]
        
        bars = ax1.bar(names, times, color=self.colors['success'], alpha=0.8)
        ax1.set_title('🏆 Top 5 Fastest Servers', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Response Time (ms)')
        ax1.grid(True, alpha=0.3)
        
        for bar, time in zip(bars, times):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{time:.1f}ms', ha='center', va='bottom', fontsize=9)
        
        # Success rate pie chart
        ax2 = self.fig.add_subplot(gs[1, 0])
        ax2.set_facecolor(self.colors['surface_container_high'])
        
        total_queries = sum(s.total_queries for s in self.current_data)
        successful_queries = sum(s.successful_queries for s in self.current_data)
        failed_queries = total_queries - successful_queries
        
        if total_queries > 0:
            sizes = [successful_queries, failed_queries]
            labels = ['Successful', 'Failed']
            colors_pie = [self.colors['success'], self.colors['error']]
            
            wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors_pie, 
                                              autopct='%1.1f%%', startangle=90)
            ax2.set_title('📊 Query Success Rate', fontweight='bold', fontsize=12)
        
        # Provider distribution
        ax3 = self.fig.add_subplot(gs[1, 1])
        ax3.set_facecolor(self.colors['surface_container_high'])
        
        provider_counts = {}
        for server in self.current_data:
            provider = server.server.provider
            provider_counts[provider] = provider_counts.get(provider, 0) + 1
        
        if provider_counts:
            providers = list(provider_counts.keys())
            counts = list(provider_counts.values())
            colors_bar = [colors[i % len(colors)] for i in range(len(providers))]
            
            ax3.bar(providers, counts, color=colors_bar, alpha=0.8)
            ax3.set_title('🌐 Provider Distribution', fontweight='bold', fontsize=12)
            ax3.set_ylabel('Server Count')
            ax3.tick_params(axis='x', rotation=45)
        
        self.fig.suptitle('⚡ Live Performance Dashboard', fontweight='bold', fontsize=14)
    
    def on_chart_type_changed(self, selection):
        """Handle chart type change"""
        if hasattr(self, 'current_data') and self.current_data:
            self.update_graphs(self.current_data)
        else:
            self.show_placeholder()
    
    def clear_graphs(self):
        """Clear all graphs"""
        self.current_data = []
        self.show_placeholder()
    
    def update_live_data(self, result):
        """Update graphs with a single live benchmark result"""
        if not result.success:
            return
            
        try:
            # This could accumulate live data for real-time chart updates
            # For now, we'll skip to avoid performance issues during heavy benchmarking
            # The full update happens at completion via update_graphs()
            pass
            
        except Exception as e:
            # Fail silently to not interrupt the benchmark
            pass