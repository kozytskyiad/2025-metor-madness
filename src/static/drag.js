// Make the floating window draggable by mouse
(function() {
	const dragItem = document.getElementById("floatingWindow");
	let active = false;
	let currentX, currentY, initialX, initialY;
	let xOffset = 0, yOffset = 0;

	if (!dragItem) return;

	dragItem.style.cursor = "move";

	dragItem.addEventListener("mousedown", dragStart);
	document.addEventListener("mouseup", dragEnd);
	document.addEventListener("mousemove", drag);

	function dragStart(e) {
		active = true;
		initialX = e.clientX - xOffset;
		initialY = e.clientY - yOffset;
	}

	function dragEnd(e) {
		active = false;
		xOffset = currentX;
		yOffset = currentY;
	}

	function drag(e) {
		if (!active) return;
	
		e.preventDefault();
	
		currentX = e.clientX - initialX;
		currentY = e.clientY - initialY;
	
		setTranslate(currentX, currentY, dragItem);
	}

	function setTranslate(xPos, yPos, el) {
		el.style.transform = `translate(${xPos}px, ${yPos}px)`;
	}
})();

