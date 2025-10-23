"""Companies API endpoints."""
from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from ..database import SessionLocal
from ..models import Company
from ..auth import token_required

companies_bp = Blueprint('companies', __name__, url_prefix='/api/companies')


@companies_bp.route('/', methods=['GET'])
def get_companies():
    """Get all companies with optional filtering."""
    try:
        db = SessionLocal()

        # Get query parameters
        company_type = request.args.get('type')
        city = request.args.get('city')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # Build query
        query = db.query(Company).filter_by(is_active=True)

        if company_type:
            query = query.filter_by(company_type=company_type)

        if city:
            query = query.filter(Company.city.ilike(f'%{city}%'))

        if search:
            query = query.filter(
                or_(
                    Company.company_name.ilike(f'%{search}%'),
                    Company.description.ilike(f'%{search}%')
                )
            )

        # Count total
        total = query.count()

        # Paginate
        companies = query.offset((page - 1) * per_page).limit(per_page).all()

        result = {
            'companies': [company.to_dict() for company in companies],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }

        db.close()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """Get single company by ID."""
    try:
        db = SessionLocal()

        company = db.query(Company).filter_by(id=company_id, is_active=True).first()

        if not company:
            db.close()
            return jsonify({'error': 'Company not found'}), 404

        result = company.to_dict()
        db.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_company_id):
    """Update company profile."""
    try:
        data = request.get_json()
        db = SessionLocal()

        company = db.query(Company).filter_by(id=current_company_id).first()

        if not company:
            db.close()
            return jsonify({'error': 'Company not found'}), 404

        # Update fields
        if 'company_name' in data:
            company.company_name = data['company_name']
        if 'company_type' in data:
            company.company_type = data['company_type']
        if 'description' in data:
            company.description = data['description']
        if 'website' in data:
            company.website = data['website']
        if 'phone' in data:
            company.phone = data['phone']
        if 'address' in data:
            company.address = data['address']
        if 'city' in data:
            company.city = data['city']
        if 'country' in data:
            company.country = data['country']
        if 'logo_url' in data:
            company.logo_url = data['logo_url']

        db.commit()
        db.refresh(company)

        result = company.to_dict()
        db.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
