const isOk = response => response.ok ? response.json() : Promise.reject(new Error('Failed the request'));

function postRequest(url, data) {
    /**
     * Helper function to send a post request.
     * @param {String} - url as string to send the HTTP request to
     * @param {Object} - Data to send along with the request
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
     * @param value - Value to check for Integer membership
     * @return {Boolean} - Whether the value is an integer or not
     */
    return Number.isInteger(value) || Number.isInteger(parseInt(value));
}

function makeInterval(startValue, stopValue, numPoints) {
    /**
     * Generates a list between 2 ranges, with a predetermined amount of points.
     * @param {Number} startValue - Integer to start the range at
     * @param {Number} stopValue - Integer to stop the range at
     * @param {Number} numPoints - Integer amount to indicate the amount of points in the range
     * @return {Array<Number>} - Array of indicated specification
     */
    let arr = [];
    let step = (stopValue - startValue) / (numPoints - 1);
    for (let i = 0; i < numPoints; i++) {
        arr.push(startValue + (step * i));
    }
    return arr;
}


function outer(v1, v2) {
    /**
     * Computes the outer product of 2 vectors to generate a matrix
     * Ref: https://numpy.org/doc/stable/reference/generated/numpy.outer.html
     * @param {Array<Number>} v1 - First vector
     * @param {Array<Number>} v2 - Second vector
     * @return {Array<Array<Number>>} - Matrix of the 2 vectors
     */
    let outerArray = [];
    for (let i = 0; i < v1.length; i++) {
        let innerArray = [];
        for (let j = 0; j < v2.length; j++) {
            innerArray.push(v1[i] * v2[j]);
        }
        outerArray.push(innerArray);
    }
    return outerArray;
}


/**
 * Applies a function to a nested array
 * Ref: https://stackoverflow.com/a/58223155/7174982
 * @param {Array<Array>} input - Nested array
 * @param {} callback - Function to apply to input array
 * @return {Array} - modified input
 */
const deepMap = (input, callback) => input.map(entry => entry.map ? deepMap(entry, callback) : callback(entry));

/**
 * Cartesian product of multiple arrays
 * Ref: https://stackoverflow.com/a/43053803/7174982
 * @param {...Array} a - Multiple arrays of size n
 * @return {Array} - Cartesian product of input arrays
 */
const cartesian = (...a) => a.reduce((a, b) => a.flatMap(d => b.map(e => [d, e].flat())));