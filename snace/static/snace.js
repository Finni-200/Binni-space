const svg = document.getElementById('field');




async function updateViewport() {
	const width = window.innerWidth;
	const height = window.innerHeight;

	svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
	svg.setAttribute('width', width);
	svg.setAttribute('height', height);

	await fetch(`/fenster/${Math.round(width)}/${Math.round(height)}`);
}

window.addEventListener('resize', updateViewport);
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

	try {

		const response = await fetch("/api/snake");
		const circles = await response.json();
		const width = window.innerWidth;
		const height = window.innerHeight;

		circles.forEach((circle, index) => {

			let elem = document.getElementById(`circle-${index}`);

			if (!elem) {

				elem = document.createElementNS(
					"http://www.w3.org/2000/svg",
					"circle"
				);

				elem.setAttribute("id", `circle-${index}`);
				elem.setAttribute("fill", circle.color);
				elem.setAttribute("stroke", "#222");

				svg.appendChild(elem);
			}

			const radius = circle.r || 0;
			const cx = Math.max(radius, Math.min(width - radius, circle.cx));
			const cy = Math.max(radius, Math.min(height - radius, circle.cy));

			elem.setAttribute("cx", cx);
			elem.setAttribute("cy", cy);
			elem.setAttribute("r", radius);

		});

	} catch (error) {

		console.error(error);

	}

}, 100);

