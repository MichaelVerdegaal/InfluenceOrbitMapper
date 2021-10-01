let view_layout = {
    plot_bgcolor: "rgb(5,5,5)",
    paper_bgcolor: "rgb(5,5,5)",
    'height': '100vh',
    title: '3D orbits',
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
            title: 'Distance X',
            titlefont_color: '#0a0a0a',
            range: [-1000, 1000],
            backgroundcolor: '#0a0a0a',
            color: 'white',
            gridcolor: '#0a0a0a'
        },
        yaxis: {
            title: 'Distance Y',
            titlefont_color: '#0a0a0a',
            range: [-1000, 1000],
            backgroundcolor: '#0a0a0a',
            color: 'white',
            gridcolor: '#0a0a0a'
        },
        zaxis: {
            title: 'Distance Z',
            range: [-1000, 1000],
            backgroundcolor: '#0a0a0a',
            color: 'white',
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

function createAsteroidViewer(urlBase) {
    /**
     * Creates the asteroid viewer via Plotly.js
     * @param {String} urlBase - Endpoint to send route request to
     */
    let startingAsteroids = $('#asteroidStartInput').select2('data');
    let targetAsteroids = $('#asteroidTargetInput').select2('data');

    let startAsteroidIDList = asteroidIDList(startingAsteroids);
    let targetAsteroidIDList = asteroidIDList(targetAsteroids);

    postRequest(urlBase, {start_asteroids: startAsteroidIDList, target_asteroids: targetAsteroidIDList})
        .then(isOk)
        .then(response => {
            let startingAsteroids = response.starting_asteroids;
            let targetAsteroids = response.target_asteroids;
            let traces = createTraces(startingAsteroids, targetAsteroids);
            view_layout.scene.annotations = createAnnotations(startingAsteroids, targetAsteroids);

            Plotly.newPlot('view', traces, view_layout, {'responsive': true});
            window.dispatchEvent(new Event('resize')); // Plotly graph doesn't fill screen until window resize
        })
        .catch(error => {
            console.log(error);
            alert("Rocks not found");
        });
}