const svg = document.getElementById("field");

const SPIELRAND = 50;
const DURCHMESSER = 50;

let mouthPhase = 0;

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
        const angryBirds = data.angry_birds || [];
        const currentLevel = data.current_level ?? 1;
        const score = data.score ?? 0;

        const levelText = document.getElementById("level-text");
        if (levelText) {
            levelText.textContent = `Level ${currentLevel}`;
        }

        const scoreText = document.getElementById("score-text");
        if (scoreText) {
            scoreText.textContent = `Punkte: ${score}`;
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

        const existingAngryBirds = Array.from(
            svg.querySelectorAll('[id^="angry-bird-"]')
        );

        angryBirds.forEach((bird, index) => {
            let birdElem = document.getElementById(`angry-bird-${index}`);
            if (!birdElem) {
                birdElem = document.createElementNS(
                    "http://www.w3.org/2000/svg",
                    "path"
                );
                birdElem.setAttribute("id", `angry-bird-${index}`);
                svg.appendChild(birdElem);
            }

            birdElem.dataset.cx = bird.cx;
            birdElem.dataset.cy = bird.cy;
            birdElem.dataset.r = bird.r;
            birdElem.setAttribute("fill", bird.color);
            birdElem.setAttribute(
                "d",
                createMouthPath(bird.cx, bird.cy, bird.r, mouthPhase)
            );
        });

        existingAngryBirds.forEach(birdElem => {
            const index = Number(
                birdElem.id.replace("angry-bird-", "")
            );
            if (index >= angryBirds.length) {
                birdElem.remove();
            }
        });


    } catch (error) {

        console.error(
            "Fehler beim Aktualisieren der Schlange:",
            error
        );

    }
}

function createMouthPath(cx, cy, radius, phase) {
    const mouthAngle = 22 + (Math.sin(phase) + 1) * 24;
    const halfAngle = mouthAngle * Math.PI / 360;
    const upperX = cx + radius * Math.cos(halfAngle);
    const upperY = cy - radius * Math.sin(halfAngle);
    const lowerX = cx + radius * Math.cos(halfAngle);
    const lowerY = cy + radius * Math.sin(halfAngle);

    return `M ${cx} ${cy} L ${upperX} ${upperY} A ${radius} ${radius} 0 1 1 ${lowerX} ${lowerY} Z`;
}

function animateMouth(timestamp) {
    mouthPhase = timestamp / 260;
    document.querySelectorAll('[id^="angry-bird-"]').forEach(bird => {
        bird.setAttribute(
            "d",
            createMouthPath(
                Number(bird.dataset.cx),
                Number(bird.dataset.cy),
                Number(bird.dataset.r),
                mouthPhase
            )
        );
    });
    requestAnimationFrame(animateMouth);
}

window.addEventListener("load", () => {
    requestAnimationFrame(animateMouth);
});

let scoreSubmitted = false;
window.addEventListener("pagehide", () => {
    if (scoreSubmitted) {
        return;
    }
    scoreSubmitted = true;
    fetch("/api/finish-game", {
        method: "POST",
        keepalive: true
    }).catch(error => {
        console.error("Score konnte nicht gespeichert werden:", error);
    });
});


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