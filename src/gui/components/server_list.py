"""
DNS Server List Component with DNS Pulse Design
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Set
from src.data.dns_servers import DNSServer

class ServerListFrame(ctk.CTkFrame):
    """Frame containing the DNS server list with selection capabilities"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_servers: Set[str] = set()
        self.server_items: Dict[str, Dict] = {}
        
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
        
        # Configure frame styling (transparent as parent has card)
        self.configure(
            fg_color="transparent",
            corner_radius=0
        )
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the server list UI with modern design"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Modern title section
        title_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=45
        )
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 5))
        title_frame.grid_propagate(False)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="🌐 DNS SERVERS",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=self.colors['secondary']
        )
        title_label.pack(side="left")
        
        # Server count badge
        self.count_badge = ctk.CTkLabel(
            title_frame,
            text="0",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color=self.colors['tertiary'],
            fg_color=self.colors['surface_container'],
            corner_radius=12,
            width=35,
            height=24
        )
        self.count_badge.pack(side="left", padx=(10, 0))
        
        # Controls card
        self.controls_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=50
        )
        self.controls_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        self.controls_frame.grid_columnconfigure(2, weight=1)
        self.controls_frame.grid_propagate(False)
        
        # Select all/none buttons with modern styling
        self.select_all_btn = ctk.CTkButton(
            self.controls_frame,
            text="✓ ALL",
            width=70,
            height=32,
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            fg_color=self.colors['secondary'],
            hover_color=self.colors['success'],
            text_color="#000000",
            corner_radius=6,
            command=self.select_all_servers
        )
        self.select_all_btn.grid(row=0, column=0, padx=(10, 5), pady=9)
        
        self.select_none_btn = ctk.CTkButton(
            self.controls_frame,
            text="✗ NONE",
            width=70,
            height=32,
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            fg_color=self.colors['surface_container_high'],
            hover_color=self.colors['error'],
            text_color=self.colors['on_surface_variant'],
            corner_radius=6,
            border_width=1,
            border_color=self.colors['outline_variant'],
            command=self.select_no_servers
        )
        self.select_none_btn.grid(row=0, column=1, padx=5, pady=9)
        
        # Filter dropdown with modern styling
        self.filter_var = ctk.StringVar(value="All")
        self.filter_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=["All", "Responsive", "Google", "Cloudflare", "Quad9", "OpenDNS"],
            variable=self.filter_var,
            width=130,
            height=32,
            font=ctk.CTkFont(family="Arial", size=11),
            fg_color=self.colors['surface_container_high'],
            button_color=self.colors['primary'],
            button_hover_color=self.colors['tertiary'],
            dropdown_fg_color=self.colors['surface_container_high'],
            dropdown_hover_color=self.colors['surface_container'],
            dropdown_text_color=self.colors['on_surface_variant'],
            text_color=self.colors['on_surface_variant'],
            corner_radius=6,
            command=self.on_filter_changed
        )
        self.filter_menu.grid(row=0, column=2, padx=(5, 10), pady=9, sticky="e")
        
        # Server list container with modern scrollbar
        list_container = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface_container'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        list_container.grid(row=2, column=0, sticky="nsew", padx=15, pady=(5, 10))
        list_container.grid_columnconfigure(0, weight=1)
        list_container.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame for server items
        self.list_frame = ctk.CTkScrollableFrame(
            list_container,
            fg_color="transparent",
            scrollbar_button_color=self.colors['outline_variant'],
            scrollbar_button_hover_color=self.colors['primary']
        )
        self.list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.list_frame.grid_columnconfigure(0, weight=1)
        
        # Selection status bar
        status_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=30
        )
        status_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 5))
        status_frame.grid_propagate(False)
        
        self.selection_label = ctk.CTkLabel(
            status_frame,
            text="⚡ 0 servers selected",
            font=ctk.CTkFont(family="Arial", size=11),
            text_color=self.colors['text_muted']
        )
        self.selection_label.pack(side="left")
    
    def populate_server_list(self, servers: List[DNSServer]):
        """Populate the server list with DNS servers"""
        # Clear existing items
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        self.server_items.clear()
        
        for i, server in enumerate(servers):
            self.create_server_item(server, i)
        
        self.count_badge.configure(text=str(len(servers)))
        self.update_selection_count()
    
    def create_server_item(self, server: DNSServer, row: int):
        """Create a single server item with modern card design"""
        # Main card frame for the server
        item_frame = ctk.CTkFrame(
            self.list_frame,
            fg_color=self.colors['surface_container_high'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=70
        )
        item_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=3)
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Modern checkbox with custom styling
        checkbox_var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            item_frame,
            text="",
            variable=checkbox_var,
            width=24,
            height=24,
            fg_color=self.colors['secondary'],
            hover_color=self.colors['success'],
            border_color=self.colors['outline_variant'],
            border_width=2,
            corner_radius=4,
            command=lambda: self.on_server_selection_changed(server.ip, checkbox_var.get())
        )
        checkbox.grid(row=0, column=0, padx=12, pady=12)
        
        # Server info container
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=8)
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Server name with provider badge
        name_container = ctk.CTkFrame(info_frame, fg_color="transparent")
        name_container.grid(row=0, column=0, sticky="ew")
        
        name_label = ctk.CTkLabel(
            name_container,
            text=f"{server.name}",
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            text_color=self.colors['on_surface'],
            anchor="w"
        )
        name_label.pack(side="left")
        
        # Provider badge
        if server.provider:
            provider_color = self._get_provider_color(server.provider)
            provider_badge = ctk.CTkLabel(
                name_container,
                text=server.provider.upper(),
                font=ctk.CTkFont(family="Arial", size=9, weight="bold"),
                text_color=provider_color,
                fg_color=self.colors['surface_container'],
                corner_radius=4,
                width=60,
                height=18
            )
            provider_badge.pack(side="left", padx=(8, 0))
        
        # IP and location details
        details_text = f"🔗 {server.ip}"
        if server.location:
            details_text += f"  •  📍 {server.location}"
        
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=ctk.CTkFont(family="Arial", size=11),
            text_color=self.colors['text_muted'],
            anchor="w"
        )
        details_label.grid(row=1, column=0, sticky="ew", pady=(3, 0))
        
        # Status indicator with modern design
        status_frame = ctk.CTkFrame(
            item_frame,
            width=100,
            fg_color="transparent"
        )
        status_frame.grid(row=0, column=2, padx=10, pady=12, sticky="ns")
        status_frame.grid_propagate(False)
        
        # Response time display with pulse animation placeholder
        response_container = ctk.CTkFrame(
            status_frame,
            fg_color=self.colors['surface_container'],
            corner_radius=6,
            width=80,
            height=32
        )
        response_container.pack(expand=True)
        response_container.pack_propagate(False)
        
        response_label = ctk.CTkLabel(
            response_container,
            text="...",
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            text_color=self.colors['text_muted']
        )
        response_label.pack(expand=True)
        
        # Store references
        self.server_items[server.ip] = {
            "server": server,
            "frame": item_frame,
            "checkbox": checkbox,
            "checkbox_var": checkbox_var,
            "response_label": response_label,
            "response_container": response_container,
            "name_label": name_label
        }
        
        # Auto-select responsive servers
        if server.is_responsive:
            checkbox_var.set(True)
            self.selected_servers.add(server.ip)
    
    def _get_provider_color(self, provider: str) -> str:
        """Get color for provider badge"""
        provider_colors = {
            "google": self.colors['secondary'],
            "cloudflare": self.colors['warning'],
            "quad9": self.colors['primary'],
            "opendns": self.colors['tertiary'],
            "adguard": self.colors['success']
        }
        return provider_colors.get(provider.lower(), self.colors['text_muted'])
    
    def update_server_status(self, server: DNSServer, is_responsive: bool, response_time: float):
        """Update the status of a server after testing with animation"""
        if server.ip not in self.server_items:
            return
        
        item = self.server_items[server.ip]
        response_label = item["response_label"]
        response_container = item["response_container"]
        
        if is_responsive:
            # Color based on response time
            if response_time < 20:
                color = self.colors['success']
            elif response_time < 50:
                color = self.colors['secondary']
            elif response_time < 100:
                color = self.colors['warning']
            else:
                color = self.colors['error']
            
            response_label.configure(
                text=f"{response_time:.0f}ms",
                text_color=color
            )
            response_container.configure(
                border_width=1,
                border_color=color
            )
        else:
            response_label.configure(
                text="FAIL",
                text_color=self.colors['error']
            )
            response_container.configure(
                border_width=1,
                border_color=self.colors['error']
            )
        
        # Update server object
        item["server"].is_responsive = is_responsive
        item["server"].avg_response_time = response_time
    
    def on_server_selection_changed(self, server_ip: str, is_selected: bool):
        """Handle server selection change with animation"""
        if is_selected:
            self.selected_servers.add(server_ip)
            # Highlight the card
            if server_ip in self.server_items:
                self.server_items[server_ip]["frame"].configure(
                    border_color=self.colors['secondary'],
                    border_width=2
                )
        else:
            self.selected_servers.discard(server_ip)
            # Remove highlight
            if server_ip in self.server_items:
                self.server_items[server_ip]["frame"].configure(
                    border_color=self.colors['outline_variant'],
                    border_width=1
                )
        
        self.update_selection_count()
    
    def select_all_servers(self):
        """Select all visible servers"""
        for item in self.server_items.values():
            if item["frame"].winfo_viewable():
                item["checkbox_var"].set(True)
                self.selected_servers.add(item["server"].ip)
                item["frame"].configure(
                    border_color=self.colors['secondary'],
                    border_width=2
                )
        
        self.update_selection_count()
    
    def select_no_servers(self):
        """Deselect all servers"""
        for item in self.server_items.values():
            item["checkbox_var"].set(False)
            item["frame"].configure(
                border_color=self.colors['outline_variant'],
                border_width=1
            )
        
        self.selected_servers.clear()
        self.update_selection_count()
    
    def on_filter_changed(self, filter_value: str):
        """Handle filter selection change"""
        visible_count = 0
        for item in self.server_items.values():
            server = item["server"]
            should_show = True
            
            if filter_value == "Responsive":
                should_show = server.is_responsive
            elif filter_value in ["Google", "Cloudflare", "Quad9", "OpenDNS"]:
                should_show = server.provider.lower() == filter_value.lower()
            
            if should_show:
                item["frame"].grid()
                visible_count += 1
            else:
                item["frame"].grid_remove()
        
        self.count_badge.configure(text=str(visible_count))
        self.update_selection_count()
    
    def update_selection_count(self):
        """Update the selection count label"""
        count = len(self.selected_servers)
        total = len([item for item in self.server_items.values() if item["frame"].winfo_viewable()])
        self.selection_label.configure(
            text=f"⚡ {count}/{total} servers selected"
        )
        
        # Update app's server badge
        if hasattr(self.app, 'servers_badge'):
            self.app.servers_badge.configure(text=str(count))
    
    def get_selected_servers(self) -> List[DNSServer]:
        """Get list of selected DNS servers"""
        return [
            item["server"] for item in self.server_items.values()
            if item["server"].ip in self.selected_servers
        ]