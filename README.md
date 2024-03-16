# MPRIS Discord Presence  
  
## Overview  
MPRIS Discord Presence is a Python application designed to integrate music playback information from various MPRIS-compatible media players with Discord's Rich Presence feature. It displays current playing track information and player icons on Discord status.  
  
![Illustration](https://media.discordapp.net/attachments/1206047501740675132/1206208623097942107/image.png?ex=65db2c52&is=65c8b752&hm=428f296082a428b3f8c26ac7222af798e38efe3e267a0518af3762b97dba6808&=&format=webp&quality=lossless&width=1040&height=848)
  
## Features  
- Displays current playing song (title, artist) on Discord.  
- Shows playback status with customized player icons.  
- Supports multiple MPRIS-compatible media players.  
  
## Requirements
- Python 3.6 or later.  
- dbus, minio, pypresence, python-magic, pympris Python packages.  
- An [AWS S3 account](https://aws.amazon.com/fr/s3/).  
- A [Discord application](https://discord.com/developers/applications) with Rich Presence assets.  

## Installation
Clone the repository to your local machine:
  
```bash
git clone https://github.com/Bit-Scripts/MPRIS-Discord-Presence  
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
  
2. Configure your [AWS S3 account](https://docs.aws.amazon.com/fr_fr/AmazonS3/latest/userguide/GetStartedWithS3.html) or MinIO server and DISCORD_CLIENT_ID in the .env file. For AWS S3, this information will be supplied by AWS. For MinIO, you will have configured this information when you set up your server.
```plaintext
DISCORD_CLIENT_ID='your_discord_client_id'
MINIO_URL='s3.amazonaws.com'  # Use this value for AWS S3. For local MinIO, use the URL of your MinIO instance.
MINIO_ACCESS_KEY='your_access_key_for_aws_s3_or_minio'
MINIO_SECRET_KEY='your_secret_key_for_aws_s3_or_minio'
```
  
3. For your MPRIS Discord Presence application, music player icons are downloaded and configured in the Art Assets of your Discord application via the Discord Developer Portal.These icons are used to customize the appearance of your Discord Rich Presence, displaying the player in use. In contrast, the MinIO or AWS S3 bucket is used to store the album art and video thumbnails that are displayed in your Discord Rich Presence. It's crucial to create this bucket to store these images and configure it to allow public access. This ensures that Discord can access the images and display them correctly in the rich presence. The bucket should only contain images intended for public sharing, as access to them is open to all. Be sure to follow the bucket creation steps provided by your storage service (MinIO or AWS S3) and adjust the privacy settings to allow public access to images.  
    
4. Uploading Icons to Your Discord Bot:
- Ensure you have a folder named `playersIcons` containing all the player icons you wish to use.
- Navigate to the Discord Developer Portal, select your application, and go to the "Rich Presence" > "Art Assets" section.
- Upload each icon from the `playersIcons` folder to your Discord application. The name you give each icon in the Discord Developer Portal should match exactly with the keys in the `ICON_NAMES` dictionary within your script.  
  
#### Note
It is crucial to add all the icons from the `playersIcons` folder one by one into your Discord application, ensuring each icon's name in the Discord Developer Portal corresponds to its intended use within your application, as specified in the `ICON_NAMES` dictionary.  
  
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