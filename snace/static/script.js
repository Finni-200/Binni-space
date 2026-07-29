const svg = document.getElementById("field");
const SPIELRAND = 50;
const DURCHMESSER = 50;

let fieldWidth = 1800;
let fieldHeight = 950;

async function updateViewport() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);

    // Sende die Fenstergröße an den Backend
    try {
        const response = await fetch("/update_field_size", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                width: width,
                height: height
            })
        });
        
        const data = await response.json();
        fieldWidth = data.field_width;
        fieldHeight = data.field_height;
    } catch (error) {
        console.error("Fehler beim Update der Feldgröße:", error);
    }

    const feld = document.getElementById("spielfeld");

    // Berechne Spielfeldgröße als Vielfaches des Durchmessers
    const displayFieldWidth = Math.floor((width - SPIELRAND * 2) / DURCHMESSER) * DURCHMESSER;
    const displayFieldHeight = Math.floor((height - SPIELRAND * 2) / DURCHMESSER) * DURCHMESSER;
    
    // Zentriere das Spielfeld mit Spielrand
    feld.setAttribute("x", SPIELRAND);
    feld.setAttribute("y", SPIELRAND);
    feld.setAttribute("width", displayFieldWidth);
    feld.setAttribute("height", displayFieldHeight);
}

window.addEventListener("resize", updateViewport);
updateViewport();


// Tastatur
document.addEventListener("keydown", async function(event){

    let richtung = null;

    if(event.key === "ArrowUp"){
        richtung = "up";
    }
    else if(event.key === "ArrowDown"){
        richtung = "down";
    }
    else if(event.key === "ArrowLeft"){
        richtung = "left";
    }
    else if(event.key === "ArrowRight"){
        richtung = "right";
    }

    if(richtung){
        await fetch("/richtung/" + richtung);
    }

});


// Schlange aktualisieren
setInterval(async () => {

    try{

        const response = await fetch("/api/snake");
        const data = await response.json();
        const circles = data.snake || [];
        const foods = data.foods || [];

        circles.forEach((circle, index) => {

            let elem = document.getElementById(`circle-${index}`);

            if(!elem){

                elem = document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "circle"
                );

                elem.setAttribute("id", `circle-${index}`);
                svg.appendChild(elem);
            }

            elem.setAttribute("cx", circle.cx);
            elem.setAttribute("cy", circle.cy);
            elem.setAttribute("r", circle.r);
            elem.setAttribute("fill", circle.color);

        });

        foods.forEach((food, index) => {
            let foodElem = document.getElementById(`food-${index}`);

            if(!foodElem){
                foodElem = document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "circle"
                );

                foodElem.setAttribute("id", `food-${index}`);
                svg.appendChild(foodElem);
            }

            foodElem.setAttribute("cx", food.cx);
            foodElem.setAttribute("cy", food.cy);
            foodElem.setAttribute("r", food.r);
            foodElem.setAttribute("fill", food.color);
        });

    }
    catch(error){

        console.error(error);

    }

}, 100);