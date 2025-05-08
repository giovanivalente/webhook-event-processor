from realmate_challenge.shared.exception import ObjectNotFound


class ConversationNotFound(ObjectNotFound):
    default_detail = 'It was not found a conversation for this conversation id.'
    default_code = 'CONVERSATION_NOT_FOUND'


class MessageNotFound(ObjectNotFound):
    default_detail = 'It was not found a message for this message id.'
    default_code = 'MESSAGE_NOT_FOUND'
