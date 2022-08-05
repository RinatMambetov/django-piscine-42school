function handle_up() {
  document.getElementById("UP").click();
}

function handle_down() {
  document.getElementById("DOWN").click();
}

function handle_left() {
  document.getElementById("LEFT").click();
}

function handle_right() {
  document.getElementById("RIGHT").click();
}

function handle_a() {
  document.getElementById("A").click();
}
function handle_b() {
  document.getElementById("B").click();
}

function handle_start() {
  document.getElementById("START").click();
}

function handle_select() {
  document.getElementById("SELECT").click();
}

window.addEventListener("keydown", (event) => {
  if (event.code === "KeyW" || event.code === "ArrowUp") {
    return handle_up();
  }
  if (event.code === "KeyS" || event.code === "ArrowDown") {
    return handle_down();
  }
  if (event.code === "KeyA" || event.code === "ArrowLeft") {
    return handle_left();
  }
  if (event.code === "KeyD" || event.code === "ArrowRight") {
    return handle_right();
  }
  if (event.code === "KeyN") {
    return handle_a();
  }
  if (event.code === "KeyM") {
    return handle_b();
  }
  if (event.code === "KeyO") {
    return handle_select();
  }
  if (event.code === "KeyP") {
    return handle_start();
  }
});