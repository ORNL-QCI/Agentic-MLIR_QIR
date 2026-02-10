#!/bin/bash
# Generate online PlantUML viewer URLs

echo "==================================================="
echo "PlantUML Diagram Online Viewers"
echo "==================================================="
echo ""
echo "Open these URLs in your browser to view the diagrams:"
echo ""

for file in docs/diagrams/*.puml; do
    if [ -f "$file" ]; then
        basename=$(basename "$file" .puml)
        echo "📊 $basename"
        echo "   https://www.plantuml.com/plantuml/uml/$(cat "$file" | plantuml -encodesprite)"
        echo ""
    fi
done

echo "Alternative: Copy diagram content and paste at:"
echo "https://www.plantuml.com/plantuml/uml/"
echo ""
