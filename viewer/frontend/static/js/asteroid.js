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
     * @param asteroidInputs - Select2 values
     */
    let idList = [];
    for (let selection of asteroidInputs) {
        let asteroidID = selection.text;
        if (isInt(asteroidID)) {
            idList.push(parseInt(asteroidID))
        }
    }
    return idList
}

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


function sphereTrace(size, pos, clr) {
    const theta = makeInterval(0, 2 * Math.PI, 100);
    const phi = makeInterval(0, Math.PI, 100);

    let xProduct =  outer(theta.map(x => Math.cos(x)), phi.map(x => Math.sin(x)));
    let x0 = deepMap(xProduct, x => x * size + pos[0])
    let yProduct = outer(theta.map(x => Math.sin(x)), phi.map(x => Math.sin(x)))
    let y0 = deepMap(yProduct, x => x * size + pos[1])
    let zProduct = outer(new Array(100).fill(1), phi.map(x => Math.cos(x)))
    let z0 = deepMap(zProduct, x => x * size + pos[2])

    return {
        z: z0,
        y: y0,
        x: x0,
        colorscale: [[0, clr], [1, clr]],
        showscale: false,
        type: 'surface'
    }
}


function createAsteroidViewer(urlBase) {
    /**
     * Retrieves an asteroid
     * @param {String} urlBase - endpoint to send request to
     */
    let startingAsteroids = $('#asteroidStartInput').select2('data');
    let targetAsteroids = $('#asteroidTargetInput').select2('data');

    let startAsteroidIDList = asteroidIDList(startingAsteroids);
    let targetAsteroidIDList = asteroidIDList(targetAsteroids);

    postRequest(urlBase, {start_asteroids: startAsteroidIDList, target_asteroids: targetAsteroidIDList})
        .then(isOk)
        .then(response => {
            let startingOrbits = response['starting_orbits'];
            let targetOrbits = response['target_orbits'];
            let traces = []

            for (let orbit of startingOrbits) {
                traces.push(orbitTrace(orbit['orbit']));
            }
            for (let orbit of targetOrbits) {
                traces.push(orbitTrace(orbit['orbit']));
            }
            for (let orbit of startingOrbits) {
                let sphere = sphereTrace(20, orbit['pos'], '#bfbfbf');
                traces.push(sphere)
            }

            Plotly.newPlot('view', traces, view_layout, {'responsive': true});
            window.dispatchEvent(new Event('resize')); // Plotly graph doesn't fill screen until window resize
        })
        .catch(error => {
            console.log(error);
            alert("Rocks not found");
        });
}