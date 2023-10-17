"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const dotenv_1 = __importDefault(require("dotenv"));
const https = require('https');
dotenv_1.default.config();
const app = (0, express_1.default)();
const port = process.env.PORT;
const api_key = process.env.SNIPE_API_KEY;
const api_base_url = "https://nationalrobotarium.snipe-it.io/api/v1/";
const api_url = api_base_url + api_key + "/";
console.log(api_url);
let request = https.get(api_url + "hardware", res => {
    console.log(res.body);
    console.log("did request");
});
app.get('/', (req, res) => {
    res.send("test\n");
});
;
app.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
