from pywebpush import webpush
import os
import json
from models import db, PushSubscription
from flask import current_app
from datetime import datetime

class PushNotificationService:
    def __init__(self):
        self.vapid_private_key = os.environ.get('VAPID_PRIVATE_KEY')
        self.vapid_public_key = os.environ.get('VAPID_PUBLIC_KEY')
        self.vapid_claims = {
            "sub": os.environ.get('VAPID_SUBJECT', 'mailto:your-email@example.com')
        }

    def register_subscription(self, user_id, subscription_info):
        """Register push subscription for a user"""
        try:
            # Check if subscription already exists
            existing_subscription = PushSubscription.query.filter_by(
                user_id=user_id,
                endpoint=subscription_info['endpoint']
            ).first()

            if existing_subscription:
                existing_subscription.is_active = True
                existing_subscription.p256dh_key = subscription_info['keys']['p256dh']
                existing_subscription.auth_key = subscription_info['keys']['auth']
            else:
                new_subscription = PushSubscription(
                    user_id=user_id,
                    endpoint=subscription_info['endpoint'],
                    p256dh_key=subscription_info['keys']['p256dh'],
                    auth_key=subscription_info['keys']['auth']
                )
                db.session.add(new_subscription)

            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(f"Error registering push subscription: {str(e)}")
            return False

    def unregister_subscription(self, user_id, endpoint):
        """Unregister push subscription"""
        try:
            subscription = PushSubscription.query.filter_by(
                user_id=user_id,
                endpoint=endpoint
            ).first()

            if subscription:
                subscription.is_active = False
                db.session.commit()
                return True
            return False
        except Exception as e:
            current_app.logger.error(f"Error unregistering push subscription: {str(e)}")
            return False

    def send_notification_to_user(self, user_id, title, body, data=None):
        """Send push notification to a user"""
        try:
            subscriptions = PushSubscription.query.filter_by(
                user_id=user_id,
                is_active=True
            ).all()

            if not subscriptions:
                return False

            results = []
            message_data = data or {}
            message_data['title'] = title
            message_data['body'] = body

            for subscription in subscriptions:
                result = self._send_push_notification(
                    subscription.endpoint,
                    subscription.p256dh_key,
                    subscription.auth_key,
                    message_data
                )
                results.append(result)

            return any(results)
        except Exception as e:
            current_app.logger.error(f"Error sending notification to user: {str(e)}")
            return False

    def _send_push_notification(self, endpoint, p256dh_key, auth_key, data):
        """Send push notification using Web Push API"""
        try:
            subscription_info = {
                "endpoint": endpoint,
                "keys": {
                    "p256dh": p256dh_key,
                    "auth": auth_key
                }
            }

            # Send the push notification
            response = webpush(
                subscription_info,
                json.dumps(data),
                vapid_private_key=self.vapid_private_key,
                vapid_claims=self.vapid_claims
            )

            return response.status_code in [200, 201]
        except Exception as e:
            current_app.logger.error(f"Error sending push notification: {str(e)}")
            return False

    def send_study_reminder(self, user_id, subject, message):
        """Send study reminder notification"""
        return self.send_notification_to_user(
            user_id,
            f"Study Reminder: {subject}",
            message,
            {"type": "study_reminder", "subject": subject}
        )

    def send_progress_update(self, user_id, subject, progress):
        """Send progress update notification"""
        return self.send_notification_to_user(
            user_id,
            f"Progress Update: {subject}",
            f"You've completed {progress}% of {subject}",
            {"type": "progress_update", "subject": subject, "progress": progress}
        )

# Create instance
notification_service = PushNotificationService()