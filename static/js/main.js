document.querySelector(".nav-bar__hamburger-place").addEventListener("click", () => {
    document.querySelector(".hamburger").classList.toggle("hamburger_active")
    document.querySelector(".nav-bar__menu").classList.toggle("nav-bar__menu_wide")
})

try {
    document.querySelector(".switcher").addEventListener("click", () => {
        document.querySelector(".switcher").classList.toggle("switcher_switched")
        document.querySelector(".grid__tiles").classList.toggle("grid__tiles_collection")
        for (elem of document.querySelectorAll(".grid__tiles__tile"))
            elem.classList.toggle("grid__tiles__tile_collection")
        for (elem of document.querySelectorAll(".grid__tiles__tile__image"))
            elem.classList.toggle("grid__tiles__tile__image_collection")
        for (elem of document.querySelectorAll(".grid__tiles__tile__name"))
            elem.classList.toggle("grid__tiles__tile__name_collection")
    })
} catch (error) {}

function switchTransition(event) {
    if (event.matches) {
        document.querySelector(".nav-bar__menu").style.transition = "transform 500ms"
    } else {
        document.querySelector(".nav-bar__menu").style.transition = "none"
    }
}
window.matchMedia("(width < 568px)").addEventListener("change", switchTransition)
switchTransition({ matches: window.matchMedia("(width < 568px)").matches })

function addIllustrationToRemove(event) {
    let f = document.querySelector(`#i${event.target.dataset.identifier}`)
    f.dataset.removements += event.target.dataset.i + '|'
    f.querySelector(".removements").value = f.dataset.removements
    event.target.style = "display: none !important;"
}

try {
    for (elem of document.querySelectorAll(".comments-box__item-name__header")) {
        elem.addEventListener("click", (event) => {
            event.target.parentElement.parentElement.querySelector(".comments-box__item").classList.toggle("nodisplay")
        })
    }
    for (elem of document.querySelectorAll(".replybutton")) {
        elem.addEventListener("click", (event) => {
            let form = document.querySelector(`#i${event.target.dataset.identifier}`)
            form.classList.toggle("nodisplay")
            form.querySelector(".met").setAttribute("value", "post")
            form.querySelector("textarea").textContent = ""
            if (form.classList.contains("nodisplay")) {
                for (el of document.querySelectorAll(".menu__item"))
                    if (!el.classList.contains("replybutton"))
                        el.style = "opacity: 1; pointer-events: all;"
            } else {
                for (el of document.querySelectorAll(".menu__item"))
                    if (!el.classList.contains("replybutton"))
                        el.style = "opacity: 0.5; pointer-events: none;"
            }
        })
    }
    for (elem of document.querySelectorAll(".editbutton")) {
        elem.addEventListener("click", (event) => {
            let form = document.querySelector(`#i${event.target.dataset.identifier}`)
            form.classList.toggle("nodisplay")
            form.querySelector(".met").setAttribute("value", "put")
            form.querySelector("textarea").textContent = form.dataset.text
            form.dataset.removements = ""
            for (el of document.querySelectorAll(".message-box__carousel__item"))
                el.style = "display: block !important"
            for (el of document.querySelector(`#ii${event.target.dataset.identifier}`).querySelectorAll(".message-box__carousel__item")) {
                el.classList.toggle("cross")
                if (el.classList.contains("cross")) {
                    el.addEventListener("click", addIllustrationToRemove)  // transfer image
                } else {
                    el.removeEventListener("click", addIllustrationToRemove)
                }
            }
            if (form.classList.contains("nodisplay")) {
                for (el of document.querySelectorAll(".menu__item"))
                    if (!el.classList.contains("editbutton") && `i${el.dataset.identifier}` == form.getAttribute("id"))
                        el.style = "opacity: 1; pointer-events: all;"
            } else {
                for (el of document.querySelectorAll(".menu__item"))
                    if (!el.classList.contains("editbutton") && `i${el.dataset.identifier}` == form.getAttribute("id"))
                        el.style = "opacity: 0.5; pointer-events: none;"
            }
        })
    }
    for (elem of document.querySelectorAll(".obtainbutton")) {
        elem.addEventListener("click", (event) => {
            document.querySelector("#keyplace").value = event.target.dataset.identifier
            document.querySelector(".obtain-box").classList.toggle("nodisplay")
        })
    }
    for (elem of document.querySelectorAll(".obtain-box")) {
        elem.addEventListener("click", (event) => {
            if (event.target.classList.contains("obtain-box"))
            event.target.classList.toggle("nodisplay")
        })
    }
} catch (error) {}

try {
    for (elem of document.querySelectorAll(".message-box__carousel-button")) {
        elem.addEventListener("click", (event) => {
            event.target.classList.toggle("message-box__carousel-button_full")
            event.target.parentElement.querySelector(".message-box__carousel").classList.toggle("message-box__carousel_full")
            let carousel = event.target.parentElement.querySelector(".message-box__carousel")
            if (!elem.dataset.wasopened) {
                setTimeout(() => {
                    carousel.style.display = "none"
                    carousel.offsetHeight
                    carousel.style.display = "flex"
                }, 200)
            }
            elem.setAttribute("data-wasopened", true)
            event.target.parentElement.classList.toggle("message-box_extended")
            fullObserver.unobserve(event.target.parentElement.querySelector(".message-box__carousel"))
            fullObserver.observe(event.target.parentElement.querySelector(".message-box__carousel"))
        })
    }
} catch (error) {}



var intersectedElems = []
let fullObserver = new IntersectionObserver((entries) => {
    for (entry of entries) {
        if (entry.isIntersecting && entry.target.classList.contains("message-box__carousel_full")) {
            document.querySelector(".nav-bar").classList.add("backward")
            intersectedElems.push(entry.target)
        } else if (intersectedElems.indexOf(entry.target) != -1 && intersectedElems.length == 1) {
            document.querySelector(".nav-bar").classList.remove("backward")
            intersectedElems.splice(intersectedElems.indexOf(entry.target), 1)
        }
    }
}, { root: null, threshold: 0.7, rootMargin: "0px" })

try {
    for (elem of document.querySelectorAll(".message-box__carousel")) {
        fullObserver.observe(elem)
    }
} catch (error) {}



