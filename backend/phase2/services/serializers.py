from phase2.schemas.restaurant import RestaurantOut
from shared.db.models import Restaurant


def to_restaurant_out(restaurant: Restaurant) -> RestaurantOut:
    return RestaurantOut(
        id=restaurant.id,
        name=restaurant.name,
        url=restaurant.url,
        address=restaurant.address,
        location=restaurant.location,
        city=restaurant.city,
        rest_type=restaurant.rest_type,
        cuisines=restaurant.cuisines,
        cuisine_tags=restaurant.cuisine_tag_list,
        rating=restaurant.rating,
        votes=restaurant.votes,
        cost_for_two=restaurant.cost_for_two,
        dish_liked=restaurant.dish_liked,
        online_order=restaurant.online_order,
        book_table=restaurant.book_table,
        listed_in_type=restaurant.listed_in_type,
        review_snippet=restaurant.review_snippet,
    )
