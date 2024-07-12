document.addEventListener("DOMContentLoaded", function(){

    const head = document.getElementById("profile_img");
    const gender = head.className;

    const male_img = "/static/images/head.png"
    const female_img = "/static/images/head2.png"

    if (gender == "male"){
        head.src = male_img;
    }
    else{
        head.src = female_img;
    }

});