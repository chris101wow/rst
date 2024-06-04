function change(){
    element = document.getElementById("am_pm")
    if (element.innerHTML =="PM"){
        element.innerHTML = "AM"
        document.getElementById("per_of_day").value = "am"
    }else{
        element.innerHTML = "PM"
        document.getElementById("per_of_day").value = "pm"

    }
}