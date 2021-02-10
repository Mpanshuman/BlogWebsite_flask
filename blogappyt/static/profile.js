console.log('hey')
function myFunction() {
    var x = document.getElementById("update_form");
    var y = document.getElementById("update_hide");
    x.style.display = "none";
    y.style.innerHTML = "Hide";
    if (x.style.display === "none") {
      x.style.display = "block";
      
    } else {
      x.style.display = "none";
    }
  }