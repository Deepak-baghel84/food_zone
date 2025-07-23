import random
import uuid
from app import send_whatsapp, user_orders, orders, PRICES


class intent_handler():
    # 3) Handlers for each intent
    def Default_Welcome_Intent(self, phone_id, user):
        text_1 = (
            "Hello there! 😄 Ready to satisfy your hunger?\n"
            '- Type "New Order" to see our delicious options 🍽️ \n'
            '- Type "Track Order" to check the status of your food 🚚\n'
            "Let’s get started!"
        )
        text_2 = "Welcome to our food delivery bot! 🍛  " \
        "What would you like to do today? " \
        " 👉 New Order  " \
        "👉 Track Order  " \
        "👉 See Menu"
        text_3 = "Hi! 👋 Welcome to TastyBot — your WhatsApp food assistant. 🍕🍔\n" \
        "You can:\n" \
        " 1. Place a new order\n"  \
        " 2. Track an existing order \n"  \
        " 3. Ask for our menu\n"  

        text = random.choice([text_1, text_2, text_3])
        send_whatsapp.send(phone_id, user, text)
    
    def handle_new_order(self, phone_id, user):
        # Create new order_id
        order_id = "QBF"+uuid.uuid4().hex[:6].upper()
        user_orders[user] = order_id
        orders[order_id] = {"items":{}, "total":0}

        menu = "\n".join(f"🍽 {k} – ₹{v}" for k,v in PRICES.items())
        text = (
            f"✅ New order started!\n"
            f"🆔 Order ID: {order_id}\n\n"
            f"Menu:\n{menu}\n\n"
            "Type e.g. “Add Pizza” to add items."
        )
        send_whatsapp.send(phone_id, user, text)

    def handle_add_item(self, phone_id, user, params):
        order_id = user_orders.get(user)
        item = params.get("FoodItem")
        if not order_id or item not in PRICES:
            return send_whatsapp(phone_id, user, "Please start a new order first with “New Order”.")
        orders[order_id]["items"][item] = orders[order_id]["items"].get(item,0) + 1
        total = sum(PRICES[i]*q for i,q in orders[order_id]["items"].items())
        orders[order_id]["total"] = total
        send_whatsapp.send(phone_id, user,
            f"✅ Added 1 {item}. Current total: ₹{total}\n"
            "Type “Show total” or add/remove more."
        )

    def handle_remove_item(self, phone_id, user, params):
        order_id = user_orders.get(user)
        item = params.get("FoodItem")
        if not order_id or item not in orders[order_id]["items"]:
            return send_whatsapp.send(phone_id, user, "That item isn’t in your order.")
        orders[order_id]["items"][item] -= 1
        if orders[order_id]["items"][item] <= 0:
            del orders[order_id]["items"][item]
        total = sum(PRICES[i]*q for i,q in orders[order_id]["items"].items())
        orders[order_id]["total"] = total
        send_whatsapp.send(phone_id, user,
            f"🗑 Removed {item}. New total: ₹{total}"
        )

    def handle_show_total(self, phone_id, user):
        order_id = user_orders.get(user)
        if not order_id:
            return send_whatsapp.send(phone_id, user, "No active order. Type “New Order” to start.")
        lines = [f"- {i} x{q} = ₹{PRICES[i]*q}" for i,q in orders[order_id]["items"].items()]
        total = orders[order_id]["total"]
        send_whatsapp.send(phone_id, user,
            "🧾 Order Summary:\n" +
            "\n".join(lines) +
            f"\n\n💰 Total: ₹{total}\nType “Confirm” to place order."
        )

    def handle_confirm(self, phone_id, user):
        order_id = user_orders.get(user)
        if not order_id:
            return send_whatsapp.send(phone_id, user, "No order to confirm.")
        send_whatsapp.send(phone_id, user,
            f"🎉 Order {order_id} confirmed! It will arrive soon. Thanks!"
        )
        # Optionally clear session
        del user_orders[user]
        del orders[order_id]
       