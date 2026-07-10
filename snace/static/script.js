const svg = document.getElementById("field");
const SPIELRAND = 50;

function updateViewport() {

    const width = window.innerWidth;
    const height = window.innerHeight;

    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);

    const feld = document.getElementById("spielfeld");

    feld.setAttribute("x", SPIELRAND);
    feld.setAttribute("y", SPIELRAND);
    feld.setAttribute("width", width - SPIELRAND * 2);
    feld.setAttribute("height", height - SPIELRAND * 2);
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
        const circles = await response.json();

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

    }
    catch(error){

        console.error(error);

    }

}, 100);