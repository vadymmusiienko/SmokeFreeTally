// Sidebar - navbar switch for mobile devices vs computes

function showSidebar(){
    const sidebar = document.querySelector(".sidebar");
    sidebar.style.display = "flex";

    const logo = document.querySelector(".logo-hide")
    logo.style.display = "none";

    const menu = document.querySelector(".menu-button");
    menu.style.display = "none";
}

function hideSidebar(){
    const sidebar = document.querySelector(".sidebar");
    sidebar.style.display = "none";

    const logo = document.querySelector(".logo-hide")
    logo.style.display = "flex";

    const menu = document.querySelector(".menu-button");
    menu.style.display = "flex";
}

// Make sure the user cannot type more characters than maxlength of the html element
function limitInput(input){
    const maxLength = input.getAttribute("maxlength");

    if (input.value.length > maxLength){
        input.value = input.value.slice(0, 2);
    }
};


// Handle the underline for the input on setting page (when no text - underline, otherwise - nothing)
function handleBlur(input){
    if (input.value){
        input.style.borderBottomColor = "transparent";
    }
    else{
        input.style.borderBottomColor = "white";
    }
}

document.addEventListener("DOMContentLoaded", function(){
    const inputs = document.querySelectorAll(".info-form input")

    for (let i = 0, len = inputs.length; i < len; i++){
        if (inputs[i].value){
            inputs[i].style.borderBottomColor = "transparent";
        }
    }
})