from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.notification import (
    Notification
)

from app.schemas.notification import (
    NotificationCreate
)

from app.api.deps import (
    get_current_active_user,
    require_super_admin
)

from app.models.user import User

from app.services.websocket_manager import (
    manager
)

router = APIRouter()


# =========================
# CREATE NOTIFICATION
# =========================

@router.post("/")
async def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_super_admin
    )
):

    notification = Notification(
        title=payload.title,
        message=payload.message,
        notification_type=payload.notification_type,
        user_id=payload.user_id
    )

    db.add(notification)

    db.commit()

    db.refresh(notification)

    # REAL-TIME BROADCAST
    await manager.broadcast(
        f"{payload.title}: {payload.message}"
    )

    return {
        "message": "Notification sent",
        "notification": notification
    }


# =========================
# GET USER NOTIFICATIONS
# =========================

@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    notifications = db.query(
        Notification
    ).filter(
        Notification.user_id == current_user.id
    ).all()

    return notifications


# =========================
# MARK AS READ
# =========================

@router.patch("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    notification = db.query(
        Notification
    ).filter(
        Notification.id == notification_id
    ).first()

    if notification:

        notification.is_read = True

        db.commit()

    return {
        "message": "Notification marked as read"
    }


# =========================
# WEBSOCKET
# =========================

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await manager.connect(websocket)

    try:

        while True:

            data = await websocket.receive_text()

            await manager.send_personal_message(
                f"You wrote: {data}",
                websocket
            )

    except WebSocketDisconnect:

        manager.disconnect(websocket)