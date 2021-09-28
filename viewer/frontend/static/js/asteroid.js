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


function orbitTrace(fullPosition) {
    /**
     * Creates a plotly trace
     * @param fullPosition - List of xyz coordinates
     */
    return {
        x: fullPosition.map(function (value) {
            return value[0];
        }),
        y: fullPosition.map(function (value) {
            return value[1];
        }),
        z: fullPosition.map(function (value) {
            return value[2];
        }),
        mode: 'markers',
        marker: {
            size: 0.3,
            line: {
                color: 'white',
                width: 5
            },
        },
        type: 'scatter3d'
    }
}


function asteroidGet(urlBase) {
    /**
     * Retrieves an asteroid
     * @param {String} urlBase - endpoint to send request to
     */
    let startingAsteroids = $('#asteroidStartInput').select2('data');
    let targetAsteroids = $('#asteroidTargetInput').select2('data');

    let startAsteroidIDList = [];
    let endAsteroidIDList = [];
    for (let selection of startingAsteroids) {
        let asteroidID = selection.text;
        if (isInt(asteroidID)) {
            startAsteroidIDList.push(parseInt(asteroidID))
        }
    }
    for (let selection of targetAsteroids) {
        let asteroidID = selection.text;
        if (isInt(asteroidID)) {
            endAsteroidIDList.push(parseInt(asteroidID))
        }
    }

    postRequest(urlBase, {start_asteroids: startAsteroidIDList, target_asteroids: endAsteroidIDList})
        .then(isOk)
        .then(response => {
            let startingOrbits = response['starting_orbits'];
            let targetOrbits = response['target_orbits'];
            let data = []

            for (let orbit of startingOrbits) {
                data.push(orbitTrace(orbit['orbit']));
            }
            for (let orbit of targetOrbits) {
                data.push(orbitTrace(orbit['orbit']));
            }


            Plotly.newPlot('view', data, view_layout, {'responsive': true});
            window.dispatchEvent(new Event('resize')); // Plotly graph doesn't fill screen until window resize
        })
        .catch(error => {
            console.log(error);
            alert("Rocks not found");
        });
}