// Make sure the user cannot type more characters than maxlength of the html element
function limitInput(input){
    const maxLength = input.getAttribute("maxlength");

    if (input.value.length > maxLength){
        input.value = input.value.slice(0, 2);
    }
};


// Handle the underline for the input on setting page (when no text - underline, otherwise - nothing)
function handleBlur(element) {
    if (element.value) {
        element.parentElement.classList.remove("line");
    } 
    else {
        element.parentElement.classList.add("line");
    }
}

document.addEventListener("DOMContentLoaded", function(){
    const elements = document.querySelectorAll(".mini-wrapper input");

    elements.forEach(element => {
        if (element.value){
            element.parentElement.classList.remove("line");
        } 
        else{
            element.parentElement.classList.add("line");
        };
    });


    // Change the head in the setting page when choose a gender
    const dropdown = document.getElementById("gender");
    const head = document.getElementById("profile_img");

    const male_img = "/static/images/head.png"
    const female_img = "/static/images/head2.png"


    const gender = dropdown.options[dropdown.selectedIndex].value;

    if (gender == "male"){
        head.src = male_img;
        head.style.width = "12rem";
    }
    else{
        head.src = female_img;
        head.style.width = "9rem";
    }

    dropdown.addEventListener("change", function(){
        const gender = dropdown.options[dropdown.selectedIndex].value;

        if (gender == "male"){
            head.src = male_img;
            head.style.width = "12rem";
        }
        else{
            head.src = female_img;
            head.style.width = "9rem";
        }
    });

});