document.addEventListener("DOMContentLoaded", function () {
    var sidenav = document.querySelectorAll(".sidenav");
    var sideNavInstances = M.Sidenav.init(sidenav);
    var dropdown = document.querySelectorAll(".dropdown-trigger");
    var dropdownInstances = M.Dropdown.init(dropdown);
    var select = document.querySelectorAll("select");
    var selectInstances = M.FormSelect.init(select);
    var floatingActionButtons = document.querySelectorAll(".fixed-action-btn");
    var floatingActionButtonInstances = M.FloatingActionButton.init(floatingActionButtons, {
        hoverEnabled: false
    });
});

function openTab(event, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    };
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].firstChild.className = tablinks[i].firstChild.className.replace("active", "");
    };
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.className += "active";
}

function selectDay(event) {
    var i, days_list;
    days_list = document.getElementsByClassName("calendar-day");
    for (i = 0; i < days_list.length; i++) {
        days_list[i].firstChild.className = days_list[i].firstChild.className.replace("active", "");
    };
    event.currentTarget.className += "active";
}
