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
exports.CURRENT_STAGE = exports.NUM_TRIALS = exports.STAGE_SIMILARITY = exports.STAGE_STABILITY = exports.CHARACTER_LIST = void 0;
const score_1 = require("./score");
const chatgpt4pcg_node_1 = require("chatgpt4pcg-node");
// @ts-ignore
const node_1 = require("@json2csv/node");
const bignumber_js_1 = __importDefault(require("bignumber.js"));
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
exports.CHARACTER_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
exports.STAGE_STABILITY = 'stability';
exports.STAGE_SIMILARITY = 'similarity';
exports.NUM_TRIALS = 10;
exports.CURRENT_STAGE = 'result';
function main() {
    var _a, _b, _c;
    return __awaiter(this, void 0, void 0, function* () {
        let sourceFolder = '';
        sourceFolder = '/Users/amy/Downloads/TONSOFPROMPTS/0/competition'; //'/Users/amy/code/2023/10.october/ScienceBirds/response-gathering-script/competition/'
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
        const prompts = yield (0, chatgpt4pcg_node_1.listAllDirs)(sourceFolder);
        const weights = yield (0, score_1.getWeights)(sourceFolder);
        const allTeamTrialScores = [];
        const allTeamAverageStabilityScores = [];
        const allTeamAverageSimilarityScores = [];
        const allTeamCharacterScores = [];
        const allTeamPromptScores = [];
        const allTeamsFinalScoresAndRanks = [];
        for (const prompt of prompts) {
            const teamLog = `[${new Date().toISOString()}] Processing - prompt: ${[prompt]}`;
            yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, teamLog);
            const promptFilePath = path_1.default.posix.join(sourceFolder, prompt);
            let stability = [];
            let similarity = [];
            try {
                const stabilityPath = path_1.default.posix.join(promptFilePath, exports.STAGE_STABILITY);
                stability = yield (0, chatgpt4pcg_node_1.listAllFiles)(stabilityPath);
            }
            catch (e) {
                const promptLog = `[${new Date().toISOString()}] Processing - prompt: ${prompt} - Failed`;
                if (e instanceof Error) {
                    yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, `${promptLog} - ${e.message.toString()}`);
                }
                else if (typeof e === 'string') {
                    yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, `${promptLog} - ${e}`);
                }
            }
            try {
                const similarityPath = path_1.default.posix.join(promptFilePath, exports.STAGE_SIMILARITY);
                similarity = yield (0, chatgpt4pcg_node_1.listAllFiles)(similarityPath);
            }
            catch (e) {
                const promptLog = `[${new Date().toISOString()}] Processing - prompt: ${prompt} - Failed`;
                if (e instanceof Error) {
                    yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, `${promptLog} - ${e.message.toString()}`);
                }
                else if (typeof e === 'string') {
                    yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, `${promptLog} - ${e}`);
                }
            }
            if (stability.length !== similarity.length) {
                const promptLog = `[${new Date().toISOString()}] Processing - prompt: ${prompt} - Failed`;
                yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, `${promptLog} - Number of stability files and similarity files are not equal.`);
                return;
            }
            const characterScores = [];
            for (const character of exports.CHARACTER_LIST) {
                const characterFilePath = `${character}.json`;
                const characterStabilityFilePath = path_1.default.posix.join(promptFilePath, exports.STAGE_STABILITY, characterFilePath);
                const characterSimilarityFilePath = path_1.default.posix.join(promptFilePath, exports.STAGE_SIMILARITY, characterFilePath);
                let stabilityResult = {
                    dataCount: 0,
                    rate: 0,
                    raws: [],
                };
                let similarityResult = {
                    count: 0,
                    similarityRate: 0,
                    trials: [],
                    similarities: []
                };
                try {
                    const stabilityFile = yield fs_1.default.promises.readFile(characterStabilityFilePath, 'utf8');
                    const similarityFile = yield fs_1.default.promises.readFile(characterSimilarityFilePath, 'utf8');
                    stabilityResult = (yield JSON.parse(stabilityFile));
                    similarityResult = (yield JSON.parse(similarityFile));
                }
                catch (e) {
                    const characterLog = `[${new Date().toISOString()}] Processing - prompt: ${prompt} - character: ${character}`;
                    if (e instanceof Error) {
                        yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, `${characterLog} - ${e.message.toString()}`);
                    }
                    else if (typeof e === 'string') {
                        yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, `${characterLog} - ${e}`);
                    }
                }
                const trialScores = [];
                const stabilityScores = [];
                const similarityScores = [];
                const averageStabilityScores = [];
                const averageSimilarityScores = [];
                for (let i = 0; i < exports.NUM_TRIALS; i++) {
                    const stabilityScore = ((_a = stabilityResult.raws[i]) === null || _a === void 0 ? void 0 : _a.score) || 0;
                    const trialStability = new bignumber_js_1.default(stabilityScore);
                    stabilityScores.push({ stabilityScore: trialStability, character, team: prompt, trial: i + 1 });
                    console.log('__________________________________-');
                    console.log('Trial: ', i + 1);
                    console.log('stabilityScores.push({})');
                    console.log('stabilityScore: ', (_b = stabilityResult.raws[i]) === null || _b === void 0 ? void 0 : _b.score);
                    console.log('character: ', character);
                    console.log('team: ', prompt);
                    console.log('trial: ', i + 1);
                    console.log('');
                    const similarityScore = ((_c = similarityResult.trials[i]) === null || _c === void 0 ? void 0 : _c.similarity) || 0;
                    console.log('similarityScores.push({})');
                    console.log('similarityScore: ', similarityScore);
                    const trialSimilarity = new bignumber_js_1.default(similarityScore);
                    similarityScores.push({ similarityScore: trialSimilarity, character, team: prompt, trial: i + 1 });
                    console.log('character: ', character);
                    console.log('team: ', prompt);
                    console.log('trial: ', i + 1);
                    console.log('getTrialScore(weights, character, trialStability, trialSimilarity)');
                    console.log('');
                    const trialScore = (0, score_1.getTrialScore)(weights, character, trialStability, trialSimilarity);
                    trialScores.push({ trialScore, character, team: prompt, trial: i + 1 });
                    const trialLog = `[${new Date().toISOString()}] Calculating trial score - prompt: ${prompt} - character: ${character} - trial: ${i + 1} - stability: ${trialStability} - similarity: ${trialSimilarity} - trial_score: ${trialScore === null || trialScore === void 0 ? void 0 : trialScore.toFixed()}`;
                    (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, trialLog);
                    averageStabilityScores.push(trialStability);
                    averageSimilarityScores.push(trialSimilarity);
                }
                allTeamTrialScores.push({ trialScores, character, team: prompt, stabilityScores, similarityScores });
                const avgStability = (0, score_1.getAverageStabilityScore)(averageStabilityScores);
                allTeamAverageStabilityScores.push({ avgStability, character, team: prompt });
                const avgSimilarity = (0, score_1.getAverageSimilarityScore)(averageSimilarityScores);
                allTeamAverageSimilarityScores.push({ avgSimilarity, character, team: prompt });
                const averageLog = `[${new Date().toISOString()}] Calculating average stability and similarity - prompt: ${prompt} - character: ${character} - stability: ${avgStability.toFixed()} - similarity: ${avgSimilarity.toFixed()}`;
                (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, averageLog);
                const characterScore = (0, score_1.getCharacterScore)(trialScores.map((x) => x.trialScore));
                characterScores.push({ characterScore, character, team: prompt });
                allTeamCharacterScores.push({ characterScore, character, team: prompt });
                const characterLog = `[${new Date().toISOString()}] Calculating character score - prompt: ${prompt} - character: ${character} - character_score: ${characterScore === null || characterScore === void 0 ? void 0 : characterScore.toFixed()}`;
                (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, characterLog);
            }
            const promptScore = (0, score_1.getPromptScore)(characterScores);
            allTeamPromptScores.push({ team: prompt, promptScore });
            const promptLog = `[${new Date().toISOString()}] Calculating prompt score - prompt: ${prompt} - prompt_score: ${promptScore === null || promptScore === void 0 ? void 0 : promptScore.toFixed()}`;
            (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, promptLog);
        }
        const competitionScore = (0, score_1.getCompetitionScore)(allTeamPromptScores);
        const competitionLog = `[${new Date().toISOString()}] Calculating competition score - competition_score: ${competitionScore.toFixed()}`;
        (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, competitionLog);
        const normPromptScores = (0, score_1.getNormalizedPromptScores)(allTeamPromptScores, competitionScore);
        normPromptScores.forEach((p, i) => {
            const normPromptLog = `[${new Date().toISOString()}] Calculating normalized prompt score - prompt: ${p.team} - normalized_prompt_score: ${p.promptScore} - rank: ${i + 1}`;
            (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, exports.CURRENT_STAGE, normPromptLog);
        });
        normPromptScores.forEach((p, i) => {
            var _a, _b;
            allTeamsFinalScoresAndRanks.push({
                team: p.team, normalizedPromptScore: p.promptScore, promptScore: ((_b = (_a = allTeamPromptScores.find((x) => x.team === p.team)) === null || _a === void 0 ? void 0 : _a.promptScore) === null || _b === void 0 ? void 0 : _b.toFixed()) || '0', rank: i + 1
            });
        });
        yield outputToFiles({
            scores: {
                allTeamTrialScores,
                competitionScore,
                allTeamsFinalScoresAndRanks,
                allTeamAverageStabilityScores,
                allTeamAverageSimilarityScores,
                allTeamCharacterScores,
            },
            sourceFolder,
            weights
        });
    });
}
function outputToFiles({ scores: { allTeamTrialScores, competitionScore, allTeamsFinalScoresAndRanks, allTeamAverageStabilityScores, allTeamAverageSimilarityScores, allTeamCharacterScores, }, sourceFolder, weights }) {
    return __awaiter(this, void 0, void 0, function* () {
        const allTeamTrialScoresObj = allTeamTrialScores.map((x) => {
            return x.trialScores.map((y) => {
                var _a, _b, _c;
                return {
                    teamName: x.team,
                    character: y.character,
                    trial: y.trial,
                    trial_Score: (_a = y.trialScore) === null || _a === void 0 ? void 0 : _a.toFixed(),
                    stabilityScore: (_b = x.stabilityScores.find((z) => z.team === x.team && z.character === y.character && z.trial === y.trial)) === null || _b === void 0 ? void 0 : _b.stabilityScore.toFixed(),
                    similarityScore: (_c = x.similarityScores.find((z) => z.team === x.team && z.character === y.character && z.trial === y.trial)) === null || _c === void 0 ? void 0 : _c.similarityScore.toFixed()
                };
            });
        }).flat();
        const allTeamCharacterScoresObj = allTeamCharacterScores.map((x) => {
            var _a, _b, _c;
            return {
                teamName: x.team,
                character: x.character,
                characterScore: (_a = x.characterScore) === null || _a === void 0 ? void 0 : _a.toFixed(),
                nonWeightedAverageStabilityScore: (_b = allTeamAverageStabilityScores.find((y) => y.team === x.team && y.character === x.character)) === null || _b === void 0 ? void 0 : _b.avgStability.toFixed(),
                nonWeightedAverageSimilarityScore: (_c = allTeamAverageSimilarityScores.find((y) => y.team === x.team && y.character === x.character)) === null || _c === void 0 ? void 0 : _c.avgSimilarity.toFixed()
            };
        });
        const constantsJSON = JSON.stringify({
            competitionScore: competitionScore.toFixed(),
            'weights': weights.map(w => ({
                character: w.character,
                weight: w.weight.toFixed(),
                weightStability: w.weightStability.toFixed(),
                weightSimilarity: w.weightSimilarity.toFixed()
            }))
        });
        const outputDir = yield (0, chatgpt4pcg_node_1.createResultOutputFolder)(sourceFolder);
        const constantsOutputFile = path_1.default.posix.join(outputDir, 'constants.json');
        yield fs_1.default.promises.writeFile(constantsOutputFile, constantsJSON);
        try {
            const parser = new node_1.AsyncParser();
            const trialsOutputFile = path_1.default.posix.join(outputDir, 'trial_scores.csv');
            const charactersOutputFile = path_1.default.posix.join(outputDir, 'character_scores.csv');
            const ranksOutputFile = path_1.default.posix.join(outputDir, 'prompt_scores_ranks.csv');
            const allTeamTrialScoresCSV = yield parser.parse(JSON.stringify(allTeamTrialScoresObj)).promise();
            const allTeamCharacterScoresCSV = yield parser.parse(JSON.stringify(allTeamCharacterScoresObj)).promise();
            const allTeamFinalScoresAndRanksCSV = yield parser.parse(JSON.stringify(allTeamsFinalScoresAndRanks)).promise();
            yield fs_1.default.promises.writeFile(trialsOutputFile, allTeamTrialScoresCSV);
            yield fs_1.default.promises.writeFile(charactersOutputFile, allTeamCharacterScoresCSV);
            yield fs_1.default.promises.writeFile(ranksOutputFile, allTeamFinalScoresAndRanksCSV);
        }
        catch (e) {
            console.error(e);
        }
    });
}
main();
