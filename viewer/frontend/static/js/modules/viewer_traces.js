const MARKER_SIZE = {"SMALL": 3, "MEDIUM": 6, "LARGE": 9, "HUGE": 15, "SUN": 30};

function orbitTrace(fullPosition) {
    /**
     * Creates a plotly trace for the orbit of an asteroid
     * @param fullPosition - List of xyz coordinates
     * @param {Array} - List of Plotly scatter3D traces
     */
    return {
        x: fullPosition.map((value) => value[0]),
        y: fullPosition.map((value) => value[1]),
        z: fullPosition.map((value) => value[2]),
        mode: "markers",
        marker: {
            size: 0.3,
            line: {
                color: "white",
                width: 5
            },
        },
        type: "scatter3d"
    };
}

function sphereTrace(size, pos, clr) {
    /**
     * Creates a sphere at a set xyz coordinate by creating new points around it
     * @param {Number} size - multiplication factor to determine sphere size
     * @param {Array} pos - List of xyz coordinates
     * @param {String} clr - Color, string of RGB or hex denotation
     * @return {Object} - Plotly surface trace as an object
     */
    const theta = makeInterval(0, 2 * Math.PI, 100);
    const phi = makeInterval(0, Math.PI, 100);

    let xProduct = outer(theta.map((x) => Math.cos(x)), phi.map((x) => Math.sin(x)));
    let x0 = deepMap(xProduct, (x) => x * size + pos[0]);
    let yProduct = outer(theta.map((x) => Math.sin(x)), phi.map((x) => Math.sin(x)));
    let y0 = deepMap(yProduct, (x) => x * size + pos[1]);
    let zProduct = outer(new Array(100).fill(1), phi.map((x) => Math.cos(x)));
    let z0 = deepMap(zProduct, (x) => x * size + pos[2]);

    return {
        z: z0,
        y: y0,
        x: x0,
        colorscale: [[0, clr], [1, clr]],
        showscale: false,
        type: "surface"
    };
}

function pathTrace(pos1, pos2) {
    /**
     * Creates a plotly trace for a path line between two asteroids
     * @param {Array} pos1 - List with xyz coordinates
     * @param {Array} pos2 - List with xyz coordinates
     * @param {Array} - Plotly path trace as object
     */
    return {
        x: [pos1[0], pos2[0]],
        y: [pos1[1], pos2[1]],
        z: [pos1[2], pos2[2]],
        mode: "lines",
        line: {
            width: 5,
            color: "#ffffba"
        },
        type: "scatter3d"
    };
}

function createDimensionalAnchors() {
    /**
     * Create traces at fixed points in the view corners to stop spheres from deflating. This happens because plotly
     * reduce the view ratio if things are plotted together closely.
     * @return {Array} - List of Plotly scatter3D traces
     */
    let cornerCombos = cartesian([1000, -1000], [1000, -1000], [1000, -1000]);
    let traceList = [];
    for (let c of cornerCombos) {
        traceList.push({
                x: [c[0]],
                y: [c[1]],
                z: [c[2]],
                mode: "markers",
                marker: {
                    size: 0.001,
                    line: {
                        color: "rgb(5,5,5)",
                    },
                },
                type: "scatter3d"
            }
        );
    }
    return traceList;
}

function annot(pos, name) {
    /**
     * Helper function for annotation creation
     * @param {Array} pos - List of xyz coordinates
     * @param {String} name - What text will hover over the annotation
     * @return {Object} - Object representing a Plotly annotation
     */
    return {
        showarrow: false,
        x: pos[0],
        y: pos[1],
        z: pos[2] + 30,
        text: name,
        xanchor: 5,
        font: {
            color: "white",
            size: 12
        }
    };
}

function createAnnotations(startingAsteroids, targetAsteroids, travelAsteroids) {
    /**
     * Iterates over the asteroid lists to create an annotation at their location
     * @param {Array<Object>} startingAsteroids - list of start asteroids
     * @param {Array<Object>} targerAsteroids - list of target asteroids
     * @return {Array} - List of objects representing Plotly annotations
     */
    let annotationList = [];
    annotationList.push(annot([0, 0, 10], "Adalia"));
    for (const asteroid of startingAsteroids.concat(targetAsteroids, travelAsteroids)) {
        let pos = asteroid.pos;
        annotationList.push(annot(pos, asteroid.name));
    }
    return annotationList;
}

function createTraces(startingAsteroids, targetAsteroids, travelAsteroids) {
    /**
     * Master function to create traces for the 3d view
     * @param {Array<Object>} startingAsteroids - list of start asteroids
     * @param {Array<Object>} targerAsteroids - list of target asteroids
     * @return {Array} - List of all Plotly traces necessary for the asteroid viewer
     */
    let traces = [];

    // Dimensional anchors
    for (const anchor of createDimensionalAnchors()) {
        traces.push(anchor);
    }

    // Adalia Prime trace
    traces.push(sphereTrace(MARKER_SIZE.SUN, [0, 0, 0], "#eaeaea"));

    // Starting asteroid traces
    for (let asteroid of startingAsteroids) {
        traces.push(orbitTrace(asteroid.orbit));
        traces.push(sphereTrace(MARKER_SIZE[asteroid.size], asteroid.pos, "#56a3f2"));
    }
    // Travel asteroids traces
    for (let asteroid of travelAsteroids) {
        traces.push(sphereTrace(MARKER_SIZE[asteroid.size], asteroid.pos, "#b7b7b7"));
    }
    // Target asteroid traces
    for (let asteroid of targetAsteroids) {
        traces.push(orbitTrace(asteroid.orbit));
        traces.push(sphereTrace(MARKER_SIZE[asteroid.size], asteroid.pos, "#4fff7b"));
    }
    // Asteroid path traces
    let pathAsteroidList = startingAsteroids.concat(travelAsteroids, targetAsteroids);
    for (let i = 0; i < pathAsteroidList.length - 1; i++) {
        traces.push(pathTrace(pathAsteroidList[i].pos, pathAsteroidList[i + 1].pos));
    }
    return traces;
}