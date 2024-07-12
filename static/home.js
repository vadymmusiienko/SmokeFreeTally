document.addEventListener("DOMContentLoaded", function(){

    // Change user's head depending on gender
    const head = document.getElementById("profile_img");
    const gender = head.className;

    const male_img = "/static/images/person/head.png"
    const female_img = "/static/images/person/head2.png"

    if (gender == "female"){
        head.src = female_img;
    }
    else{
        head.src = male_img;
    }

    // Change user's lungs css depending on the skin
    const lungs = document.getElementById("lungs_img");

    if (lungs.src.endsWith("1.png")){
        lungs.style.top = "-1%";
        lungs.style.left = "22%"; 
    } else if (lungs.src.endsWith("2.png")){
        lungs.style.top = "0";
        lungs.style.left = "19%";
    } else if (lungs.src.endsWith("3.png")){
        lungs.style.top = "0";
        lungs.style.left = "19%";
    } else if (lungs.src.endsWith("4.png")){
        lungs.style.top = "-3%";
        lungs.style.left = "20%";
    }else if (lungs.src.endsWith("5.png")){
        lungs.style.top = "0";
        lungs.style.left = "19%";
    }
});