# Multiplayer Snake (2 Spieler Online) – Saubere Software-Architektur

## Ziel

Ein Online-Snake-Spiel für 2 Spieler mit moderner Architektur, klarer Trennung von Frontend, Backend und Game-Logik.

---

# Features (geordnet)

## Gameplay

* Zwei Spieler spielen gleichzeitig online.
* Jede Schlange bewegt sich unabhängig.
* Nahrung erscheint zufällig.
* Beim Essen wächst die Schlange.
* Nach jedem Essen erhöht sich die Geschwindigkeit.
* Kollision mit Wand = Game Over.
* Kollision mit eigener Schlange = Game Over.
* Kollision mit gegnerischer Schlange = Game Over.
* Wenn ein Spieler verliert, gewinnt der andere.

## UI / Frontend

* Responsives Spielfeld.
* Schönes CSS-Design.
* Anzeige von:

  * Spielernamen
  * Punktestand
  * Geschwindigkeit
  * Gewinner
* Game Over Bildschirm.
* Möglichkeit zum Neustart.
* Unterstützung für Bildschirmrotation (Portrait/Landscape).

## Netzwerk

* Online-Multiplayer über WebSockets.
* Synchronisation des Game States.
* Lobby/Room-System für 2 Spieler.

---

# Architekturübersicht

```text
Frontend (React / Canvas)
        |
        | WebSocket
        |
Backend (Node.js + Socket.IO)
        |
        |
Game Engine (OOP)
```

---

# Frontend-Struktur

## Seiten

```text
/pages
  HomePage
  LobbyPage
  GamePage
  GameOverPage
```

## Komponenten

```text
/components
  GameCanvas
  ScoreBoard
  PlayerInfo
  WinnerBanner
  RestartButton
```

## Services

```text
/services
  socketService
  inputService
```

## Styles

```text
/styles
  global.css
  game.css
  responsive.css
```

---

# Backend-Struktur

```text
/server
  server.js
  socketHandler.js
  RoomManager.js
  GameLoop.js
```

---

# Game Engine (OOP)

```text
/game
  Game.js
  Snake.js
  Food.js
  CollisionService.js
  SpeedService.js
  Vector.js
  Constants.js
```

---

# Klassen

## Game

Verantwortlich für:

* Spieler verwalten
* Food erzeugen
* Update-Schleife
* Gewinner bestimmen

### Methoden

* start()
* update()
* spawnFood()
* checkGameOver()
* getState()

---

## Snake

Verantwortlich für:

* Position
* Richtung
* Bewegung
* Wachstum

### Methoden

* move()
* grow()
* setDirection()
* checkSelfCollision()

---

## Food

* Position speichern
* Zufällig erzeugen

---

## CollisionService

* Wandkollision
* Selbstkollision
* Gegnerkollision
* Nahrungskollision

---

## SpeedService

* Geschwindigkeit berechnen
* Erhöhung nach Punkten

---

## RoomManager

* Räume erstellen
* Spieler verbinden
* Spiel starten

---

# Datenmodell

## Player

```ts
{
  id: string,
  name: string,
  score: number,
  alive: boolean,
  snake: Snake
}
```

## GameState

```ts
{
  players: Player[],
  food: Position,
  speed: number,
  winner: string | null,
  status: 'waiting' | 'running' | 'gameover'
}
```

---

# WebSocket Events

## Client → Server

* createRoom
* joinRoom
* playerInput
* restartGame

## Server → Client

* roomCreated
* gameStart
* gameState
* gameOver
* playerDisconnected

---

# Spielablauf

```text
1. Spieler erstellt Raum.
2. Zweiter Spieler tritt bei.
3. Spiel startet.
4. Spieler senden Richtungen.
5. Server aktualisiert Spiel.
6. Server sendet Game State.
7. Bei Verlust → Game Over Seite.
```

---

# Kollisionslogik

## Wand

```text
x < 0
x >= gridWidth
y < 0
y >= gridHeight
```

## Selbst

Kopf trifft eigenen Körper.

## Gegner

Kopf trifft Segment des Gegners.

## Nahrung

Kopf trifft Food.

---

# Geschwindigkeit

```text
speed = baseSpeed + score * increment
```

Beispiel:

* Start: 5 FPS
* Pro Punkt: +0.5 FPS
* Maximal: 15 FPS

---

# Responsive Design

* Canvas passt sich an Bildschirmgröße an.
* Mobile und Desktop.
* Landscape bevorzugt.
* Bei Hochformat Hinweis anzeigen.

---

# CSS Design

## Stil

* Dunkler Hintergrund.
* Neon-Farben.
* Glowing Snake.
* Smooth Animationen.

## Farben

* Hintergrund: #0f172a
* Spieler 1: Grün
* Spieler 2: Blau
* Food: Rot

---

# Seitenwechsel

## Routing

* `/` → Startseite
* `/lobby/:id` → Lobby
* `/game/:id` → Spiel
* `/game-over` → Game Over

---

# Technologien

## Frontend

* React
* TypeScript
* HTML5 Canvas
* CSS
* React Router
* Socket.IO Client

## Backend

* Node.js
* Express
* Socket.IO

---

# OOP-Prinzipien

* Single Responsibility Principle
* Kapselung
* Wiederverwendbare Services
* Klare Datenmodelle

---

# Empfohlene Ordnerstruktur

```text
snake-multiplayer/
├── client/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   ├── styles/
│   │   └── types/
│
├── server/
│   ├── game/
│   ├── rooms/
│   ├── socket/
│   └── server.js
│
└── shared/
    ├── constants.ts
    └── types.ts
```

---

# Prioritäten für Umsetzung

## Phase 1

* Spielfeld
* Snake Bewegung
* Food
* Wachstum
* Wandkollision

## Phase 2

* WebSockets
* 2 Spieler
* Room-System

## Phase 3

* Gegnerkollision
* Geschwindigkeit
* Game Over Seite

## Phase 4

* Schönes CSS
* Responsive Design
* Bildschirmrotation

---

# Kurzfassung

Das Projekt wird in drei Schichten aufgebaut:

1. Frontend (React + Canvas)
2. Backend (Node.js + Socket.IO)
3. Game Engine (OOP-Klassen)

Alle Spiellogiken wie Kollisionen, Wachstum und Geschwindigkeit liegen zentral in der Game Engine.
Der Server ist die einzige Quelle der Wahrheit und sendet den aktuellen Game State an beide Spieler.
