from dbus import SessionBus
import dbus
import os
import time
import json
import requests
from dotenv import load_dotenv
from pyimgur import Imgur
from pypresence import Presence
import pympris

# Charge les variables d'environnement depuis un fichier .env
load_dotenv()

IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')  # Assurez-vous que ceci est votre propre Client ID Discord
CACHE_PATH = "./image_cache.json"  # Chemin vers un fichier de cache pour les images téléchargées

ICON_NAMES = {
    'Clementine': 'clementine',
    'Media Player Classic Qute Theater': 'mpc-qt',
    'mpv': 'mpv',
    'Music Player Daemon': 'mpd',
    'VLC media player': 'vlc',
    'SMPlayer': 'smplayer',
    'Lollypop': 'lollypop',
    'Mozilla Firefox': 'firefox',
    'MellowPlayer': 'mellowplayer',
    'Chrome': 'chrome',
    'Spotify': 'spotify',
    'default_icon': 'default_icon',
}

RPC = Presence(DISCORD_CLIENT_ID)
RPC.connect()

def get_icon_by_name(icon_name):
    # Retourne le nom de l'icône basé sur le nom de l'application
    return ICON_NAMES.get(icon_name)

def get_mpris_players():
    session_bus = SessionBus()
    return [service for service in session_bus.list_names() if service.startswith('org.mpris.MediaPlayer2.')]

def get_active_player():
    players = get_mpris_players()
    if not players:
        print("Aucun lecteur trouvé.")
        return None, None
    player_id = players[0]  # Exemple : Prend le premier lecteur trouvé
    bus = dbus.SessionBus()
    players_ids = list(pympris.available_players())
    mp = pympris.MediaPlayer(players_ids[0], bus)
    player_name = mp.root.Identity
    player_bus = SessionBus().get_object(player_id, "/org/mpris/MediaPlayer2")
    return dbus.Interface(player_bus, "org.freedesktop.DBus.Properties"), player_name

def get_current_track_info(player_properties):
    metadata = player_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    title = metadata.get('xesam:title', "Titre inconnu")
    artist = metadata.get('xesam:artist', ["Artiste inconnu"])[0]
    art_url = metadata.get('mpris:artUrl', "")
    return title, artist, art_url

# Récupération
def get_json(f="image_cache", encoding="utf-8"):
    try:
        with open(f"./{f}.json", "r", encoding=encoding) as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        update_json({})

# Mise à Jour
def update_json(data, f="image_cache", encoding="utf-8"):
    with open(f"{f}.json", "w", encoding=encoding) as file:
        json.dump(data, file, indent=4)

def upload_image_to_imgur(image_path):
    # Assurez-vous de normaliser le chemin de l'image avant de l'utiliser.
    image_path_str = image_path.removeprefix('file://')
    data = get_json("image_cache")
    
    if data is None:
        data = {}
        update_json(data)
    
    # Utilisez la méthode get pour éviter KeyError et vérifiez si l'image est déjà dans le cache.
    cached_url = data.get(image_path_str)
    if cached_url:
        # print(f'URL depuis le cache pour {image_path_str}:', cached_url)
        return cached_url

    # Si l'image n'est pas dans le cache, procédez à l'upload.
    if os.path.isfile(image_path_str):
        try:
            imgur = Imgur(IMGUR_CLIENT_ID)
            uploaded_image = imgur.upload_image(path=image_path_str, title="Now Playing")
            # Mise à jour du cache avec la nouvelle image.
            data[image_path_str] = uploaded_image.link
            update_json(data)
            return uploaded_image.link
        except requests.exceptions.HTTPError as e:
            print(f"Erreur lors de l'upload de l'image: {e}")
            if e.response.status_code == 429:
                print("Taux limite atteint, veuillez attendre avant de réessayer.")
        except Exception as e:
            print(f"Erreur inattendue: {e}")
    else:
        print("Le fichier n'existe pas:", image_path_str)

    return None

def format_time(microseconds):
    # Convertit les microsecondes en minutes et secondes
    seconds = int(microseconds / 1000000)  # Convertit en secondes
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

def update_discord_presence(title, artist, position, duration, image_link, player_name):
    current_time = time.time()  # Temps actuel en secondes
    start_timestamp = current_time - (position / 1000000)  # Convertit position en secondes et soustrait de l'heure actuelle
    end_timestamp = start_timestamp + (duration / 1000000) 

    # Utilisez une icône par défaut si le lecteur n'est pas dans la liste
    icon_name = get_icon_by_name(player_name) or get_icon_by_name("default_icon")
    large_image = image_link or icon_name

    # Met à jour la présence Discord avec une barre de progression
    RPC.update(
        details=title,
        state=f"par {artist}",
        start=start_timestamp,
        end=end_timestamp,
        large_image=large_image,
        small_image=icon_name,
        large_text="Écoute en cours",
        small_text=player_name
    )

def get_player_properties():
    session_bus = SessionBus()
    for service in session_bus.list_names():
        if service.startswith('org.mpris.MediaPlayer2.'):
            try:
                player = session_bus.get_object(service, '/org/mpris/MediaPlayer2')
                properties_manager = dbus.Interface(player, dbus_interface='org.freedesktop.DBus.Properties')
                metadata = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
                position = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'Position')
                duration = metadata.get('mpris:length', 0)  # Fournit une valeur par défaut de 0 si non trouvé
                return position, duration
            except dbus.DBusException as e:
                print(f"Erreur DBus lors de la récupération des propriétés du lecteur : {e}")
                continue  # Continue à essayer avec les autres services si l'un échoue
    return None, None

def main():
    while True:
        player_properties, player_name = get_active_player()
        if player_properties:
            title, artist, art_url = get_current_track_info(player_properties)
            position, duration = get_player_properties()  # Assurez-vous que cette fonction retourne ces deux valeurs

            if title and artist:
                image_link = handle_image_caching_and_upload(art_url) if art_url else None
                update_discord_presence(title, artist, position, duration, image_link, player_name)
            else:
                clear_discord_presence()
        else:
            print("Aucun lecteur trouvé.")
            clear_discord_presence()

        time.sleep(5)

def clear_discord_presence():
    try:
        RPC.clear()  # Efface la présence sur Discord
        print("Présence Discord effacée.")
    except Exception as e:
        print(f"Erreur lors de l'effacement de la présence Discord: {e}")

def handle_image_caching_and_upload(art_url):
    # Logique de cache et d'upload d'image comme montré précédemment
    # Retourne le lien de l'image uploadée ou le lien du cache
    return upload_image_to_imgur(art_url)

if __name__ == "__main__":
    main()