import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';

const https = require('https');

dotenv.config();

const app: Express = express();
const port: number = process.env.PORT;

const api_key: string = process.env.SNIPE_API_KEY;
const api_base_url: string = "https://nationalrobotarium.snipe-it.io/api/v1/";
const api_url: string = api_base_url + api_key + "/";

console.log(api_url)

let request = https.get(api_url+"hardware", res => {
    console.log(res.body);
    console.log("did request");
});


app.get('/', (req: Request, res: Response) => {
    res.send("test\n"));
});

app.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
