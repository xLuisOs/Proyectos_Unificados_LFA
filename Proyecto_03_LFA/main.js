function validateParentheses(regex){
    let stack = []
    for(let i = 0; i < regex.length; i++){
        let char = regex[i]
        if(char === "(" || char === "["){
            stack.push(char)
        }
        else if(char === ")"){
            if(stack.pop() !== "("){
                return "Paréntesis Sin Cerrar"
            }
        }
        else if(char === "]"){
            if(stack.pop() !== "["){
                return "Corchete Sin Cerrar"
            }
        }
    }
    if(stack.length > 0){
        let last = stack[stack.length - 1]
        return last === "(" ? "Paréntesis Sin Cerrar" : "Corchete Sin Cerrar"
    }
    return ""
}

function validateCharacters(regex){
    const validEscapes = [
        "\\d", "\\w", "\\s", "\\b", "\\B", "\\t", "\\n", "\\r",
        "\\f", "\\v", "\\\\", "\\.", "\\*", "\\+", "\\?", "\\(", "\\)", "\\[", "\\]", "\\|"
    ]
    for(let i = 0; i < regex.length; i++){
        if(regex[i] === "\\"){
            let next = regex[i + 1] || ""
            if(/\d/.test(next)){
                i++
                continue
            }
            let sequence = regex[i] + next
            if(!validEscapes.includes(sequence)){
                return `Escape Inválido: ${sequence}`
            }
            i++
        }
    }
    if(/\*\*|\+\+|\?\?/.test(regex)){
        return "Cuantificador Consecutivo Inválido"
    }
    return ""
}

document.getElementById("regex").addEventListener("input", (e) => {
    const input = e.target
    const value = input.value.trim()
    const errorDiv = document.getElementById("error")
    input.style.boxShadow = "none"
    input.style.borderColor = "#334155"
    errorDiv.textContent = ""
    if (value === "") return
    let error = validateParentheses(value) || validateCharacters(value)
    if(error){
        input.style.borderColor = "red"
        input.style.boxShadow = "0 0 10px red"
        errorDiv.textContent = "Error: " + error
        return
    }
    try{
        new RegExp(value)
        input.style.borderColor= "limegreen"
        input.style.boxShadow = "0 0 10px limegreen"
    }catch(e){
        input.style.borderColor = "red"
        input.style.boxShadow = "0 0 10px red"
        errorDiv.textContent = "Error: Expresión Regular Inválida"
    }
})

document.getElementById("procesar").addEventListener("click", () => {
    const regexInput = document.getElementById("regex").value
    const text = document.getElementById("texto").value
    const errorDiv = document.getElementById("error")
    const resultDiv = document.getElementById("resultado")
    const list = document.getElementById("coincidencias")
    errorDiv.textContent = ""
    resultDiv.innerHTML = ""
    list.innerHTML = ""
    let error = validateParentheses(regexInput)
    if(error){
        errorDiv.textContent = "Error" + error
        return
    }
    error = validateCharacters(regexInput)
    if(error){
        errorDiv.textContent = "Error: " + error
        return
    }
    let regex
    try{
        regex = new RegExp(regexInput, "g")
    }catch(e){
        errorDiv.textContent = "Error: Expresión Regular Inválida"
        return
    }
    const matches = [...text.matchAll(regex)]
    if(matches.length === 0){
        resultDiv.textContent = text
        return
    }
    let highlighted = text.replace(regex, match => 
        `<span class="highlight">${match}</span>`
    )
    resultDiv.innerHTML = highlighted
    matches.forEach(m => {
        let li = document.createElement("li")
        li.innerHTML = `<span class="highlight">${m[0]}</span>`
        list.appendChild(li)
    })
})