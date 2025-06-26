const menu = document.getElementById("mobileMenu");
const overlay = document.getElementById("overlay");

function openMenu() {
    menu.style.left = "0";
    overlay.classList.remove("hidden");
}

function closeMenu() {
    menu.style.left = "-100%";
    overlay.classList.add("hidden");
}


overlay.addEventListener("click", closeMenu);
