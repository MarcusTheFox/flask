function remove_task(event) {
    const id = event.target.parentNode.id
    fetch('/remove_task/' + id).then(response => window.location.reload())
    console.log(id)
}

function create_task(event) {
    // const id = event.target.parentNode.id
    const task = event.target.previousElementSibling.value
    fetch('/create_task/' + task).then(response => window.location.reload())
    console.log(task)
}

function remove_user(event) {
    const name = event.target.parentNode.childNodes[1].value
    // const task = event.target.previousElementSibling.value
    fetch('/remove_user/' + name).then(response => window.location.reload())
    console.log(event)
}

// function edit_user(event) {
//     const name = event.target.parentNode.childNodes[1].value
//     // const task = event.target.previousElementSibling.value
//     fetch('/edit_user/' + name)
//     console.log(name)
// }