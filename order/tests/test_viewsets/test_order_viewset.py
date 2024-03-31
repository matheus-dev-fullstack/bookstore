import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from product.models import Product
from order.models import Order

class TestOrderView(APITestCase):
    
    client = APIClient()
    
    def setUp(self):
        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(title='mouse', price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product])
        
    def test_order(self):
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        order_data = json.loads(response.content)[0]
        self.assertEqual(order_data['product'][0]['title'], self.product.title)
        self.assertEqual(order_data['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['product'][0]['active'], self.product.active)
        self.assertEqual(order_data['product'][0]['category'][0]['title'], self.category.title)
        
    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        
        data ={
            'products_id': [product.id],
            'user_id': user.id,
        }

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=json.dumps(data),
            # data=data,
            # content_type='application/json',
            format='json'
        )
        
        print("Response content:", response.content)

        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_order = Order.objects.get(user=user)

        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # # Verifica se o pedido foi criado com sucesso
        # created_order = Order.objects.filter(user=user).first()
        # self.assertIsNotNone(created_order)
            
        # # Verifica se o usuário associado ao pedido está correto
        # self.assertEqual(created_order.user, user)