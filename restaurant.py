from flask import Flask
from flask import render_template, request, url_for, redirect, flash, jsonify
from database_setup import db, Restaurant, MenuItem

app = Flask(__name__)

app.secret_key = 'super secret key'

# For database stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'
db.init_app(app)


@app.route('/')
@app.route('/restaurants')
def index():
    restaurants = Restaurant.query.all()
    return render_template('index.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        restaurant_name = request.form['name']
        if restaurant_name:
            newRestaurant = Restaurant(name=restaurant_name)
            db.session.add(newRestaurant)
            db.session.commit()
            flash("New restaurant created!")  # TODO: html for this
        return redirect(url_for('index'))
    return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        new_name = request.form['name']
        if new_name:
            restaurant.name = new_name
            db.session.add(restaurant)
            db.session.commit()
            flash("Restaurant updated!")
        return redirect(url_for('index'))

    return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        db.session.delete(restaurant)
        db.session.commit()
        flash("Restaurant was deleted!")
        return redirect(url_for('index'))
    return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    menu = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return render_template('restaurantMenu.html', restaurant=restaurant, restaurant_id=restaurant_id, menu=menu)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def new_restaurant_menu(restaurant_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        new_menu_item = MenuItem(name=name, description=description, price=price, restaurant_id=restaurant_id)
        db.session.add(new_menu_item)
        db.session.commit()
        flash("new menu create")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_restaurant_menu(restaurant_id, menu_id):
    menu = MenuItem.query.filter_by(id=menu_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        menu.name = name
        menu.description = description
        menu.price = price
        db.session.add(menu)
        db.session.commit()
        flash("Updated the menu!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id, menu=menu))

    return render_template('editMenuItem.html', menu=menu, restaurant_id=restaurant_id, menu_id=menu_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_restaurant_menu(restaurant_id, menu_id):
    menu = MenuItem.query.filter_by(id=menu_id).one()
    if request.method == 'POST':
        db.session.delete(menu)
        db.session.commit()
        flash("Menu Item was deleted!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    return render_template('deleteMenuItem.html', menu=menu, restaurant_id=restaurant_id, menu_id=menu_id)


@app.route('/restaurants/JSON', methods=['GET'])
def restaurants_json():
    restaurants = Restaurant.query.all()
    return jsonify(restaurants=[i.serialize for i in restaurants])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON', methods=['GET'])
def restaurant_menu_json(restaurant_id):
    menus = MenuItem.query.filter_by(restaurant_id=restaurant_id)
    return jsonify(menus=[i.serialize for i in menus])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON', methods=['GET'])
def restaurant_menu_item_json(restaurant_id,menu_id):
    menu_item = MenuItem.query.filter_by(id=menu_id).one()
    return jsonify(menu=menu_item.serialize)


if __name__ == '__main__':
    app.run(debug=True)
