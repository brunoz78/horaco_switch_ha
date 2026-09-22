# HORACO Managed Switch — Home-Assistant-Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/brunoz78/horaco_switch_ha)](https://github.com/brunoz78/horaco_switch_ha/releases)
[![Validate](https://github.com/brunoz78/horaco_switch_ha/actions/workflows/validate.yml/badge.svg)](https://github.com/brunoz78/horaco_switch_ha/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue)](https://www.home-assistant.io/)

Überwache deine günstigen Managed Switches von **HORACO**, **keepLink** und baugleichen OEM-Herstellern (Realtek-Chipsatz) direkt in Home Assistant — **ohne zusätzliche App, ohne Docker, ohne Zwischendienst**.

Die Integration meldet sich an der Weboberfläche des Switches an und liest Geräte-Info, Port-Status und Zähler direkt von dessen Seiten aus. Sie erkennt dabei zwei Seitenaufbauten: den der HORACO-Modelle und den der keepLink-KP-9000-Serie, bei der die Port-Daten auf einer anderen Seite stehen. Pro Switch entsteht ein Gerät mit deutschsprachigen Entitäten; mehrere Switches lassen sich parallel einbinden.

---

## Unterstützte Geräte

| Modell | Ports | SFP+ | Status |
|--------|-------|------|--------|
| HORACO HC-SWTGW218AS | 8 × GbE | 2 × 10G | ✅ Bestätigt |
| HORACO HC-SWTGW215AS | 5 × GbE | — | ✅ Bestätigt |
| keepLink KP9000-9XH-X | 8 × GbE | 1 × 10G | ✅ Bestätigt |
| keepLink KP-9000-9XHML-X (FW V100.9.9.1.7) | 8 × 2.5GbE | 1 × 10G | ✅ Bestätigt |
| OEM-Switches mit Realtek RTL8373 | unterschiedlich | — | ✅ Wahrscheinlich |

> Wenn dein Switch eine Weboberfläche auf Port 80 mit Benutzername/Passwort-Anmeldung hat, funktioniert er sehr wahrscheinlich. Eröffne ein Issue, damit er in die Tabelle aufgenommen wird.

---

## Funktionen

- 🔌 **Port-Überwachung** — ein Sensor pro Port mit Verbindung und Geschwindigkeit (z. B. `Getrennt`, `1000M`, `2500M`), optional Duplex, Flusskontrolle und Paketzähler
- 🔄 **Neustart-Taste** — Switch per Knopfdruck aus jedem Dashboard oder jeder Automation neu starten
- ⚡ **Direkte Abfrage im LAN** — vollständig lokal, keine Cloud, kein Proxy
- 🔧 **Einstellbares Abfrageintervall** — 10 bis 300 Sekunden (Standard 30 s)

---

## Installation

### Über HACS (empfohlen)

1. HACS → Integrationen → ⋮ → **Benutzerdefinierte Repositories**
2. URL: `https://github.com/brunoz78/horaco_switch_ha` · Typ: **Integration**
3. **HORACO Managed Switch** installieren und Home Assistant neu starten
4. **Einstellungen → Geräte & Dienste → Integration hinzufügen → HORACO Managed Switch**

### Manuell

1. Die neueste `horaco_switch.zip` unter [Releases](https://github.com/brunoz78/horaco_switch_ha/releases/latest) herunterladen
2. Entpacken und den Ordner `horaco_switch/` nach `<config>/custom_components/` kopieren
3. Home Assistant neu starten und die Integration über die Oberfläche hinzufügen

---

## Einrichtung

| Feld | Standard | Hinweis |
|------|----------|---------|
| IP-Adresse des Switches | — | z. B. `192.168.1.100` |
| HTTP-Port | `80` | Nur ändern, wenn die Weboberfläche auf einem anderen Port läuft |
| Benutzername | `admin` | Standard-Zugangsdaten von HORACO |
| Passwort | `admin` | Standard-Zugangsdaten von HORACO |

Nach der Einrichtung kannst du über **Konfigurieren** auf der Integrationskarte das Abfrageintervall anpassen (10–300 s).

---

## Entitäten

Pro Switch gibt es **ein Gerät**. Alle Entitäten — auch die der einzelnen Ports — hängen direkt an diesem Gerät.

### Switch

| Entität | Typ | Beschreibung |
|---------|-----|--------------|
| Betriebszeit | Sensor | z. B. `3d 14h 22m` — nur wenn die Firmware die Laufzeit meldet |
| Firmware | Sensor | Firmware-Version |
| MAC-Adresse | Sensor | MAC-Adresse des Switches |
| Aktive Ports | Sensor | Anzahl verbundener Ports |
| Ports gesamt | Sensor | Anzahl physischer Ports |
| **Neustart** | **Taste** | Sendet `POST /reboot.cgi` an den Switch |

### Pro Port *(N = 1 … Anzahl Ports)*

| Entität | Typ | Standard | Beschreibung |
|---------|-----|----------|--------------|
| Port N | Sensor | aktiv | Verbindung und Geschwindigkeit in einem: `Getrennt` · `Deaktiviert` · `10M` · `100M` · `1000M` · `2500M` · `5000M` · `10G`. Enthält alle Port-Werte als Attribute. |
| Port N Duplex | Sensor | deaktiviert | `Vollduplex` oder `Halbduplex` |
| Port N Flusskontrolle | Sensor | deaktiviert | `Ein` oder `Aus` |
| Port N Gesendete Pakete | Sensor | deaktiviert | Gesendete Pakete (fortlaufend) |
| Port N Empfangene Pakete | Sensor | deaktiviert | Empfangene Pakete (fortlaufend) |
| Port N Gesendet / Empfangen | Sensor | deaktiviert | Bytes (fortlaufend) — nur wenn der Switch Byte-Zähler liefert |

**Getrennt** heisst: Der Port ist eingeschaltet, aber es ist kein Gerät verbunden (kein Kabel oder Gegenstelle aus). **Deaktiviert** heisst: Der Port wurde in der Weboberfläche des Switches bewusst abgeschaltet.

Deaktivierte Entitäten lassen sich bei Bedarf unter **Einstellungen → Geräte & Dienste → Entitäten** einschalten.

Die Entitäts-IDs folgen dem Muster `sensor.switch_192_168_1_100_port_3` bzw. `sensor.switch_192_168_1_100_port_3_duplex`.

---

## Beispiel-Automationen

### Benachrichtigung, wenn ein Port ausfällt

```yaml
alias: "Switch-Port 3 getrennt"
triggers:
  - trigger: state
    entity_id: sensor.switch_192_168_1_100_port_3
    to: "disconnected"
    for: "00:00:30"
actions:
  - action: notify.mobile_app
    data:
      title: "⚠️ Netzwerk-Warnung"
      message: "Switch-Port 3 ist nicht mehr verbunden"
```

### Wöchentlicher Neustart

```yaml
alias: "Switch-Neustart Sonntag 3 Uhr"
triggers:
  - trigger: time
    at: "03:00:00"
conditions:
  - condition: time
    weekday: [sun]
actions:
  - action: button.press
    target:
      entity_id: button.switch_192_168_1_100_reboot
```

---

## Funktionsweise

1. **Anmeldung** — `MD5(Benutzername + Passwort)` → `POST /login.cgi`, Sitzung per Cookie
2. **Abfrage** (alle N Sekunden):
   - `GET /info.cgi` → Modell, Firmware, MAC, Laufzeit, Link/Geschwindigkeit pro Port
   - `GET /port.cgi` → Aktiviert/deaktiviert pro Port (beim KP-9000 zusätzlich Link, Geschwindigkeit/Duplex und Flow Control)
   - `GET /port.cgi?page=stats` → TX/RX-Zähler
3. **Neustart** — `POST /reboot.cgi {"cmd":"reboot"}`

Zwischen den einzelnen Anfragen liegt eine Pause von 0,4 s, damit der uIP-Mikrocontroller des Switches nicht durch zu viele Sitzungen überlastet wird.

---

## Mitwirken

Ablauf: Fork → Branch → Pull Request → beide CI-Prüfungen grün → Merge.

**Kompatibles Gerät gefunden?** Eröffne ein [Issue](https://github.com/brunoz78/horaco_switch_ha/issues/new) mit Modell, Firmware-Version und Port-Ausstattung, dann wird es in die Tabelle aufgenommen.

---

## Lizenz

MIT — siehe [LICENSE](LICENSE)

## Danksagung

Fork von [gtrancillo/horaco_switch_ha](https://github.com/gtrancillo/horaco_switch_ha).

Wissen über die CGI-Endpunkte und den Abfrage-Ansatz stammt aus [byte4geek/switch-dashboard](https://github.com/byte4geek/switch-dashboard).
