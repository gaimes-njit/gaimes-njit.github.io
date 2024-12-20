import { appendLog, createLogFolder, createOutputFolder, listAllDirs, listAllFiles, listCharactersDirs, parseSourceFolderArgument } from 'chatgpt4pcg-node';

import { extractCode } from 'chatgpt4pcg';
import fs from 'fs'
import path from 'path'

const INPUT_STAGE = 'raw'
const CURRENT_STAGE = 'intermediate'

async function main() {
  let sourceFolder = ''
  sourceFolder = '/Users/amy/code/2023/10.october/ScienceBirds/response-gathering-script/competition/'


  try {
    //sourceFolder = parseSourceFolderArgument()
  } catch (e) {
    if (e instanceof Error) {
      console.error(e.message)
    }
    return
  }

  const logFolderPath = await createLogFolder(sourceFolder)

  const teamFolders = await listAllDirs(sourceFolder)

  if (teamFolders.length === 0) {
    const log = `[${new Date().toISOString()}] Processing - No team folders found.`
    await appendLog(logFolderPath, CURRENT_STAGE, log)
    return
  }

  teamFolders.forEach(async (team) => {
    const teamLog = `[${new Date().toISOString()}] Processing - team: ${team}`
    await appendLog(logFolderPath, CURRENT_STAGE, teamLog)

    const teamFolderPath = path.posix.join(sourceFolder, team)
    let characters = [] as string[]

    try {
      characters = await listCharactersDirs(teamFolderPath, INPUT_STAGE)
    } catch (e) {
      const teamLog = `[${new Date().toISOString()}] Processing - team: ${team} - Failed`
      if (e instanceof Error) {
        await appendLog(logFolderPath, CURRENT_STAGE, `${teamLog} - ${e.message.toString()}`)
      } else if (typeof e === 'string') {
        await appendLog(logFolderPath, CURRENT_STAGE, `${teamLog} - ${e}`)
      }
    }

    if (characters.length === 0) {
      return
    }

    characters.forEach(async (character) => {
      const characterLog = `[${new Date().toISOString()}] Processing - team: ${team} - character: ${character}`
      await appendLog(logFolderPath, CURRENT_STAGE, characterLog)

      const characterFolderPath = path.posix.join(teamFolderPath, INPUT_STAGE, character)
      const trials = await listAllFiles(characterFolderPath)

      if (trials.length === 0) {
        const trialLog = `[${new Date().toISOString()}] Processing - team: ${team} - Failed`
        await appendLog(logFolderPath, CURRENT_STAGE, `${trialLog} - No trials found.`)
        return
      }

      trials.forEach(async (trial) => {
        await processTrialFile(team, character, trial, logFolderPath, characterFolderPath);
      })
    })
  })
}

async function processTrialFile(team: string, character: string, trial: string, logFolderPath: string, characterFolderPath: string) {
  const trialLog = `[${new Date().toISOString()}] Processing - team: ${team} - character: ${character} - trial: ${trial}`;
  await appendLog(logFolderPath, CURRENT_STAGE, trialLog);

  const trialFilePath = path.posix.join(characterFolderPath, trial);
  const rawFileContent = await fs.promises.readFile(trialFilePath, 'utf-8');

  try {
    const codeResult = extractCode(rawFileContent);

    if (codeResult === null) {
      throw Error('Code not found.');
    }

    try {
      const outputPath = await createOutputFolder(characterFolderPath, CURRENT_STAGE, INPUT_STAGE);

      const finalFileName = trial.split('.').slice(0, -1).join('.');
      const outputFile = path.posix.join(outputPath, `${finalFileName}.txt`);
      await fs.promises.writeFile(outputFile, codeResult);

      const fileLog = `[${new Date().toISOString()}] Processing - team: ${team} - character: ${character} - trial: ${trial} - Succeed`;
      await appendLog(logFolderPath, CURRENT_STAGE, fileLog);
    } catch (e) {
      await processTrialFile(team, character, trial, logFolderPath, characterFolderPath)
    }
  } catch (e) {
    const fileLog = `[${new Date().toISOString()}] Processing - team: ${team} - character: ${character} - trial: ${trial} - Failed`;
    if (e instanceof Error) {
      await appendLog(logFolderPath, CURRENT_STAGE, `${fileLog} - ${e.message.toString()}`);
    } else if (typeof e === 'string') {
      await appendLog(logFolderPath, CURRENT_STAGE, `${fileLog} - ${e}`);
    }
  }
}

main()