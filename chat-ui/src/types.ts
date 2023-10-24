export interface Question {
  question_id: string;
  question_text: string;
  response_type: AnnotationResponseType;
  answer: string | null;
}

export type ConversationAnnotation = Question[];

export interface UtteranceAnnotation {
  utterance_id: string;
  questions: Question[];
}

export type AnnotationResponseType = 'Yes/No' | 'Likert' | 'Text';

export interface Message {
  id: number;
  chat_id: string;
  text: string;
  type: 'user' | 'bot';
  topic: string;
}

export interface ChatModel {
  id: string;
  title: string;
  isRemovable: boolean
}
