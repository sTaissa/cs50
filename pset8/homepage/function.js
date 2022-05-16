document.addEventListener('DOMContentLoaded', () => {
    const lightModeStorage = localStorage.getItem('light-mode')
    const body = document.querySelector('body')
    const nav = document.querySelectorAll('a')
    const inputLightMode = document.getElementById('light-mode')

    if(lightModeStorage) {
        body.setAttribute("light", "true")
        a(0)
    }

    inputLightMode.addEventListener('change', () => {
        if(inputLightMode.checked){
            body.setAttribute("light", "true")
            a(0)
            localStorage.setItem('light-mode', true)
        }else{
            body.removeAttribute("light")
            a(1)
            localStorage.removeItem('light-mode')
        }
    })

    function a(num) {
        if (num == 0) {
            for(var i = 0; i < nav.length; i++) {
                nav[i].setAttribute("light", "true");
            }
        } else {
            for(var i = 0; i < nav.length; i++) {
                nav[i].removeAttribute("light");
            }
        }
}
})
