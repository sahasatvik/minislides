
var slides = document.getElementsByTagName("section");
var totalSlides = slides.length;
var prev = [37, 75, 72]; // Left arrow, K, H
var next = [39, 74, 76, 13]; // Right arrow, J, L, Enter
var start = [48]; // Zero
var end = [57]; // Nine

function percentageVisible(element) {
    const viewHeight = (window.innerHeight || document.documentElement.clientHeight);
    const bounds = element.getBoundingClientRect();

    if (bounds.bottom < 0 || bounds.top > viewHeight) {
        return 0;
    }
    
    if (bounds.top < 0 && bounds.bottom > viewHeight) {
        return bounds.height * 100 / viewHeight;
    } else if (bounds.top < 0) {
        return bounds.bottom * 100 / viewHeight;
    } else if (bounds.bottom > viewHeight) {
        return (viewHeight - bounds.top) * 100 / viewHeight;
    }
    return 100;
}

function getCurrentSlide() {
    var index = 0;
    var maxPercent = 0;
    for (var i = 0; i < totalSlides; i++) {
        let p = percentageVisible(slides[i]);
        if (p > maxPercent) {
            index = i;
            maxPercent = p;
        }
    }
    return index;
}

function navigate(nextSlide) {
    let target = nextSlide;
    if (nextSlide < 0) {
        target = 0;
    } else if (nextSlide >= totalSlides) {
        target = totalSlides - 1;
    }
    window.scrollTo(0, slides[target].offsetTop - 8);
}

document.addEventListener("keydown", event => {
    let code = event.keyCode;
    let currentSlide = getCurrentSlide();
    if (prev.includes(code)) {
        navigate(currentSlide - 1);
    } else if (next.includes(code)) {
        navigate(currentSlide + 1);
    } else if (start.includes(code)) {
        navigate(0);
    } else if (end.includes(code)) {
        navigate(totalSlides - 1);
    }
});
