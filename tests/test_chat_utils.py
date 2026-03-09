from chat.utils import create_personal_room
from chat.models import ChatRoom


def test_personal_room_creation():
    """create_personal_room should create a ChatRoom with the correct name and participants."""
    room = create_personal_room("alice")
    assert isinstance(room, ChatRoom)
    assert room.name == "personal-alice"
    # should include the user and an agent identifier
    assert "alice" in room.participants
    assert any(p.startswith("agent-") for p in room.participants)
