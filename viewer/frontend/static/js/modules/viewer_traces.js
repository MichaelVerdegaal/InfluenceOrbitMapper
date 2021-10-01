function createTraces(startingAsteroids, targetAsteroids) {
    /**
     * Master function to create traces for the 3d view
     */
    let marker_size = {'SMALL': 3, 'MEDIUM': 6, 'LARGE': 9, "HUGE": 15, 'SUN': 30};
    let traces = [];

    // Dimensional anchors
    for (const anchor of createDimensionalAnchors()) {
        traces.push(anchor);
    }

    // Adalia Prime
    traces.push(sphereTrace(marker_size.SUN, [0, 0, 0], '#eaeaea'));

    for (let asteroid of startingAsteroids) {
        traces.push(orbitTrace(asteroid.orbit));
        traces.push(sphereTrace(marker_size[asteroid.size], asteroid.pos, '#56a3f2'));
    }
    for (let asteroid of targetAsteroids) {
        traces.push(orbitTrace(asteroid.orbit));
        traces.push(sphereTrace(marker_size[asteroid.size], asteroid.pos, '#4fff7b'));
    }
    return traces;
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
    };
}

function sphereTrace(size, pos, clr) {
    /**
     * Creates a sphere at a set xyz coordinate by creating new points around it
     */
    const theta = makeInterval(0, 2 * Math.PI, 100);
    const phi = makeInterval(0, Math.PI, 100);

    let xProduct = outer(theta.map(x => Math.cos(x)), phi.map(x => Math.sin(x)));
    let x0 = deepMap(xProduct, x => x * size + pos[0]);
    let yProduct = outer(theta.map(x => Math.sin(x)), phi.map(x => Math.sin(x)));
    let y0 = deepMap(yProduct, x => x * size + pos[1]);
    let zProduct = outer(new Array(100).fill(1), phi.map(x => Math.cos(x)));
    let z0 = deepMap(zProduct, x => x * size + pos[2]);

    return {
        z: z0,
        y: y0,
        x: x0,
        colorscale: [[0, clr], [1, clr]],
        showscale: false,
        type: 'surface'
    };
}

function createDimensionalAnchors() {
    /**
     * Set fixed points in the view corners to stop spheres from deflating
     */
    let cornerCombos = cartesian([1000, -1000], [1000, -1000], [1000, -1000]);
    let traceList = [];
    for (let c of cornerCombos) {
        traceList.push({
                x: [c[0]],
                y: [c[1]],
                z: [c[2]],
                mode: 'markers',
                marker: {
                    size: 0.001,
                    line: {
                        color: 'rgb(5,5,5)',
                    },
                },
                type: 'scatter3d'
            }
        );
    }
    return traceList;
}

function annot(pos, name) {
    return {
        showarrow: false,
        x: pos[0],
        y: pos[1],
        z: pos[2] + 30,
        text: name,
        xanchor: 5,
        font: {
            color: 'white',
            size: 12
        }
    };
}

function createAnnotations(startingOrbits, targetOrbits) {
    let annotationList = [];
    annotationList.push(annot([0, 0, 10], 'Adalia'));
    for (const asteroid of startingOrbits.concat(targetOrbits)) {
        let pos = asteroid.pos;
        annotationList.push(annot(pos, asteroid.name));
    }
    return annotationList;
}