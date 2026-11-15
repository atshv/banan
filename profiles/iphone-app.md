# Profil iphone-app

Native Apps für iPhone und iPad.

## Stack-Vorschlag (Station 3)
- Swift und SwiftUI, aktuelle Xcode-Version, strenge Nebenläufigkeits-Prüfung
- Daten lokal mit SwiftData, sofern nichts dagegen spricht
- Tests mit Swift Testing, Abläufe mit XCUITest
- So wenig fremde Pakete wie möglich
- Nur wenn ausdrücklich React Native oder Expo gewünscht ist: Animationen nach `animate-expo`

## Pflicht-Prüfungen (Station 6 → `memory/gates.json`)
```json
{
  "pflicht": ["build", "test"],
  "build": "xcodebuild build -scheme <Schema> -destination 'platform=iOS Simulator,name=<Gerät>' -quiet",
  "test": "xcodebuild test -scheme <Schema> -destination 'platform=iOS Simulator,name=<Gerät>' -quiet"
}
```
`<Gerät>` aus `xcrun simctl list devices available` wählen. Warnungen des Compilers gelten als Fehler. Ist ein Linter wie SwiftLint installiert, kommt `lint` als Pflicht dazu.

## Design (Station 4)
- Apples Gestaltungsregeln gehen vor: System-Schrift mit Dynamic Type, System-Farben, SF Symbols, Standard-Navigation
- Haltung und Bewegung: `apple-design`
- Aus `factory/design/design-regeln.md` gelten nur Motion, Lesbarkeit und Gate. Magic UI gilt hier nicht.
- Jeder Screen mit den Zuständen leer, lädt, Fehler und gefüllt, dazu hell und dunkel

## Bau (Station 9)
- Swift-Code: `write-swift`
- Bewegung respektiert die Einstellung „Bewegung reduzieren“
- Berechtigungen (Kamera, Mitteilungen usw.) erst fragen, wenn sie gebraucht werden, mit klarem Grund

## Test (Station 10)
- Logik mit Swift Testing, Hauptabläufe mit XCUITest im Simulator
- Screenshots im Simulator auf dem kleinsten und grössten unterstützten Gerät, hell und dunkel, mit grosser Schrift
- Extremdaten nach dem Vorbild von `break-ui`

## Vor dem Release (Station 13)
- Bundle-ID, Version und Build-Nummer gesetzt, Signierung über das Entwicklerkonto
- App-Icon in allen Grössen, Startbildschirm
- Begründungstexte für jede Berechtigung in der Info.plist
- Datenschutz-Manifest und Datenschutzangaben in App Store Connect
- Link zur Datenschutzerklärung
- Screenshots und Beschreibung für den App Store
- Zuerst TestFlight, dann Einreichung zur Prüfung
- Abstürze im Xcode Organizer beobachten
