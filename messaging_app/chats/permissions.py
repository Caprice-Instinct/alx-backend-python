from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants to access a conversation/messages
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Check if obj is a Conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Check if obj is a Message
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
