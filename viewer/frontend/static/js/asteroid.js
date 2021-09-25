function asteroidGet(urlBase) {
    /**
     * Retrieves an asteroid
     * @param {String} urlBase - endpoint to send request to
     */
    let asteroidID = document.querySelector('#asteroidIdInput').value;
    let requestUrl = urlBase.slice(0, -1) + asteroidID;

    fetch(requestUrl)
        .then(isOk)
        .then(data => {
            document.querySelector('#filler').textContent = JSON.stringify(data);
        })
        .catch(error => {
            console.log(error);
            alert("Rock not found");
        });
}