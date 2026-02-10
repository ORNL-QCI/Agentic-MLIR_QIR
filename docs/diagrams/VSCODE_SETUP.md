# VSCode PlantUML Extension Setup (Without Graphviz)

Since you don't have Graphviz installed, configure the PlantUML extension to use an online server.

## Quick Setup (2 Steps)

### Step 1: Open Settings
Press `Ctrl+,` (or `Cmd+,` on Mac)

### Step 2: Configure These Two Settings

Search for and set:

1. **PlantUML: Render**
   - Change to: `PlantUMLServer`

2. **PlantUML: Server**
   - Set to: `https://www.plantuml.com/plantuml`

That's it! Now press `Alt+D` on any `.puml` file to preview.

## Alternative: Edit settings.json

Press `Ctrl+Shift+P` → type "Preferences: Open User Settings (JSON)"

Add these lines:

```json
{
  "plantuml.render": "PlantUMLServer",
  "plantuml.server": "https://www.plantuml.com/plantuml"
}
```

## Verify Setup

1. Open: `docs/diagrams/sequence_diagram.puml`
2. Press: `Alt+D`
3. Should see the diagram preview!

## Troubleshooting

### "Cannot find 'dot' executable"
- This means you're still using Local render mode
- Make sure `plantuml.render` is set to `PlantUMLServer`

### Diagram doesn't load
- Check internet connection (server mode requires internet)
- Try different server: `https://kroki.io/plantuml/svg`

### Slow rendering
- Online servers can be slower than local
- Consider asking admin to install Graphviz for faster local rendering

## Export Diagrams

Once rendered, you can export:
1. Right-click on the preview
2. Select "Export Current Diagram"
3. Choose PNG, SVG, or PDF
