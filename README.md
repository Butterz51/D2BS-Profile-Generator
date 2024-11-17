# D2BS Profile Generator

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [How to Use](#how-to-use)
- [Error Checking](#error-checking)
- [Support](#support)
- [License](#license)

## Overview
The D2BS Profile Generator is a graphical user interface (GUI) application designed to simplify the process of generating profiles for the Diablo II Botting System (D2BS). It allows users to quickly create profiles in JSON format by inputting required details, such as game path, profile counts, and class-specific builds. The generated profiles are compatible with popular D2BS scripts, such as **D2BotSoloPlay.dbj** and **D2BotLead.dbj**. The tool eliminates the potential for errors by automating many aspects of the profile creation process, making it faster and more reliable.

## Features
- **Automated Profile Generation**: Easily create profile files with minimal manual input.
- **Game Path Configuration**: Input the game path for automated profile setup.
- **Profile Count Settings**: Set the number of profiles per class and configure game executable limits.
- **Class-Specific Build Options**: Choose from multiple Diablo II character classes (e.g., Paladin, Sorceress, Barbarian) and their specific builds.
- **Dual Game Executable Support**: Specify if you want to create profiles that use multiple `Game.exe` paths.
- **Profile Prefix Selection**: Choose from predefined profile prefixes (e.g., Hardcore Classic, Softcore Expansion).
- **InfoTags and Additional Options**: Configure special build options for each class (e.g., Bumper, MF, Zealer).
- **Profile File Saving**: Save the generated profiles to a `profile.json` file in the `Generated Profiles` folder.
- **Dark and Light Themes**: Switch between dark and light modes for comfortable use.
- **Save and Load Configurations**: Save your settings and load them later for continued use.
- **User-friendly Interface**: The GUI is built with Tkinter, offering an intuitive and easy-to-navigate layout.

## Requirements
- **Python 3.x**
- **Tkinter** for the GUI
- **JSON** for profile file handling

## How to Use
1. **Set Game Path**: Enter the path to your Diablo II installation.
2. **Configure Profile Count**: Set the number of profiles to generate for each character class (Paladin, Sorceress, etc.).
3. **Select Entry Script**: Choose the D2Bot script (`D2BotSoloPlay.dbj` or `D2BotLead.dbj`) to be used with the profiles.
4. **Choose Profile Prefixes**: Select the appropriate prefix for each class (e.g., Hardcore, Softcore).
5. **Generate Profiles**: Once all settings are configured, click the "Generate Profile" button to create your profiles.
6. **Save Configurations**: Save your settings for future use through the "Save All" option in the menu.
7. **View Profiles**: The generated `profile.json` will be saved in the `Generated Profiles` folder.

## Error Checking
- **Profile Count Warning**: Ensures that the total number of profiles does not exceed the maximum allowed by your `Game.exe` count.
- **Key Count Warning**: Makes sure the number of game executable paths does not exceed the total number of keys to be used.
- **Required Build Class Check**: When using `D2BotSoloPlay.dbj`, it ensures at least one class is selected.

## Support
- **JBH Services Discord**: For general support, join the [JBH Services Discord](https://discord.gg/cUBqFpYHjh).
- **SoloPlay Support**: For **D2BotSoloPlay.dbj** script-related issues, join the [SoloPlay Discord](https://discord.gg/pjKFtfyQK9).
- **BlizzHackers Support**: For **D2BotLead.dbj** script-related issues, join the [BlizzHackers Discord](https://discord.gg/6t45tVF6).

## License
This script is open-source and free to use. Contributions are welcome via the provided Discord channels. You can contribute to the project here on GitHub also.
