function login_page() {
    
}

function none_opacity(child, add_op) {
    let op = (add_op > 0) ? 0 : 1
    console.log(op)
    let timerId = setInterval(() => {
        op += add_op
        child.style.opacity = op.toString()
    }, 1000*add_op); 
    setTimeout(() => {
        clearInterval(timerId);
        if (add_op <= 0) {
            setTimeout(function () {document.location.href = "/login"}, 0)
        }
    }, 1000);
}

function animation(add_op) {
    const form = document.querySelector("form")
    const children = form.childNodes
    for (let i=1; i<children.length; i+=2) {
        setTimeout(none_opacity, 0, children[i], add_op);
    }
    console.log(children[1])
}

window.onload = function() {animation(0.01)}