const svg = document.getElementById("field");

const SPIELRAND = 50;
const DURCHMESSER = 50;

let fieldWidth = 1800;
let fieldHeight = 950;


// =====================================================
// SPIELFELD / FENSTERGRÖSSE
// =====================================================

async function updateViewport() {

    const width = window.innerWidth;
    const height = window.innerHeight;

    try {

        // Zuerst Backend über neue Größe informieren
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


    // SVG passend zum Fenster
    svg.setAttribute(
        "viewBox",
        `0 0 ${width} ${height}`
    );


    // Spielfeldgröße berechnen
const displayFieldWidth = fieldWidth;
const displayFieldHeight = fieldHeight;

const feld = document.getElementById("spielfeld");

feld.setAttribute("x", SPIELRAND);
feld.setAttribute("y", SPIELRAND);
feld.setAttribute("width", displayFieldWidth);
feld.setAttribute("height", displayFieldHeight);


    // WICHTIG:
    // Erst nachdem das Backend die neue Schlange erstellt hat,
    // die Schlange sofort aktualisieren.
    await updateSnake();
}


// =====================================================
// SCHLANGE AKTUALISIEREN
// =====================================================

async function updateSnake() {

    try {

        const response = await fetch("/api/snake");
        const data = await response.json();

        const circles = data.snake || [];
        const foods = data.foods || [];
        const smallFoods = data.small_foods || [];
        const currentLevel = data.current_level ?? 1;

        const levelText = document.getElementById("level-text");
        if (levelText) {
            levelText.textContent = `Level ${currentLevel}`;
        }

        // ---------------------------------------------
        // Schlange
        // ---------------------------------------------

        circles.forEach((circle, index) => {

            let elem =
                document.getElementById(`circle-${index}`);


            if (!elem) {

                elem = document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "circle"
                );

                elem.setAttribute(
                    "id",
                    `circle-${index}`
                );

                svg.appendChild(elem);
            }


            elem.setAttribute("cx", circle.cx);
            elem.setAttribute("cy", circle.cy);
            elem.setAttribute("r", circle.r);
            elem.setAttribute("fill", circle.color);
        });


        // Alte Schlangenteile entfernen
        const existingCircles =
            Array.from(
                svg.querySelectorAll('[id^="circle-"]')
            );

        existingCircles.forEach(elem => {

            const index =
                Number(
                    elem.id.replace("circle-", "")
                );

            if (index >= circles.length) {
                elem.remove();
            }
        });


        // ---------------------------------------------
        // Normales Essen
        // ---------------------------------------------

        foods.forEach((food, index) => {

            let foodElem =
                document.getElementById(`food-${index}`);


            if (!foodElem) {

                foodElem = document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "circle"
                );

                foodElem.setAttribute(
                    "id",
                    `food-${index}`
                );

                svg.appendChild(foodElem);
            }


            foodElem.setAttribute("cx", food.cx);
            foodElem.setAttribute("cy", food.cy);
            foodElem.setAttribute("r", food.r);
            foodElem.setAttribute(
                "fill",
                "url(#foodGradient)"
            );
        });


        // ---------------------------------------------
        // Kleines Essen
        // ---------------------------------------------

        smallFoods.forEach((food, index) => {

            let foodElem =
                document.getElementById(
                    `small_food-${index}`
                );


            if (!foodElem) {

                foodElem = document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "circle"
                );

                foodElem.setAttribute(
                    "id",
                    `small_food-${index}`
                );

                svg.appendChild(foodElem);
            }


            foodElem.setAttribute("cx", food.cx);
            foodElem.setAttribute("cy", food.cy);
            foodElem.setAttribute("r", food.r);
            foodElem.setAttribute(
                "fill",
                "url(#small_foodGradient)"
            );
        });

        const existingSmallFoods =
            Array.from(
                svg.querySelectorAll('[id^="small_food-"]')
            );

        existingSmallFoods.forEach(foodElem => {

            const index =
                Number(
                    foodElem.id.replace("small_food-", "")
                );

            if (index >= smallFoods.length) {
                foodElem.remove();
            }
        });


    } catch (error) {

        console.error(
            "Fehler beim Aktualisieren der Schlange:",
            error
        );

    }
}


// =====================================================
// TASTATUR
// =====================================================

document.addEventListener(
    "keydown",
    async function(event) {

        let richtung = null;


        if (event.key === "ArrowUp") {
            richtung = "up";
        }

        else if (event.key === "ArrowDown") {
            richtung = "down";
        }

        else if (event.key === "ArrowLeft") {
            richtung = "left";
        }

        else if (event.key === "ArrowRight") {
            richtung = "right";
        }


        if (richtung) {

            await fetch(
                "/richtung/" + richtung
            );

        }

    }
);


// =====================================================
// START
// =====================================================

// WICHTIG:
// Einmal beim Start ausführen.
// updateViewport wartet dabei auf das Backend
// und lädt anschließend sofort die richtige Schlange.
updateViewport();


// Danach regelmäßig aktualisieren
setInterval(
    updateSnake,
    100
);


// Bei Fenstergrößenänderung
window.addEventListener(
    "resize",
    updateViewport
);