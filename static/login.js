function none_opacity(child) {
    let op = 0
    let timerId = setInterval(() => {
        op += 0.01
        child.style.opacity = op.toString()
    }, 10); 
    setTimeout(() => {
        clearInterval(timerId)
    }, 1000);
}

window.onload = function() {
    const form = document.querySelector("form")
    const children = form.childNodes
    for (let i=1; i<children.length; i+=2) {
        setTimeout(none_opacity, 0, children[i]);
    }
    console.log(children[1])
}