# Welche Magic-UI-Komponente wofür

| Zweck | Komponenten | Regel |
|---|---|---|
| Social Proof | `marquee`, `avatar-circles` | Pausierbar, kurze Texte |
| Hero-Visual | `globe`, `warp-background`, `animated-grid-pattern`, `retro-grid` | Nur einer pro Hero |
| Text-Motion | `blur-fade`, `text-animate`, `word-rotate`, `typing-animation`, `sparkles-text` | Für Betonung, nicht für Fliesstext |
| CTA | `shiny-button`, `shimmer-button`, `rainbow-button`, `ripple-button` | Ein Stil pro Abschnitt |
| Hintergrund | `grid-pattern`, `dot-pattern`, `particles`, `flickering-grid`, `light-rays`, `dither-field` | Nur Nebenebene, Kontrast prüfen |
| Feature-Grid | `bento-grid` | Gleiche Kartenhöhen, wenig Motion |

## Fertige Rezepte
- **Hero mit Tiefe** `warp-background` oder `animated-grid-pattern` + `blur-fade` + `shiny-button`
- **Vertrauensleiste** `marquee` + `avatar-circles`
- **Feature-Grid** `bento-grid` + `text-animate` auf 1–2 Karten

Alle Komponenten: https://magicui.design/docs/components
