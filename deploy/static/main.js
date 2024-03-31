document.addEventListener("DOMContentLoaded", (event) => {
    const canvas = document.getElementById("drawing_canvas")
    const context = canvas.getContext('2d')
    const clearButton = document.getElementById('clr')
    const submitButton = document.getElementById('sub')
    const predText = document.getElementById('pred')
    let isDrawing = false

    // setup canvas to black
    context.fillStyle = 'black'
    context.fillRect(0, 0, canvas.width, canvas.height)
    // brush properties
    context.lineWidth = 15
    context.strokeStyle = 'white'

    
    const startDrawing = (event) => {
        isDrawing = true;
        draw(event)
    }
    const draw = (event) => {
        if(!isDrawing) return;
        const x = event.clientX - canvas.offsetLeft
        const y = event.clientY - canvas.offsetTop
        context.lineTo(x, y)
        context.stroke()
    }
    const stopDrawing = () => {
        isDrawing = false
        context.beginPath()
    } 
    const predict = () => {
        canvas_data = canvas.toDataURL()
        const predictURL = '/predict'
        const data = {
            image: canvas_data
        }
        const requestOpt = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
        fetch(predictURL, requestOpt)
            .then(response => {
                if(!response.ok){
                    throw new Error('API call failed')
                }
                return response.json()
            })
            .then(data => {
                let prediction = data.prediction
                predText.innerHTML = `Prediction: ${prediction}`
            })
            .catch(error => {
                console.error('Error', error)
            })
    }
    
    canvas.addEventListener('mousedown', startDrawing)
    canvas.addEventListener('mousemove', draw)
    canvas.addEventListener('mouseup', stopDrawing)
    canvas.addEventListener('mouseout', stopDrawing)
    clearButton.addEventListener('click', () => {
        context.clearRect(0, 0, canvas.width, canvas.height)
        context.fillStyle = 'black'
        context.fillRect(0, 0, canvas.width, canvas.height)
    })
    submitButton.addEventListener('click', predict)
    
})
