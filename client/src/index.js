const express = require("express");
const redis = require("redis");
const app = express();

const td = "<td style='padding: 4px; border-style: dotted; border-width: 1px; text-align: center'>";
const td2 = "<td style='padding: 4px; border-style: dotted; border-width: 1px; text-align: left'>";
const client = redis.createClient({url: 'redis://iot-datastack'})
client.connect()

app.get('/', (req, res) => {
    (async () => {
        let raw_data = await client.get('iot-data')
        let data = JSON.parse(raw_data)

        let text = "<h1>IoT Line Production Stats</h1>"
        text += "<table style='border: black; border-width: 2px; border-style: double;'>";
        text += "<tr><th>COLOR</th><th>COUNT</th><th>AVG WIDTH</th></tr>";

        let keys = Object.keys(data)
        keys.sort((a, b) => -(Number(data[a][0]) - Number(data[b][0])))

        for (const x of keys) {
            text += "<tr>";
            text += td2 + x + "</td>";
            text += td + data[x][0] + "</td>";
            text += td + Number(data[x][1]).toFixed(2) + "</td></tr>";
        }

        text += "</table>";
        res.send(text)
    })();
});

app.listen(8080, () => {
    console.log("Node server started at: http://localhost:8080/");
});

