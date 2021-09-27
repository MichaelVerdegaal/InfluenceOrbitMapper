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
            console.log(response);
            let sorbet = response['starting_orbits'][0]['orbit']


            let layout = {
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
                        titlefont_color: 'black',
                        range: [-1000, 1000],
                        backgroundcolor: 'black',
                        color: 'black',
                        gridcolor: 'black'
                    },
                    yaxis: {
                        title: 'Distance Y',
                        titlefont_color: 'black',
                        range: [-1000, 1000],
                        backgroundcolor: 'black',
                        color: 'black',
                        gridcolor: 'black'
                    },
                    zaxis: {
                        range: [-1000, 1000],
                        backgroundcolor: 'black',
                        color: 'white',
                        gridcolor: 'black'
                    }
                }
            };

            let data = [
                {
                    x: sorbet.map(function (value, index) {
                        return value[0];
                    }),
                    y: sorbet.map(function (value, index) {
                        return value[1];
                    }),
                    z: sorbet.map(function (value, index) {
                        return value[2];
                    }),
                    mode: 'markers',
                    marker: {
                        size: 0.1,
                        line: {
                            color: 'rgb(0,0,0)',
                            width: 2
                        },
                        opacity: 0.5
                    },
                    type: 'scatter3d'
                }
            ]


            Plotly.newPlot('view', data, layout);

        })
        .catch(error => {
            console.log(error);
            alert("Rocks not found");
        });
}