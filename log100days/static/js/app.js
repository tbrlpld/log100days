
function toggleNav() {
  const toggler = document.getElementById("nav-toggle");
  const navItems = document.getElementsByClassName("nav-item");
  const itemsVisible = navItems[0].classList.contains("visible")

  if (itemsVisible) {
    for (var i = navItems.length - 1; i >= 0; i--) {
      navItems[i].classList.remove("visible");
      toggler.classList.remove("open");
      toggler.classList.add("closed");
    }
  } else {
    for (var i = navItems.length - 1; i >= 0; i--) {
      navItems[i].classList.add("visible");
      toggler.classList.add("open");
      toggler.classList.remove("closed");

    }
  }
}

