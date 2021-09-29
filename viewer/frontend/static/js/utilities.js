const isOk = response => response.ok ? response.json() : Promise.reject(new Error('Failed the request'));

function postRequest(url, data) {
    /**
     * Helper function to send a post request.
     */
    return fetch(url, {
        credentials: 'same-origin',
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'},
    });
}


function isInt(value) {
    /**
     * Checks value for being an integer, including strings
     */
    return Number.isInteger(value) || Number.isInteger(parseInt(value))
}

function makeInterval(startValue, stopValue, numPoints) {
    let arr = [];
    let step = (stopValue - startValue) / (numPoints - 1);
    for (let i = 0; i < numPoints; i++) {
        arr.push(startValue + (step * i));
    }
    return arr;
}


function outer(a1, a2) {
    let outerArray = [];
    for (let i = 0; i < a1.length; i++) {
        let innerArray = []
        for (let j = 0; j < a2.length; j++) {
            innerArray.push(a1[i] * a2[j])
        }
        outerArray.push(innerArray)
    }
    return outerArray
}

const deepMap=(input,callback)=>input.map(entry=>entry.map?deepMap(entry,callback):callback(entry))
