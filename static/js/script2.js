let sendBtn = document.getElementById('sendBtn');
let mainSpace = document.querySelector(".mainSpace");
let formSpace = document.getElementById("composer");

sendBtn.addEventListener('click', () => {
    mainSpace.classList.add("displayNone");
});
