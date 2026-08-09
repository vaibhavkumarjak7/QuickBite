from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Item, Order


class LandingPageTests(TestCase):
    def test_root_redirects_to_the_public_menu(self):
        response = self.client.get("/")

        self.assertRedirects(response, reverse("Food:index"))

    def test_anonymous_visitor_can_view_the_menu(self):
        response = self.client.get(reverse("Food:index"))

        self.assertEqual(response.status_code, 200)

    def test_htmx_menu_request_returns_only_menu_results(self):
        response = self.client.get(reverse("Food:index"), HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Food/partials/menu_results.html")
        self.assertNotContains(response, "Made for hungry moments")


class ItemWebFlowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", password="test-password", is_staff=True
        )
        self.other_user = User.objects.create_user(username="other", password="test-password")
        self.item = Item.objects.create(
            user_name=self.owner,
            item_name="Veg burger",
            item_desc="A burger with fresh vegetables",
            item_price=Decimal("129.00"),
        )

    def test_logged_in_user_creates_an_item_as_the_owner(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("Food:create_item"),
            {
                "item_name": "Masala dosa",
                "item_desc": "Crisp dosa served with sambar",
                "item_price": "150.00",
            },
        )

        self.assertRedirects(response, reverse("Food:index"))
        item = Item.objects.get(item_name="Masala dosa")
        self.assertEqual(item.user_name, self.owner)

    def test_another_user_cannot_update_or_delete_an_item(self):
        self.client.force_login(self.other_user)

        update_response = self.client.get(reverse("Food:update_item", args=[self.item.pk]))
        delete_response = self.client.get(reverse("Food:delete_item", args=[self.item.pk]))

        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)

    def test_regular_user_cannot_access_item_creation(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("Food:create_item"))

        self.assertEqual(response.status_code, 403)


class ItemApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api-user", password="test-password", is_staff=True
        )
        self.client = APIClient()

    def test_authenticated_api_user_owns_created_item(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse("Food:item-list"),
            {
                "item_name": "Paneer wrap",
                "item_desc": "Grilled paneer with vegetables",
                "item_price": "180.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Item.objects.get(item_name="Paneer wrap").user_name, self.user)

    def test_anonymous_user_cannot_create_an_item(self):
        response = self.client.post(
            reverse("Food:item-list"),
            {
                "item_name": "Paneer wrap",
                "item_desc": "Grilled paneer with vegetables",
                "item_price": "180.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_regular_user_cannot_create_an_item(self):
        regular_user = User.objects.create_user(username="regular", password="test-password")
        self.client.force_authenticate(user=regular_user)

        response = self.client.post(
            reverse("Food:item-list"),
            {
                "item_name": "Paneer wrap",
                "item_desc": "Grilled paneer with vegetables",
                "item_price": "180.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)


class CartAndCheckoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="customer", password="test-password")
        self.seller = User.objects.create_user(username="seller", password="test-password")
        self.item = Item.objects.create(
            user_name=self.seller,
            item_name="Chole bhature",
            item_desc="Fluffy bhature with spiced chickpea curry",
            item_price=Decimal("199.00"),
        )
        self.client.force_login(self.user)

    def test_customer_can_add_item_to_cart(self):
        response = self.client.post(reverse("Food:add_to_cart", args=[self.item.pk]))

        self.assertRedirects(response, reverse("Food:cart"))
        self.assertEqual(self.client.session["cart_item_ids"], [str(self.item.pk)])

    def test_checkout_creates_order_and_clears_cart(self):
        session = self.client.session
        session["cart_item_ids"] = [str(self.item.pk)]
        session.save()

        response = self.client.post(reverse("Food:checkout"))

        self.assertRedirects(response, reverse("Food:order_history"))
        order = Order.objects.get(user=self.user)
        self.assertEqual(list(order.item.all()), [self.item])
        self.assertEqual(self.client.session["cart_item_ids"], [])

    def test_unavailable_item_cannot_be_added_to_cart(self):
        self.item.is_available = False
        self.item.save()

        response = self.client.post(reverse("Food:add_to_cart", args=[self.item.pk]))

        self.assertEqual(response.status_code, 404)


class OrderApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="order-user", password="test-password")
        self.item = Item.objects.create(
            user_name=self.user,
            item_name="Veg pizza",
            item_desc="Stone-baked pizza with seasonal vegetables",
            item_price=Decimal("299.00"),
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_can_create_an_order_with_item_ids(self):
        response = self.client.post(
            reverse("Food:order-list"),
            {"item_ids": [self.item.pk]},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"], self.user.username)
        self.assertEqual(response.data["items"][0]["id"], self.item.pk)

    def test_anonymous_user_cannot_view_orders(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse("Food:order-list"))

        self.assertEqual(response.status_code, 401)


class StaffOrderManagementTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff", password="test-password", is_staff=True
        )
        self.customer = User.objects.create_user(
            username="customer", first_name="Asha", last_name="Sharma", email="asha@example.com", password="test-password"
        )
        self.item = Item.objects.create(
            user_name=self.staff_user,
            item_name="Tandoori wrap",
            item_desc="Smoky tandoori filling with fresh vegetables",
            item_price=Decimal("220.00"),
        )
        self.order = Order.objects.create(user=self.customer)
        self.order.item.add(self.item)

    def test_staff_can_view_received_orders_with_customer_details(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(reverse("Food:received_orders"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asha Sharma")
        self.assertContains(response, "asha@example.com")
        self.assertContains(response, "Tandoori wrap")

    def test_staff_can_mark_a_pending_order_as_completed(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(reverse("Food:complete_order", args=[self.order.pk]))

        self.assertRedirects(response, reverse("Food:received_orders"))
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.COMPLETED)

    def test_regular_customer_cannot_access_received_orders(self):
        self.client.force_login(self.customer)

        response = self.client.get(reverse("Food:received_orders"))

        self.assertEqual(response.status_code, 403)
