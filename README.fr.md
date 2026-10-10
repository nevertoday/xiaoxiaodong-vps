# XXD VPS

[中文](./README.md) · [English](./README.en.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [العربية](./README.ar.md) · [Español](./README.es.md) · **Français** · [Русский](./README.ru.md) · [Deutsch](./README.de.md) · [Português](./README.pt.md)

Vous partez dans un pays où internet est difficile d'accès ? Continuez à utiliser vos sites et vos outils d'IA habituels.

Le principe : vous achetez votre propre serveur à l'étranger, une IA le configure avec ce projet, puis vous importez un abonnement sur votre téléphone et votre ordinateur. La connexion est à vous seul, sans la partager avec des inconnus.

## Ce que vous obtenez

- **Votre propre connexion** pour ordinateur, téléphone et routeur. Un nœud principal et un nœud de secours : si l'un tombe, l'autre prend le relais automatiquement.
- **Prêt dès l'import.** Les règles pour les sites et outils d'IA courants sont déjà en place. Les sites de Chine continentale se connectent directement ; tout le reste passe par votre serveur.
- **CLIProxyAPI** : votre propre point d'accès API et son panneau d'administration, mis à jour automatiquement vers la dernière version.
- **Sécurisé** : le serveur n'accepte que la clé de votre ordinateur et utilise un vrai certificat HTTPS, donc pas d'avertissement « non sécurisé » dans le navigateur.
- **Presque aucun entretien** : certificats, règles et CLIProxyAPI se mettent à jour tout seuls, et la configuration est sauvegardée chaque jour.

## Trois étapes

### 1. Achetez un serveur

En ce moment, prenez **BandwagonHost**. Le réseau est stable, c'est celui que j'utilise moi-même :

**[Acheter BandwagonHost](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)**

[DMIT](https://www.dmit.io/aff.php?aff=23544) est bien aussi, mais il est en rupture de stock. Inutile d'attendre.

> Ce sont mes deux liens de parrainage. Je peux toucher une commission si vous achetez par leur biais, et je consacrerai ce revenu à des actions caritatives. Prix et disponibilité selon les sites officiels.

Choisissez **Ubuntu 24.04** comme système. Une fois le serveur prêt, notez trois informations dans le panneau : **IP du serveur, mot de passe root (ou fichier de clé) et port SSH**.

### 2. Laissez une IA le configurer

Ouvrez un outil d'IA capable d'exécuter des commandes sur votre ordinateur, comme [Codex](https://github.com/openai/codex) ou [Claude Code](https://claude.com/claude-code) (sous Windows, utilisez-le dans WSL). Copiez le texte ci-dessous, complétez-le et envoyez-le :

```text
Merci de configurer mon nouveau serveur selon le plan « XXD VPS ».

Plan : https://github.com/nevertoday/xiaoxiaodong-vps
Téléchargez d'abord ce projet sur mon ordinateur et lisez entièrement
skills/xiaoxiaodong-vps/SKILL.md. Suivez exactement ses étapes et ses règles,
et utilisez les scripts du projet pour la configuration et la vérification.
Parlez-moi en français, s'il vous plaît.

Mon serveur :
- IP :
- Connexion : mot de passe initial (laissez-moi le saisir moi-même dans le terminal)
- Utilisateur et port SSH : par défaut
- Nom que je veux utiliser pour me connecter : bwg
```

Il n'y a que trois choses à changer :

- **IP** : l'IP du serveur indiquée dans le panneau.
- **Connexion** : si votre fournisseur vous a donné un fichier de clé, remplacez par `fichier de clé : chemin du fichier` (un zip convient).
- **Nom** : remplacez `bwg` par le nom de votre choix. Ensuite, il suffit de taper `ssh ce-nom` pour entrer sur le serveur.

Si l'utilisateur et le port ne sont pas root / 22, remplacez « par défaut » par les vraies valeurs.

Attendez ensuite que l'IA termine, en général 10 à 20 minutes. À un moment, elle vous demandera de saisir le mot de passe du serveur dans le terminal. **Ne collez jamais le mot de passe dans la discussion.** Une fois terminé, la connexion par mot de passe est désactivée et seul cet ordinateur peut se connecter.

Si l'IA n'arrive pas à télécharger le projet, [téléchargez le ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) vous-même, décompressez-le et ajoutez une ligne au texte : « Le projet se trouve déjà ici : chemin du dossier ».

À la fin, un fichier `XXD-VPS-votre-nom-login-fr.md` apparaît sur votre bureau, avec :

- l'**URL d'abonnement Clash** pour ordinateur et routeur, et l'**URL d'abonnement Shadowrocket** pour iPhone ;
- l'adresse, l'utilisateur et le mot de passe du panneau 3x-ui ;
- l'adresse du panneau CLIProxyAPI, sa clé de connexion, l'adresse de l'API et la clé API.

<details>
<summary>Vous configurez souvent des serveurs ? Installez-le comme skill et appelez-le en une phrase</summary>

À exécuter une fois dans le terminal :

```bash
git clone https://github.com/nevertoday/xiaoxiaodong-vps.git
mkdir -p ~/.claude/skills ~/.codex/skills
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.claude/skills/
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.codex/skills/
```

Ensuite, il suffit de dire à l'IA « utilise xiaoxiaodong-vps pour configurer mon nouveau serveur » et elle vous demandera les informations.

</details>

### 3. Importez l'abonnement

- **Ordinateur** : installez [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases), importez l'URL d'abonnement Clash, choisissez le mode **Règles (Rule)** et activez le **proxy système**.
- **iPhone** : importez l'URL d'abonnement Shadowrocket dans Shadowrocket.
- **Routeur** : importez l'URL d'abonnement Clash dans OpenClash.

Ouvrez ensuite <https://ipinfo.io>. Si l'IP de votre serveur s'affiche, vous êtes connecté.

## Avant de partir

- **Configurez et testez tout avant le départ.** Une fois sur un réseau restreint, télécharger le projet ou même ouvrir des outils d'IA peut devenir bien plus difficile.
- Installez les clients et importez les abonnements sur le téléphone et l'ordinateur, puis vérifiez que les deux nœuds se connectent.
- Si un réseau local n'atteint pas votre serveur, essayez d'abord un autre réseau (Wi-Fi de l'hôtel, données mobiles, autre opérateur). Si rien ne marche, l'IP du serveur est probablement bloquée sur place. Aucun réglage n'y changera rien : demandez une nouvelle IP à votre fournisseur.
- Gardez la connexion pour vous et votre famille. Ne la partagez pas.

## Vérifier le serveur plus tard

Envoyez ceci à l'IA (remplacez `bwg` par votre nom) :

```text
Merci de vérifier mon serveur selon le plan « XXD VPS » : ssh bwg

Plan : https://github.com/nevertoday/xiaoxiaodong-vps
Téléchargez le projet et lisez la partie « 以后的复核和维护 » (vérifications
et maintenance ultérieures) de skills/xiaoxiaodong-vps/SKILL.md.
Commencez par vérifier seulement, dites-moi ce qui a échoué et pourquoi, et ne corrigez rien sans mon accord.
N'affichez ni mots de passe, ni URLs d'abonnement, ni clés dans la discussion. Parlez-moi en français.
```

La documentation détaillée ([dépannage](./skills/xiaoxiaodong-vps/references/troubleshooting.md), [notes de conception](./skills/xiaoxiaodong-vps/references/design.md)) n'existe pour l'instant qu'en chinois ; votre IA peut la lire pour vous.

## Confidentialité

- Ce projet ne contient aucune information sur un serveur réel.
- Les mots de passe, clés, URLs d'abonnement et clés API de chaque serveur sont générés à neuf pendant la configuration et stockés uniquement sur le serveur et sur votre ordinateur. L'IA ne les affiche pas dans la discussion.
- Ne publiez nulle part votre fichier de connexion, vos URLs d'abonnement ou vos clés, et n'en faites pas de capture.
- Pour signaler un problème de sécurité, voir [SECURITY.md](./SECURITY.md).

La possibilité de se connecter, et la vitesse, dépendent aussi du réseau local et de l'acheminement du serveur. Ce projet garantit que le serveur est correctement configuré, pas qu'une même IP soit joignable depuis tous les pays et tous les opérateurs.

## Licence

[MIT](./LICENSE)
