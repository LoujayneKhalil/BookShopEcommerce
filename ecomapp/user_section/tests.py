from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from admin_section.models import Category, Product
from .models import Customer


class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword")
        self.customer = Customer.objects.create(
            user=self.user, phone="1234567890", address="Test Address")

    def test_customer_creation(self):
        self.assertEqual(self.customer.user, self.user)
        self.assertEqual(self.customer.phone, "1234567890")
        self.assertEqual(self.customer.address, "Test Address")

    def test_customer_str_method(self):
        self.assertEqual(str(self.customer), "Customer 2")


class UserSectionViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword")

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_section/home.html')

    def test_category_products_view(self):
        category = Category.objects.create(name='Oxford')
        url = reverse('category_products', args=['Oxford'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'user_section/category_products.html')
        category.delete()

    def test_products_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_section/products.html')

    def test_search_products_view(self):
        url = reverse('search_products')
        query_param = {'q': 'Math'}
        response = self.client.get(url, data=query_param)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_section/search_results.html')

    def test_cart_view_authenticated_user(self):

        login_successful = self.client.login(
            username="testuser", password="testpassword")

        if not login_successful:
            print("\nLogin failed.")
        else:
            print("\nSuccess")

        self.assertTrue(login_successful)

        url_login = reverse('login')
        response = self.client.get(url_login)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_section/login.html')

    def tearDown(self):
        self.user.delete()


class ProductDetailTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name_en='Test Product',
            name_ar='اسم المنتج الاختباري',
            unit_price=10.99,
            stock_quantity=50,
            category=self.category,
            image='test_image.jpg',
            isbn='1234567890123'
        )

    def test_product_detail_view(self):
        url = reverse('product_detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_section/product_detail.html')
        self.assertContains(response, self.product.name_en)
        self.assertContains(response, self.product.unit_price)
