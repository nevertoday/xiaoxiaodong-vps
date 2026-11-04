# XXD VPS

[中文](./README.md) · [English](./README.en.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [العربية](./README.ar.md) · [Español](./README.es.md) · [Français](./README.fr.md) · [Русский](./README.ru.md) · **Deutsch** · [Português](./README.pt.md)

Geschäftsreise in ein Land, in dem das Internet schwer nutzbar ist? Nutzen Sie Ihre gewohnten Websites und KI-Tools einfach weiter.

Schritt-für-Schritt-Anleitung als Website (auf Englisch und Chinesisch): <https://vps.xiaoxiaodong.ai/en/> (chinesische Version: <https://vps.xiaoxiaodong.ai>; Spiegel: <https://nevertoday.github.io/xiaoxiaodong-vps/en/>)

So geht's: Sie installieren Codex auf Ihrem eigenen Computer, kaufen einen Server im Ausland, lassen ihn von Codex mit diesem Projekt aus der Ferne einrichten und importieren ein Abo auf Handy und Computer. **Auf dem Server installieren Sie nichts, und Sie müssen sich dort auch nicht anmelden.** Die Verbindung gehört nur Ihnen und wird nicht mit Fremden geteilt.

## Was Sie bekommen

- **Ihre eigene Verbindung** für Computer, Handy und Router. Es gibt einen Haupt- und einen Reserveknoten: Fällt einer aus, wird automatisch auf den anderen umgeschaltet.
- **Sofort nutzbar nach dem Import.** Regeln für gängige Websites und KI-Tools sind schon eingerichtet. Websites aus Festlandchina werden direkt verbunden, alles andere läuft über Ihren Server.
- **CLIProxyAPI**: Ihr eigener API-Zugang mit Verwaltungsoberfläche, der sich automatisch auf die neueste Version aktualisiert.
  - ⚠️ **Verbinden Sie kein Claude-Konto mit CLIProxyAPI**: Die Richtlinien von Anthropic erlauben das nicht. OpenAI hat erklärt, dass ChatGPT-Konten so genutzt werden dürfen – ich nutze das selbst sehr gern zum Erstellen von Bildern.
- **Sicher**: Der Server akzeptiert nur den Schlüssel auf Ihrem Computer und nutzt ein echtes HTTPS-Zertifikat, der Browser warnt also nie mit „nicht sicher“.
- **Kaum Wartung**: Zertifikate, Regeln und CLIProxyAPI aktualisieren sich selbst, die Konfiguration wird täglich gesichert.

## Vier Schritte

### 1. Codex auf dem Computer installieren

Codex ist die KI-App von OpenAI; Sie melden sich mit einem bezahlten ChatGPT-Tarif an. Sie kommt auf **Ihren eigenen Computer**, nicht auf den Server.

- **Einsteiger**: Installieren Sie die Desktop-App. Unter Windows suchen Sie im Microsoft Store nach **Codex** und installieren es; auf dem Mac laden Sie es von der [Codex-Website](https://openai.com/codex/) herunter. Öffnen und mit dem ChatGPT-Konto anmelden.
- **Erfahrene**: Nutzen Sie [Codex](https://github.com/openai/codex) auf der Kommandozeile. Schon installiert? Führen Sie im Terminal `codex` aus und sprechen Sie einfach mit ihm.

Kein ChatGPT-Tarif? Schritt 3 auf der [Anleitungs-Website](https://vps.xiaoxiaodong.ai/en/guide/3-deploy/) bietet den Weg „Type it yourself“ (alles selbst eingeben).

### 2. Server kaufen

Nehmen Sie derzeit **BandwagonHost** – ich nutze es selbst.

Dass ich genau diese Art Server empfehle, ist eine **teuer bezahlte und schmerzhaft gelernte Lektion**: Die Leitungen sind für Verbindungen aus Festlandchina optimiert, und sie laufen so stabil, dass ich zum treuen Fan geworden bin.

**[BandwagonHost kaufen](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=88&billingcycle=quarterly&configoption%5B17%5D=55)**

Der Tarif hinter diesem Link enthält **2 TB Datenvolumen pro Monat** und 2 GB RAM, im CN2-GIA-Rechenzentrum in Los Angeles – mehr als genug für Sie und Ihre Familie.

Der bisher empfohlene ~~[1-TB-Tarif](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)~~ ist ausverkauft und lässt sich derzeit nicht bestellen.

[DMIT](https://www.dmit.io/aff.php?aff=23544) nutze ich ebenfalls sehr gern, aber es ist im Moment leider ausverkauft. Warten lohnt sich nicht.

**Warum empfehle ich nur diese beiden?** BandwagonHost und DMIT sind die zwei, bei denen ich nach vielen Tests geblieben bin, und die einzigen, die ich derzeit guten Gewissens empfehlen kann. Der Tarif im Link oben ist außerdem der einzige Einstiegstarif, den die beiden gerade auf Lager haben. Viele andere Anbieter wirken anfangs gut, haben aber viele Haken: An normalen Tagen läuft es, doch wenn es angespannt wird, halten sie nicht durch – die Verbindung bricht ab oder kommt gar nicht erst zustande, und bei KI-Diensten kann das sogar Ihr Konto gefährden. Ich habe mich damit so oft herumgeärgert, dass ich es ehrlich gesagt leid bin. Kaufen Sie deshalb am besten direkt hier und sparen Sie sich die Umwege, die ich gegangen bin.

> Alle Links hier sind meine Empfehlungslinks. Wenn Sie darüber kaufen, erhalte ich unter Umständen eine Provision; diese Einnahmen verwende ich für wohltätige Zwecke. Preise und Verfügbarkeit laut den offiziellen Websites.

Wählen Sie **Ubuntu 24.04** als System. Sobald der Server bereit ist, notieren Sie aus dem Kundenbereich drei Dinge: **Server-IP, root-Passwort (oder Schlüsseldatei) und SSH-Port**. Bei BandwagonHost notieren Sie außerdem **VEID und API Key** (Seite „API“ im linken Menü von KiwiVM, [so finden Sie sie](https://vps.xiaoxiaodong.ai/en/howto/traffic-and-ip/)), damit der Verbrauch in Ihren Apps mit dem Kundenbereich übereinstimmt.

Nach dem Kauf melden Sie sich nicht am Server an und installieren dort nichts – der nächste Schritt ist Sache von Codex.

### 3. Von Codex einrichten lassen

Öffnen Sie Codex aus Schritt 1 (jedes andere KI-Tool, das Befehle auf Ihrem Computer ausführen kann, geht auch). Kopieren Sie den Text unten, füllen Sie ihn aus und senden Sie ihn ab:

```text
Bitte richte meinen neuen Server nach dem Plan „XXD VPS“ ein.

Plan: https://github.com/nevertoday/xiaoxiaodong-vps
Lade dieses Projekt zuerst auf meinen Computer und lies
skills/xiaoxiaodong-vps/SKILL.md vollständig. Halte dich genau an die
Schritte und Regeln dort und nutze die Skripte des Projekts für Einrichtung
und Prüfung. Bitte sprich mit mir auf Deutsch.

Mein Server:
- IP:
- Anmeldung: Startpasswort (lass es mich selbst eingeben; bitte mich nicht, es im Chat zu schicken)
- SSH-Benutzer und Port: Standard
- Name, mit dem ich mich künftig anmelden will: bwg
- BandwagonHost VEID und API Key (für den offiziellen Verbrauch; Zeile löschen, wenn es kein BandwagonHost ist):
```

Was Sie ausfüllen:

- **IP**: die Server-IP aus dem Kundenbereich.
- **Anmeldung**: Wenn Ihr Anbieter eine Schlüsseldatei mitgegeben hat, ersetzen Sie es durch `Schlüsseldatei: Pfad zur Datei` (ein Zip geht auch).
- **Name**: Ersetzen Sie `bwg` durch einen beliebigen Namen. Danach genügt `ssh dieser-name`, um sich am Server anzumelden.
- **BandwagonHost**: Tragen Sie VEID und API Key in die letzte Zeile ein. Dann lesen Ihre Apps Datenvolumen, Verbrauch und Rücksetztag direkt bei BandwagonHost – bei 1 TB wie bei 2 TB stimmt die Anzeige. **Kein BandwagonHost? Dann löschen Sie diese Zeile**; angezeigt wird dann gegen 1000 GB pro Monat.

Wenn Benutzer und Port nicht root / 22 sind, ersetzen Sie „Standard“ durch die echten Werte.

Dann warten Sie, bis die KI fertig ist, meist 10–20 Minuten. Zwischendurch öffnet sich auf Ihrem Computer einmal ein Passwortfenster; geben Sie dort das Server-Passwort ein. **Fügen Sie das Passwort nie in den Chat ein.** Nach der Einrichtung ist die Passwort-Anmeldung abgeschaltet; anmelden kann sich nur noch dieser Computer.

Kann die KI das Projekt nicht herunterladen, [laden Sie das ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) selbst herunter, entpacken Sie es und ergänzen Sie den Text um die Zeile: „Das Projekt liegt bereits hier: Ordnerpfad“.

Danach liegt auf Ihrem Schreibtisch die Datei `my-server-ihr-name-subscriptions-and-accounts-de.md` mit:

- der **Clash-Abo-URL** für Computer und Router und der **Shadowrocket-Abo-URL** fürs iPhone;
- Adresse, Benutzername und Passwort des 3x-ui-Panels;
- Adresse der CLIProxyAPI-Verwaltung, deren Anmeldeschlüssel, API-Adresse und API-Schlüssel.

<details>
<summary>Richten Sie öfter Server ein? Als Skill installieren und mit einem Satz aufrufen</summary>

Einmal im Terminal ausführen:

```bash
git clone https://github.com/nevertoday/xiaoxiaodong-vps.git
mkdir -p ~/.claude/skills ~/.codex/skills
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.claude/skills/
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.codex/skills/
```

Danach genügt es, der KI „richte meinen neuen Server mit xiaoxiaodong-vps ein“ zu sagen; die nötigen Angaben fragt sie selbst ab.

</details>

### 4. Abo importieren

- **Computer (empfohlen: Clash Verge Rev)**: [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases) installieren, die Clash-Abo-URL importieren, den Modus **Regel (Rule)** wählen und den **TUN-Modus** (virtuelle Netzwerkkarte; bei Nachfrage den Dienst installieren) einschalten. Mit nur dem System-Proxy kann WebRTC im Browser Ihre echte IP verraten – siehe die [Anleitung gegen WebRTC-Lecks](./docs/Clash-Verge-WebRTC泄露修复手册.md) (auf Chinesisch, so geschrieben, dass ein KI-Assistent sie Schritt für Schritt befolgen kann).
- **iPhone**: die Shadowrocket-Abo-URL in Shadowrocket importieren.
- **Router (OpenClash)**: dieselbe Clash-Abo-URL funktioniert, so nutzen alle Geräte zu Hause die Leitung. Unter Konfigurations-Abo hinzufügen (die YAML-Datei nicht hochladen, sonst fehlt die Verbrauchsanzeige und die Regeln aktualisieren sich nicht), die Online-Abo-Konvertierung ausschalten und den Meta-Kern verwenden.
- **Sie nutzen bereits v2rayN (Windows / Mac / Linux)**: funktioniert, aber nur als Ausweichlösung. Importieren Sie die Abo-URL aus der Zeile „Shadowrocket (iPhone)“ (nicht die Clash-Zeile), wählen Sie das Routing „Festlandchina umgehen“ und schalten Sie TUN gegen WebRTC-Lecks ein. Dieses Abo enthält nur die Knoten, ohne KI-Routing und WeChat-Direktregeln – deshalb bleibt Clash Verge Rev die Empfehlung am Computer. Siehe [v2rayN-Anleitung](https://vps.xiaoxiaodong.ai/en/howto/v2rayn/) (Englisch).

Öffnen Sie dann <https://ip.net.coffee/claude/>. Wird die IP Ihres Servers angezeigt, sind Sie verbunden.

## Vor der Reise

- **Richten Sie alles vor der Abreise ein und testen Sie es.** In einem eingeschränkten Netz kann schon das Herunterladen des Projekts oder das Öffnen von KI-Tools viel schwieriger werden.
- Installieren Sie die Clients und importieren Sie die Abos auf Handy und Computer, und prüfen Sie, ob beide Knoten verbinden.
- Erreicht ein lokales Netz Ihren Server nicht, probieren Sie zuerst ein anderes (Hotel-WLAN, mobile Daten, anderer Anbieter). Geht gar nichts, ist die Server-IP dort vermutlich gesperrt. Das lässt sich nicht per Konfiguration beheben; bitten Sie Ihren Anbieter um eine neue IP.
- Nutzen Sie die Verbindung nur selbst und mit Ihrer Familie. Geben Sie sie nicht weiter.

## Server später prüfen

Senden Sie der KI diesen Text (ersetzen Sie `bwg` durch Ihren Namen):

```text
Bitte prüfe meinen Server nach dem Plan „XXD VPS“: ssh bwg

Plan: https://github.com/nevertoday/xiaoxiaodong-vps
Lade das Projekt herunter und lies den Teil „以后的复核和维护“ (spätere
Prüfung und Wartung) in skills/xiaoxiaodong-vps/SKILL.md.
Prüfe zuerst nur, sag mir, was fehlgeschlagen ist und warum, und repariere erst, wenn ich zustimme.
Zeige keine Passwörter, Abo-URLs oder Schlüssel im Chat. Bitte sprich mit mir auf Deutsch.
```

Die ausführliche Dokumentation ([Fehlerbehebung](./skills/xiaoxiaodong-vps/references/troubleshooting.md), [Aufbau im Detail](./skills/xiaoxiaodong-vps/references/design.md)) gibt es derzeit nur auf Chinesisch; Ihre KI kann sie für Sie lesen.

## Feedback und Vorschläge

Sie haben einen Vorschlag, oder etwas ist unklar bzw. funktioniert nicht wie beschrieben? [Eröffnen Sie ein Issue auf GitHub](https://github.com/nevertoday/xiaoxiaodong-vps/issues), [schreiben Sie mir auf X](https://x.com/xiaoxiaodong) (@xiaoxiaodong) oder fügen Sie mich auf WeChat hinzu (Xiaoxiaodong, 小小东). Ich nehme es in die Anleitung auf.

<img src="https://vip.xiaoxiaodong.ai/site-assets/wechat-qr.png" width="160" alt="WeChat-QR-Code von Xiaoxiaodong">

## Datenschutz

- Dieses Projekt enthält keinerlei Informationen über echte Server.
- Passwörter, Schlüssel, Abo-URLs und API-Schlüssel jedes Servers werden bei der Einrichtung neu erzeugt und nur auf dem Server und Ihrem Computer gespeichert. Die KI zeigt sie nicht im Chat.
- Veröffentlichen Sie Ihre Zugangsdatei, Abo-URLs und Schlüssel nirgends und machen Sie keine Screenshots davon.
- Sicherheitsprobleme melden Sie bitte gemäß [SECURITY.md](./SECURITY.md).

Ob und wie schnell Sie sich verbinden können, hängt auch vom lokalen Netz und vom Routing des Servers ab. Dieses Projekt sorgt dafür, dass der Server richtig eingerichtet ist, kann aber nicht garantieren, dass dieselbe IP aus jedem Land und von jedem Anbieter erreichbar ist.

## Lizenz

[MIT](./LICENSE)
