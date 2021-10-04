let viewLayout = {
    plot_bgcolor: "rgb(5,5,5)",
    paper_bgcolor: "rgb(5,5,5)",
    height: "100vh",
    title: "3D orbits",
    autosize: true,
    showlegend: false,
    margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 0
    },
    scene: {
        xaxis: {
            title: "Distance X",
            titlefont_color: '#0a0a0a',
            range: [-1000, 1000],
            backgroundcolor: '#0a0a0a',
            color: "white",
            gridcolor: '#0a0a0a'
        },
        yaxis: {
            title: "Distance Y",
            titlefont_color: '#0a0a0a',
            range: [-1000, 1000],
            backgroundcolor: '#0a0a0a',
            color: "white",
            gridcolor: '#0a0a0a'
        },
        zaxis: {
            title: "Distance Z",
            range: [-1000, 1000],
            backgroundcolor: '#0a0a0a',
            color: "white",
            gridcolor: '#0a0a0a'
        }
    }
};

function asteroidIDList(asteroidInputs) {
    /**
     * Parses inputs from the pillbox to integers
     * @param  {Array<Object>} asteroidInputs - Select2 values
     * @return {Array} - List of integers representing asteroid ID numbers
     */
    let idList = [];
    for (let selection of asteroidInputs) {
        let asteroidID = selection.text;
        if (isInt(asteroidID)) {
            idList.push(parseInt(asteroidID));
        }
    }
    return idList;
}

function setRouteCard(startName, targetName, distance, time, path, heuristic) {
    /**
     *
     * @param {String} startName - name of starting asteroid
     * @param {String} targetName - name of target asteroid
     * @param {Number} distance - distance taken in units of million kilometer
     * @param {String} time - time taken to travel from start to target
     * @param {Array} path - Array filled with asteroid ID's to indicate path traveled
     * @param {String} heuristic - Heuristic used to calculate the best route
     */
    document.querySelector('#route-title').textContent = `From ${startName} to ${targetName}`;
    document.querySelector('#route-distance').textContent = `${distance} million kilometer`;
    document.querySelector('#route-heuristic').textContent = `Heuristic = ${heuristic}`;
    document.querySelector('#route-time').textContent = time;
    document.querySelector('#route-path').textContent = path.join(" --> ");

}


function createAsteroidViewer(urlBase) {
    /**
     * Creates the asteroid viewer via Plotly.js
     * @param {String} urlBase - Endpoint to send route request to
     */
    // Retrieve asteroid tags
    let startingAsteroids = $('#asteroidStartInput').select2("data");
    let targetAsteroids = $('#asteroidTargetInput').select2("data");
    let heuristic = $('#heuristicInput').select2("data")[0].id;

    // Get asteroid ID list
    let startAsteroidIDList = asteroidIDList(startingAsteroids);
    startAsteroidIDList.length = Math.min(startAsteroidIDList.length, 1);
    let targetAsteroidIDList = asteroidIDList(targetAsteroids);
    targetAsteroidIDList.length = Math.min(targetAsteroidIDList.length, 5);

    postRequest(urlBase, {
        start_asteroids: startAsteroidIDList,
        target_asteroids: targetAsteroidIDList,
        heuristic: heuristic
    })
        .then(isOk)
        .then(response => {
            let startingAsteroids = response.starting_asteroids;
            let targetAsteroids = response.target_asteroids;
            let route = response.route;

            setRouteCard(route.start, route.target, route.distance, route.time, route.path, heuristic);

            let traces = createTraces(startingAsteroids, targetAsteroids);
            viewLayout.scene.annotations = createAnnotations(startingAsteroids, targetAsteroids);
            Plotly.newPlot("view", traces, viewLayout, {responsive: true});
            window.dispatchEvent(new Event("resize")); // Plotly graph doesn't fill screen until window resize
        })
        .catch(error => {
            console.log(error);
            alert("Rocks not found");
        });
}