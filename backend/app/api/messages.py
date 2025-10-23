"""Messages API endpoints."""
from flask import Blueprint, request, jsonify
from sqlalchemy import or_, desc
from ..database import SessionLocal
from ..models import Message, Company
from ..auth import token_required

messages_bp = Blueprint('messages', __name__, url_prefix='/api/messages')


@messages_bp.route('/', methods=['GET'])
@token_required
def get_messages(current_company_id):
    """Get messages for current company."""
    try:
        db = SessionLocal()

        # Get query parameters
        message_type = request.args.get('type', 'received')  # received, sent, all

        # Build query
        if message_type == 'received':
            query = db.query(Message).filter_by(receiver_id=current_company_id)
        elif message_type == 'sent':
            query = db.query(Message).filter_by(sender_id=current_company_id)
        else:  # all
            query = db.query(Message).filter(
                or_(
                    Message.receiver_id == current_company_id,
                    Message.sender_id == current_company_id
                )
            )

        messages = query.order_by(desc(Message.created_at)).all()

        result = {
            'messages': [message.to_dict() for message in messages]
        }

        db.close()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/<int:message_id>', methods=['GET'])
@token_required
def get_message(message_id, current_company_id):
    """Get single message."""
    try:
        db = SessionLocal()

        message = db.query(Message).filter_by(id=message_id).first()

        if not message:
            db.close()
            return jsonify({'error': 'Message not found'}), 404

        # Check if current company is sender or receiver
        if message.sender_id != current_company_id and message.receiver_id != current_company_id:
            db.close()
            return jsonify({'error': 'Unauthorized'}), 403

        # Mark as read if receiver
        if message.receiver_id == current_company_id and not message.is_read:
            message.is_read = True
            db.commit()

        result = message.to_dict()
        db.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/', methods=['POST'])
@token_required
def send_message(current_company_id):
    """Send a new message."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['receiver_id', 'subject', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        db = SessionLocal()

        # Check if receiver exists
        receiver = db.query(Company).filter_by(id=data['receiver_id']).first()
        if not receiver:
            db.close()
            return jsonify({'error': 'Receiver not found'}), 404

        # Create new message
        new_message = Message(
            sender_id=current_company_id,
            receiver_id=data['receiver_id'],
            subject=data['subject'],
            message=data['message']
        )

        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        result = new_message.to_dict()
        db.close()

        return jsonify(result), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/<int:message_id>/read', methods=['PUT'])
@token_required
def mark_as_read(message_id, current_company_id):
    """Mark message as read."""
    try:
        db = SessionLocal()

        message = db.query(Message).filter_by(id=message_id).first()

        if not message:
            db.close()
            return jsonify({'error': 'Message not found'}), 404

        # Check if current company is receiver
        if message.receiver_id != current_company_id:
            db.close()
            return jsonify({'error': 'Unauthorized'}), 403

        message.is_read = True
        db.commit()

        result = message.to_dict()
        db.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/unread-count', methods=['GET'])
@token_required
def get_unread_count(current_company_id):
    """Get count of unread messages."""
    try:
        db = SessionLocal()

        count = db.query(Message).filter_by(
            receiver_id=current_company_id,
            is_read=False
        ).count()

        db.close()

        return jsonify({'unread_count': count}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
