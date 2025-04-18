window.addEventListener('load', () => {
    const width = window.innerWidth;

    if (width >= 1900) {
        document.body.style.zoom = "90%";
    } else if (width <= 1600) {
        document.body.style.zoom = "75%";
    }
});
