search = (val) => {
    var t = document.getElementById('t').innerHTML
    let nextOcc = t.indexOf(val)

    while (t.indexOf(val, nextOcc) != -1 && val.length > 0) {
        console.log(`The index of the  "${val}" is ${t.indexOf(val, nextOcc)}`)
        nextOcc += 1
    }
}