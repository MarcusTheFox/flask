function add_task_form() {
    const form = document.getElementsByTagName("form")[0]
    const close = document.getElementById("close_form")
    form.style.display = "block"
    close.style.display = "block"
}

function close_task_form() {
    const form = document.getElementsByTagName("form")[0]
    const close = document.getElementById("close_form")
    form.style.display = "none"
    close.style.display = "none"
}
// const add = document.getElementById("plus")
// add.addEventListener("click", add_task_form)