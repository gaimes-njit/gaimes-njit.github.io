"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const chatgpt4pcg_node_1 = require("chatgpt4pcg-node");
const chatgpt4pcg_1 = require("chatgpt4pcg");
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const INPUT_STAGE = 'raw';
const CURRENT_STAGE = 'intermediate';
function main() {
    return __awaiter(this, void 0, void 0, function* () {
        let sourceFolder = '';
        sourceFolder = '/Users/amy/code/2023/10.october/ScienceBirds/response-gathering-script/competition/';
        try {
            //sourceFolder = parseSourceFolderArgument()
        }
        catch (e) {
            if (e instanceof Error) {
                console.error(e.message);
            }
            return;
        }
        const logFolderPath = yield (0, chatgpt4pcg_node_1.createLogFolder)(sourceFolder);
        const teamFolders = yield (0, chatgpt4pcg_node_1.listAllDirs)(sourceFolder);
        if (teamFolders.length === 0) {
            const log = `[${new Date().toISOString()}] Processing - No team folders found.`;
            yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, log);
            return;
        }
        teamFolders.forEach((team) => __awaiter(this, void 0, void 0, function* () {
            const teamLog = `[${new Date().toISOString()}] Processing - team: ${team}`;
            yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, teamLog);
            const teamFolderPath = path_1.default.posix.join(sourceFolder, team);
            let characters = [];
            try {
                characters = yield (0, chatgpt4pcg_node_1.listCharactersDirs)(teamFolderPath, INPUT_STAGE);
            }
            catch (e) {
                const teamLog = `[${new Date().toISOString()}] Processing - team: ${team} - Failed`;
                if (e instanceof Error) {
                    yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, `${teamLog} - ${e.message.toString()}`);
                }
                else if (typeof e === 'string') {
                    yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, `${teamLog} - ${e}`);
                }
            }
            if (characters.length === 0) {
                return;
            }
            characters.forEach((character) => __awaiter(this, void 0, void 0, function* () {
                const characterLog = `[${new Date().toISOString()}] Processing - team: ${team} - character: ${character}`;
                yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, characterLog);
                const characterFolderPath = path_1.default.posix.join(teamFolderPath, INPUT_STAGE, character);
                const trials = yield (0, chatgpt4pcg_node_1.listAllFiles)(characterFolderPath);
                if (trials.length === 0) {
                    const trialLog = `[${new Date().toISOString()}] Processing - team: ${team} - Failed`;
                    yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, `${trialLog} - No trials found.`);
                    return;
                }
                trials.forEach((trial) => __awaiter(this, void 0, void 0, function* () {
                    yield processTrialFile(team, character, trial, logFolderPath, characterFolderPath);
                }));
            }));
        }));
    });
}
function processTrialFile(team, character, trial, logFolderPath, characterFolderPath) {
    return __awaiter(this, void 0, void 0, function* () {
        const trialLog = `[${new Date().toISOString()}] Processing - team: ${team} - character: ${character} - trial: ${trial}`;
        yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, trialLog);
        const trialFilePath = path_1.default.posix.join(characterFolderPath, trial);
        const rawFileContent = yield fs_1.default.promises.readFile(trialFilePath, 'utf-8');
        try {
            const codeResult = (0, chatgpt4pcg_1.extractCode)(rawFileContent);
            if (codeResult === null) {
                throw Error('Code not found.');
            }
            try {
                const outputPath = yield (0, chatgpt4pcg_node_1.createOutputFolder)(characterFolderPath, CURRENT_STAGE, INPUT_STAGE);
                const finalFileName = trial.split('.').slice(0, -1).join('.');
                const outputFile = path_1.default.posix.join(outputPath, `${finalFileName}.txt`);
                yield fs_1.default.promises.writeFile(outputFile, codeResult);
                const fileLog = `[${new Date().toISOString()}] Processing - team: ${team} - character: ${character} - trial: ${trial} - Succeed`;
                yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, fileLog);
            }
            catch (e) {
                yield processTrialFile(team, character, trial, logFolderPath, characterFolderPath);
            }
        }
        catch (e) {
            const fileLog = `[${new Date().toISOString()}] Processing - team: ${team} - character: ${character} - trial: ${trial} - Failed`;
            if (e instanceof Error) {
                yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, `${fileLog} - ${e.message.toString()}`);
            }
            else if (typeof e === 'string') {
                yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, CURRENT_STAGE, `${fileLog} - ${e}`);
            }
        }
    });
}
main();
