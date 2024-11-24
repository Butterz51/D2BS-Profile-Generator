# D2BS Profile Generator

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How to Use](#how-to-use)
- [Optional Features](#optional-features)
- [Error Checking](#error-checking)
- [Support](#support)
- [License](#license)

---

## Overview
The D2BS Profile Generator is a graphical user interface (GUI) application designed to simplify the process of generating profiles for the Diablo II Botting System (D2BS). It allows users to quickly create profiles in JSON format by inputting required details, such as game path, profile counts, and class-specific builds. The generated profiles are compatible with popular D2BS scripts, such as **D2BotSoloPlay.dbj** and **D2BotLead.dbj**. The tool eliminates the potential for errors by automating many aspects of the profile creation process, making it faster and more reliable.

![Overview Screenshot](https://i.imgur.com/a72gcsn.png)

---

## Features
- **Automated Profile Generation**: Easily create profile files with minimal manual input.
- **Game Path Configuration**: Input the game path for automated profile setup (optional).
- **Profile Count Settings**: Set the number of profiles per class and configure game executable limits.
- **Class-Specific Build Options**: Choose from multiple Diablo II character classes (e.g., Paladin, Sorceress, Barbarian) and their specific builds.
- **Dual Game Executable Support**: Specify if you want to create profiles that use multiple `Game.exe` paths.
- **Profile Prefix Selection**: Choose from predefined profile prefixes (e.g., Hardcore Classic, Softcore Expansion).
- **InfoTags and Additional Options**: Configure special build options for each class (e.g., Bumper, MF, Zealer).
- **Dark and Light Themes**: Switch between dark and light modes for comfortable use.
- **Save and Load Configurations**: Save your settings and load them later for continued use.
- **User-friendly Interface**: The GUI is built with Tkinter, offering an intuitive and easy-to-navigate layout.

![Feature Screenshot](https://i.imgur.com/iohwQka.png)

---

## How to Use

### Step 1: Set Game Path
- Enter the path to your Diablo II installation and click **Save** (optional).
![Game Path Input](https://i.imgur.com/7uZQfvs.png)

### Step 2: Set Profile Count Settings
- Set the max number of game executables (`Game.exe`) to create.
- Set the number of keys to use (ensure `Game.exe` count does not exceed the total keys available).

---

### Step 3: Set Game Settings
- Choose the game mode from the dropdown menu (e.g., **Battle.net**, **Single Player**).
- Select the realm (e.g., East, West, Europe, Asia).
- Choose the D2Bot script:
  - **D2BotLead**: You can specify a game name, which will have numbers appended (e.g., `test1-`).
  - **D2BotSoloPlay**: The game name field is disabled.

---

### Step 4: Configure Profile Count
- Set the number of profiles to generate for each character class (Paladin, Sorceress, etc.).

---

### Step 5: Choose Profile Prefixes
- Select the appropriate prefix for each class (e.g., Hardcore, Softcore).

---

### Step 6: Choose Builds
- Specify the number of build types you want to generate for each class (e.g., Hammerdin).
  - The number of builds **cannot exceed the profile count**.
  - Builds are only applicable when using **D2BotSoloPlay**.

---

### Step 7: Generate Profiles
- Once all settings are configured, click the **Generate Profile** button to create your profiles.
![Generate Profiles](https://i.imgur.com/F6ECiPb.png)

---

### Step 8: View Profiles
- The generated `profile.json` will be saved in the `Generated Profiles` folder.
- Copy and paste this file into your **kolbot/data** folder for use.
![Generated Profiles Folder](https://i.imgur.com/5yWG89W.png)

---

### Optional Features

### Save All Configurations
- Save your current settings for future use through the **Save All** option in the **File** menu.
  - Note: The **Game Path** field is **not saved** in this configuration.


### Load Configurations
- Load previously saved settings through the **File > Load Profile** option.

---

## Error Checking
- **Profile Count Warning**: Ensures that the total number of profiles does not exceed the maximum allowed by your `Game.exe` count.
- **Key Count Warning**: Ensures that the number of `Game.exe` paths does not exceed the total number of keys available.
- **Required Build Class Check**: When using **D2BotSoloPlay.dbj**, it ensures that at least one build class is selected.

---

## Support
- **JBH Services Discord**: For general support, join the [JBH Services Discord](https://discord.gg/cUBqFpYHjh).
- **SoloPlay Support**: For **D2BotSoloPlay.dbj** script-related issues, join the [SoloPlay Discord](https://discord.gg/pjKFtfyQK9).
- **BlizzHackers Support**: For **D2BotLead.dbj** script-related issues, join the [BlizzHackers Discord](https://discord.gg/6t45tVF6).

---

## License
This tool is open-source and free to use. Contributions are welcome through the provided Discord channels or via GitHub.
