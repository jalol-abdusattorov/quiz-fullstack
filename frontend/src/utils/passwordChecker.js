import { ZxcvbnFactory } from '@zxcvbn-ts/core'
import { adjacencyGraphs, dictionary } from '@zxcvbn-ts/language-common'
import { translations, dictionary as enDictionary } from '@zxcvbn-ts/language-en'

const options = {
  translations,
  graphs: adjacencyGraphs,
  dictionary: {
    ...dictionary,
    ...enDictionary,
  },
}

const checker = new ZxcvbnFactory(options)

// Library that determines if the password is easy to crach, or not. Returns 0 <= Score <= 4 in this range
export function checkPassword(password) {
    if (!password) return { score: 0, feedback: {} }
    return checker.check(password)
}