# MPRIS Discord Presence  
  
## Overview  
MPRIS Discord Presence is a Python application designed to integrate music playback information from various MPRIS-compatible media players with Discord's Rich Presence feature. It displays current playing track information and player icons on Discord status.  
  
## Features  
- Displays current playing song (title, artist) on Discord.  
- Shows playback status with customized player icons.  
- Supports multiple MPRIS-compatible media players.  
  
## Requirements
- Python 3.6 or later.  
- dbus, pyimgur, pypresence, pympris Python packages.  
- An Imgur client ID for image hosting.  
- A Discord application with Rich Presence assets.  

## Installation
Clone the repository to your local machine:
  
```bash
git clone https://your-repository-url/mpris-discord-presence.git  
cd mpris-discord-presence  
```
  
### Install the required Python packages:
  
```bash
pip install -r requirements.txt
```
  
### Configuration
1. Copy the .env-example file to .env:
  
```bash
cp .env-example .env
```
  
2. Obtain and configure your IMGUR_CLIENT_ID and DISCORD_CLIENT_ID in the .env file. You can get these IDs from the Imgur API and Discord Developer Portal respectively.
```plaintext
IMGUR_CLIENT_ID='your_imgur_client_id'
DISCORD_CLIENT_ID='your_discord_client_id'
```
3. Go to the Discord Developer Portal and upload icons for each media player with the names as mentioned in the ICON_NAMES dictionary. Ensure each icon's name matches the key in the dictionary exactly.
  
## Usage
Run the application:
  
```bash
python main.py
```
  
The script will automatically update your Discord presence with the currently playing track information from the active MPRIS media player.
  
## Contributing
Contributions to the MPRIS Discord Presence project are welcome. Please feel free to submit pull requests or open issues to suggest improvements or add new features.

## License
MPRIS Discord Presence is licensed under the GNU General Public License v3.0 (GPLv3). See the [LICENSE](./LICENSE.md) file for more details.