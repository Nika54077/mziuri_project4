from flask import Flask, session, request, render_template, redirect, url_for, flash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ეს-არის-ჩემი-საიდუმლო-გასაღები-12345-ძალიან-საიდუმლო'

@app.route('/')
def products_page():
    return render_template('index.html')

@app.route('/cart')
def cart_page():
    user_cart = session.get('cart', [])
    total_cart_price = 0.0

    for item in user_cart:
        quantity = item.get('quantity', 1)
        price = item.get('price', 0.0)
        total_cart_price += (price * quantity)

    return render_template('cart.html', cart_items=user_cart, full_session=session, total_price=total_cart_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('id'))
    product_name = request.form.get('name')
    product_price = float(request.form.get('price'))

    if 'cart' not in session:
        session['cart'] = []

    found = False
    for item in session['cart']:
        if item['id'] == product_id:
            item['quantity'] = item.get('quantity', 0) + 1
            found = True
            break
    if not found:
        session['cart'].append({'id': product_id, 'name': product_name, 'price': product_price, 'quantity': 1})

    session.modified = True

    return redirect(url_for('products_page'))

@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    product_id_to_delete = int(request.form.get('id'))

    if 'cart' in session:
        new_cart = []
        for item in session['cart']:
            if item['id'] == product_id_to_delete:
                if item.get('quantity', 1) > 1:
                    item['quantity'] -= 1
                    new_cart.append(item)
            else:
                new_cart.append(item)
        session['cart'] = new_cart
        session.modified = True

    return redirect(url_for('cart_page'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    if 'cart' in session:
        session.pop('cart', None)
        session.modified = True
    return redirect(url_for('cart_page'))

@app.route('/clear_full_session')
def clear_full_session():
    session.clear()
    flash('All session data cleared!', 'info')
    return redirect(url_for('cart_page'))


if __name__ == '__main__':
    app.run(debug=True)