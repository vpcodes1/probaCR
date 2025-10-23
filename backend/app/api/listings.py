"""Listings API endpoints."""
from flask import Blueprint, request, jsonify
from sqlalchemy import or_, desc
from ..database import SessionLocal
from ..models import Listing, Company
from ..auth import token_required

listings_bp = Blueprint('listings', __name__, url_prefix='/api/listings')


@listings_bp.route('/', methods=['GET'])
def get_listings():
    """Get all listings with optional filtering."""
    try:
        db = SessionLocal()

        # Get query parameters
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        location = request.args.get('location')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # Build query
        query = db.query(Listing).filter_by(is_active=True)

        if category:
            query = query.filter_by(category=category)

        if subcategory:
            query = query.filter_by(subcategory=subcategory)

        if location:
            query = query.filter(Listing.location.ilike(f'%{location}%'))

        if search:
            query = query.filter(
                or_(
                    Listing.title.ilike(f'%{search}%'),
                    Listing.description.ilike(f'%{search}%')
                )
            )

        # Count total
        total = query.count()

        # Paginate
        listings = query.order_by(desc(Listing.created_at)).offset((page - 1) * per_page).limit(per_page).all()

        result = {
            'listings': [listing.to_dict() for listing in listings],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }

        db.close()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@listings_bp.route('/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    """Get single listing by ID."""
    try:
        db = SessionLocal()

        listing = db.query(Listing).filter_by(id=listing_id).first()

        if not listing:
            db.close()
            return jsonify({'error': 'Listing not found'}), 404

        # Increment views
        listing.views_count += 1
        db.commit()

        result = listing.to_dict()
        db.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@listings_bp.route('/', methods=['POST'])
@token_required
def create_listing(current_company_id):
    """Create a new listing."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['title', 'description', 'category']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        db = SessionLocal()

        # Create new listing
        new_listing = Listing(
            company_id=current_company_id,
            title=data['title'],
            description=data['description'],
            category=data['category'],
            subcategory=data.get('subcategory'),
            price_range=data.get('price_range'),
            location=data.get('location'),
            image_url=data.get('image_url')
        )

        db.add(new_listing)
        db.commit()
        db.refresh(new_listing)

        result = new_listing.to_dict()
        db.close()

        return jsonify(result), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@listings_bp.route('/<int:listing_id>', methods=['PUT'])
@token_required
def update_listing(listing_id, current_company_id):
    """Update a listing."""
    try:
        data = request.get_json()
        db = SessionLocal()

        listing = db.query(Listing).filter_by(id=listing_id).first()

        if not listing:
            db.close()
            return jsonify({'error': 'Listing not found'}), 404

        # Check ownership
        if listing.company_id != current_company_id:
            db.close()
            return jsonify({'error': 'Unauthorized'}), 403

        # Update fields
        if 'title' in data:
            listing.title = data['title']
        if 'description' in data:
            listing.description = data['description']
        if 'category' in data:
            listing.category = data['category']
        if 'subcategory' in data:
            listing.subcategory = data['subcategory']
        if 'price_range' in data:
            listing.price_range = data['price_range']
        if 'location' in data:
            listing.location = data['location']
        if 'image_url' in data:
            listing.image_url = data['image_url']
        if 'is_active' in data:
            listing.is_active = data['is_active']

        db.commit()
        db.refresh(listing)

        result = listing.to_dict()
        db.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@listings_bp.route('/<int:listing_id>', methods=['DELETE'])
@token_required
def delete_listing(listing_id, current_company_id):
    """Delete a listing."""
    try:
        db = SessionLocal()

        listing = db.query(Listing).filter_by(id=listing_id).first()

        if not listing:
            db.close()
            return jsonify({'error': 'Listing not found'}), 404

        # Check ownership
        if listing.company_id != current_company_id:
            db.close()
            return jsonify({'error': 'Unauthorized'}), 403

        db.delete(listing)
        db.commit()
        db.close()

        return jsonify({'message': 'Listing deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@listings_bp.route('/my', methods=['GET'])
@token_required
def get_my_listings(current_company_id):
    """Get listings for current company."""
    try:
        db = SessionLocal()

        listings = db.query(Listing).filter_by(company_id=current_company_id).order_by(desc(Listing.created_at)).all()

        result = {
            'listings': [listing.to_dict(include_company=False) for listing in listings]
        }

        db.close()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@listings_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get available categories."""
    categories = [
        {'value': 'transport', 'label': 'Transport i Logistika'},
        {'value': 'dobavljaci', 'label': 'Dobavljači'},
        {'value': 'proizvodnja', 'label': 'Proizvodnja'},
        {'value': 'usluge', 'label': 'Poslovne Usluge'},
        {'value': 'gradjevina', 'label': 'Građevina'},
        {'value': 'trgovina', 'label': 'Trgovina'},
        {'value': 'it', 'label': 'IT i Tehnologija'},
        {'value': 'marketing', 'label': 'Marketing i PR'},
        {'value': 'finansije', 'label': 'Finansije i Računovodstvo'},
        {'value': 'ostalo', 'label': 'Ostalo'}
    ]

    return jsonify({'categories': categories}), 200
