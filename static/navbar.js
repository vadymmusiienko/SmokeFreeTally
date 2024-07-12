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
