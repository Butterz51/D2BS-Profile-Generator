import sys
import json
import os
import tkinter as tk
import webbrowser
import glob
from tkinter import messagebox, ttk
from tkinter import filedialog

# Function to determine base path
def get_base_path():
    """Get the base directory for the script or executable."""
    if getattr(sys, 'frozen', False):  # If running as a compiled executable
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)  # If running as a script

PV = "1.1.2"

# GUI class
class ProfileGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("D2BS Profile Generator")

        # Set a fixed window size
        window_width = 1770
        window_height = 780

        # Update tasks to ensure the root window is fully initialized
        self.root.update_idletasks()

        # Get the screen width and height after the update
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate x and y coordinates for the main window to be centered on the screen
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 3) - (window_height // 2)

        # Set the geometry of the main window
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Define script directory first
        self.script_directory = get_base_path()  # Use the base path function

        # Set the icon for the GUI window
        self.root.iconbitmap(os.path.join(self.script_directory, "icon.ico"))

        # Set a fixed window and lock it
        self.root.resizable(False, False)

        # Define paths for data saving
        self.saved_data_dir = os.path.join(self.script_directory, "Saved Data")
        self.generated_profiles_dir = os.path.join(self.script_directory, "Generated Profiles")

        # Ensure the directories exist
        os.makedirs(self.saved_data_dir, exist_ok=True)
        os.makedirs(self.generated_profiles_dir, exist_ok=True)

        # Track the game name counter
        self.game_name_counter = 1

        # Define default settings for profile counts, theme, paths, realm, mode, and entry script
        self.game_path = tk.StringVar()
        self.theme = tk.StringVar(value="Light Mode")
        self.game_exe_limit = tk.IntVar(value=0)
        self.double_limit = tk.IntVar(value=0)
        self.key_count = tk.IntVar(value=0)
        self.realm = tk.StringVar(value="East")
        self.mode = tk.StringVar(value="Battle.net")
        self.entry_script = tk.StringVar(value="D2BotSoloPlay.dbj")
        self.game_name = tk.StringVar(value="")

        # Load configuration on start-up
        self.load_config()
        self.loaded_profile_game_name = False

        # Profile counts for each class
        self.pal_count = tk.IntVar(value=0)
        self.sorc_count = tk.IntVar(value=0)
        self.zon_count = tk.IntVar(value=0)
        self.necro_count = tk.IntVar(value=0)
        self.barb_count = tk.IntVar(value=0)
        self.dru_count = tk.IntVar(value=0)
        self.sin_count = tk.IntVar(value=0)

        # Dropdown options for Profile Prefixes
        self.prefix_options = [
            "HCCNL - Hardcore Classic NonLadder", "HCCL - Hardcore Classic Ladder",
            "HCNL - Hardcore Expansion NonLadder", "HCL - Hardcore Expansion Ladder",
            "SCCNL - Softcore Classic NonLadder", "SCCL - Softcore Classic Ladder",
            "SCNL - Softcore Expansion NonLadder", "SCL - Softcore Expansion Ladder"
        ]

        # Dropdown options for Profile Classes
        self.class_options = {
            "PAL": "Paladin",
            "SORC": "Sorceress",
            "ZON": "Amazon",
            "NECRO": "Necromancer",
            "BARB": "Barbarian",
            "DRU": "Druid",
            "SIN": "Assassin"
        }

        # Create prefix selection variables for each profile type
        self.prefix_selection = {
            "PAL": tk.StringVar(value=self.prefix_options[0]),
            "SORC": tk.StringVar(value=self.prefix_options[0]),
            "ZON": tk.StringVar(value=self.prefix_options[0]),
            "NECRO": tk.StringVar(value=self.prefix_options[0]),
            "BARB": tk.StringVar(value=self.prefix_options[0]),
            "DRU": tk.StringVar(value=self.prefix_options[0]),
            "SIN": tk.StringVar(value=self.prefix_options[0])
        }

        # InfoTag counts for all classes
        self.info_tag_counts = {
            "PAL": {"Hammerdin": tk.IntVar(value=0), "Smiter": tk.IntVar(value=0), "Auradin": tk.IntVar(value=0),
                    "Zealer": tk.IntVar(value=0), "Torchadin": tk.IntVar(value=0), "Classicauradin": tk.IntVar(value=0),
                    "Hammershock": tk.IntVar(value=0), "Sancdreamer": tk.IntVar(value=0), "Bumper": tk.IntVar(value=0),
                    "SocketMule": tk.IntVar(value=0), "ImbueMule": tk.IntVar(value=0)},

            "SORC": {"Blizzballer": tk.IntVar(value=0), "Lightning": tk.IntVar(value=0),
                     "Cold": tk.IntVar(value=0), "Meteorb": tk.IntVar(value=0), "Blova": tk.IntVar(value=0),
                     "Bumper": tk.IntVar(value=0), "SocketMule": tk.IntVar(value=0), "ImbueMule": tk.IntVar(value=0)},

            "ZON": {"Javazon": tk.IntVar(value=0), "Witchyzon": tk.IntVar(value=0), "Bumper": tk.IntVar(value=0),
                    "SocketMule": tk.IntVar(value=0), "ImbueMule": tk.IntVar(value=0)},

            "NECRO": {"Poison": tk.IntVar(value=0), "Bone": tk.IntVar(value=0), "Summon": tk.IntVar(value=0),
                      "Bumper": tk.IntVar(value=0), "SocketMule": tk.IntVar(value=0), "ImbueMule": tk.IntVar(value=0)},

            "BARB": {"Whirlwind": tk.IntVar(value=0), "Immortalwhirl": tk.IntVar(value=0), "Frenzy": tk.IntVar(value=0),
                     "Uberconc": tk.IntVar(value=0), "Singer": tk.IntVar(value=0), "Bumper": tk.IntVar(value=0),
                     "SocketMule": tk.IntVar(value=0), "ImbueMule": tk.IntVar(value=0)},

            "DRU": {"Wind": tk.IntVar(value=0), "Elemental": tk.IntVar(value=0), "Plaguewolf": tk.IntVar(value=0),
                    "Wolf": tk.IntVar(value=0), "Bumper": tk.IntVar(value=0), "SocketMule": tk.IntVar(value=0),
                    "ImbueMule": tk.IntVar(value=0)},

            "SIN": {"Trapsin": tk.IntVar(value=0), "Whirlsin": tk.IntVar(value=0), "Bumper": tk.IntVar(value=0),
                    "SocketMule": tk.IntVar(value=0), "ImbueMule": tk.IntVar(value=0)}
        }

        # Configure the GUI layout
        self.create_widgets()
        self.apply_theme()
        self.update_game_name_state()

    def create_widgets(self):
        # Menu bar for themes
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save All", command=self.save_all_data)
        file_menu.add_command(label="Load Profile", command=self.load_profile)

        # Theme menu
        theme_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(state="normal", label="View", menu=theme_menu)
        theme_menu.add_command(label="Light Mode", command=lambda: self.change_theme("Light Mode"))
        theme_menu.add_command(label="Dark Mode", command=lambda: self.change_theme("Dark Mode"))

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About D2BS Profile Generator", command=self.show_about)
        help_menu.add_command(label="Support The Development", command=self.open_paypal)

        # Game Directory Frame
        self.sel_frame = tk.LabelFrame(self.root, text="Game Directory", font=("Arial", 11, "bold"), padx=5, pady=5, bd=3, relief="groove")
        self.sel_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Input Game Path field and Save button
        tk.Label(self.sel_frame, text="Input Game Path:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(self.sel_frame, textvariable=self.game_path, width=50).grid(row=0, column=1, columnspan=6, padx=5, pady=5, sticky="w")
        self.save_button = tk.Button(self.sel_frame, text="Save", command=self.save_game_path)
        self.save_button.grid(row=0, column=8, padx=5, pady=5, sticky="w")

        # Profile Count Settings Frame
        self.selec_frame = tk.LabelFrame(self.root, text="Profile Count Settings", font=("Arial", 11, "bold"), padx=5, pady=5, bd=3, relief="groove")
        self.selec_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Row for settings
        tk.Label(self.selec_frame, text="Max Game.exe Paths to Make:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky="e", padx=8, pady=5)
        tk.Entry(self.selec_frame, textvariable=self.game_exe_limit, width=10).grid(row=1, column=1, pady=5, sticky="w")

        tk.Label(self.selec_frame, text="Max Game Paths to Double Up:", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky="w", padx=8, pady=5)
        tk.Entry(self.selec_frame, textvariable=self.double_limit, width=10).grid(row=1, column=3, pady=5, sticky="w")

        tk.Label(self.selec_frame, text="Total Keys to Use:", font=("Arial", 9, "bold")).grid(row=1, column=4, sticky="w", padx=8, pady=5)
        tk.Entry(self.selec_frame, textvariable=self.key_count, width=10).grid(row=1, column=5, pady=5, sticky="w")

        # Frame for all dropdown selections
        self.selection_frame = tk.LabelFrame(self.root, text="Game Settings", font=("Arial", 11, "bold"), padx=5, pady=5, bd=3, relief="groove")
        self.selection_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Dropdown for Game Mode selection
        tk.Label(self.selection_frame, text="Select Game Mode:", font=("Arial", 9, "bold")).grid(row=2, column=0, padx=8, pady=5)
        mode_dropdown = ttk.Combobox(self.selection_frame, textvariable=self.mode, values=["Battle.net", "Single Player", "Open Battle.net", "Host TCP/IP Game", "Join TCP/IP Game"], state="readonly", width=20)
        mode_dropdown.grid(row=2, column=1, pady=5, sticky="w")
        mode_dropdown.current(0)  # Set default to "Battle.net"

        # Dropdown for Realm selection
        tk.Label(self.selection_frame, text="Select Realm:", font=("Arial", 9, "bold")).grid(row=2, column=2, padx=8, pady=5)
        realm_dropdown = ttk.Combobox(self.selection_frame, textvariable=self.realm, values=["East", "West", "Europe", "Asia"], state="readonly", width=10)
        realm_dropdown.grid(row=2, column=3, pady=5, sticky="w")
        realm_dropdown.current(0)  # Set default to "East"

        # Dropdown for Entry Script selection
        tk.Label(self.selection_frame, text="Select Entry Script:", font=("Arial", 9, "bold")).grid(row=2, column=4, padx=8, pady=5)
        entry_dropdown = ttk.Combobox(self.selection_frame, textvariable=self.entry_script, values=["D2BotSoloPlay.dbj", "D2BotLead.dbj"], state="readonly", width=20)
        entry_dropdown.grid(row=2, column=5, pady=5, sticky="w")
        entry_dropdown.current(0)  # Set default to "D2BotSoloPlay.dbj"

        # Game Name entry (disabled by default)
        tk.Label(self.selection_frame, text="Game Name:", font=("Arial", 9, "bold")).grid(row=3, column=0, sticky="e", padx=8, pady=5)
        self.game_name_entry = tk.Entry(self.selection_frame, textvariable=self.game_name, width=20, state="disabled")
        self.game_name_entry.grid(row=3, column=1, pady=5, sticky="w")
        self.game_name.trace_add("write", self.update_game_name_state)

        # Bind entry script selection to update the game name field’s state
        entry_dropdown.bind("<<ComboboxSelected>>", self.update_game_name_state)

        self.class_frames = []

        # Profile Counts and Prefix Selection
        profile_classes = [
            ("PAL", self.pal_count, self.info_tag_counts["PAL"]),
            ("SORC", self.sorc_count, self.info_tag_counts["SORC"]),
            ("ZON", self.zon_count, self.info_tag_counts["ZON"]),
            ("NECRO", self.necro_count, self.info_tag_counts["NECRO"]),
            ("BARB", self.barb_count, self.info_tag_counts["BARB"]),
            ("DRU", self.dru_count, self.info_tag_counts["DRU"]),
            ("SIN", self.sin_count, self.info_tag_counts["SIN"]),
        ]

        # Loop through each class to create a labeled frame for InfoTag Counts
        for col, (class_key, count_var, tags) in enumerate(profile_classes):
            # Create a LabelFrame for each class
            class_frames = tk.LabelFrame(self.root, text=f"{self.class_options[class_key]} Builds", font=("Arial", 11, "bold"), padx=5, pady=5, bd=3)
            class_frames.grid(row=6, column=col, padx=5, pady=5, sticky="nsew")
            self.class_frames.append(class_frames)

            # Profile Count entry at the top of each frame
            profile_count_frame = tk.Frame(class_frames)
            profile_count_frame.pack(anchor="center", padx=5, pady=2)
            tk.Label(profile_count_frame, text="Profile Count:", font=("Arial", 9, "bold"), anchor="ne").pack(side="left")
            tk.Entry(profile_count_frame, textvariable=count_var, width=5).pack(side="left")

            # Prefix dropdown for each class
            tk.Label(class_frames, text="Prefix:", font=("Arial", 9, "bold")).pack(anchor="center")
            prefix_dropdown = ttk.Combobox(class_frames, textvariable=self.prefix_selection[class_key], values=self.prefix_options, state="readonly", width=34)
            prefix_dropdown.pack(anchor="center", pady=5)

            for tag_name, var in tags.items():
                # Add "Additional Options" label above "Bumper"
                if tag_name == "Bumper":
                    tk.Label(class_frames, text="Additional Options:", font=("Arial", 10, "italic", "bold")).pack(anchor="e", padx=5, pady=(10, 0))

                # Add "Fastest Recommended Additional Options" label just above "Bumper" for Sorceress only
                if class_key == "SORC" and tag_name == "Bumper":
                    tk.Label(class_frames, text="(Fastest Recommended)", font=("Arial", 10, "italic")).pack(anchor="e", padx=5, pady=0)

                # Create a frame for each InfoTag entry within the class frame
                tag_frame = tk.Frame(class_frames)
                tag_frame.pack(anchor="e", padx=5, pady=3)

                # Label and Entry for each InfoTag
                tk.Label(tag_frame, text=tag_name, anchor="e").pack(side="left")
                tk.Entry(tag_frame, textvariable=var, width=5).pack(anchor="w", side="left")

        # Generate button
        self.save_button2 = tk.Button(self.root, text="Generate Profile", command=self.generate_profiles)
        self.save_button2.grid(row=7, column=0, columnspan=14, pady=20)

        self.apply_theme()

    # About Window
    def show_about(self):
        """Displays an About window with author and version information."""
        about_window = tk.Toplevel(self.root, background="#0f1416")
        about_window.title("About D2BS Profile Generator")

        # Calculate position to center the pop-up window
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()

        pop_up_width = 350
        pop_up_height = 215

        # Calculate x and y coordinates for the pop-up window to be centered on the main window
        x = main_x + (main_width // 2) - (pop_up_width // 2)
        y = main_y + (main_height // 2) - (pop_up_height // 2)
         # Set the geometry of the pop-up window to the calculated position
        about_window.geometry(f"{pop_up_width}x{pop_up_height}+{x}+{y}")

        about_window.geometry("350x215")
        about_window.resizable(False, False)

        # About text
        tk.Label(about_window, background="#0f1416", foreground="#1a8ec8", text=f"Author: Butterz", font=("Arial", 15, "italic", "bold")).pack(anchor="center", pady=5)
        tk.Label(about_window, background="#0f1416", foreground="#1a8ec8", text=f"Version: {PV}", font=("Arial", 15, "italic", "bold")).pack(anchor="center", pady=1)

        # Discord link1 label
        discord_link = tk.Label(about_window, background="#0f1416", text="Join our Discord", font=("Arial", 13, "underline", "bold"), fg="blue", cursor="hand2")
        discord_link.pack(pady=1)
        discord_link.bind("<Button-1>", lambda e: self.open_discord())

        # Discord link2 label
        discord_link = tk.Label(about_window, background="#0f1416", text="Join SoloPlay's Discord", font=("Arial", 12, "underline", "bold"), fg="blue", cursor="hand2")
        discord_link.pack(pady=1)
        discord_link.bind("<Button-1>", lambda e: self.open_discord2())

        # Discord link2 label
        discord_link = tk.Label(about_window, background="#0f1416", text="Join BlizzHackers Discord", font=("Arial", 12, "underline", "bold"), fg="blue", cursor="hand2")
        discord_link.pack(pady=1)
        discord_link.bind("<Button-1>", lambda e: self.open_discord3())

        # OK button to close the About window
        tk.Button(about_window, activebackground="#606060", background="#515151", text="Close", command=about_window.destroy).pack(anchor="center", ipadx=10, pady=15)

    # JBH Services Discord
    def open_discord(self):
        webbrowser.open("https://discord.gg/cUBqFpYHjh")

    # SoloPlay Discord
    def open_discord2(self):
        webbrowser.open("https://discord.gg/pjKFtfyQK9")

    # BlizzHackers Discord
    def open_discord3(self):
        webbrowser.open("https://discord.gg/6t45tVF6")

    # Dontation Supporter
    def open_paypal(self):
        webbrowser.open("https://paypal.me/D2ServicesByJBH?country.x=CA&locale.x=en_US")

    # Game Name Fuction
    def update_game_name_state(self, *args):
        """Enable or disable the Game Name entry based on the selected script."""
        if self.entry_script.get() == "D2BotLead.dbj":
            # Only enable and clear the game name field if it was previously disabled
            if self.game_name_entry.cget("state") == "disabled":
                self.game_name_entry.configure(state="normal")
                if not self.loaded_profile_game_name:
                    self.game_name.set("")  # Clear the name to allow fresh input
        else:
            self.game_name_entry.configure(state="disabled")
            self.game_name.set("Disabled")

    # Theme Settings
    def apply_theme(self):
        self.dark_theme = {
            "bg": "#2E2E2E",                # Background color for dark mode
            "font": "#1a8ec8",              # Font color (text) for dark mode
            "entry_bg": "#6b6b6b",          # Entry field background in dark mode
            "button_fg": "#1a8ec8",         # Button font in dark mode
            "active_button": "#2c2c2c",     # Button-Press color for dark mode
            "Combobox": "#6b6b6b",          # ComboBox background
            "Comboboxfont": "black",        # ComboBox font color
            "activeCombobox": "606060",     # ComboBox background when clicked
        }

        self.light_theme = {
            "bg": "SystemButtonFace",       # Background color for light mode
            "font": "black",                # Foreground color (text) for light mode
            "entry_bg": "white",            # Entry field background in light mode
            "button_fg": "black",           # Button foreground in light mode
            "active_button": "#e2e2e2",     # Button-Press color for light mode
            "Combobox": "white",            # ComboBox background
            "Comboboxfont": "black",        # ComboBox font color
            "activeCombobox": "white",      # ComboBox background when clicked
        }

        theme = self.dark_theme if self.theme.get() == "Dark Mode" else self.light_theme

        # Set main window background color
        self.root.configure(bg=theme["bg"])

        # Apply theme to all frames
        self.apply_theme_to_widget(self.sel_frame, theme)
        self.apply_theme_to_widget(self.selec_frame, theme)
        self.apply_theme_to_widget(self.selection_frame, theme)
        self.apply_theme_to_widget(self.save_button2, theme)

        for frame in self.class_frames:
            self.apply_theme_to_widget(frame, theme)

    def apply_theme_to_widget(self, widget, theme):
        """Recursively applies theme colors to a widget and its children, only applying foreground where applicable."""
        try:
            # Apply background to all widgets that support it
            widget.configure(background=theme["bg"])

            # Apply foreground only to widgets that support it
            if isinstance(widget, (tk.Label, tk.LabelFrame)):
                widget.configure(foreground=theme["font"])
                widget.configure(activebackground=theme["active_button"])

            if isinstance(widget, (tk.Button)):
                widget.configure(foreground=theme["button_fg"])
                widget.configure(activebackground=theme["active_button"])

            if isinstance(widget, (tk.Entry)):
                widget.configure(background=theme["entry_bg"])
                widget.configure(foreground=theme["Comboboxfont"])
                widget.configure(activebackground=theme["active_button"])

            if isinstance(widget, (ttk.Combobox)):
                #widget.configure(background=theme["activeCombobox"])
                widget.configure(foreground=theme["Comboboxfont"])
                #widget.configure(activebackground=theme["activeCombobox"])

            # Special handling for ttk Combobox background/foreground in dropdown
            if isinstance(widget, ttk.Combobox):
                widget.tk.eval(f'option add *TCombobox*Listbox.background {theme["Combobox"]}')
                #widget.tk.eval(f'option add *TCombobox*Listbox.foreground {theme["Comboboxfont"]}')
                widget.tk.eval(f'option add *TCombobox*Listbox.activebackground {theme["Combobox"]}')

        except tk.TclError:
            # If a widget does not support a specific option, ignore and continue
            pass

        # Apply theme to all child widgets recursively
        for child in widget.winfo_children():
            self.apply_theme_to_widget(child, theme)

    def change_theme(self, selected_theme):
        """Change and save the selected theme."""
        self.theme.set(selected_theme)
        self.apply_theme()
        self.save_config({"Theme": selected_theme})

    def generate_profiles(self):
        # Retrieve user-defined settings
        pal_count = self.pal_count.get()
        sorc_count = self.sorc_count.get()
        zon_count = self.zon_count.get()
        necro_count = self.necro_count.get()
        barb_count = self.barb_count.get()
        dru_count = self.dru_count.get()
        sin_count = self.sin_count.get()
        double_limit = self.double_limit.get()
        key_count = self.key_count.get()
        game_exe_limit = self.game_exe_limit.get()
        realm = self.realm.get()
        mode = self.mode.get()
        entry_script = self.entry_script.get()

        # Warning checks for Profile Count vs Game.exe Count
        total_profiles_required = pal_count + sorc_count + zon_count + necro_count + barb_count + dru_count + sin_count
        profile_number = 1  # Start a continuous counter here
        max_possible_profiles = game_exe_limit if double_limit <= 0 else game_exe_limit + double_limit
        if total_profiles_required > max_possible_profiles:
            messagebox.showerror("Warning", f"Lower the profile count so it doesn't exceed the\nmax game count or increase Double up counter.")
            return

        if game_exe_limit == 0 or key_count == 0:
            messagebox.showerror("Warning", "Game.exe & Total Keys To Use cannot be 0")
            return

        if game_exe_limit > key_count:
            messagebox.showerror("Warning", "Max Game Paths limit is incorrect. It must not be greater then the Total Keys.")
            return

        # Check if D2BotSoloPlay.dbj is selected and ensure at least one build class is selected
        if self.entry_script.get() == "D2BotSoloPlay.dbj":
            total_build_classes_selected = (
                self.pal_count.get() + self.sorc_count.get() + self.zon_count.get() +
                self.necro_count.get() + self.barb_count.get() + self.dru_count.get() +
                self.sin_count.get()
            )

            if total_build_classes_selected == 0:
                messagebox.showerror("Warning", "At least one build class must be selected\nwhen using D2BotSoloPlay.dbj.")
                return

            # Warning checks for Class Builds
            for class_name, class_count in {
                "PAL": pal_count,
                "SORC": sorc_count,
                "ZON": zon_count,
                "NECRO": necro_count,
                "BARB": barb_count,
                "DRU": dru_count,
                "SIN": sin_count
            }.items():
                total_tags = sum(var.get() for var in self.info_tag_counts[class_name].values())
                if total_tags < class_count:
                    messagebox.showerror("Warning", f"Not enough build names selected for {class_name}.\nThe amount should only equal the profile count {class_count}.")
                    return

                if total_tags > class_count:
                    messagebox.showerror("Warning", f"Too many build names selected for {class_name}.\nThe amount should only equal the profile count {class_count}.")
                    return

        # Check if D2BotLead.dbj is selected and ensure at least one build class is selected
        if self.entry_script.get() == "D2BotLead.dbj":
            total_build_classes_selected = (
                self.pal_count.get() + self.sorc_count.get() + self.zon_count.get() +
                self.necro_count.get() + self.barb_count.get() + self.dru_count.get() +
                self.sin_count.get()
            )

            if total_build_classes_selected == 0:
                messagebox.showerror("Warning", "At least one profile count must be selected\nwhen using D2BotLead.dbj.")
                return

        # Warning checks for Game Path
        base_path = self.game_path.get().strip()
        if not base_path:
            messagebox.showwarning("Warning", "Game Field was left blank.\nProfiles will be created without game paths.")

        if base_path and not base_path.endswith("\\"):
            base_path += "\\"

        profiles = []
        d2path_counter = 1
        d2path_use_count = 0

        for class_key, count in {
            "PAL": pal_count,
            "SORC": sorc_count,
            "ZON": zon_count,
            "NECRO": necro_count,
            "BARB": barb_count,
            "DRU": dru_count,
            "SIN": sin_count
        }.items():
            prefix_code = self.prefix_selection[class_key].get().split(' ')[0]

            builds = [tag for tag, var in self.info_tag_counts[class_key].items() for _ in range(var.get())]
            for i in range(count):
                profile_name = f"{prefix_code}-{class_key}-{str(profile_number).zfill(3)}"
                key_list = f"Key {str(profile_number).zfill(3)}"
                # Ensure the game name is blank if it is 'Disabled'
                final_game_name = "" if self.game_name.get() == "Disabled" else f"{self.game_name.get()}{self.game_name_counter}-"
                self.game_name_counter += 1  # Increment for the next profile

                if base_path:
                    if d2path_counter <= game_exe_limit:
                        if d2path_counter <= double_limit and d2path_use_count < 2:
                            # Double up logic
                            d2path = f"{base_path}Game{d2path_counter}.exe"
                            d2path_use_count += 1
                        else:
                            # Move to the next game path
                            d2path_counter += 1
                            d2path_use_count = 1
                            d2path = f"{base_path}Game{d2path_counter}.exe"
                    else:
                        # Use the last available game path if exceeding the game_exe_limit
                        d2path = f"{base_path}Game{game_exe_limit}.exe"
                else:
                    d2path = ""

                info_tag = builds[i % len(builds)] if builds else ""
                profiles.append(self.create_profile_entry(profile_name, d2path, key_list, info_tag, realm, mode, entry_script, final_game_name))
                profile_number += 1

        self.save_profiles(profiles)

    def create_profile_entry(self, profile_name, d2path, key_list, info_tag, realm, mode, entry_script, final_game_name):
        return {
            "Account": "", "Password": "", "Character": "", "GameName": final_game_name, "GamePass": "",
            "D2Path": d2path, "Realm": realm, "Mode": mode, "Difficulty": "Normal",
            "Parameters": "-w -ns -lq -sleepy -ftj", "Entry": entry_script,
            "Location": "x, y", "KeyList": key_list, "Schedule": "", "GameCount": 0,
            "Runs": 0, "Chickens": 0, "Deaths": 0, "Crashes": 0, "Restarts": 0,
            "RunsPerKey": 0, "KeyRuns": 0, "InfoTag": info_tag, "Visible": False,
            "SwitchKeys": False, "ScheduleEnable": False, "Type": 0, "Name": profile_name, "Group": "default"
        }

    # Save profiles to "Generated Profiles" folder
    def save_profiles(self, profiles):
        output_file_path = os.path.join(self.generated_profiles_dir, "profile.json")
        with open(output_file_path, "w") as file:
            for profile in profiles:
                json.dump(profile, file, separators=(',', ':'), ensure_ascii=False)
                file.write("\n")

        messagebox.showinfo("Success", f"Profiles generated and saved to:\n{output_file_path}")

    # Save All File Menu
    def save_all_data(self):
        """Collect all data from the GUI and save it to a JSON file."""
        # Collect data
        data = {
            'Profile Count Settings': {
                'Max Game.exe Paths to Make': self.game_exe_limit.get(),
                'Max Game Paths to Double Up': self.double_limit.get(),
                'Total Keys to Use': self.key_count.get()
            },
            'Game Settings': {
                'Select Game Mode': self.mode.get(),
                'Select Realm': self.realm.get(),
                'Select Entry Script': self.entry_script.get(),
                'Game Name': self.game_name.get()
            },

            'Builds': {}
        }

        # Builds
        data['Builds'] = {}
        for class_key in ['PAL', 'SORC', 'ZON', 'NECRO', 'BARB', 'DRU', 'SIN']:
            class_data = {}
            class_data['Profile Count'] = getattr(self, f"{class_key.lower()}_count").get()
            class_data['Prefix'] = self.prefix_selection[class_key].get()
            class_data['tag_name'] = {tag_name: var.get() for tag_name, var in self.info_tag_counts[class_key].items()}
            data['Builds'][class_key] = class_data

        # Handle multiple files by appending a number if the file exists
        base_filename = 'D2PG'
        file_counter = 1
        while True:
            filename = f"{base_filename}{file_counter}.json" if file_counter > 1 else f"{base_filename}.json"
            file_path = os.path.join(self.saved_data_dir, filename)
            if not os.path.exists(file_path):
                break
            else:
                file_counter += 1

        # Save the data
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Success", f"All data saved to:\n{file_path}")

    # Configuration File Settings
    # Update with the game path from the input field
    def save_game_path(self):
        config_file_path = os.path.join(self.saved_data_dir, "config.json")
        config_data = {"Path": self.game_path.get(), "Theme": self.theme.get()}
        with open(config_file_path, "w") as file:
            json.dump(config_data, file, indent=2)
        messagebox.showinfo("Success", f"Game path saved to:\n{config_file_path}")

    # Save to "Saved Data" folder
    def save_config(self, config_data):
        config_file_path = os.path.join(self.script_directory, "Saved Data", "config.json")
        with open(config_file_path, "w") as file:
            json.dump(config_data, file, indent=2, ensure_ascii=False)

    def load_config(self):
        # Load if "config.json" exists, and set the game path and theme
        config_file_path = os.path.join(self.script_directory, "Saved Data", "config.json")
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as file:
                config_data = json.load(file)
                self.game_path.set(config_data.get("Path", ""))
                self.theme.set(config_data.get("Theme", "Light Mode"))

    def load_config(self):
        # Load if "config.json" exists, and set the game path and theme
        config_file_path = os.path.join(self.saved_data_dir, "config.json")
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as file:
                config_data = json.load(file)
                self.game_path.set(config_data.get("Path", ""))
                self.theme.set(config_data.get("Theme", "Light Mode"))

    def load_profile(self):
        # Get all files matching D2PG*.json in the Saved Data directory
        profile_files = glob.glob(os.path.join(self.saved_data_dir, "D2PG*.json"))
        self.loaded_profile_game_name = True  # Set flag to True when loading a profile

        if profile_files:
            # Open a file dialog to choose a file to load
            selected_file = filedialog.askopenfilename(
                initialdir=self.saved_data_dir,
                title="Select D2PG Profile",
                filetypes=(("JSON Files", "*.json"),)
            )

            # Load the selected file
            if selected_file:
                with open(selected_file, "r") as file:
                    profile_data = json.load(file)

                    # Populate Profile Count Settings
                    profile_count_settings = profile_data.get("Profile Count Settings", {})
                    self.game_exe_limit.set(profile_count_settings.get("Max Game.exe Paths to Make", 0))
                    self.double_limit.set(profile_count_settings.get("Max Game Paths to Double Up", 0))
                    self.key_count.set(profile_count_settings.get("Total Keys to Use", 0))

                    # Populate Game Settings
                    game_settings = profile_data.get("Game Settings", {})
                    self.mode.set(game_settings.get("Select Game Mode", "Battle.net"))
                    self.realm.set(game_settings.get("Select Realm", "East"))
                    self.entry_script.set(game_settings.get("Select Entry Script", "D2BotSoloPlay.dbj"))
                    self.game_name.set(game_settings.get("Game Name", ""))

                    # Populate Builds
                    builds_data = profile_data.get("Builds", {})
                    for class_key, class_data in builds_data.items():
                        # Set prefix
                        self.prefix_selection[class_key].set(class_data.get("Prefix", self.prefix_options[0]))

                        # Set profile count for each class
                        profile_count = class_data.get("Profile Count", 0)
                        count_var = getattr(self, f"{class_key.lower()}_count", None)
                        if count_var:
                            count_var.set(profile_count)

                        # Set tag counts for each InfoTag
                        tags = class_data.get("tag_name", {})
                        for tag_name, count in tags.items():
                            if tag_name in self.info_tag_counts[class_key]:
                                self.info_tag_counts[class_key][tag_name].set(count)

            # After loading the profile, reset the flag
            self.loaded_profile_game_name = False
        else:
            messagebox.showwarning("No Profiles Found", "No D2PG profile files found in the Saved Data folder.")

# Run the GUI
root = tk.Tk()
app = ProfileGeneratorGUI(root)
root.mainloop()
