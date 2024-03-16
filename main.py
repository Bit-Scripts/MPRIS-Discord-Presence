from dbus import SessionBus
import dbus
import os
import time
import json
from dotenv import load_dotenv
from pypresence import Presence
import pypresence
import pympris
from minio import Minio
from minio.error import S3Error
from mimetypes import guess_type
import magic

# Obtient le chemin d'accès au dossier du script actuel
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construit le chemin d'accès au fichier .env basé sur le dossier du script
env_path = os.path.join(script_dir, '.env')

# Charge les variables d'environnement depuis le fichier .env spécifié
load_dotenv(env_path)

# Discord RPC and AWS S3/MinIO configuration :
MINIO_URL = os.getenv('MINIO_URL')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')  # Assurez-vous que ceci est votre propre Client ID Discord

# Construit le chemin d'accès au fichier de cache d'image basé sur le dossier du script
CACHE_PATH = os.path.join(script_dir, 'image_cache.json')  # Chemin vers un fichier de cache pour les images téléchargées

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
    'Strawberry': 'strawberry',
    'default_icon': 'default_icon',
}

RPC = Presence(DISCORD_CLIENT_ID, response_timeout=15)
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
    print(player_name)
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

def upload_file_to_minio(bucket_name, file_path, object_name=None):
    if file_path.startswith('file://'):
        image_path_str = file_path[7:]
    else:
        image_path_str = file_path

    # Lecture du cache
    data = get_json("image_cache")

    # Vérification du cache
    cached_url = data.get(image_path_str)
    if cached_url:
        print(f"URL depuis le cache pour {image_path_str}: {cached_url}")
        return cached_url

    # Configuration du client MinIO
    client = Minio(
        MINIO_URL,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=True
    )
    
    if object_name is None:
        object_name = os.path.basename(image_path_str)

    mime_type = magic.from_file(image_path_str, mime=True)

    try:
        # Utilisez python-magic pour deviner le type MIME basé sur le contenu du fichier
        client.fput_object(
            bucket_name, object_name, image_path_str,
            content_type=mime_type,  # Utilisez le type MIME déterminé par python-magic
        )
        print(f"Fichier {image_path_str} uploadé comme {object_name} avec le type MIME {mime_type}.")

        # Construire l'URL de l'objet
        scheme = "https://"
        object_url = f"{scheme}{MINIO_URL}/{bucket_name}/{object_name}"

        # Mise à jour du cache uniquement si l'upload réussit
        data[image_path_str] = object_url
        update_json(data, "image_cache")

        return object_url
    except S3Error as exc:
        print("Erreur lors de l'upload:", exc)
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
    try:
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
    except pypresence.exceptions.ResponseTimeout:
        print("Timeout en attente de réponse de Discord. Tentative de reconnexion...")

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
    return upload_file_to_minio('coversimage', art_url)

if __name__ == "__main__":
    main()