from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users who are participants
    of a conversation to access/modify its messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False

    def has_permission_for_action(self, request, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()
        return False
