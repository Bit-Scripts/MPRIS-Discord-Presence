# MPRIS Discord Presence  
  
For English, [rendez-vous](./README.md)
  
## En introduction
      
**MPRIS Discord Presence** est une application Python conçue pour intégrer les informations de lecture musicale de divers lecteurs de médias compatibles MPRIS avec la fonctionnalité Rich Presence de Discord. Elle affiche les informations de la piste en cours de lecture ainsi que les icônes des lecteurs sur le statut Discord. Sur les systèmes Linux, grâce à MPRIS, qui permet d'afficher sur le système le média en cours de lecture sur une grande variété de lecteurs de médias (y compris les navigateurs web) dans l'interface utilisateur, ce script récupère ces données pour les afficher directement dans le profil Discord en utilisant la technologie Discord Rich Presence (Discord RPC). Pour cela, l'installation du client Discord sur le système est nécessaire.
  
Cette intégration permet une expérience utilisateur enrichie, offrant la possibilité de partager avec sa communauté Discord le contenu multimédia en cours de lecture, tout en personnalisant son profil avec des informations détaillées et des icônes spécifiques au lecteur utilisé. Que vous écoutiez de la musique, regardiez une vidéo ou un podcast, MPRIS Discord Presence rend ces moments visibles et partagés avec votre cercle sur Discord, ajoutant ainsi une couche sociale à votre expérience multimédia. 
  
**Illustration :**
  
![Illustration](https://media.discordapp.net/attachments/1206047501740675132/1206208623097942107/image.png?ex=65db2c52&is=65c8b752&hm=428f296082a428b3f8c26ac7222af798e38efe3e267a0518af3762b97dba6808&=&format=webp&quality=lossless&width=1040&height=848)
   
## Caractéristiques  
- Affiche la chanson en cours de lecture (titre, artiste) sur Discord.  
- Affiche l'état de la lecture avec des icônes de lecteur personnalisées.  
- Prend en charge plusieurs lecteurs multimédias compatibles MPRIS.  
  
## Exigences
- Python 3.6 ou supérieur.  
- Paquets Python dbus, minio, pypresence, python-magic, pympris.  
- Un [compte AWS S3](https://aws.amazon.com/fr/s3/).  
- Une [application Discord](https://discord.com/developers/applications) avec des ressources Rich Presence.  

## Installation
Clonez le dépôt sur votre machine locale :
  
```bash
git clone https://github.com/Bit-Scripts/MPRIS-Discord-Presence  
cd mpris-discord-presence  
```
  
### Installer les paquets Python requis :
  
```bash
pip install -r requirements.txt
```
  
### Configuration
1. Copiez le fichier .env-example dans .env :
  
```bash
cp .env-example .env
```
  
2. Configurez votre [compte AWS S3](https://docs.aws.amazon.com/fr_fr/AmazonS3/latest/userguide/GetStartedWithS3.html) ou votre serveur MinIO et DISCORD_CLIENT_ID dans le fichier .env. Pour AWS S3, ces informations seront fournies par AWS. Pour MinIO, vous aurez configuré ces informations lors de la configuration de votre serveur.
  
```plaintext
DISCORD_CLIENT_ID='votre_id_client_discord'
MINIO_URL='s3.amazonaws.com' # Utilisez cette valeur pour AWS S3. Pour MinIO local, utilisez l'URL de votre instance MinIO.
MINIO_ACCESS_KEY='votre_clé_d_accès_pour_aws_s3_ou_minio'
MINIO_SECRET_KEY='votre_clé_secrète_pour_aws_s3_ou_minio'
```
  
3. Pour votre application MPRIS Discord Presence, les icônes des lecteurs de musique sont à télécharger et à configurer dans les `Art Assets` de votre application Discord via le portail développeur de Discord. Ces icônes sont utilisées pour personnaliser l'apparence de votre Discord Rich Presence, en affichant le lecteur en cours d'utilisation. En revanche, le bucket MinIO ou AWS S3 est utilisé pour stocker les pochettes d'album et les vignettes vidéo qui sont affichées dans votre Discord Rich Presence. Il est essentiel de créer ce bucket pour stocker ces images et de lui donner un accès public. Cela garantit que Discord peut accéder aux images et les afficher correctement avec Discord RPC. Le bucket ne doit contenir que des images destinées à être partagées publiquement, car l'accès à ces images est ouvert à tous. Veillez à suivre les étapes de création du bucket fournies par votre service de stockage (MinIO ou AWS S3) et réglez les paramètres de confidentialité pour autoriser l'accès public aux images.   
    
4. Téléchargement des icônes sur votre Discord Bot :
- Assurez-vous d'avoir un dossier nommé `playersIcons` contenant toutes les icônes de joueurs que vous souhaitez utiliser.
- Naviguez sur le portail des développeurs Discord, sélectionnez votre application et allez dans la section "Rich Presence" > "Art Assets".
- Téléchargez chaque icône du dossier `playersIcons` dans votre application Discord. Le nom que vous donnez à chaque icône dans le portail du développeur Discord doit correspondre exactement aux clés du dictionnaire `ICON_NAMES` dans votre script.
  
#### Note
Il est crucial d'ajouter toutes les icônes du dossier `playersIcons` une par une dans votre application Discord, en s'assurant que le nom de chaque icône dans le portail du développeur Discord correspond à son utilisation prévue dans votre application, comme spécifié dans le dictionnaire `ICON_NAMES`.    
  
## Utilisation
Lancez l'application :  
  
```bash
python main.py
```
  
Le script mettra automatiquement à jour votre présence Discord avec les informations sur la piste en cours de lecture à partir du lecteur multimédia MPRIS actif.
  
## Contribuer
Les contributions au projet MPRIS Discord Presence sont les bienvenues. N'hésitez pas à soumettre des pull requests ou des open issues pour suggérer des améliorations ou ajouter de nouvelles fonctionnalités.

## Licence
MPRIS Discord Presence est sous licence GNU General Public License v3.0 (GPLv3). Voir le fichier [LICENSE](./LICENSE.md) pour plus de détails.