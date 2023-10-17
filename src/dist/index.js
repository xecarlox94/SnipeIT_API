"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
const app = (0, express_1.default)();
const port = process.env.PORT;
const api_key = process.env.SNIPE_API_KEY;
const api_base_url = "https://nationalrobotarium.snipe-it.io/api/v1/";
app.get('/', (req, res) => {
    res.send('Express + TypeScript Server\n' + api_key + '\n' + api_base_url);
});
app.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
