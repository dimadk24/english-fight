import tcomb from 'tcomb'
import { createModel, ModelInstance } from '../core/model-utils'
import { ID, Null } from '../core/tcomb-types'

const attributes = {
  id: ID,
  question: tcomb.String,
  answerWords: tcomb.list(tcomb.String),
  correctAnswer: tcomb.union([Null, tcomb.String]),
  selectedAnswer: tcomb.union([Null, tcomb.String]),
  isCorrect: tcomb.Boolean,
}

export interface QuestionInstance extends ModelInstance {
  id: number
  question: string
  answerWords: string[]
  correctAnswer: null | string
  selectedAnswer: null | string
  isCorrect: boolean
}

export class Question extends createModel<QuestionInstance>(
  attributes,
  'Question'
) {}
