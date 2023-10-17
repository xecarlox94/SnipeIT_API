import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';

dotenv.config();

const app: Express = express();
const port: number = process.env.PORT;

const api_key: string = process.env.SNIPE_API_KEY;
const api_base_url: string = "https://nationalrobotarium.snipe-it.io/api/v1/"


app.get('/', (req: Request, res: Response) => {
    res.send('Express + TypeScript Server\n'+api_key+'\n'+api_base_url);
});

app.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
