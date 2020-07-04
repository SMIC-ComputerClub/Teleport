function upload(files) {
    document.getElementById("loading-container").style.display = "flex"
    let data = new FormData()
    for (let i = 0; i < files.length; i++) {
        data.append(files[i].name, files[i])
    }
    let previousLoaded = 0
    let previousTime = Date.now()
    $.ajax({
        type: "POST",
        data: data,
        contentType: false,
        processData: false,
        xhr: () => {
            let xhr = $.ajaxSettings.xhr()
            xhr.upload.onprogress = progress => {
                let time = Date.now()
                let remainingTime = new Date((progress.total - progress.loaded) / ((progress.loaded - previousLoaded) / (time - previousTime)))
                document.getElementById("loading-percentage").innerText = `${Math.trunc(progress.loaded / progress.total * 100)}%`
                document.getElementById("loading-speed").innerText = `${simplify((progress.loaded - previousLoaded) / (time - previousTime) * 1000)}/s`
                document.getElementById("loading-time").innerText = `${pad(remainingTime.getUTCHours())}:${pad(remainingTime.getUTCMinutes())}:${pad(remainingTime.getUTCSeconds())}`
                previousLoaded = progress.loaded
                previousTime = time
            }
            return xhr
        },
        complete: () => {
            location.reload()
        }
    })
}

function simplify(size) {
    for (let unit of ["B", "KB", "MB", "GB"]) {
        if (size < 1000) {
            return `${Math.trunc(size * 100) / 100} ${unit}`
        } else {
            size /= 1000
        }
    }
}

function pad(number) {
    number = String(number)
    if (number.length == 1) {
        return "0" + number
    } else {
        return number
    }
}