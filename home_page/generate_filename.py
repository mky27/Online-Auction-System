import os
import uuid

def generate_filename(instance, filename):
    """Generate a unique filename for the uploaded file."""
    extension = os.path.splitext(filename)[1]
    auction_id = instance.auction.id
    item_name = instance.auction.item_name
    index = instance.index
    new_filename = f"{auction_id}_{item_name}_{index}{extension}"
    return os.path.join('auction_pictures', new_filename)
