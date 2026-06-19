const svg = document.getElementById('field');

// Update die SVG-Kreise alle 100ms mit neuen Positionen von der API
setInterval(async () => {
    try {
        const response = await fetch("/api/snake");
        const circles = await response.json();

        circles.forEach((circle, index) => {
            let elem = document.getElementById(`circle-${index}`);
            
            // Falls Element nicht existiert, erstelle es
            if (!elem) {
                elem = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                elem.setAttribute('id', `circle-${index}`);
                elem.setAttribute('fill', circle.color);
                elem.setAttribute('stroke', '#222');
                svg.appendChild(elem);
            }
            
            // Aktualisiere die Position und Größe
            elem.setAttribute('cx', circle.cx);
            elem.setAttribute('cy', circle.cy);
            elem.setAttribute('r', circle.r);
        });
    } catch (error) {
        console.error('Fehler beim Abrufen der Schlange:', error);
    }
}, 100);
