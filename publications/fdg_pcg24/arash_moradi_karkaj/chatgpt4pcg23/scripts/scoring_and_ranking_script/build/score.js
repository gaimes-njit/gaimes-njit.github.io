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
exports.getWeights = exports.getPromptScore = exports.getTrialScore = exports.getAverageStabilityScore = exports.getAverageSimilarityScore = exports.getCharacterScore = exports.getCompetitionScore = exports.getNormalizedPromptScores = void 0;
const _1 = require(".");
const chatgpt4pcg_node_1 = require("chatgpt4pcg-node");
const bignumber_js_1 = __importDefault(require("bignumber.js"));
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
function getNormalizedPromptScores(allTeamPromptScores, competitionScore) {
    const divider = competitionScore.valueOf() === "0" ? new bignumber_js_1.default(1) : competitionScore;
    return allTeamPromptScores
        .map(p => {
        var _a;
        return ({
            team: p.team,
            promptScore: ((_a = p.promptScore) === null || _a === void 0 ? void 0 : _a.dividedBy(divider).multipliedBy(100)) || new bignumber_js_1.default(0)
        });
    })
        .sort((a, b) => a.promptScore.gt(b.promptScore || new bignumber_js_1.default(0)) ? -1 : 1)
        .map(p => ({
        team: p.team,
        promptScore: p.promptScore.toFixed()
    }));
}
exports.getNormalizedPromptScores = getNormalizedPromptScores;
function getCompetitionScore(allTeamPromptScores) {
    let competitionScore = new bignumber_js_1.default(0);
    for (const promptScore of allTeamPromptScores) {
        competitionScore = competitionScore.plus(promptScore.promptScore || new bignumber_js_1.default(0));
    }
    return competitionScore;
}
exports.getCompetitionScore = getCompetitionScore;
function getCharacterScore(trialScores) {
    var _a;
    return ((_a = trialScores.reduce((acc, cur) => acc === null || acc === void 0 ? void 0 : acc.plus(cur || new bignumber_js_1.default(0)), new bignumber_js_1.default(0))) === null || _a === void 0 ? void 0 : _a.dividedBy(_1.NUM_TRIALS)) || new bignumber_js_1.default(0);
}
exports.getCharacterScore = getCharacterScore;
function getAverageSimilarityScore(averageSimilarityScores) {
    return averageSimilarityScores.reduce((acc, cur) => acc.plus(cur), new bignumber_js_1.default(0)).dividedBy(_1.NUM_TRIALS);
}
exports.getAverageSimilarityScore = getAverageSimilarityScore;
function getAverageStabilityScore(averageStabilityScores) {
    return averageStabilityScores.reduce((acc, cur) => acc.plus(cur), new bignumber_js_1.default(0)).dividedBy(_1.NUM_TRIALS);
}
exports.getAverageStabilityScore = getAverageStabilityScore;
function getTrialScore(weights, character, trialStability, trialSimilarity) {
    var _a;
    return (_a = weights
        .find(w => w.character === character)) === null || _a === void 0 ? void 0 : _a.weight.multipliedBy(trialStability).multipliedBy(trialSimilarity);
}
exports.getTrialScore = getTrialScore;
function getPromptScore(characterScores) {
    var _a;
    return (_a = characterScores
        .map(score => score.characterScore)
        .reduce((acc, cur) => acc === null || acc === void 0 ? void 0 : acc.plus(cur || new bignumber_js_1.default(0)), new bignumber_js_1.default(0))) === null || _a === void 0 ? void 0 : _a.dividedBy(characterScores.length);
}
exports.getPromptScore = getPromptScore;
function getWeights(sourceFolder) {
    return __awaiter(this, void 0, void 0, function* () {
        const teamFolders = yield (0, chatgpt4pcg_node_1.listAllDirs)(sourceFolder);
        const logFolderPath = yield (0, chatgpt4pcg_node_1.createLogFolder)(sourceFolder);
        const characterWeights = [];
        for (const character of _1.CHARACTER_LIST) {
            const characterFilePath = `${character}.json`;
            const averageStability = yield getAverageStabilityAcrossTeams(teamFolders, characterFilePath);
            const weightStability = bignumber_js_1.default.max(new bignumber_js_1.default(1).minus(averageStability), new bignumber_js_1.default(1).dividedBy(_1.CHARACTER_LIST.length));
            const averageSimilarity = yield getAverageSimilarityAcrossTeams(characterFilePath);
            const weightSimilarity = bignumber_js_1.default.max(new bignumber_js_1.default(1).minus(averageSimilarity), new bignumber_js_1.default(1).dividedBy(_1.CHARACTER_LIST.length));
            const weight = {
                character: character,
                weightStability,
                weightSimilarity,
                weight: weightStability.multipliedBy(weightSimilarity)
            };
            characterWeights.push(weight);
            const weightLog = `[${new Date().toISOString().replaceAll(':', '_')}] character: ${weight.character} - weight: ${weight.weight.toFixed()} - weightStability: ${weight.weightStability.toFixed()} - weightSimilarity: ${weight.weightSimilarity.toFixed()}`;
            yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, _1.CURRENT_STAGE, weightLog);
        }
        return characterWeights;
        // ------------------------------
        function getAverageStabilityAcrossTeams(teamFolders, character) {
            return __awaiter(this, void 0, void 0, function* () {
                let sumOfStabilityOfAllTeams = new bignumber_js_1.default(0);
                for (const team of teamFolders) {
                    const trialStability = yield getTrialStability(team, character);
                    sumOfStabilityOfAllTeams = sumOfStabilityOfAllTeams.plus(trialStability);
                }
                return sumOfStabilityOfAllTeams.dividedBy(teamFolders.length * _1.NUM_TRIALS);
            });
        }
        function getAverageSimilarityAcrossTeams(character) {
            return __awaiter(this, void 0, void 0, function* () {
                let sumOfSimilarityOfAllTeams = new bignumber_js_1.default(0);
                for (const team of teamFolders) {
                    const trialSimilarity = yield getTrialSimilarity(team, character);
                    sumOfSimilarityOfAllTeams = sumOfSimilarityOfAllTeams.plus(trialSimilarity);
                }
                return sumOfSimilarityOfAllTeams.dividedBy(teamFolders.length * _1.NUM_TRIALS);
            });
        }
        function getTrialSimilarity(prompt, character) {
            return __awaiter(this, void 0, void 0, function* () {
                const similarityResultPath = path_1.default.posix.join(sourceFolder, prompt, _1.STAGE_SIMILARITY, character);
                let similarityResult = {
                    count: 0,
                    similarityRate: 0,
                    trials: [],
                    similarities: []
                };
                try {
                    const similarityFile = yield fs_1.default.promises.readFile(similarityResultPath, 'utf8');
                    similarityResult = (yield JSON.parse(similarityFile));
                }
                catch (e) {
                    const similarityLog = `[${new Date().toISOString()}] Processing similarity - prompt: ${prompt} - character: ${character}`;
                    if (e instanceof Error) {
                        yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, _1.CURRENT_STAGE, `${similarityLog} - ${e.message.toString()}`);
                    }
                    else if (typeof e === 'string') {
                        yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, _1.CURRENT_STAGE, `${similarityLog} - ${e}`);
                    }
                }
                const trialSimilarity = similarityResult.trials.reduce((acc, cur) => acc.plus(new bignumber_js_1.default(cur.similarity)), new bignumber_js_1.default(0));
                return trialSimilarity;
            });
        }
        function getTrialStability(prompt, character) {
            return __awaiter(this, void 0, void 0, function* () {
                const stabilityResultPath = path_1.default.posix.join(sourceFolder, prompt, _1.STAGE_STABILITY, character);
                let stabilityResult = {
                    dataCount: 0,
                    rate: 0,
                    raws: [],
                };
                try {
                    const stabilityFile = yield fs_1.default.promises.readFile(stabilityResultPath, 'utf8');
                    stabilityResult = (yield JSON.parse(stabilityFile));
                }
                catch (e) {
                    const stabilityLog = `[${new Date().toISOString()}] Processing stability - prompt: ${prompt} - character: ${character}`;
                    if (e instanceof Error) {
                        yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, _1.CURRENT_STAGE, `${stabilityLog} - ${e.message.toString()}`);
                    }
                    else if (typeof e === 'string') {
                        yield (0, chatgpt4pcg_node_1.appendLog)(logFolderPath, _1.CURRENT_STAGE, `${stabilityLog} - ${e}`);
                    }
                }
                const trialStability = stabilityResult.raws.reduce((acc, cur) => acc.plus(new bignumber_js_1.default(cur.score)), new bignumber_js_1.default(0));
                return trialStability;
            });
        }
    });
}
exports.getWeights = getWeights;
