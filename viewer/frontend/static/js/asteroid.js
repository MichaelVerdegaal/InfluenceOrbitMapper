function asteroidGet(urlBase) {
    /**
     * Retrieves an asteroid
     * @param {String} urlBase - endpoint to send request to
     */
    let asteroidIDInputData = $('#asteroidIdInput').select2('data');
    let asteroidIDList = [];
    for (let selection of asteroidIDInputData) {
        let asteroidID = selection.text;
        asteroidIDList.push(parseInt(asteroidID))
    }
    console.log(asteroidIDInputData);

    postRequest(urlBase, {asteroid_id_list: asteroidIDList})
        .then(isOk)
        .then(data => {
            document.querySelector('#filler').textContent = JSON.stringify(data);
        })
        .catch(error => {
            console.log(error);
            alert("Rocks not found");
        });
}