"""Authentication API endpoints."""
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from ..database import SessionLocal
from ..models import Company
from ..auth import hash_password, verify_password, create_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new company."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['email', 'password', 'company_name', 'company_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        db = SessionLocal()

        # Check if company already exists
        existing_company = db.query(Company).filter_by(email=data['email']).first()
        if existing_company:
            db.close()
            return jsonify({'error': 'Email already registered'}), 400

        # Create new company
        new_company = Company(
            email=data['email'],
            password_hash=hash_password(data['password']),
            company_name=data['company_name'],
            company_type=data['company_type'],
            description=data.get('description', ''),
            website=data.get('website', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            city=data.get('city', ''),
            country=data.get('country', '')
        )

        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        # Create token
        token = create_token(new_company.id, new_company.email)

        result = {
            'message': 'Company registered successfully',
            'token': token,
            'company': new_company.to_dict()
        }

        db.close()
        return jsonify(result), 201

    except IntegrityError:
        return jsonify({'error': 'Email already registered'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login company."""
    try:
        data = request.get_json()

        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400

        db = SessionLocal()

        # Find company
        company = db.query(Company).filter_by(email=data['email']).first()

        if not company:
            db.close()
            return jsonify({'error': 'Invalid email or password'}), 401

        # Verify password
        if not verify_password(company.password_hash, data['password']):
            db.close()
            return jsonify({'error': 'Invalid email or password'}), 401

        # Check if company is active
        if not company.is_active:
            db.close()
            return jsonify({'error': 'Account is deactivated'}), 403

        # Create token
        token = create_token(company.id, company.email)

        result = {
            'message': 'Login successful',
            'token': token,
            'company': company.to_dict()
        }

        db.close()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
def get_current_company():
    """Get current company info from token."""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token is missing'}), 401

        token = auth_header.split(' ')[1]
        from ..auth import decode_token
        payload = decode_token(token)

        if not payload:
            return jsonify({'error': 'Invalid token'}), 401

        db = SessionLocal()
        company = db.query(Company).filter_by(id=payload['company_id']).first()

        if not company:
            db.close()
            return jsonify({'error': 'Company not found'}), 404

        result = company.to_dict()
        db.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
